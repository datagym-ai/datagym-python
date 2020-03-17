from datagym.models.dataset import Dataset


class Project:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.short_description = data['shortDescription']
        self.timestamp = data['timestamp']
        self.label_config_id = data['labelConfigurationId']
        self.label_iteration_id = data['labelIterationId']
        self.owner = data['owner']
        self.datasets = [Dataset(dataset_response_dict) for dataset_response_dict in data['datasets']]