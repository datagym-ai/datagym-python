from datagym.models.image import Image
from typing import List, Dict
import re


class Dataset:
    """ The Dataset class is the model of a DataGym.io Dataset

    DataGym.io Datasets fetched from the DataGym API will be parsed
    into Dataset objects.

    """

    def __init__(self, data: Dict):
        """ Initializes DataGym Dataset instance

        :param Dict data: Response data from the DataGym API

        """
        self.id = data['id']
        self.name = data['name']
        self.short_description = data['shortDescription']
        self.timestamp = data['timestamp']
        self.owner = data['owner']

        if 'images' in data:
            self.images: List[Image] = [Image(image_data) for image_data in data['images']]
        else:
            self.images: List[Image] = []

    def __repr__(self):
        """ Return useful representation of a the Dataset

        The Dataset attributes should be readable, template:
            <Dataset { attribute1: value1, attribute2: value2, ... }>
        Special case:
            <Dataset { ... images: <List[Image] with n elements> ... }>

        :return: Return readable repr of the dataset
        """
        properties = [f"'{e[0]}': '{e[1]}'" for e in self.__dict__.items() if e[0] != "images"]
        properties += ["'images': <List[Image] with {} elements>".format(len(self.images))]
        r = "<{class_name} {{{properties}}}>".format(properties=", ".join(properties),
                                                     class_name=self.__class__.__name__)
        return r

    def __str__(self):
        """ Return useful representation of a the Dataset when called with print()

                :return: Return readable string for the Dataset
                """
        string_repr = f'\n{"Dataset:":<18} {self.name}\n' \
                      f'{"Dataset_id:":<18} {self.id}\n' \
                      f'{"Description:":<18} {self.short_description}\n' \
                      f'{"Images:":<18} {len(self.images)} \n'
        return string_repr

    def get_images_by_name(self, image_name: str, regex: bool = False) -> List[Image]:
        """ Get Images by a specific name or search term

        :param str image_name: Image name or search term
        :param bool regex: If regex is True search with regular expressions
        :returns: List of Images from this Dataset
        :rtype: List[Image]

        """
        if regex:
            r = re.compile(image_name)
            return [img for img in self.images if r.match(img.image_name)]
        else:
            return [img for img in self.images if img.image_name == image_name]
