from anytree import findall
from dictionaries import *
import json


class Translator:
    def translate(self):
        pass


class Cisco2GenericTranslator(Translator):
    INTERFACE_FASTETHERNET = "interface FastEthernet"
    def __init__(self, root):
        self.root = root
        self.cisco_dict = CiscoDict()
        self.config = {}


    def translate(self):
        # --- translate simple nodes
        generic_nodes = findall(self.root, filter_=lambda node : len(node.children) == 0)
        for node in generic_nodes:
            name = node.name
            for keys, callback in self.cisco_dict.generic_dict.items():
                if name.startswith(keys.left):
                    self.add_json_generic_entry(callback(keys, node))

        # -- translation of interface nodes (ethernet for now only
        self.config["intefaces"] = {}
        self.interfaces = {}
        self.config["intefaces"] = self.interfaces

        # --- ethernet interfaces
        interface_nodes = findall(self.root, filter_=lambda node : node.name.startswith(self.INTERFACE_FASTETHERNET))
        for node in interface_nodes:
            self.add_json_interface_entry(self.cisco_dict.interface_dict[self.INTERFACE_FASTETHERNET](node))

        return self.config

    def get_json(self, indent):
        return json.dumps(self.config, indent=indent)

    def add_json_generic_entry(self, pair):
        self.config[pair.left] = pair.right

    def add_json_interface_entry(self, pair):
        self.interfaces[pair.left] = pair.right


