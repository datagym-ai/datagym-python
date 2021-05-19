from typing import Dict


class Video:
    """ The Video class is modelled after the DataGym.io Video

    DataGym.io Videos fetched from the DataGym API will be parsed
    into Video objects.

    """

    def __init__(self, data: Dict):
        """ Initializes DataGym Video instance

        :param Dict data: Response data from the DataGym API

        """
        self.id = data['id']
        self.video_name = data['mediaName']
        self.video_type = data['mediaSourceType']
        self.timestamp = data['timestamp']

    def __repr__(self):
        """ Return useful representation of a the Video
        The Video attributes should be readable, template:
        <Video { attribute1: value1, attribute2: value2, ... }>

        :return: Return readable repr of the Video
        """
        return f'<Video {self.__dict__}>'

    def __str__(self):
        """ Return useful representation of a the Video when called with print()
        :return: Return readable string for the Video
        """
        string_repr = f'\n{"Video:":<18} {self.video_name}\n' \
                      f'{"Video_id:":<18} {self.id}\n' \
                      f'{"Video type:":<18} {self.video_type}\n' \
                      f'{"Video timestamp:":<18} {self.timestamp} \n'
        return string_repr
