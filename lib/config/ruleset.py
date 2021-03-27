import yaml
import os


class Ruleset:
    _instance = None

    def __init__(self):
        raise RuntimeError("Call instance() instead")

    @classmethod
    def rules(cls) -> dict:
        if not cls._instance:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../rules.yaml")
            with open(file_path) as myFile:
                cls._instance = yaml.safe_load(myFile).get("rules")
            print(cls._instance)
        return cls._instance
