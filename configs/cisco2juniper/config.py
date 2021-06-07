# --- REQUIRED IMPORTS
from .input_translator import *
# --- AVAIABLE MODULES
import re
from anytree import find, Node
from netaddr import IPAddress


VERSION = "1.0.1"
TYPE = "CISCO TREE => JUNIPER TREE"



DICTIONARY_TREE ={
    "hostname": "hostname_callback",
    "version": "version_callback",
    "interface FastEthernet[0-9]*" : "fastethernet_callback"
}

# Example Tree -> Tree
class Config(BaseParser):
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
