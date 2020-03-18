from datagym.models.image import Image


class Dataset:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.short_description = data['shortDescription']
        self.timestamp = data['timestamp']
        self.owner = data['owner']
        if 'imagesCount' in data:
            self.images_count = data['imagesCount']
        else:
            self.images_count = len(data['images'])

        self.project_count = data['projectCount']

        if 'images' in data:
            self.images = [Image(image_data) for image_data in data['images']]
        else:
            self.images = []
