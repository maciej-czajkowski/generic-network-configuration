from anytree import Node
import re

""" @parsers """


class ConfigParser:
    """ @brief interface for all network configuration parsers """
    def parse(self):
        pass


class CiscoConfigParser(ConfigParser):
    """ @brief class responsible for parsing cisco network configuration into a node tree """

    __COMMENT_REGEX = re.compile("[\s]*[!]")

    def __init__(self, filename):
        # --- open file and read it
        self.__filename = filename
        self.__fd = open(filename, "r")
        self.__config = self.__fd.readlines()
        # --- create root node
        self.__root = Node("root")

    def parse(self):
        """ @brief parses the config file into a tree """
        indent = 0
        i = iter(self.__config)
        parent = self.__root
        while True:
            try:
                line = next(i).rstrip('\n')

                if self.__COMMENT_REGEX.search(line):
                    continue

                if indent == (len(line) - len(line.lstrip(' ')) - 1):
                    parent = parent.children[-1]
                    Node(line.lstrip(' '), parent=parent)
                    indent = indent + 1
                elif indent == (len(line) - len(line.lstrip(' ')) + 1):
                    parent = parent.parent
                    Node(line.lstrip(' '), parent=parent)
                    indent = indent - 1
                else:
                    Node(line.lstrip(' '), parent=parent)
            except StopIteration:
                break
        return self.__root


class JuniperConfigParser(ConfigParser):
    """ @brief class responsible for parsing juniper network configuration into a node tree """

    __COMMENT_REGEX = re.compile(".*[##]")

    def __init__(self, filename):
        self.__filename = filename
        self.__fd = open(filename, "r")
        self.__config = self.__fd.readlines()
        self.__root = Node("root")

    def parse(self):
        """ @brief parses the config file into a tree """
        i = iter(self.__config)
        parent = self.__root
        while True:
            try:
                line = next(i)
                if line.startswith("##"):
                    continue

                if self.__COMMENT_REGEX.search(line):
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
        return self.__root


