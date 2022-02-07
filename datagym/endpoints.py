class Endpoint:
    """ The Endpoint class provides endpoint references

    The Endpoint class has two types of endpoints:
    Static endpoints (upper case variables) and dynamics endpoints
    (protected variables). Calling the dynamic endpoints with the
    respective parameters (ex. Project ID, Dataset ID, etc.) returns
    the desired endpoint string for accessing the DataGym API

    """

    PROJECT: str = "api/v1/project?token={token}"
    DATASET: str = "api/v1/dataset?token={token}"
    MEDIA: str = "api/v1/media?token={token}"
 	BASE_PATH: str = "https://app.datagym.ai/"
    
    _export_labels: str = "api/v1/export/{project_id}?token={token}"
    _export_labels_url: str = "api/v1/export/{project_id}?token={token}"
    _download_media: str = "api/v1/media/{media_id}?token={token}"
    _add_dataset: str = "api/v1/project/{project_id}/dataset/{dataset_id}?token={token}"
    _remove_dataset: str = "api/v1/project/{project_id}/dataset/{dataset_id}/remove?token={token}"
    _create_image: str = "api/v1/media/{dataset_id}/url?token={token}"
    _delete_media: str = "api/v1/media/{media_id}?token={token}"
    _get_dataset_by_id: str = "api/v1/dataset/{dataset_id}?token={token}"
    _import_labels: str = "api/v1/project/{project_id}/prediction?token={token}"
    _upload_media: str = "api/v1/media/{dataset_id}/file?token={token}"
    _clear_label_config: str = "/api/v1/config/{configId}?token={token}"
    _upload_label_config: str = "/api/v1/config/{configId}?token={token}"

    def __init__(self, base_path: str = "https://app.datagym.ai/"):
        if base_path[-1] != '/':
            raise ValueError('Base path of endpoint has to end with a trailing slash')
        Endpoint.BASE_PATH = base_path

    def project(self, token: str):
        return self.PROJECT.format(token=token)

    def dataset(self, token: str):
        return self.DATASET.format(token=token)

    def media(self, token: str):
        return self.MEDIA.format(token=token)

    def export_labels(self, project_id: str, token: str) -> str:
        return self._export_labels.format(project_id=project_id, token=token)

    def export_labels_url(self, project_id: str, token: str) -> str:
        return self._export_labels_url.format(project_id=project_id,
                                              token=token)

    def download_media(self, media_id: str, token: str) -> str:
        return self._download_media.format(media_id=media_id, token=token)

    def create_image(self, dataset_id: str, token: str) -> str:
        return self._create_image.format(dataset_id=dataset_id, token=token)

    def add_dataset(self, project_id: str, dataset_id: str, token: str) -> str:
        return self._add_dataset.format(project_id=project_id,
                                        dataset_id=dataset_id,
                                        token=token)

    def remove_dataset(self, project_id: str, dataset_id: str, token: str) -> str:
        return self._remove_dataset.format(project_id=project_id,
                                           dataset_id=dataset_id,
                                           token=token)

    def delete_media(self, media_id: str, token: str) -> str:
        return self._delete_media.format(media_id=media_id, token=token)

    def get_dataset_by_id(self, dataset_id: str, token: str) -> str:
        return self._get_dataset_by_id.format(dataset_id=dataset_id, token=token)

    def import_labels(self, project_id: str, token: str):
        return self._import_labels.format(project_id=project_id, token=token)

    def upload_media(self, dataset_id: str, token: str):
        return self._upload_media.format(dataset_id=dataset_id, token=token)

    def clear_label_config(self, config_id: str, token: str):
        return self._clear_label_config.format(configId=config_id, token=token)

    def upload_label_config(self, config_id: str, token: str):
        return self._upload_label_config.format(configId=config_id, token=token)
