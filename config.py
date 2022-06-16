import yaml


class Config:
    def __init__(self, _networks: dict):
        self.networks = _networks


def load_config(filename: str):
    with open("config.yaml") as file:
        data_dict = yaml.load(file, Loader=yaml.FullLoader)
    config = Config(data_dict["networks"])
    return config
