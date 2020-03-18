import requests
import json
import logging

from typing import List, Dict
from .endpoints import API_PATH, BASE_PATH
from .models import Project, Dataset
from .exceptions import APIException, InvalidTokenException, ClientException

logger = logging.getLogger(__name__)


class Client:

    def __init__(self, api_key) -> None:
        self.__api_key = api_key
        self.__auth = {"Authorization": f'Token {api_key}'}
        response = self._request(method="HEAD",
                                 endpoint=API_PATH['project'],
                                 headers=self.__auth,
                                 data=None)
        if response.status_code != 200:
            raise InvalidTokenException()

    def _request(self, method: str, endpoint: str, headers: Dict, data: Dict) -> requests.Response:
        try:
            return requests.request(method=method,
                                    url=BASE_PATH + endpoint,
                                    headers=headers,
                                    json=data)
        except requests.exceptions.RequestException as e:
            raise e

    def _response_valid(self, response: requests.Response) -> bool:
        if response.status_code == 200:
            return True
        elif response.status_code == 500:
            if response.content:
                raise APIException(**json.loads(response.content))
            else:
                raise APIException(status_code=response.status_code)
        else:
            if response.content:
                raise ClientException(**json.loads(response.content))
            else:
                raise ClientException(status_code=response.status_code)

    def get_projects(self) -> List[Project]:
        response = self._request(method="GET",
                                 endpoint=API_PATH['project'],
                                 headers=self.__auth,
                                 data=None)

        if self._response_valid(response):
            content = json.loads(response.content)
            return [Project(project) for project in content]

    def get_datasets(self) -> List[Dataset]:
        response = self._request(method="GET",
                                 endpoint=API_PATH['dataset'],
                                 headers=self.__auth,
                                 data=None)

        if self._response_valid(response):
            content = json.loads(response.content)
            return [Dataset(dataset) for dataset in content]

    def export_labels(self, project_id: str) -> Dict:
        endpoint = f'{API_PATH["export"]}/{project_id}'

        response = self._request(method="GET",
                                 endpoint=endpoint,
                                 headers=self.__auth,
                                 data=None)

        if self._response_valid(response):
            return json.loads(response.content)

    def export_labels_url(self, project_id: str) -> str:
        endpoint = f'{API_PATH["export"]}/{project_id}?token={self.__api_key}'

        response = self._request(method="HEAD",
                                 endpoint=endpoint,
                                 headers=None,
                                 data=None)

        if self._response_valid(response):
            return response.url

    def download_image(self, image_id: str, image_format: str, file_path: str) -> None:
        endpoint = f'{API_PATH["image"]}/{image_id}'

        response = self._request(method="GET",
                                 endpoint=endpoint,
                                 headers=self.__auth,
                                 data=None)

        if self._response_valid(response):
            with open(f'{file_path}{image_id}.{image_format}', 'wb') as handler:
                handler.write(response.content)

    def download_image_bytes(self, image_id: str):
        endpoint = f'{API_PATH["image"]}/{image_id}'

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
                                 endpoint=API_PATH['dataset'],
                                 headers=headers,
                                 data=data)

        if self._response_valid(response):
            return Dataset(json.loads(response.content))

    def add_dataset(self, dataset_id: str, project_id: str) -> bool:
        endpoint = f'{API_PATH["project"]}/{project_id}/dataset/{dataset_id}'

        headers = {
            'Content-type': 'application/json',
            "Accept": "application/json",
            **self.__auth
        }

        response = self._request(method="POST",
                                 endpoint=endpoint,
                                 headers=headers,
                                 data=None)

        if self._response_valid(response):
            return True
