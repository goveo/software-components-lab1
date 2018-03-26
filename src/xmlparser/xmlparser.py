import os
from lxml import etree
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom


def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def write_array_to_file(filename, arrayname, childname, array):

    xml_element = Element("data")
    data_array = SubElement(xml_element, arrayname)

    for child in array:
        text = child
        child = SubElement(data_array, childname)
        child.text = text

    string_xml = prettify(xml_element)
    file = open(filename, 'w')
    file.write(string_xml)
    file.close()

    return string_xml


class Parser:
    def __init__(self, filename):
        path = os.path.dirname(os.path.realpath(__file__))
        path = path + "/../" + filename
        try:
            with open(path) as file:
                self.xml = file.read()
                self.soup = BeautifulSoup(self.xml, "html.parser")
        except(TypeError):
            raise Exception("Wrong filename")
            

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
