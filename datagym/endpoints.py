class Endpoint:
    """ The Endpoint class provides endpoint references

    The Endpoint class has two types of endpoints:
    Static endpoints (upper case variables) and dynamics endpoints
    (protected variables). Calling the dynamic endpoints with the
    respective parameters (ex. Project ID, Dataset ID, etc.) returns
    the desired endpoint string for accessing the DataGym API

    """
    BASE_PATH = "https://app.datagym.ai/"

    PROJECT: str = "api/v1/project"
    DATASET: str = "api/v1/dataset"
    IMAGE: str = "api/v1/image"

    _export_labels: str = "api/v1/export/{project_id}"
    _export_labels_url: str = "api/v1/export/{project_id}?token={token}"
    _download_image: str = "api/v1/image/{image_id}"
    _add_dataset: str = "api/v1/project/{project_id}/dataset/{dataset_id}"
    _remove_dataset: str = "api/v1/project/{project_id}/dataset/{dataset_id}/remove"
    _create_image: str = "api/v1/image/{dataset_id}/url"
    _delete_image: str = "api/v1/image/{image_id}"
    _get_dataset_by_id: str = "api/v1/dataset/{dataset_id}"
    _import_labels: str = "api/v1/project/{project_id}/prediction"
    _upload_image: str = "/api/v1/image/{dataset_id}/file"

    def export_labels(self, project_id: str) -> str:
        return self._export_labels.format(project_id=project_id)

    def export_labels_url(self, project_id: str, token: str) -> str:
        return self._export_labels_url.format(project_id=project_id,
                                              token=token)

    def download_image(self, image_id: str) -> str:
        return self._download_image.format(image_id=image_id)

    def create_image(self, dataset_id: str) -> str:
        return self._create_image.format(dataset_id=dataset_id)

    def add_dataset(self, project_id: str, dataset_id: str) -> str:
        return self._add_dataset.format(project_id=project_id,
                                        dataset_id=dataset_id)

    def remove_dataset(self, project_id: str, dataset_id: str) -> str:
        return self._remove_dataset.format(project_id=project_id,
                                           dataset_id=dataset_id)

    def delete_image(self, image_id: str) -> str:
        return self._delete_image.format(image_id=image_id)

    def get_dataset_by_id(self, dataset_id: str) -> str:
        return self._get_dataset_by_id.format(dataset_id=dataset_id)

    def import_labels(self, project_id: str):
        return self._import_labels.format(project_id=project_id)

    def upload_image(self, dataset_id: str):
        return self._upload_image.format(dataset_id=dataset_id)