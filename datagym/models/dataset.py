class Dataset:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.short_description = data['shortDescription']
        self.timestamp = data['timestamp']
        self.owner = data['owner']
        self.images_count = data['imagesCount']
        self.project_count = data['projectCount']