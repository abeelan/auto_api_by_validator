from xml.etree.ElementTree import ElementTree
from common import path


class ParserXml:

    def __init__(self, file_path):
        self.path = file_path
        self.tree = ElementTree()
        self.tree.parse(self.path)

    def write_xml(self):
        self.tree.write(self.path, encoding="utf-8", xml_declaration=True)

    def set_node(self):
        for node in self.tree.iter("environment"):
            print(node.attrib)
        ...
        pass


if __name__ == '__main__':
    _path = "".join([path.report_path(), "/environment.xml"])
    print(_path)
    print(ParserXml(_path).set_node())