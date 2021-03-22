from netconfparsers import JuniperConfigParser, CiscoConfigParser
from translators import *
from ConfigGenerator import ciscoGenerator
from anytree import RenderTree, AsciiStyle
from anytree.exporter import JsonExporter

config = JuniperConfigParser("juniperexample.txt")
configC = CiscoConfigParser("ciscoexample.txt")

root2 = configC.parse()
root = config.parse()

print(RenderTree(root2, style=AsciiStyle()).by_attr())

generator = ciscoGenerator(root2)
cfg = generator.cfgGenerator()
generator.write_to_file("generatedCisco.txt", cfg)
# for i in generator.cfgGenerator():
#     print(i)

exporter = JsonExporter(indent=4)


trans = Cisco2GenericTranslator(root)
trans.translate()
print(trans.get_json(4))

file = open("output.json", "w")
file.write(trans.get_json(4))