import unittest
from xmlparser import xmlparser
from lxml import etree

parser = xmlparser.Parser("./tests/test.xml")

write_parser = xmlparser.Parser("./tests/write_test.xml")


class TestXmlParser(unittest.TestCase):

	def test_get_one_attribute(self):
		result = parser.get_one_attribute('solo')
		self.assertEqual('solo_test', result)

	def test_get_array_attributes(self):
		result = parser.get_array_attributes('test')

		test_result = [
			'test_text_first',
			'test_text_second'
		]
		self.assertEqual(test_result, result)

	def test_write_array_to_file(self):
		array_to_write = [
			'first',
			'second'
		]

		xml = xmlparser.write_array_to_file(
			'./tests/write_test.xml', 'test_array', 'test', array_to_write)

		result = []
		root = etree.fromstring(xml)
		for region in root.getchildren():
			for field in region.getchildren():
				if field.tag == "test":
					result.append(field.text)

		self.assertEqual(array_to_write, result)
