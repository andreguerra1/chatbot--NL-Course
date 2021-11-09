from textwrap import dedent, fill, wrap

footer_msg = 'Group 15: André Guerra (86382), António Borba (97096), Mark Baltič (94859)'


class CommonHeader:
    @staticmethod
    def line_len():
        return len(footer_msg) + 6

    @staticmethod
    def common_header(body_msgs, header_msg='NL - MP1: ChatBot'):
        line_len = CommonHeader.line_len()
        print("=" * line_len)
        print('\n', header_msg.center(line_len), '\n')
        for message in body_msgs:
            print(fill(dedent(message), line_len))
        print("-" * line_len)
        print(footer_msg.center(line_len))
        print("=" * line_len)
