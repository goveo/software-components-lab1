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

    def getArrayAttributes(self, elementName):
        array = []
        xml = self.xml
        root = etree.fromstring(xml)
        for region in root.getchildren():
            for field in region.getchildren():
                if field.tag == elementName:
                    array.append(field.text)
        return array

    def getOneAttribute(self, elementName):
        element = self.soup.find(elementName)
        if element.text:
            return element.text
        return None

    def writeArrayToFile(self, filename, arrayName, childName, array):

        xmlArray = Element(arrayName)

        for child in array:
            text = child
            child = SubElement(xmlArray, childName)
            child.text = text

        file = open(filename, 'w')
        file.write(prettify(xmlArray))
        file.close()
