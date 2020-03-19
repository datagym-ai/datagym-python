class Endpoint:
    BASE_PATH = "http://localhost:8080/"

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

    def export_labels(self, project_id: str) -> str:
        return self._export_labels.format(project_id=project_id)

    def export_labels_url(self, project_id: str, token: str) -> str:
        return self._export_labels_url.format(project_id=project_id, token=token)

    def download_image(self, image_id: str) -> str:
        return self._download_image.format(image_id=image_id)

    def create_image(self, dataset_id: str) -> str:
        return self._create_image.format(dataset_id=dataset_id)

    def add_dataset(self, project_id: str, dataset_id: str) -> str:
        return self._add_dataset.format(project_id=project_id, dataset_id=dataset_id)

    def remove_dataset(self, project_id: str, dataset_id: str) -> str:
        return self._remove_dataset.format(project_id=project_id, dataset_id=dataset_id)

    def delete_image(self, image_id: str) -> str:
        return self._delete_image.format(image_id=image_id)
