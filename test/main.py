from netconfparsers import JuniperConfigParser
from anytree import RenderTree, AsciiStyle


config = JuniperConfigParser("juniperexample.txt")


root = config.parse()
print(RenderTree(root, style=AsciiStyle()).by_attr())