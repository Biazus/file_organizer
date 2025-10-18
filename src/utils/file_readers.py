import yaml

class YamlReader:
    data: dict = None

    def __init__(self, path: str):
        with open(path, 'r') as file:
            try:
                self.data = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print("Error loading your file")