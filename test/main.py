from netconfparsers import JuniperConfigParser, CiscoConfigParser
from translators import *

from anytree import RenderTree, AsciiStyle
from anytree.exporter import JsonExporter

config = JuniperConfigParser("juniperexample.txt")


root = config.parse()

print(RenderTree(root, style=AsciiStyle()).by_attr())
exporter = JsonExporter(indent=4)


trans = Cisco2GenericTranslator(root)
trans.translate()
print(trans.get_json(4))

file = open("output.json", "w")
file.write(trans.get_json(4))