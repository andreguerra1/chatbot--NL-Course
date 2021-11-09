import xml.etree.ElementTree as ET

from datasources.super_xml_docs_data_source import DataProvider


class Cli(DataProvider):

    def __init__(self, data_path):
        tree = ET.parse(data_path)
        super().__init__(tree, data_path)
