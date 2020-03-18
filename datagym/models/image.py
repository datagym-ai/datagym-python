class Image:

    def __init__(self, data):
        self.id = data['id']
        self.image_name = data['imageName']
        self.image_type = data['imageType']
        self.timestamp = data['timestamp']
