import os

import requests
from requests.auth import HTTPBasicAuth
import json
import logging
from pathlib import Path
from typing import List, Dict, BinaryIO, Optional, Union
from .endpoints import Endpoint
from .models import Project, Dataset, Image, Video
from datagym.exceptions.exceptions import (APIException,
                                           InvalidTokenException,
                                           ClientException,
                                           ClientExceptionNonFatal,
                                           ExceptionMessageBuilder)

from datagym.utils.loadingbar import progressbar
from datagym.constants import WARNING_KEYS


class Client:
    """The Client class provides convenient access to DataGym's API.

    Instances of this class are the gateway to interacting with the
    DataGym API. The canonical way to obtain an instance of this
    class is via:

    .. code-block:: python

       from datagym import Client
       client = Client(api_key='API_KEY')

    """

    MAX_NUM_URLS_PER_UPLOAD = 50
    logger = logging.getLogger(__name__)

    def __init__(self, api_key: str, base_url: str = 'https://app.datagym.ai/',
                 basic_auth: Optional[HTTPBasicAuth] = None) -> None:
        """ Initializes DataGym Client instance
        
        :param base_url: URL to your Datagym instance
        :param str api_key: The API key of your organization
        :param Optional(HTTPBasicAuth) basic_auth: The basic authentification (username, password) for Datagym.ai

        """
        self._endpoint = Endpoint(base_path=base_url)
        """ An instance of :class:`.Endpoint`.

        Provides the endpoints of DataGym's API
        """

        self._msg_builder = ExceptionMessageBuilder()
        """An instance of :class:`.ExceptionMessageBuilder`.

        Builds readable messages from DataGym endpoint exceptions

        """

        self.__api_key = api_key
        self.__basic_auth = basic_auth

    def __repr__(self):
        return f'Client(api_key="{self.__api_key}")'

    def __str__(self):
        return self.__repr__()

    def _request(
            self,
            method: str,
            endpoint: str,
            headers: Optional[dict] = None,
            auth: Optional[HTTPBasicAuth] = None,
            json: Optional[Union[list, dict]] = None,
            data: Optional[Union[BinaryIO, dict]] = None
    ) -> requests.Response:
        """ Send a HTTP request to a DataGym endpoint

        :param str method: The HTTP method (ex. GET, POST, PUT, etc.)
        :param str endpoint: The DataGym API endpoint
        :param dict headers: The HTTP request header
        :param HTTPBasicAuth auth: The basic authentification for this request.
        :param dict json: The request body as json
        :param dict data: The request body

        :raises requests.exceptions.ConnectionError: Connection errors

        :returns: HTTP Response
        :rtype: requests.Response
        """
        try:
            if json:
                return requests.request(method=method,
                                        url=self._endpoint.BASE_PATH + endpoint,
                                        auth=auth,
                                        headers=headers,
                                        json=json)
            elif data:
                return requests.request(method=method,
                                        url=self._endpoint.BASE_PATH + endpoint,
                                        auth=auth,
                                        headers=headers,
                                        data=data)
            else:
                return requests.request(method=method,
                                        url=self._endpoint.BASE_PATH + endpoint,
                                        auth=auth,
                                        headers=headers)
        except requests.exceptions.ConnectionError as e:
            raise e
        except requests.exceptions.RequestException as e:
            raise e

    def _response_valid(self, response: requests.Response) -> bool:
        """ Checks if Response from DataGym was successful

        :param requests.Response response:
        :returns: True if response was successful
        :rtype: bool
        """
        if response.ok:
            return True
        elif response.status_code == 500:
            if response.content:
                raise APIException(self._msg_builder, **json.loads(response.content))
            else:
                response.raise_for_status()
        elif json.loads(response.content)["key"] in WARNING_KEYS:
            ClientExceptionNonFatal(self._msg_builder, self.logger, **json.loads(response.content))
            return False
        else:
            if response.content:
                raise ClientException(self._msg_builder, **json.loads(response.content))
            else:
                response.raise_for_status()

    def _is_token_valid(self) -> bool:
        response = self._request(method="HEAD",
                                 endpoint=self._endpoint.project(token=self.__api_key),
                                 auth=self.__basic_auth,
                                 )

        if not response.ok:
            raise InvalidTokenException(msg_builder=self._msg_builder,
                                        key='ex_unauthorized',
                                        params=[], code=500)
        else:
            return True

    def _get_projects_without_images(self) -> List[Project]:
        """ Fetch all Projects with all Datasets but without Images

        The api/v1/project endpoint returns all Projects with all Datasets
        but omits the Images for faster queries

        :returns: A list of all Projects without Images from your organization
        :rtype: List[Project]

        """
        response = self._request(method="GET",
                                 endpoint=self._endpoint.project(token=self.__api_key),
                                 auth=self.__basic_auth)

        if self._response_valid(response):
            content = json.loads(response.content)
            return [Project(project) for project in content]

    def get_projects(self) -> List[Project]:
        """ Fetch all Projects with all Datasets and Images

        :returns: A List of all Projects from your organization
        :rtype: List[Project]

        """
        projects = self._get_projects_without_images()
        datasets = self.get_datasets()

        for project in projects:
            project.update_existing_datasets(datasets)

        return projects

    def get_project_by_name(self, project_name: str) -> Project or None:
        """ Fetch Project by its name from DataGym

        :param str project_name: The Project name
        :returns: The Project with the given name
        :rtype: Project or None

        """
        projects = self.get_projects()

        for project in projects:
            if project.name == project_name:
                return project

        return None

    def get_datasets(self) -> List[Dataset]:
        """ Fetch all Datasets from DataGym

        :returns: List of all Datasets from your organization
        :rtype: List[Dataset]

        """
        response = self._request(method="GET",
                                 endpoint=self._endpoint.dataset(token=self.__api_key),
                                 auth=self.__basic_auth)

        if self._response_valid(response):
            content = json.loads(response.content)
            return [Dataset(dataset) for dataset in content]

    def get_dataset_by_name(self, dataset_name: str) -> Dataset or None:
        """ Fetch Dataset by its name from DataGym

        :param str dataset_name: The Dataset's name
        :returns: The Dataset with the given name
        :rtype: Dataset or None

        """
        datasets = self.get_datasets()

        for dataset in datasets:
            if dataset.name == dataset_name:
                return dataset

        return None

    def export_labels(self, project_id: str) -> Dict:
        """ Export the labeled data from a specific Project

        :param str project_id: The Project ID
        :returns: The labeled data as Dictionary
        :rtype: Dict

        """
        endpoint = self._endpoint.export_labels(project_id, token=self.__api_key)

        response = self._request(method="GET",
                                 endpoint=endpoint,
                                 auth=self.__basic_auth)

        if self._response_valid(response):

            export_dict = json.loads(response.content)

            for media_export in export_dict[1:]:
                if 'task_export_url' in media_export:
                    # Remove the beginning to leave only endpoint
                    inner_endpoint = media_export['task_export_url'].replace(self._endpoint.BASE_PATH, "")

                    inner_response = self._request(method="GET",
                                                   endpoint=inner_endpoint,
                                                   auth=self.__basic_auth)

                    if self._response_valid(inner_response):
                        temp_label = json.loads(inner_response.content)

                        media_export['labels'] = temp_label
            return export_dict
        else:
            return dict()

    def export_single_video_labels(self, project_id: str, video_id: str) -> Dict:
        """ Export the labeled data from a specific Video

        :param str project_id: The Project ID
        :param str video_id: The Video ID
        :returns: The labeled data as Dictionary
        :rtype: Dict

        """
        endpoint = self._endpoint.export_labels(project_id, token=self.__api_key)

        response = self._request(method="GET",
                                 endpoint=endpoint,
                                 auth=self.__basic_auth)

        if self._response_valid(response):

            export_dict = json.loads(response.content)

            for media_export in export_dict[1:]:
                if media_export['internal_media_ID'] == video_id:
                    if 'task_export_url' in media_export:
                        # Remove the beginning to leave only endpoint
                        inner_endpoint = media_export['task_export_url'].replace(self._endpoint.BASE_PATH, "")
                        inner_response = self._request(method="GET",
                                                       endpoint=inner_endpoint,
                                                       auth=self.__basic_auth)

                        if self._response_valid(inner_response):
                            temp_label = json.loads(inner_response.content)
                            media_export['labels'] = temp_label
                    return media_export

            return dict()

    def export_labels_url(self, project_id: str) -> str:
        """ Generate a URL to the labeled data from a specific Project

        :param str project_id: The Project ID
        :returns: A URL to the labeled data from a given Project
        :rtype: str

        """
        endpoint = self._endpoint.export_labels_url(project_id, self.__api_key)

        response = self._request(method="HEAD",
                                 endpoint=endpoint,
                                 auth=self.__basic_auth)

        if self._response_valid(response):
            return response.url

    def download_video(self, video: Video, file_path: str) -> None:
        """ Download a Video and store it in a specific file path

        :param Video video: The Video Object to be downloaded
        :param file_path: The destination path for storing the Video

        """
        video_content = self.download_video_bytes(video)
        if video_content:
            path_dir = Path(file_path)
            path_file = path_dir.joinpath(video.video_name)
            with open(path_file, 'wb') as handler:
                handler.write(video_content)

    def download_video_bytes(self, video: Video) -> bytes:
        """ Download a Video and store it in a specific file path

        :param Video video: The Video Object to be downloaded
        :returns: Byte stream of the requested Video
        :rtype: bytes

        """
        endpoint = self._endpoint.download_media(video.id, token=self.__api_key)

        response = self._request(method="GET",
                                 endpoint=endpoint,
                                 auth=self.__basic_auth)

        if self._response_valid(response):
            inner_response = requests.request(method="GET",
                                              url=response.content.decode("utf-8"))

            if self._response_valid(inner_response):
                return inner_response.content

    def download_image(self, image: Image, file_path: str) -> None:
        """ Download an Image and store it in a specific file path

        :param Image image: The Image Object to be downloaded
        :param file_path: The destination path for storing the Image

        """
        endpoint = self._endpoint.download_media(image.id, token=self.__api_key)

        path_dir = Path(file_path)
        path_file = path_dir.joinpath(image.image_name)

        response = self._request(method="GET",
                                 endpoint=endpoint,
                                 auth=self.__basic_auth)

        if self._response_valid(response):
            with open(path_file, 'wb') as handler:
                handler.write(response.content)

    def download_image_bytes(self, image: Image) -> bytes:
        """ Download Image as a byte stream

        :param Image image: Image object to be downloaded
        :returns: Byte stream of the requested Image
        :rtype: bytes

        """
        endpoint = self._endpoint.download_media(image.id, token=self.__api_key)

        response = self._request(method="GET",
                                 endpoint=endpoint,
                                 auth=self.__basic_auth)

        if self._response_valid(response):
            return response.content

    def create_dataset(
            self,
            name: str,
            short_description: str = None
    ) -> Dataset:
        """ Create Dataset in DataGym.io

        :param str name: The name of the dataset
        :param str short_description: An optional description of the Dataset
        :returns: The newly created Dataset
        :rtype: Dataset

        """
        data = {
            "name": name,
            "shortDescription": short_description
        }
        headers = {
            'Content-type': 'application/json',
            "Accept": "application/json",
        }

        response = self._request(method="POST",
                                 endpoint=self._endpoint.dataset(token=self.__api_key),
                                 headers=headers,
                                 auth=self.__basic_auth,
                                 json=data)

        if self._response_valid(response):
            return Dataset(json.loads(response.content))
        else:  # In case of non-fatal exception
            return self.get_dataset_by_name(name)

    def add_dataset(self, dataset_id: str, project_id: str) -> bool:
        """ Add a Dataset to a Project

        :param dataset_id: The Dataset ID
        :param project_id: The Project ID
        :returns: True if Dataset was added successfully
        :rtype: bool

        """
        endpoint = self._endpoint.add_dataset(project_id, dataset_id, token=self.__api_key)

        response = self._request(method="POST",
                                 endpoint=endpoint,
                                 auth=self.__basic_auth)

        if self._response_valid(response):
            return True
        else:  # In case of non-fatal exception (already attached)
            return True

    def remove_dataset(self, dataset_id: str, project_id: str) -> bool:
        """ Remove a Dataset from a Project

        :param str dataset_id: The Dataset ID
        :param str project_id: The Project ID
        :returns: True if Dataset was removed successfully
        :rtype: bool

        """
        endpoint = self._endpoint.remove_dataset(project_id, dataset_id, token=self.__api_key)

        response = self._request(method="DELETE",
                                 endpoint=endpoint,
                                 auth=self.__basic_auth)

        if self._response_valid(response):
            return True

    def create_images_from_urls(self,
                                dataset_id: str,
                                image_url_list: List[str]
                                ) -> List[Dict[str, str]]:
        """ Add Images to a Dataset from a list of URLs

        :param dataset_id: The Dataset ID
        :param image_url_list: A List of URLs referencing images
        :returns: A list of errors occurred during the Image upload
        :rtype: List[Dict[str, str]]

        """
        endpoint = self._endpoint.create_image(dataset_id, token=self.__api_key)

        if len(image_url_list) < self.MAX_NUM_URLS_PER_UPLOAD:

            response = self._request(method="POST",
                                     endpoint=endpoint,
                                     auth=self.__basic_auth,
                                     json=image_url_list)
            if self._response_valid(response):
                return json.loads(response.content)
        # If the url List contains a large number of urls it is split into mini batches for upload
        else:
            response = []

            for i in progressbar(
                    range(0, len(image_url_list), self.MAX_NUM_URLS_PER_UPLOAD),
                    "Uploading image urls: ",
                    40
            ):
                if i + self.MAX_NUM_URLS_PER_UPLOAD >= len(image_url_list):
                    slice = image_url_list[i:]
                else:
                    slice = image_url_list[i:i + self.MAX_NUM_URLS_PER_UPLOAD]

                partial_response = self._request(method="POST",
                                                 endpoint=endpoint,
                                                 auth=self.__basic_auth,
                                                 json=slice)

                if self._response_valid(partial_response):
                    response += json.loads(partial_response.content)
                else:
                    break

            return response

    def delete_image(self, image: Image) -> bool:
        """ Deletes an Image from a Dataset

        :param Image image: The Image to be deleted
        :returns: True if Image was successfully deleted
        :rtype: bool

        """
        endpoint = self._endpoint.delete_media(image.id, token=self.__api_key)

        response = self._request(method="DELETE",
                                 endpoint=endpoint,
                                 auth=self.__basic_auth)

        if self._response_valid(response):
            return True

    def import_label_data(self, project_id: str, label_data: Dict) -> List:
        """ Import labeled image data into DataGym Projects

        :param str project_id: Project_id of your project,
            use client.get_project_by_name(project_name=PROJECT_NAME).id to get the id for your project
        :param Dict label_data: Labels in JSON Format. See DataGym Docs for more information
        :returns: List of Errors if JSON is malformed or data is invalid
        """
        endpoint = self._endpoint.import_labels(project_id=project_id, token=self.__api_key)

        if len(label_data) < self.MAX_NUM_URLS_PER_UPLOAD:

            response = self._request(method="POST",
                                     endpoint=endpoint,
                                     auth=self.__basic_auth,
                                     json=label_data)

            if self._response_valid(response):
                return json.loads(response.content)
        # If the label List contains a large number of labeled images it is split into mini batches for upload
        else:
            response = []

            for i in progressbar(
                    range(0, len(label_data), self.MAX_NUM_URLS_PER_UPLOAD),
                    "Uploading annotations: ",
                    40
            ):
                if i + self.MAX_NUM_URLS_PER_UPLOAD >= len(label_data):
                    mini_batch = label_data[i:]
                else:
                    mini_batch = label_data[i:i + self.MAX_NUM_URLS_PER_UPLOAD]

                partial_response = self._request(method="POST",
                                                 endpoint=endpoint,
                                                 auth=self.__basic_auth,
                                                 json=mini_batch)

                if self._response_valid(partial_response):
                    response += json.loads(partial_response.content)
                else:
                    break

            return response

    def upload_image(self, dataset_id: str, image_path: str, image_name: str = None) -> Image or None:
        """ Uploads an Image to a Dataset

        :param str dataset_id: The dataset the image should be uploaded to
        :param str image_path: The path to the image that should be uploaded
        :param str image_name: Your prefered image name.
                                If left empty, it will automatically be extracted from the image path
        :returns: The Image if it was successfully uploaded, else None
        :rtype: Image or None

        """
        endpoint = self._endpoint.upload_media(dataset_id, token=self.__api_key)

        if not image_name:
            image_name = os.path.basename(image_path)

        files = open(image_path, 'rb')

        headers = {
            'X-filename': image_name,
        }

        response = self._request(method="POST",
                                 endpoint=endpoint,
                                 headers=headers,
                                 auth=self.__basic_auth,
                                 data=files)

        if self._response_valid(response):
            return Image(json.loads(response.content))

    def upload_label_config(self, config_id: str, label_config: List[Dict]) -> bytes or None:
        """ Clears the existing config and replaces it by a new one.
        Careful with this as clearing the config also clears all associated labels

        :param config_id:
        :param label_config:
        :return: bytes if successful, else None
        """
        clear_endpoint = self._endpoint.upload_label_config(config_id, token=self.__api_key)
        upload_endpoint = self._endpoint.clear_label_config(config_id, token=self.__api_key)

        clear_response = self._request(method="DELETE",
                                       endpoint=clear_endpoint,
                                       auth=self.__basic_auth)

        if self._response_valid(clear_response):

            upload_response = self._request(method="PUT",
                                            endpoint=upload_endpoint,
                                            auth=self.__basic_auth,
                                            json=label_config)

            if self._response_valid(upload_response):
                return upload_response.content
