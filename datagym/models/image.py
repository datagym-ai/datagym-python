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
        """ Return useful representation of a the Image when called with print()

        :return: Return readable string for the Image
        """
        string_repr = f'\n{"Image:":<18} {self.image_name}\n' \
                      f'{"Image_id:":<18} {self.id}\n' \
                      f'{"Image type:":<18} {self.image_type}\n' \
                      f'{"Image timestamp:":<18} {self.timestamp} \n'
        return string_repr
