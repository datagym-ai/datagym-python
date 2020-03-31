from datagym.models.dataset import Dataset, Image
from typing import List, Dict


class Project:
    """ The Project class is a model of the DataGym.io Project

    DataGym.io Projects fetched from the DataGym API will be parsed
    into Project objects.

    """

    def __init__(self, data: Dict):
        """ Initializes DataGym Project instance

        :param Dict data: Response data from the DataGym API

        """

        self.id: str = data['id']
        self.name: str = data['name']
        self.short_description: str = data['shortDescription']
        self.timestamp: int = data['timestamp']
        self.label_config_id: str = data['labelConfigurationId']
        self.label_iteration_id: str = data['labelIterationId']
        self.owner: str = data['owner']
        self.datasets: List[Dataset] = [Dataset(d) for d in data['datasets']]

    def __repr__(self):
        """ Return useful representation of a the Project

        The Project attributes should be readable, template:
            <Project { attribute1: value1, attribute2: value2, ... }>
        Special case:
            <Project { ... datasets: <List[Datasets] with n elements> ... }>

        :return: Return readable repr of the Project
        """
        properties = [f"'{e[0]}': '{e[1]}'" for e in self.__dict__.items() if e[0] != "datasets"]
        properties += ["'datasets': <List[Dataset] with {} elements>".format(len(self.datasets))]
        r = "<{class_name} {{{properties}}}>".format(properties=", ".join(properties),
                                                     class_name=self.__class__.__name__)
        return r

    def __str__(self):
        return self.__repr__()

    def update_existing_datasets(self, dataset_list: List[Dataset]):
        """ Update a Project with a list of Datasets

        Update only the existing Datasets of a Project. Since the
        api/v1/project endpoint returns Projects with Datasets but
        without images, this method can be used to switch the
        existing Datasets of a Project with updated Datasets that
        have Images.

        :param List[Dataset] dataset_list: List of Datasets

        """
        dataset_ids = [d.id for d in self.datasets]
        self.datasets = [d for d in dataset_list if d.id in dataset_ids]

    def get_dataset_by_name(self, dataset_name: str) -> Dataset or None:
        """ Get a Dataset by a specific Dataset name

        :rtype: Dataset, None
        """
        for dataset in self.datasets:
            if dataset.name == dataset_name:
                return dataset

        return None

    def get_images(self) -> List[Image]:
        """ Get all Images from this Project

        :returns: List of Images
        :rtype: List[Image]

        """
        return [img for dataset in self.datasets for img in dataset.images]

    def get_images_by_name(self, image_name: str, regex: bool = False) -> List[Image]:
        """ Get Images by a specific name or search term

        :param str image_name: Image name or search term
        :param bool regex: If regex is True search with regular expressions
        :returns: List of Images from this Project
        :rtype: List[Image]

        """
        image_list = []

        for dataset in self.datasets:
            image_list += dataset.get_images_by_name(image_name, regex)

        return image_list
