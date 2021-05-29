# --- REQUIRED IMPORTS
from input_translator import BaseParser, logger
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
class ConfigJson(BaseParser):
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


DICTIONARY_TREE ={
    "hostname": "hostname_callback",
    "version": "version_callback",
    "interface FastEthernet[0-9]*" : "fastethernet_callback"
}

# Example Tree -> Tree
class ConfigTree(BaseParser):
    # DO NOT EDIT THE CONSTRUCTOR
    def __init__(self, **kwargs):
        BaseParser.__init__(self, **kwargs, dict=DICTIONARY_TREE)
    # ----

    # -- Example setup method
    def setup(self):
        Node("generared by author", parent=self.out_anytree)
        self.system = Node("system", parent=self.out_anytree)
        self.interfaces = Node("interfaces", parent=self.out_anytree)
        self.protocols = Node("protocols", parent=self.out_anytree)
        self.security = Node("security", parent=self.out_anytree)
        self.vlans = Node("vlans", parent=self.out_anytree)

    # -- Example callback method
    def example_callback(self, node, key):
        pass

    def hostname_callback(self, node, key):
        hostname = "host-name " + node.name.lstrip("hostname")
        Node(hostname, parent=self.system)

    def version_callback(self, node, key):
        version = "version " + node.name.lstrip("version")
        Node(version, parent=self.out_anytree)

    def fastethernet_callback(self, node, key):
        # ip address and subnet address
        interface_number_regex = re.compile("[0-9]+")
        interface_number = re.findall(interface_number_regex, node.name)
        interface_nodename = "ge-0/0/" + interface_number[0]
        interface_node = Node(interface_nodename, parent=self.interfaces)
        unit_node = Node("unit 0", parent=interface_node)
        family_inet_node = Node("family inet", parent=unit_node)
        IPV4_REGEX = re.compile("(?:[0-9]{1,3}\.){3}[0-9]{1,3}")
        ip_node = find(node, filter_=lambda node: node.name.find("ip address") >= 0)
        if ip_node:
            if ip_node.name != "no ip address":
                address = re.findall(IPV4_REGEX, ip_node.name)
                if len(address) != 2:
                    logger("Error: ip address must be defined with subnet mask, node: " + node.__str__())
                address_node_name = "address" + " " + address[0]  + "/" \
                             + IPAddress(address[1]).netmask_bits().__str__()
                Node(address_node_name, parent=family_inet_node)
        else:
            logger("Error: ip address must be defined, node: " + node.__str__())

# Example json -> json + tree

MULTI_DICT ={
    "hostname": "hostname_callback",
    "interfaces": "interfaces_callback",
}

class ExampleJsonToAll(BaseParser):
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





