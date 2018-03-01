from lxml import etree
from bs4 import BeautifulSoup

def parse(xml_filename):
    links = []
    with open(xml_filename) as file:
        xml = file.read()
        soup = BeautifulSoup(xml, "html.parser")

    for link in soup.find_all("link"):
        if "value" in link.attrs:
            links.append(link.attrs["value"])

    return links
        