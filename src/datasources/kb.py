import xml.etree.ElementTree as ET

from helpers.file_utils import FileUtils as f_utils
from datasources.super_xml_docs_data_source import DataProvider


class KbDataSource(DataProvider):
    data_path = 'KB.xml'

    def __init__(self):
        full_path = f_utils.get_full_path(KbDataSource.data_path)
        tree = ET.parse(full_path)
        super().__init__(tree, KbDataSource.data_path)
