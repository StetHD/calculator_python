import json


class Config:
    def __init__(self, config_json):
        config_file = open(config_json)
        config = json.load(config_file)
        self.app_name = config["app_name"]
        self.messages = config["messages"]
        self.font = config["font"]
        self.window = config["window"]
        self.buttons = config["buttons"]
