import re
from textwrap import dedent, fill, wrap
from viewers.common_header import CommonHeader


class ChatBotViewer:

    def __init__(self, header_body_msgs, line_len=CommonHeader.line_len(), insights=True):
        self.line_len = line_len
        self.insights=insights
        if header_body_msgs is not None:
            CommonHeader.common_header(header_body_msgs)

    def view(self, id, answer, distance, tag, closest_question):
        sanitize = re.compile('[\s\t\n]+')
        print(fill(dedent(sanitize.sub(' ', answer)), self.line_len,
                   initial_indent='->',
                   subsequent_indent='   ',
                   drop_whitespace=True))
        if self.insights:
            print(f'\n-----> id: {id}, tag: {tag}, distance: {round(distance, 2)}')
            closest_question = sanitize.sub(' ', closest_question)
            print(f'-----> closest question: \"{closest_question}\"')

    def post(self, message, line_len=CommonHeader.line_len()):
        print(fill(dedent(message), line_len))

    def post_direct(self, message):
        print(message)
