from lxml import etree
from bs4 import BeautifulSoup

def get_links(xml_filename):
    links = []
    with open(xml_filename) as file:
        xml = file.read()
        soup = BeautifulSoup(xml, "html.parser")

    for link in soup.find_all("link"):
        if "value" in link.attrs:
            links.append(link.attrs["value"])

    return links

def get_depth(xml_filename):
    with open(xml_filename) as file:
        xml = file.read()
        soup = BeautifulSoup(xml, "html.parser")

    depthEl = soup.find("depth")
    if "value" in depthEl.attrs:
        return int(depthEl.attrs["value"])

    return 0
        