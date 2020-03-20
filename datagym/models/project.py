from datagym.models.dataset import Dataset, Image
from typing import List


class Project:

    def __init__(self, data):
        self.id: str = data['id']
        self.name: str = data['name']
        self.short_description: str = data['shortDescription']
        self.timestamp: int = data['timestamp']
        self.label_config_id: str = data['labelConfigurationId']
        self.label_iteration_id: str = data['labelIterationId']
        self.owner: str = data['owner']
        self.datasets: List[Dataset] = [Dataset(dataset_response_dict) for dataset_response_dict in data['datasets']]

    def __repr__(self):
        properties = [f"'{e[0]}': '{e[1]}'" for e in self.__dict__.items() if e[0] != "datasets"]
        properties += ["'datasets': <List[Dataset] with {} elements>".format(len(self.datasets))]
        r = "<{class_name} {{{properties}}}>".format(properties=", ".join(properties),
                                                     class_name=self.__class__.__name__)
        return r

    def __str__(self):
        return self.__repr__()

    def update_existing_datasets(self, dataset_list: List[Dataset]):
        dataset_ids = [d.id for d in self.datasets]
        self.datasets = [d for d in dataset_list if d.id in dataset_ids]

    def get_dataset_by_name(self, dataset_name: str) -> Dataset or None:
        for dataset in self.datasets:
            if dataset.name == dataset_name:
                return dataset

        return None

    def get_images_by_name(self, image_name: str, regex: bool = False) -> List[Image]:
        image_list = []

        for dataset in self.datasets:
            image_list += dataset.get_images_by_name(image_name, regex)

        return image_list
