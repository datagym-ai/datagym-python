import requests
import json
import logging

from typing import List
from .endpoints import API_PATH, BASE_PATH
from .models import Project
from .exceptions import APIException

logger = logging.getLogger(__name__)


class Client:

    def __init__(self, api_key) -> None:
        self.__api_key = f'Token {api_key}'
        self.__auth = {"Authorization": self.__api_key}

    def _request(self, method, endpoint, data) -> requests.Response:
        try:
            return requests.request(method=method,
                                    url=BASE_PATH + endpoint,
                                    headers=self.__auth,
                                    data=data)
        except requests.exceptions.RequestException as e:
            raise e

    def _response_valid(self, response) -> bool:
        if response.status_code == 200:
            return True
        else:
            raise APIException(**json.loads(response.content))

    def get_projects(self) -> List[Project]:
        response = self._request(method="GET", endpoint=API_PATH['project'], data=None)

        if self._response_valid(response):
            content = json.loads(response.content)
            return [Project(project) for project in content]

