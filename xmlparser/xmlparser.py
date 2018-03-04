from lxml import etree
from bs4 import BeautifulSoup

from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom


def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


class Parser:
    def __init__(self, filename):
        with open(filename) as file:
            self.xml = file.read()
            self.soup = BeautifulSoup(self.xml, "html.parser")

        self.filename = filename

    def get_array_attributes(self, elementname):
        array = []
        xml = self.xml
        root = etree.fromstring(xml)
        for region in root.getchildren():
            for field in region.getchildren():
                if field.tag == elementname:
                    array.append(field.text)
        return array

    def get_one_attribute(self, elementname):
        element = self.soup.find(elementname)
        if element.text:
            return element.text
        return None

    def write_array_to_file(self, filename, arrayname, childname, array):

        xml_array = Element(arrayname)

        for child in array:
            text = child
            child = SubElement(xml_array, childname)
            child.text = text

        file = open(filename, 'w')
        file.write(prettify(xml_array))
        file.close()
