from anytree import Node, RenderTree, AsciiStyle, findall, find
import re

''' @netconfparsers '''

''' interface for all network configuration parsers '''
class ConfigParser:
    def parse(self):
        pass


''' class responsible for parsing cisco network configuration into a node tree'''
class CiscoConfigParser(ConfigParser):
    nodes = []
    interfaces = []
    root = None
    config = None
    COMMENT_REGEX = re.compile("[\s]*[!]")

    def __init__(self, filename):
        # --- open file and read it
        self.filename = filename
        self.fd = open(filename, "r")
        self.config = self.fd.readlines()
        # --- create root node
        self.root = Node("root")

    ''' parses the config file into a tree '''
    def parse(self):
        indent = 0
        i = iter(self.config)
        parent = self.root
        while True:
            try:
                line = next(i).rstrip('\n')
                if self.COMMENT_REGEX.search(line):
                    continue
                if indent == (len(line) - len(line.lstrip('\t')) - 1):
                    parent = parent.children[-1]
                    Node(line.lstrip('\t'), parent=parent)
                    indent = indent + 1
                elif indent == (len(line) - len(line.lstrip('\t')) + 1):
                    parent = parent.parent
                    Node(line.lstrip('\t'), parent=parent)
                    indent = indent - 1
                else:
                    Node(line.lstrip('\t'), parent=parent)
            except StopIteration:
                break
        return self.root


''' class responsible for parsing juniper network configuration into a node tree'''
class JuniperConfigParser(ConfigParser):
    nodes = []
    interfaces = []
    root = None
    config = None
    COMMENT_REGEX = re.compile(".*[##]")
    def __init__(self, filename):
        self.filename = filename
        self.fd = open(filename, "r")
        self.config = self.fd.readlines()
        self.root = Node("root")

    def parse(self):
        i = iter(self.config)
        parent = self.root
        while True:
            try:
                line = next(i)
                if self.COMMENT_REGEX.search(line):
                    line = line.partition("##")[0]
                line = line.rstrip(" ;\n").lstrip(" ")
                if line == "}":
                    parent = parent.parent
                    continue
                if line.endswith("{"):
                    line = line.rstrip(" {")
                    Node(line, parent=parent)
                    parent = parent.children[-1]
                else:
                    Node(line, parent=parent)
            except StopIteration:
                break
        return self.root

