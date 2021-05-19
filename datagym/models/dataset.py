from datagym.models.image import Image
from datagym.models.video import Video
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

        self.media_type = data['mediaType']
        if 'media' in data:
            if self.media_type == "IMAGE":
                self.media: List[Image] = [Image(media_data) for media_data in data['media']]
                self.images = self.media
            elif self.media_type == "VIDEO":
                self.media: List[Video] = [Video(media_data) for media_data in data['media']]
                self.images = None
            else:
                self.media = []
                self.images = None
        else:
            self.media = []
            self.images = None

    def __repr__(self):
        """ Return useful representation of a the Dataset

        The Dataset attributes should be readable, template:
            <Dataset { attribute1: value1, attribute2: value2, ... }>
        Special case:
            <Dataset { ... media: <List[Image|Video] with n elements> ... }>

        :return: Return readable repr of the dataset
        """
        properties = [f"'{e[0]}': '{e[1]}'" for e in self.__dict__.items() if e[0] != "media"]

        if self.media_type == "IMAGE":
            properties += ["'media': <List[Image] with {} elements>".format(len(self.media))]
        elif self.media_type == "VIDEO":
            properties += ["'media': <List[Video] with {} elements>".format(len(self.media))]
        else:
            properties += "No media"

        r = "<{class_name} {{{properties}}}>".format(properties=", ".join(properties),
                                                     class_name=self.__class__.__name__)
        return r

    def __str__(self):
        """ Return useful representation of a the Dataset when called with print()
        :return: Return readable string for the Dataset
        """
        if self.media_type == "IMAGE":
            temp_string_repr = f'{"Images:":<18} {len(self.media)}\n'
        elif self.media_type == "VIDEO":
            temp_string_repr = f'{"Videos:":<18} {len(self.media)}\n'
        else:
            temp_string_repr = 'No media'

        string_repr = f'\n{"Dataset:":<18} {self.name}\n' \
                      f'{"Dataset_id:":<18} {self.id}\n' \
                      f'{"Description:":<18} {self.short_description}\n' \
                      f'{"Media Type:":<18} {self.media_type}\n' \
                      f'{temp_string_repr}'

        return string_repr

    def get_images_by_name(self, image_name: str, regex: bool = False) -> List[Image] or []:
        """ Get Media by a specific name or search term
        This function is now deprecated. Please use get_media_by_name(media_name, regex).

        :param str image_name: Media name or search term
        :param bool regex: If regex is True search with regular expressions
        :returns: List of Media from this Dataset
        :rtype: List[Image]

        """
        return self.get_media_by_name(image_name, regex)

    def get_media_by_name(self, media_name: str, regex: bool = False) -> List[Image] or List[Video] or []:
        """ Get Media by a specific name or search term

        :param str media_name: Media name or search term
        :param bool regex: If regex is True search with regular expressions
        :returns: List of Media from this Dataset
        :rtype: List[Image|Video]

        """
        if regex:
            r = re.compile(media_name)
            if self.media_type == "IMAGE":
                return [img for img in self.media if r.match(img.image_name)]
            elif self.media_type == "VIDEO":
                return [vid for vid in self.media if r.match(vid.video_name)]
            else:
                return []
        else:
            if self.media_type == "IMAGE":
                return [img for img in self.media if img.image_name == media_name]
            elif self.media_type == "VIDEO":
                return [vid for vid in self.media if vid.video_name == media_name]
            else:
                return []
