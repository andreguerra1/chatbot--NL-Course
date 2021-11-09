import re
from textwrap import dedent, fill

from viewers.common_header import CommonHeader


class ChatBotViewer:

    def __init__(self, header_body_msgs=None, line_len=CommonHeader.line_len(), insights=True):
        self.line_len = line_len
        self.insights = insights
        if header_body_msgs is not None:
            CommonHeader.common_header(header_body_msgs)

    # def view(self, id, answer, distance, tag, closest_question):
    def view(self, records):
        for record in records:
            id, answer, distance, tag, closest_question = record
            text = re.sub('( |\t)+', ' ', re.sub('^\n', '', re.sub('^ ', '', answer)))
            print(fill(dedent(text), self.line_len,
                       initial_indent='-> ',
                       subsequent_indent='   ',
                       drop_whitespace=True))
            if self.insights:
                print(f'\n-----> id: {id}, tag: {tag}, distance: {round(distance, 2)}')
                print(f'-----> closest question: "{closest_question}"')

    def post(self, message, line_len=CommonHeader.line_len()):
        print(fill(dedent(message), line_len))
