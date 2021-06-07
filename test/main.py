from netconfparsers import CiscoConfigParser
from translators import *
from ConfigGenerator import ciscoGenerator
from anytree import RenderTree, AsciiStyle
from anytree.exporter import JsonExporter

config = CiscoConfigParser("ciscoexample.txt")
root = config.parse()

trans = Cisco2GenericTranslator(root)
trans.translate()
print(trans.get_json(4))

file = open("output.json", "w")
file.write(trans.get_json(4))

juniper = Generic2JuniperTranslator(trans.get_json(4)).translate()
print(RenderTree(juniper, style=AsciiStyle()).by_attr())
