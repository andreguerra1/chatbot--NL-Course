import re
from pathlib import Path


class FileUtils:

    @staticmethod
    def get_project_root() -> Path:
        """
        Returns project root folder.
        :return: project root folder.
        """
        return Path(__file__).parent.parent

    @staticmethod
    def get_full_path(partial_path) -> Path:
        return Path(f'{FileUtils.get_project_root()}/{partial_path}')

    @staticmethod
    def read_tags_n_sentences(file_path):
        tags = []
        sentences = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                field = re.search(r'(\w+[^\s])\t+(.+)', line)
                if field is not None:
                    tags.append(field.group(1))
                    sentences.append(field.group(2))
        return tags, sentences

    @staticmethod
    def read_lines(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                yield line

    @staticmethod
    def write_lines(file_path, lines):
        with open(file_path, 'w+', encoding='utf-8') as file:
            file.writelines(lines)
