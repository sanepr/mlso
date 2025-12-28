"""
Flask API Application for Heart Disease Prediction Service
with Prometheus Metrics Integration
"""

from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_client import CollectorRegistry, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import logging
import time
import joblib
import numpy as np
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Prometheus metrics
registry = CollectorRegistry()

# Counters
prediction_counter = Counter(
    'heart_disease_predictions_total',
    'Total number of predictions made',
    ['model_version', 'prediction_result'],
    registry=registry
)

error_counter = Counter(
    'heart_disease_prediction_errors_total',
    'Total number of prediction errors',
    ['error_type'],
    registry=registry
)

# Histograms
prediction_latency = Histogram(
    'heart_disease_prediction_latency_seconds',
    'Time spent processing prediction request',
    ['model_version'],
    registry=registry
)

# Gauges
model_info = Gauge(
    'heart_disease_model_info',
    'Information about the loaded model',
    ['model_version', 'model_type'],
    registry=registry
)

active_requests = Gauge(
    'heart_disease_active_requests',
    'Number of active prediction requests',
    registry=registry
)

# Global model variable
model = None
MODEL_VERSION = "1.0.0"
MODEL_TYPE = "heart_disease_classifier"


def load_model(model_path='models/best_model.pkl'):
    """Load the trained model from disk"""
    global model
    try:
        import pickle
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"Model loaded successfully from {model_path}")
        model_info.labels(
            model_version=MODEL_VERSION,
            model_type=MODEL_TYPE
        ).set(1)
        return True
    except FileNotFoundError:
        logger.error(f"Model file not found at {model_path}")
        logger.info("Trying alternative model paths...")
        # Try alternative paths
        alternative_paths = [
            'models/random_forest.pkl',
            'models/logistic_regression.pkl',
            '/app/models/best_model.pkl',
            '/app/models/random_forest.pkl'
        ]
        for alt_path in alternative_paths:
            try:
                import pickle
                with open(alt_path, 'rb') as f:
                    model = pickle.load(f)
                logger.info(f"Model loaded successfully from {alt_path}")
                model_info.labels(
                    model_version=MODEL_VERSION,
                    model_type=MODEL_TYPE
                ).set(1)
                return True
            except:
                continue
        logger.error("Failed to load model from any path")
        model_info.labels(
            model_version=MODEL_VERSION,
            model_type=MODEL_TYPE
        ).set(0)
        return False
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        model_info.labels(
            model_version=MODEL_VERSION,
            model_type=MODEL_TYPE
        ).set(0)
        return False


@app.before_request
def before_request():
    """Track active requests and log incoming requests"""
    active_requests.inc()
    request.start_time = time.time()

    # Log incoming request
    logger.info(
        f"Incoming request: {request.method} {request.path} "
        f"from {request.remote_addr} "
        f"User-Agent: {request.headers.get('User-Agent', 'Unknown')}"
    )


@app.after_request
def after_request(response):
    """Track request completion and log response"""
    active_requests.dec()

    # Calculate request duration
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time

        # Log request completion
        logger.info(
            f"Request completed: {request.method} {request.path} "
            f"Status: {response.status_code} "
            f"Duration: {duration*1000:.2f}ms "
            f"Size: {response.content_length or 0} bytes"
        )

    return response


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'heart-disease-prediction',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }
    
    status_code = 200 if model is not None else 503
    return jsonify(health_status), status_code


@app.route('/predict', methods=['POST'])
def predict():
    """
    Prediction endpoint for heart disease risk
    
    Expected JSON payload:
    {
        "age": int,
        "sex": int (0 or 1),
        "cp": int (0-3),
        "trestbps": int,
        "chol": int,
        "fbs": int (0 or 1),
        "restecg": int (0-2),
        "thalach": int,
        "exang": int (0 or 1),
        "oldpeak": float,
        "slope": int (0-2),
        "ca": int (0-4),
        "thal": int (0-3)
    }
    """
    start_time = time.time()
    
    try:
        # Check if model is loaded
        if model is None:
            error_counter.labels(error_type='model_not_loaded').inc()
            return jsonify({
                'error': 'Model not loaded',
                'message': 'Prediction model is not available'
            }), 503
        
        # Validate request
        if not request.is_json:
            error_counter.labels(error_type='invalid_content_type').inc()
            return jsonify({
                'error': 'Invalid content type',
                'message': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        
        # Expected features
        required_features = [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
            'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
        ]
        
        # Validate required features
        missing_features = [f for f in required_features if f not in data]
        if missing_features:
            error_counter.labels(error_type='missing_features').inc()
            return jsonify({
                'error': 'Missing required features',
                'missing_features': missing_features
            }), 400
        
        # Log input features
        logger.info(f"Prediction request received with features: age={data.get('age')}, sex={data.get('sex')}, cp={data.get('cp')}")

        # Extract features in correct order
        features = np.array([[data[f] for f in required_features]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        prediction_proba = model.predict_proba(features)[0]
        
        # Record metrics
        prediction_result = 'positive' if prediction == 1 else 'negative'
        prediction_counter.labels(
            model_version=MODEL_VERSION,
            prediction_result=prediction_result
        ).inc()
        
        elapsed_time = time.time() - start_time
        prediction_latency.labels(model_version=MODEL_VERSION).observe(elapsed_time)
        
        # Prepare response
        response = {
            'prediction': int(prediction),
            'prediction_label': 'Heart Disease' if prediction == 1 else 'No Heart Disease',
            'confidence': {
                'no_disease': float(prediction_proba[0]),
                'disease': float(prediction_proba[1])
            },
            'risk_level': get_risk_level(float(prediction_proba[1])),
            'model_version': MODEL_VERSION,
            'timestamp': datetime.utcnow().isoformat(),
            'processing_time_ms': round(elapsed_time * 1000, 2)
        }
        
        # Detailed logging
        logger.info(
            f"Prediction completed: result={prediction_result}, "
            f"confidence={prediction_proba[1]:.4f}, "
            f"risk_level={response['risk_level']}, "
            f"processing_time={elapsed_time*1000:.2f}ms"
        )

        return jsonify(response), 200
        
    except ValueError as e:
        error_counter.labels(error_type='value_error').inc()
        logger.error(f"Value error in prediction: {str(e)}")
        return jsonify({
            'error': 'Invalid input values',
            'message': str(e)
        }), 400
        
    except Exception as e:
        error_counter.labels(error_type='unexpected_error').inc()
        logger.error(f"Unexpected error in prediction: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred during prediction'
        }), 500


@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """
    Batch prediction endpoint for multiple samples
    
    Expected JSON payload:
    {
        "samples": [
            {feature_dict_1},
            {feature_dict_2},
            ...
        ]
    }
    """
    start_time = time.time()
    
    try:
        if model is None:
            error_counter.labels(error_type='model_not_loaded').inc()
            return jsonify({
                'error': 'Model not loaded',
                'message': 'Prediction model is not available'
            }), 503
        
        if not request.is_json:
            error_counter.labels(error_type='invalid_content_type').inc()
            return jsonify({
                'error': 'Invalid content type',
                'message': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        
        if 'samples' not in data or not isinstance(data['samples'], list):
            error_counter.labels(error_type='invalid_batch_format').inc()
            return jsonify({
                'error': 'Invalid batch format',
                'message': 'Request must contain "samples" array'
            }), 400
        
        samples = data['samples']
        if len(samples) == 0:
            return jsonify({
                'error': 'Empty batch',
                'message': 'No samples provided'
            }), 400
        
        required_features = [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
            'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
        ]
        
        predictions = []
        for idx, sample in enumerate(samples):
            missing_features = [f for f in required_features if f not in sample]
            if missing_features:
                predictions.append({
                    'sample_index': idx,
                    'error': 'Missing features',
                    'missing_features': missing_features
                })
                continue
            
            try:
                features = np.array([[sample[f] for f in required_features]])
                prediction = model.predict(features)[0]
                prediction_proba = model.predict_proba(features)[0]
                
                prediction_result = 'positive' if prediction == 1 else 'negative'
                prediction_counter.labels(
                    model_version=MODEL_VERSION,
                    prediction_result=prediction_result
                ).inc()
                
                predictions.append({
                    'sample_index': idx,
                    'prediction': int(prediction),
                    'prediction_label': 'Heart Disease' if prediction == 1 else 'No Heart Disease',
                    'confidence': {
                        'no_disease': float(prediction_proba[0]),
                        'disease': float(prediction_proba[1])
                    },
                    'risk_level': get_risk_level(float(prediction_proba[1]))
                })
            except Exception as e:
                predictions.append({
                    'sample_index': idx,
                    'error': str(e)
                })
        
        elapsed_time = time.time() - start_time
        
        response = {
            'predictions': predictions,
            'total_samples': len(samples),
            'successful_predictions': sum(1 for p in predictions if 'prediction' in p),
            'model_version': MODEL_VERSION,
            'timestamp': datetime.utcnow().isoformat(),
            'processing_time_ms': round(elapsed_time * 1000, 2)
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        error_counter.labels(error_type='batch_prediction_error').inc()
        logger.error(f"Error in batch prediction: {str(e)}")
        return jsonify({
            'error': 'Batch prediction failed',
            'message': str(e)
        }), 500


def get_risk_level(disease_probability):
    """Categorize risk level based on disease probability"""
    if disease_probability < 0.3:
        return 'Low'
    elif disease_probability < 0.6:
        return 'Medium'
    elif disease_probability < 0.8:
        return 'High'
    else:
        return 'Very High'


@app.route('/model/info', methods=['GET'])
def model_info_endpoint():
    """Get information about the loaded model"""
    info = {
        'model_version': MODEL_VERSION,
        'model_type': MODEL_TYPE,
        'model_loaded': model is not None,
        'features': [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
            'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
        ],
        'feature_descriptions': {
            'age': 'Age in years',
            'sex': 'Sex (1 = male, 0 = female)',
            'cp': 'Chest pain type (0-3)',
            'trestbps': 'Resting blood pressure (mm Hg)',
            'chol': 'Serum cholesterol (mg/dl)',
            'fbs': 'Fasting blood sugar > 120 mg/dl (1 = true, 0 = false)',
            'restecg': 'Resting electrocardiographic results (0-2)',
            'thalach': 'Maximum heart rate achieved',
            'exang': 'Exercise induced angina (1 = yes, 0 = no)',
            'oldpeak': 'ST depression induced by exercise relative to rest',
            'slope': 'Slope of the peak exercise ST segment (0-2)',
            'ca': 'Number of major vessels colored by fluoroscopy (0-4)',
            'thal': 'Thalassemia (0-3)'
        }
    }
    return jsonify(info), 200


# Add Prometheus metrics endpoint
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app(registry)
})


# Load model at module level (works with gunicorn)
# This ensures model is loaded when the module is imported
logger.info("Loading model at application startup...")
load_model()
logger.info(f"Model loading complete. Model loaded: {model is not None}")


if __name__ == '__main__':
    import os

    # Get port from environment variable or default to 8000
    port = int(os.environ.get('PORT', 8000))

    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
