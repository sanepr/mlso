"""
Test suite for API application
"""
import pytest
from pathlib import Path


class TestAPISetup:
    """Test API setup and configuration"""

    def test_api_file_exists(self):
        """Test that API file exists"""
        api_path = Path("src/api/app.py")
        assert api_path.exists(), "API file should exist"

    def test_test_sample_exists(self):
        """Test that test sample JSON exists"""
        sample_path = Path("test_sample.json")
        assert sample_path.exists(), "Test sample JSON should exist"

    def test_dockerfile_exists(self):
        """Test that Dockerfile exists"""
        dockerfile_path = Path("Dockerfile")
        assert dockerfile_path.exists(), "Dockerfile should exist"


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

