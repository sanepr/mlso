"""
Unit tests for API endpoints
"""
import pytest
import json
from pathlib import Path
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestAPIFiles:
    """Test that API files exist"""

    def test_api_file_exists(self):
        """Test that API file exists"""
        api_path = Path("src/api/app.py")
        assert api_path.exists(), "API file should exist"

    def test_dockerfile_exists(self):
        """Test that Dockerfile exists"""
        dockerfile = Path("Dockerfile")
        assert dockerfile.exists(), "Dockerfile should exist"

    def test_requirements_exists(self):
        """Test that requirements.txt exists"""
        requirements = Path("requirements.txt")
        assert requirements.exists(), "requirements.txt should exist"


class TestAPIConfiguration:
    """Test API configuration"""

    def test_test_sample_exists(self):
        """Test that test sample JSON exists"""
        sample_path = Path("test_sample.json")
        assert sample_path.exists(), "test_sample.json should exist"

    def test_test_sample_valid_json(self):
        """Test that test sample is valid JSON"""
        sample_path = Path("test_sample.json")

        if not sample_path.exists():
            pytest.skip("test_sample.json not available")

        with open(sample_path, 'r') as f:
            data = json.load(f)

        assert isinstance(data, dict), "Test sample should be a dictionary"

    def test_test_sample_has_required_fields(self):
        """Test that test sample has all required fields"""
        sample_path = Path("test_sample.json")

        if not sample_path.exists():
            pytest.skip("test_sample.json not available")

        with open(sample_path, 'r') as f:
            data = json.load(f)

        required_fields = [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
            'restecg', 'thalach', 'exang', 'oldpeak',
            'slope', 'ca', 'thal'
        ]

        for field in required_fields:
            assert field in data, f"Test sample should have {field} field"

    def test_test_sample_field_types(self):
        """Test that test sample fields are numeric"""
        sample_path = Path("test_sample.json")

        if not sample_path.exists():
            pytest.skip("test_sample.json not available")

        with open(sample_path, 'r') as f:
            data = json.load(f)

        for field, value in data.items():
            assert isinstance(value, (int, float)), \
                f"Field {field} should be numeric, got {type(value)}"


class TestKubernetesManifests:
    """Test Kubernetes deployment files"""

    def test_deployment_yaml_exists(self):
        """Test that deployment YAML exists"""
        deployment_path = Path("deployment/kubernetes/deployment.yaml")
        assert deployment_path.exists(), "deployment.yaml should exist"

    def test_service_yaml_exists(self):
        """Test that service YAML exists"""
        service_path = Path("deployment/kubernetes/service.yaml")
        assert service_path.exists(), "service.yaml should exist"

    def test_ingress_yaml_exists(self):
        """Test that ingress YAML exists"""
        ingress_path = Path("deployment/kubernetes/ingress.yaml")
        assert ingress_path.exists(), "ingress.yaml should exist"


class TestDockerConfiguration:
    """Test Docker configuration"""

    def test_dockerfile_has_from(self):
        """Test Dockerfile has FROM instruction"""
        dockerfile = Path("Dockerfile")

        if not dockerfile.exists():
            pytest.skip("Dockerfile not available")

        with open(dockerfile, 'r') as f:
            content = f.read()

        assert 'FROM' in content, "Dockerfile should have FROM instruction"

    def test_dockerfile_has_workdir(self):
        """Test Dockerfile has WORKDIR instruction"""
        dockerfile = Path("Dockerfile")

        if not dockerfile.exists():
            pytest.skip("Dockerfile not available")

        with open(dockerfile, 'r') as f:
            content = f.read()

        assert 'WORKDIR' in content, "Dockerfile should have WORKDIR instruction"

    def test_dockerfile_has_cmd(self):
        """Test Dockerfile has CMD or ENTRYPOINT"""
        dockerfile = Path("Dockerfile")

        if not dockerfile.exists():
            pytest.skip("Dockerfile not available")

        with open(dockerfile, 'r') as f:
            content = f.read()

        assert 'CMD' in content or 'ENTRYPOINT' in content, \
            "Dockerfile should have CMD or ENTRYPOINT"

    def test_dockerfile_exposes_port(self):
        """Test Dockerfile exposes a port"""
        dockerfile = Path("Dockerfile")

        if not dockerfile.exists():
            pytest.skip("Dockerfile not available")

        with open(dockerfile, 'r') as f:
            content = f.read()

        assert 'EXPOSE' in content or '8000' in content, \
            "Dockerfile should expose port 8000"


class TestProjectStructure:
    """Test overall project structure"""

    def test_src_directory_exists(self):
        """Test src directory exists"""
        assert Path("src").exists(), "src/ directory should exist"

    def test_tests_directory_exists(self):
        """Test tests directory exists"""
        assert Path("tests").exists(), "tests/ directory should exist"

    def test_data_directory_exists(self):
        """Test data directory exists"""
        assert Path("data").exists(), "data/ directory should exist"

    def test_models_directory_exists(self):
        """Test models directory exists"""
        assert Path("models").exists(), "models/ directory should exist"

    def test_deployment_directory_exists(self):
        """Test deployment directory exists"""
        assert Path("deployment").exists(), "deployment/ directory should exist"


class TestHelperScripts:
    """Test helper scripts"""

    def test_deploy_k8s_script_exists(self):
        """Test deploy_k8s.sh exists"""
        script_path = Path("deploy_k8s.sh")
        assert script_path.exists(), "deploy_k8s.sh should exist"

    def test_start_jupyter_script_exists(self):
        """Test start_jupyter.sh exists"""
        script_path = Path("start_jupyter.sh")
        assert script_path.exists(), "start_jupyter.sh should exist"

    def test_scripts_are_executable(self):
        """Test that scripts are executable"""
        scripts = ['deploy_k8s.sh', 'start_jupyter.sh']

        for script in scripts:
            script_path = Path(script)
            if script_path.exists():
                import os
                assert os.access(script_path, os.X_OK), f"{script} should be executable"

