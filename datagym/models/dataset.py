from datagym.models.image import Image
from typing import List
import re


class Dataset:

    def __init__(self, data):
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
        properties = [f"'{e[0]}': '{e[1]}'" for e in self.__dict__.items() if e[0] != "images"]
        properties += ["'images': <List[Image] with {} elements>".format(len(self.images))]
        r = "<{class_name} {{{properties}}}>".format(properties=", ".join(properties),
                                                     class_name=self.__class__.__name__)
        return r

    def __str__(self):
        return self.__repr__()

    def get_images_by_name(self, image_name: str, regex: bool = False) -> List[Image]:
        if regex:
            r = re.compile(image_name)
            return [img for img in self.images if r.match(img.image_name)]
        else:
            return [img for img in self.images if img.image_name == image_name]
