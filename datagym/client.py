import requests
import json
import logging

from typing import List, Dict, Set
from .endpoints import Endpoint
from .models import Project, Dataset
from datagym.exceptions.exceptions import APIException, InvalidTokenException, ClientException, ExceptionMessageBuilder

logger = logging.getLogger(__name__)


class Client:

    def __init__(self, api_key) -> None:
        self._endpoint = Endpoint()
        self._msg_builder = ExceptionMessageBuilder()
        self.__api_key = api_key
        self.__auth = {"Authorization": f'Token {api_key}'}

        response = self._request(method="HEAD",
                                 endpoint=self._endpoint.PROJECT,
                                 headers=self.__auth,
                                 data=None)

        if not response.ok:
            raise InvalidTokenException(msg_builder=self._msg_builder, key='ex_unauthorized', params=[], code=500)

    def __repr__(self):
        return f'Client(api_key="{self.__api_key}")'

    def __str__(self):
        return f'Client(api_key="{self.__api_key}")'

    def _request(self, method: str, endpoint: str, headers: dict or None, data: dict or None) -> requests.Response:
        try:
            return requests.request(method=method,
                                    url=self._endpoint.BASE_PATH + endpoint,
                                    headers=headers,
                                    json=data)
        except requests.exceptions.ConnectionError as e:
            raise e
        except requests.exceptions.RequestException as e:
            raise e

    def _response_valid(self, response: requests.Response) -> bool:
        if response.ok:
            return True
        elif response.status_code == 500:
            if response.content:
                raise APIException(self._msg_builder, **json.loads(response.content))
            else:
                response.raise_for_status()
        else:
            if response.content:
                raise ClientException(self._msg_builder, **json.loads(response.content))
            else:
                response.raise_for_status()

    def _get_projects_without_images(self) -> List[Project]:
        response = self._request(method="GET",
                                 endpoint=self._endpoint.PROJECT,
                                 headers=self.__auth,
                                 data=None)

        if self._response_valid(response):
            content = json.loads(response.content)
            return [Project(project) for project in content]

    def get_projects(self) -> List[Project]:
        projects = self._get_projects_without_images()
        datasets = self.get_datasets()

        for project in projects:
            project.update_existing_datasets(datasets)

        return projects

    def get_project_by_name(self, project_name: str) -> Project or None:
        projects = self.get_projects()

        for project in projects:
            if project.name == project_name:
                return project

        return None

    def get_datasets(self) -> List[Dataset]:
        response = self._request(method="GET",
                                 endpoint=self._endpoint.DATASET,
                                 headers=self.__auth,
                                 data=None)

        if self._response_valid(response):
            content = json.loads(response.content)
            return [Dataset(dataset) for dataset in content]

    def get_dataset_by_name(self, dataset_name: str) -> Dataset or None:
        datasets = self.get_datasets()

        for dataset in datasets:
            if dataset.name == dataset_name:
                return dataset

        return None

    def export_labels(self, project_id: str) -> Dict:
        endpoint = self._endpoint.export_labels(project_id)

        response = self._request(method="GET",
                                 endpoint=endpoint,
                                 headers=self.__auth,
                                 data=None)

        if self._response_valid(response):
            return json.loads(response.content)

    def export_labels_url(self, project_id: str) -> str:
        endpoint = self._endpoint.export_labels_url(project_id, self.__api_key)

        response = self._request(method="HEAD",
                                 endpoint=endpoint,
                                 headers=None,
                                 data=None)

        if self._response_valid(response):
            return response.url

    def download_image(self, image_id: str, image_format: str, file_path: str) -> None:
        endpoint = self._endpoint.download_image(image_id)

        response = self._request(method="GET",
                                 endpoint=endpoint,
                                 headers=self.__auth,
                                 data=None)

        if self._response_valid(response):
            with open(f'{file_path}{image_id}.{image_format}', 'wb') as handler:
                handler.write(response.content)

    def download_image_bytes(self, image_id: str):
        endpoint = self._endpoint.download_image(image_id)

        response = self._request(method="GET",
                                 endpoint=endpoint,
                                 headers=self.__auth,
                                 data=None)

        if self._response_valid(response):
            return response.content

    def create_dataset(self, name: str, owner: str, short_description: str = None) -> Dataset:
        data = {
            "name": name,
            "owner": owner,
            "shortDescription": short_description
        }
        headers = {
            'Content-type': 'application/json',
            "Accept": "application/json",
            **self.__auth
        }

        response = self._request(method="POST",
                                 endpoint=self._endpoint.DATASET,
                                 headers=headers,
                                 data=data)

        if self._response_valid(response):
            return Dataset(json.loads(response.content))

    def add_dataset(self, dataset_id: str, project_id: str) -> bool:
        endpoint = self._endpoint.add_dataset(project_id, dataset_id)

        response = self._request(method="POST",
                                 endpoint=endpoint,
                                 headers=self.__auth,
                                 data=None)

        if self._response_valid(response):
            return True

    def remove_dataset(self, dataset_id: str, project_id: str) -> bool:
        endpoint = self._endpoint.remove_dataset(project_id, dataset_id)

        response = self._request(method="DELETE",
                                 endpoint=endpoint,
                                 headers=self.__auth,
                                 data=None)

        if self._response_valid(response):
            return True

    def create_images_from_urls(self, dataset_id: str, image_url_set: Set[str]) -> List[Dict[str, str]]:
        endpoint = self._endpoint.create_image(dataset_id)

        data = list(image_url_set)

        response = self._request(method="POST",
                                 endpoint=endpoint,
                                 headers=self.__auth,
                                 data=data)

        if self._response_valid(response):
            return json.loads(response.content)

    def delete_image(self, image_id: str) -> bool:
        endpoint = self._endpoint.delete_image(image_id)

        response = self._request(method="DELETE",
                                 endpoint=endpoint,
                                 headers=self.__auth,
                                 data=None)

        if self._response_valid(response):
            return True
