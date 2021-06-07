from anytree import PreOrderIter, Node


class Generator:
    def cfgGenerator(self):
        pass


class ciscoGenerator(Generator):
    tree = None
    config = []
    file = None

    def __init__(self, root):
        self.tree = root

    def add_spaces(self, depth):
        space = ''
        i = 1
        while i < depth:
            space = space + ' '
            i += 1
        return space

    def cfgGenerator(self):
        COMMENT_SIGN = '!'

        for node in PreOrderIter(self.tree):
            if node.parent == self.tree:
                self.config.append(COMMENT_SIGN + '\n')
            if node.name == "root":
                continue
            self.config.append(self.add_spaces(node.depth) + node.name + '\n')

        return self.config

    def write_to_file(self, file, cfg):
        self.file = open(file, "w")
        self.file.write(''.join(str(e) for e in cfg))
        self.file.close()
