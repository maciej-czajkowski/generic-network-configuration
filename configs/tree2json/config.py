# --- REQUIRED IMPORTS
from .input_translator import *
# --- AVAIABLE MODULES
import re
from anytree import find, Node
from netaddr import IPAddress


VERSION = "1.0.1"
TYPE ="CISCO TREE => JSON"

# --- all callback take 2 arugment, node and matched key
# --- out_json is json file avaibale for output
# --- out_anytree is anytree node tree avaiable for output
DICTIONARY = {
    "hostname": "generic_callback",
    "version": "generic_callback",
    "interface FastEthernet[0-9]*" : "fastethernet_callback"
}

# Example Tree -> json
class Config(BaseParser):
    # DO NOT EDIT THE CONSTRUCTOR
    def __init__(self, **kwargs):
        BaseParser.__init__(self, **kwargs, dict=DICTIONARY)
    # ----

    # -- Example setup method
    def setup(self):
        self.out_json["generated_by"] = "author"

    # -- Example callback method
    def example_callback(self, node, key):
        pass

    def generic_callback(self, node, key):
        self.out_json[key] = node.name.lstrip(key)

    def fastethernet_callback(self, node, key):
        # ip address and subnet address
        result = {}
        IPV4_REGEX = re.compile("(?:[0-9]{1,3}\.){3}[0-9]{1,3}")
        ip_node = find(node, filter_=lambda node: node.name.find("ip address") >= 0)
        if ip_node:
            if ip_node.name == "no ip address":
                result["ip address"] = False
                result["subnet"] = False
            else:
                address = re.findall(IPV4_REGEX, ip_node.name)
                if len(address) != 2:
                    logger("Error: ip address must be defined with subnet mask, node: " + node.__str__())
                result["ip address"] = address[0]
                result["subnet"] = address[1]
        else:
            logger("Error: ip address must be defined, node: " + node.__str__())

        # mode trunk
        ip_node = find(node, filter_=lambda node: node.name.find("trunk mode") >= 0)
        if ip_node:
            result["trunk mode"] = True
        else:
            result["trunk mode"] = False
        # add here more parse rules
        self.out_json[node.name] = result

