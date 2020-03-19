class Image:

    def __init__(self, data):
        self.id = data['id']
        self.image_name = data['imageName']
        self.image_type = data['imageType']
        self.timestamp = data['timestamp']

    def __repr__(self):
        return f'<Image {self.__dict__}>'

    def __str__(self):
        return f'<Image {self.__dict__}>'
