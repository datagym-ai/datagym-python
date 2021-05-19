import pytest
from unittest.mock import patch
from requests.models import Response


class TestClient:

    @pytest.fixture
    def client(self):
        the_response = Response()
        the_response.code = "expired"
        the_response.error_type = "expired"
        the_response.status_code = 200

        with patch('datagym.client.Client._request', return_value=the_response):
            from datagym import Client
            return Client("38641a09-cdf1-448e-bbc6-8e49109f7b63")

    @pytest.fixture
    def project_data(self):
        return '''[{    "id": "ID1",
                        "name": "Project1",
                        "shortDescription": "firstProject",
                        "timestamp": 122345,
                        "labelConfigurationId": "LABELID1",
                        "labelIterationId": "LABELITERID1",
                        "owner": "user1",
                        "mediaType": "IMAGE",
                        "datasets": []
                 }]'''

    @pytest.fixture
    def get_projects_response(self, project_data):
        the_response = Response()
        the_response.code = "expired"
        the_response.error_type = "expired"
        the_response.status_code = 200
        the_response._content = project_data.encode()

        return the_response

    def test_get_projects_success(self, client, project_data, get_projects_response):
        with patch('datagym.client.Client._request',
                   return_value=get_projects_response), \
             patch('datagym.client.Client._response_valid',
                   return_value=True):
            projects = client.get_projects()
            assert projects is not None
            assert len(projects) == 1

    def test_request_success(self, client):
        with patch('datagym.client.requests.request') as mock_get:
            mock_get.return_value.ok = True
            response = client._request("GET", "endpoint", None, None)
            assert response is not None
