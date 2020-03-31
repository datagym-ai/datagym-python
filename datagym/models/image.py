from typing import Dict


class Image:
    """ The Image class is modelled after the DataGym.io Image

    DataGym.io Images fetched from the DataGym API will be parsed
    into Image objects.

    """

    def __init__(self, data: Dict):
        """ Initializes DataGym Image instance

        :param Dict data: Response data from the DataGym API

        """
        self.id = data['id']
        self.image_name = data['imageName']
        self.image_type = data['imageType']
        self.timestamp = data['timestamp']

    def __repr__(self):
        """ Return useful representation of a the Image

        The Image attributes should be readable, template:
            <Image { attribute1: value1, attribute2: value2, ... }>

        :return: Return readable repr of the Image
        """
        return f'<Image {self.__dict__}>'

    def __str__(self):
        return self.__repr__()
