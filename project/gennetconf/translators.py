from dictionaries import *
import json


class Translator:
    """@brief Translator interface"""
    def __translate(self):
        pass


class Cisco2GenericTranslator(Translator):
    """@brief class for translating cisco config parsed tree into generic json format"""

    INTERFACE_FASTETHERNET_PREFIX = "interface FastEthernet"

    def __init__(self, root):
        self.__root = root
        self.__cisco_dict = CiscoDict()
        self.__config = {}
        self.__translate()

    def __translate(self):
        interfaces = {}
        for node in self.__root.children:
            for key, callback in self.__cisco_dict.cisco_dict.items():
                if node.name.startswith(key):
                    pair = callback(node)
                    if pair:
                        if pair.type is None:
                            self.add_json_entry(pair.left, pair.right)
                        if pair.type == "interface":
                            interfaces[pair.left] = pair.right
        self.__config[self.__cisco_dict.GENERIC_INTERFACES_SECTION] = {}
        self.add_json_entry(self.__cisco_dict.GENERIC_INTERFACES_SECTION, interfaces)

    def get_config(self):
        return self.__config

    def get_json(self, indent):
        return json.dumps(self.__config, indent=indent)

    def add_json_entry(self, key, value):
        self.__config[key] = value


class Generic2JuniperTranslator(Translator):
    """ @brief class for translating generic json config into juniper tree """
    def __init__(self, generic_config):
        self.__generic_config = json.loads(generic_config)

        # --- generate main nodes
        self.__root = Node("root")
        main_sections = [ "system", "interfaces", "protocols", "security", "vlans"]
        for section in main_sections:
            Node(section, parent=self.__root)

        # --- create proper dictionary object
        self.__dict = JuniperDict(self.__root)
        self.__translate()

    def __translate(self):
        for key, value in self.__generic_config.items():
            if key in self.__dict.generic_juniper:
                self.__dict.generic_juniper.get(key)(value)
        return self.__root

    def get_root(self):
        return self.__root



