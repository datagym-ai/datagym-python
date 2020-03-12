class Client:

    __api_key = ""

    def __init__(self, api_key) -> None:
        self.__api_key = api_key

    def get_projects(self):
        return [{'name': 'first_project', 'owner': 'user1'}, {'name': 'second_project', 'owner': 'user1'}]
