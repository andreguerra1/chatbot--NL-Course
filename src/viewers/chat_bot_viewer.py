import sys

from helpers.file_utils import FileUtils as f_util


class ChatBotViewer:

    def __init__(self, target_file):
        self.target_file = target_file

    def view(self, records):
        contents = []
        i = 1
        for record in records:
            id, answer, distance, tag, closest_question = record
            sys.stdout.write(f"\rWriting rec: {i:>4}, id: {id:>4}, tag: {tag:>4}, distance: {distance}")
            sys.stdout.flush()
            i += 1
            contents.append(f'{id}\n')
        f_util.write_lines(self.target_file, contents)
        print('\rDone'.ljust(60))
        print(f'File: {self.target_file}')
