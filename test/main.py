from netconfparsers import CiscoConfigParser
from anytree import RenderTree, AsciiStyle


config = CiscoConfigParser("ciscoexample.txt")
root = config.parse()
print(RenderTree(root, style=AsciiStyle()).by_attr())