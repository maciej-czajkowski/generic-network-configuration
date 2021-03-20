from anytree import find
import re

''' Simple C++ like Pair implementation'''
class Pair:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "(" + self.left + ", " + self.right + ")"


''' Dictinary interface '''
class Dict:
    IP_ADDRESS = "ip address"
    SUBNET = "subnet"

    IPV4_REGEX = re.compile("(?:[0-9]{1,3}\.){3}[0-9]{1,3}")

    def __init__(self):
        pass


''' Generic dictionary '''
class GenericDict(Dict):
    GENERIC_HOSTNAME = "hostname"
    GENERIC_UNCRYPTED_PASSWORD = "uncrypted password"
    GENERIC_INTERFACE = "interface"
    GENERIC_TRUNK_MODE = "mode trunk"


''' Cisco - Generic dictionary '''
class CiscoDict(GenericDict):
    HOSTNAME = "hostname"
    UNCRYPTED_PASSWORD = "enable password"
    INTERFACE_FASTETHERNET = "interface FastEthernet"
    CISCO_NO_SET_IP_ADDRESS = "no ip address"
    CISCO_TRUNK_MODE = "switch mode trunk"


    def __init__(self):
        # --- generic values callbacks
        self.generic_dict = {
                              Pair(self.HOSTNAME,           self.GENERIC_HOSTNAME)           : self.generic_callback,
                              Pair(self.UNCRYPTED_PASSWORD, self.GENERIC_UNCRYPTED_PASSWORD) : self.generic_callback,
                     }

        # --- interfaces callback
        self.interface_dict = {
                              self.INTERFACE_FASTETHERNET : self.fast_ethernet_callback,
                     }

    ''' generic callback for translating cisco to generic format
        @ key_pair - Pair of cisco name and generic name strings
        @ node     - parsed node
        @ returns  - key, value generic pair'''

    def generic_callback(self, key_pair, node):
        if node is None or key_pair is None:
            print("Error: provide proper args for the callback")
            return
        return Pair(key_pair.right, node.name.lstrip(key_pair.left + " "))

    '''  callback for translating fast ethernet from cisco to generic format
         @ node     - parsed fest ethernet interface node
         @ returns  - (interface name, interface values) pair'''
    def fast_ethernet_callback(self, node):
        if node is None:
            print("Error: provide proper args for the callback")

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
                print(address)
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

        return Pair(node.name, result)

