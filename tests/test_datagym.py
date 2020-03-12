import pytest


@pytest.fixture
def client():
    from datagym import Client
    return Client("api_key")


def test_get_project_success(client):
    project = client.get_projects()
    assert len(project) == 2