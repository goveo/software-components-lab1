from lxml import etree
from bs4 import BeautifulSoup

from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


class Parser:
    def __init__(self, filename):
        with open(filename) as file:
            self.xml = file.read()
            self.soup = BeautifulSoup(self.xml, "html.parser")

        self.filename = filename

    def getArrayAttributes(self, attrName, value):
        array = []

        for element in self.soup.find_all(attrName):
            if value in element.attrs:
                array.append(element.attrs[value])

        return array

    def getOneAttribute(self, attrName, value):

        element = self.soup.find(attrName)
        if value in element.attrs:
            return element.attrs[value]
        return None

    def writeArrayToFile(self, filename, arrayName, childName, array):

        xmlArray = Element(arrayName)

        for child in array:
            text = child
            child = SubElement(xmlArray, childName)
            child.text = text

        file = open(filename, 'w')
        file.write(prettify(xmlArray))
        file.close
        