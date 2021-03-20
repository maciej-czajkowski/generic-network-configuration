from dictionaries import *
import json


class Translator:
    """@brief Translator interface"""
    def translate(self):
        pass


class Cisco2GenericTranslator(Translator):
    """@brief class for translating cisco config parsed tree into generic json format"""

    INTERFACE_FASTETHERNET_PREFIX = "interface FastEthernet"

    def __init__(self, root):
        self.root = root
        self.cisco_dict = CiscoDict()
        self.config = {}

    def translate(self):
        interfaces = {}
        for node in self.root.children:
            for key, callback in self.cisco_dict.cisco_dict.items():
                if node.name.startswith(key):
                    pair = callback(node)
                    if pair:
                        if pair.type is None:
                            self.add_json_entry(pair.left, pair.right)
                        if pair.type == "interface":
                            interfaces[pair.left] = pair.right
        self.config[self.cisco_dict.GENERIC_INTERFACES_SECTION] = {}
        self.add_json_entry(self.cisco_dict.GENERIC_INTERFACES_SECTION, interfaces)
        return self.config

    def get_json(self, indent):
        return json.dumps(self.config, indent=indent)

    def add_json_entry(self, key, value):
        self.config[key] = value


class Generic2JuniperTranslator(Translator):
    """ @brief class for translating generic json config into juniper tree """
    def __init__(self, generic_config):
        self.generic_config = json.loads(generic_config)

        # --- generate main nodes
        self.root = Node("root")
        main_sections = [ "system", "interfaces", "protocols", "security", "vlans"]
        for section in main_sections:
            Node(section, parent=self.root)

        # --- create proper dictionary object
        self.dict = JuniperDict(self.root)

    def translate(self):
        for key, value in self.generic_config.items():
            if key in self.dict.generic_juniper:
                self.dict.generic_juniper.get(key)(value)
        return self.root



