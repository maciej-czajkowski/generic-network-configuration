from GNCapp.python_scripts.test.netconfparsers import CiscoConfigParser
from GNCapp.python_scripts.test.translators import *
from GNCapp.python_scripts.test.ConfigGenerator import ciscoGenerator
from anytree import RenderTree, AsciiStyle
from anytree.exporter import JsonExporter

# add splitting filename to name/dot/extension, will be necessary for creating output filename
def ciscoToJSON(filename):
    file = ""
    filepath = "GNCapp/static/uploads/" + filename
    outfilepath = "GNCapp/static/uploads/" + filename + ".json"
    config = CiscoConfigParser(filepath)
    file = open(filepath)
    root = config.parse()

    trans = Cisco2GenericTranslator(root)
    trans.translate()
    print(trans.get_json(4))
    file = open(outfilepath, "w")
    file.write(trans.get_json(4))
    file.close()


def ciscoToJuniper(filename):print('ciscoToJuniper')
def juniperToCisco(filename):print('juniperToCisco')
def juniperToJSON(filename):print('juniperToJSON')
def JSONToCisco(filename):print('JSONToCisco')
def JSONToJuniper(filename):print('JSONToJuniper')

