
class Node:
    def __init__(self, value):
        self.value = value
        self.childs = []
        self.parent = None

    def __str__(self):
        return self.value

    def __repr__(self):

        return self.value + self.childs.__repr__()


def generate_indent(number):
    string = ""
    for x in number:
        string = string + "\t"
    return string


class CiscoConfig:
    nodes = []

    def __init__(self, file):
        self.file = file
        self.fd = open(file, "r")
        root = Node("root")
        config = self.create_entry_list(self.fd.readlines())

        i = iter(config)
        indent = 0
        parent = root

        while True:
            try:
                line = next(i)
                if indent == (len(line) - len(line.lstrip('\t')) - 1):
                    parent = parent.childs[-1]
                    node = Node(line.lstrip('\t'))
                    node.parent = parent
                    indent = indent +1
                elif indent == (len(line) - len(line.lstrip('\t')) + 1):
                    parent = parent.parent
                    node = Node(line.lstrip('\t'))
                    node.parent = parent
                    indent = indent -1
                else:
                    node = Node(line.lstrip('\t'))
                    node.parent = parent

                if parent == root:
                    self.nodes.append(node)
                parent.childs.append(node)


            except StopIteration:
                if indent > 0:
                    print("error in prasing, too many indents")# if StopIteration is raised, break from loop
                break
        print(self.nodes)


    def create_entry_list(self, config):
        parsed_config = []
        for line in config:
            entry = line.replace("\n","")
            if "!" not in entry:
                parsed_config.append(entry)
        return parsed_config




        #
        # while True:
        #     try:
        #         self.config.remove("!")
        #     except ValueError:
        #         break;
        # print(self.config)
        # i = iter(self.config)
        # indent = 0
        # while True:
        #     try:
        #         line = next(i)
        #         if line == "!":
        #             line = next(i)
        #             while line == "!":
        #                 line = next(i)
        #             node = Node(line)
        #             line = next(i)
        #             if line.startswith(generate_spaces(indent + 1)):
        #                 Node
        #
        #
        #         # do something with element
        #     except StopIteration:
        #         if indent > 0:
        #             print("error in prasing, too many indents")# if StopIteration is raised, break from loop
        #         break

config = CiscoConfig("test.cfg")

for item in config.nodes:
    print (repr(item))