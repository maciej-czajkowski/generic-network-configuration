# --- REQUIRED IMPORTS
from .input_translator import *
# --- AVAIABLE MODULES
import re
from anytree import find, Node
from netaddr import IPAddress


VERSION = "1.0.1"

# --- all callback take 2 arugment, node and matched key
# --- out_json is json file avaibale for output
# --- out_anytree is anytree node tree avaiable for output
DICTIONARY = {
    "hostname": "generic_callback",
    "version": "generic_callback",
    "interface FastEthernet[0-9]*" : "fastethernet_callback"
}

# Example Tree -> json

# Example json -> json + tree

MULTI_DICT ={
    "hostname": "hostname_callback",
    "interfaces": "interfaces_callback",
}

class Config(BaseParser):
    # DO NOT EDIT THE CONSTRUCTOR
    def __init__(self, **kwargs):
        BaseParser.__init__(self, **kwargs, dict=MULTI_DICT)
    # ----

    # -- Example setup method
    def setup(self):
        Node("generared by ExampleJsonToAll", parent=self.out_anytree)
        self.system = Node("system", parent=self.out_anytree)
        self.interfaces = Node("interfaces", parent=self.out_anytree)
        self.protocols = Node("protocols", parent=self.out_anytree)
        self.security = Node("security", parent=self.out_anytree)
        self.vlans = Node("vlans", parent=self.out_anytree)

    # -- Example callback method
    def example_callback(self, node, key):
        pass

    def hostname_callback(self, node, key):
        hostname = "host-name " + node[1]
        Node(hostname, parent=self.system)

    def interfaces_callback(self, node, key):
        interface_number_regex = re.compile("[0-9]+")
        for entry in node[1]:
            for key, value in entry.items():
                if key.startswith("gigaethernet"):
                    interface_number = re.findall(interface_number_regex, key)
                    interface_nodename = "ge-0/0/" + interface_number[0]
                    interface_node = Node(interface_nodename, parent=self.interfaces)
                    unit_node = Node("unit 0", parent=interface_node)
                    family_inet_node = Node("family inet", parent=unit_node)
                    IPV4_REGEX = re.compile("(?:[0-9]{1,3}\.){3}[0-9]{1,3}")
                    ip_address = ""
                    subnet = ""
                    for if_key, if_value in value.items():
                        if if_key == "ip address":
                            ip_address = if_value
                        if if_key == "subnet":
                            subnet = if_value
                    address_node_name = "address" + " " + ip_address  + "/" \
                             + IPAddress(subnet).netmask_bits().__str__()
                    Node(address_node_name, parent=family_inet_node)





