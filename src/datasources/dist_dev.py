from src.datasources.super_txt_data_source import DataProvider
from helpers.file_utils import FileUtils as f_utils


class DistDev(DataProvider):
    data_path = 'data/corpora/dist-desen.txt'

    def __init__(self):
        full_path = f_utils.get_full_path(DistDev.data_path)
        tags, sentences = f_utils.read_tags_n_sentences(full_path)
        super().__init__(tags, sentences, DistDev.data_path)
