import gennetconf as cfg
from anytree import RenderTree
import json as js

def printHeader(string):
    print("###"*10)
    print("### ", string, " ###")
    print("###"*10)



cisco_config_tree = cfg.CiscoConfigParser("input/ciscoexample.txt").parse()

printHeader("Input tree")
print(RenderTree(cisco_config_tree).by_attr('name'))

printHeader("TREE => JSON")

example_json = cfg.ConfigJson(tree=cisco_config_tree)
example_json.parse_tree()
json = example_json.get_json(4)
print(json)

printHeader("TREE => TREE")


example_tree = cfg.ConfigTree(tree=cisco_config_tree)
example_tree.parse_tree()
tree = example_tree.get_tree()
print(RenderTree(tree).by_attr('name'))




file = open("input/sampleJson.json", "r").read()
json_in = js.loads(file)

printHeader("Input Json")
print(file)

printHeader("JSON => TREE")

example2 = cfg.ExampleJsonToAll(json=json_in)
example2.parse_json()
output_tree = example2.get_tree()
print(RenderTree(output_tree).by_attr('name'))



