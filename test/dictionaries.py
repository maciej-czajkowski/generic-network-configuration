from anytree import find, Node
import re
from enum import Enum
from netaddr import IPAddress


class Interfaces(Enum):
    """ @brief Enum class for interface types"""
    FASTETHERNET = 1

class Pair:
    """ @brief Simple C++ like Pair implementation with added type field for general usage"""
    def __init__(self, left, right, type=None):
        self.left = left
        self.right = right
        self.type = type

    def __repr__(self):
        return "(" + self.left + ", " + self.right + ")"


class Dict:
    """ @brief Dictionary interface
        holds objects shared by all dictionary objects """

    IP_ADDRESS = "ip address"
    SUBNET = "subnet"
    IPV4_REGEX = re.compile("(?:[0-9]{1,3}\.){3}[0-9]{1,3}")

    def __init__(self):
        pass


class GenericDict(Dict):
    """ @brief Generic dictionary """

    GENERIC_HOSTNAME = "hostname"
    GENERIC_UNCRYPTED_PASSWORD = "uncrypted password"
    GENERIC_INTERFACES_SECTION = "interfaces"
    GENERIC_INTERFACE = "interface"
    GENERIC_FASTETHERNET_INTERFACE = "interface FastEthernet"
    GENERIC_TRUNK_MODE = "mode trunk"


class CiscoDict(GenericDict):
    """ @brief Cisco - Generic dictionary
        class used for translating cisco configuration into generic json"""

    HOSTNAME = "hostname"
    UNCRYPTED_PASSWORD = "enable password"
    INTERFACE_FASTETHERNET = "interface FastEthernet"
    CISCO_NO_SET_IP_ADDRESS = "no ip address"
    CISCO_TRUNK_MODE = "switch mode trunk"
    INTERFACE_PREFIX = "interface "

    def __init__(self):
        self.cisco_dict = {
                          self.HOSTNAME           : self.generic_callback,
                          self.UNCRYPTED_PASSWORD : self.generic_callback,
                          self.INTERFACE_PREFIX   : self.interface_callback,
                         }

        self.cisco2generic_dict = {
                                   self.HOSTNAME           : self.GENERIC_HOSTNAME,
                                   self.UNCRYPTED_PASSWORD : self.GENERIC_UNCRYPTED_PASSWORD,
                                  }

    def generic_callback(self, node):
        """ @brief callback for translating simple cisco key - value pairs to generic format
            @ node     - parsed node
            @ returns  - key, value generic pair"""
        if node is None :
            print("Error: provide proper args for the callback")
            return
        for cisco_key, generic_key in self.cisco2generic_dict.items():
            if node.name.startswith(cisco_key):
                return Pair(generic_key, node.name.lstrip(cisco_key + " "))
        return None

    def interface_callback(self, node):
        """ @brief callback for translating interfaces
            @ node     - parsed fest ethernet interface node
            @ returns  - (interface name, interface values) pair"""
        type = self.check_cisco_interface_type(node.name)
        if type == Interfaces.FASTETHERNET:
            return self.fastethernet_callback(node)

    def fastethernet_callback(self, node):
        """  @brief callback for translating fast ethernet interfaces
             @ node     - parsed fest ethernet interface node
             @ returns  - (interface name, interface values) pair"""
        result = {}
        # ip address and subnet address
        ip_node = find(node, filter_=lambda node: node.name.find(self.IP_ADDRESS) >= 0)
        if ip_node:
            if ip_node.name == self.CISCO_NO_SET_IP_ADDRESS:
                result[self.IP_ADDRESS] = False
                result[self.SUBNET] = False
            else:
                address = re.findall(self.IPV4_REGEX, ip_node.name)
                if len(address) != 2:
                    print("Error: ip address must be defined with subnet mask, node: " + node.__str__())
                result[self.IP_ADDRESS] = address[0]
                result[self.SUBNET] = address[1]
        else:
            print("Error: ip address must be defined, node: " + node.__str__())
            return

        # mode trunk
        ip_node = find(node, filter_=lambda node: node.name.find(self.GENERIC_TRUNK_MODE) >= 0)
        if ip_node:
            result[self.GENERIC_TRUNK_MODE] = True
        else:
            result[self.GENERIC_TRUNK_MODE] = False
        # add here more parse rules

        return Pair(node.name, result, type="interface")
            # return Pair(node.name, result)

    def check_cisco_interface_type(self, string):
        """  @brief checks string for interface type
             @ string   - name of interface node
             @ returns  - Interface Enum with type"""
        if string.startswith(self.INTERFACE_FASTETHERNET):
            return Interfaces.FASTETHERNET


class JuniperDict(GenericDict):
    """ @brief Juniper - Generic dictionary
        class used for translating juniper configuration into generic json"""
    HOSTNAME = "host-name"
    GIGAETHERNET_PREFIX = "ge-0/0/"
    LINE_END = ";"
    ENCRYPTED_PASSWORD = "encrypted password"

    def __init__(self, root):
        self.root = root
        self.generic_juniper = {
                               self.GENERIC_HOSTNAME           : self.hostname_callback,
                               self.GENERIC_UNCRYPTED_PASSWORD : self.uncrypted_password_callback,
                               self.GENERIC_INTERFACES_SECTION : self.interfaces_callback,
                               }

    def hostname_callback(self, value):
        """ @brief callback for translating generic hostname value into juniper configuration
            generates juniper hostname node
            @ node     - parsed fest ethernet interface node
            @ returns  - juniper hostname node"""
        system = find(self.root, filter_=lambda node : node.name == "system")
        node = Node(self.HOSTNAME + " " + value + self.LINE_END, parent=system)
        return node

    def uncrypted_password_callback(self, value):
        """ @brief callback for translating generic uncrypted password value into juniper configuration
            generates juniper uncrypted password node
            @ node     - parsed fest ethernet interface node
            @ returns  - juniper uncrypted password node"""
        system = find(self.root, filter_=lambda node : node.name == "system")
        root_authentication = find(system, filter_=lambda node : node.name == "root-authentication")
        if root_authentication is None:
            root_authentication = Node("root_authentication", parent=system)
        node = Node(self.ENCRYPTED_PASSWORD + " " + value + self.LINE_END, parent=root_authentication)
        return node

    def interfaces_callback(self, dict):
        """ @brief callback for translating interfaces
            generates juniper interface nodes
            @ node     - parsed fest ethernet interface node
            @ returns  - (interface name, interface values) pair"""
        for interface in dict.keys():
            type = self.check_interface_type(interface)
            if type == Interfaces.FASTETHERNET:
                self.fastethernet_callback(interface, dict[interface])

    def check_interface_type(self, string):
        if string.startswith(self.GENERIC_FASTETHERNET_INTERFACE):
            return Interfaces.FASTETHERNET

    def fastethernet_callback(self, key, values):
        """ @brief callback for translating fastethernet interfaces
            generates juniper fastethernet node
            @ key     - interface name in generic json
            @ values  - interface values dict in generic json"""
        # -- tempory we change fast to giga/0/0 <- don't know what those two 0 mean
        interfaces = find(self.root, filter_=lambda node : node.name == self.GENERIC_INTERFACES_SECTION)
        interface_name = self.GIGAETHERNET_PREFIX + key.lstrip(self.GENERIC_FASTETHERNET_INTERFACE)
        main = Node(interface_name, parent=interfaces)
        unit_0 = Node("unit 0", parent=main)
        family_inet = Node("family inet", parent=unit_0)
        if values[self.IP_ADDRESS]:
            ip_address_value = "address" + " " + values[self.IP_ADDRESS]  + "/" \
                             + IPAddress(values[self.SUBNET]).netmask_bits().__str__() + self.LINE_END
            ip_address = Node(ip_address_value, parent=family_inet)


