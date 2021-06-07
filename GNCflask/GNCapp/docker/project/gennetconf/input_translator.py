import json
import re
from anytree import PreOrderIter, Node
import nanolog as nl
from .mainlog import logger



class BaseParser:
    # tree - input tree
    # json - input json
    # dict - dictionary
    def __init__(self, **kwargs):
        if 'tree' in kwargs:
            self.__any_tree = kwargs["tree"]
        if 'json' in kwargs:
            self.__json = kwargs["json"]
        self.out_json = {}
        self.out_anytree = Node("root")
        if 'dict':
            self.__dictionary = kwargs["dict"]

    def parse_tree(self):
        self.setup()
        myself = self
        for node in PreOrderIter(self.__any_tree):
            for key, value in self.__dictionary.items():
                if re.match(key, node.name):
                    # logger.info("Parsing node: ", node.name, "according to configuration.")
                    getattr(myself, value)(node, key)
                # else:
                    # logger.info("Skipping node: ", node.name, "as callbacks for it were not defined in config file.")

    def parse_json(self):
        self.setup()
        myself = self
        for config_key, config_value in self.__json.items():
            match = False
            for key, value in self.__dictionary.items():
                if re.match(key, config_key):
                    match = True
                    getattr(myself, value)((config_key, config_value), key)
            # if match:
                # logger.info("Parsing entry: ", config_key, " : ", config_value, " according to configuration.")
            # else:
                # logger.info("Skipping entry: ", config_key, " : ", config_value, " as callbacks for it were not defined in config file.")

    def get_json(self, indent):
        return json.dumps(self.out_json, indent=indent)

    def get_tree(self):
        return self.out_anytree

    def clear(self):
        self.__any_tree = None
        self.out_json = {}
        self.out_anytree = Node("root")
        self.__dictionary = None

    def generic_callback(self, node, key):
        pass

    def setup(self):
        pass


