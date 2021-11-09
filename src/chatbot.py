import os.path as path
import re
import sys

from configuration import Configuration as config
from controllers.chat_bot_controller import ChatBotController as Controller
from datasources.cli import Cli as DataSource
from helpers.file_utils import FileUtils as f_utils

usage = f'Usage: python3 {path.basename(sys.argv[0])} <KB.xml> <questions_file> [<results_id_file>="resultados.txt"]'


def main():
    # Verify CLI arguments
    if len(sys.argv) < 3:
        print(usage)
        print('exiting...')
        return

    for i in [1, 2]:
        if not path.exists(sys.argv[i]):
            print(usage)
            print(f'file {sys.argv[i]} not found.')
            print('exiting...')
            return

    # Important args
    kb = sys.argv[1]
    questions_file = sys.argv[2]
    target_file = "resultados.txt" if len(sys.argv) < 4 else sys.argv[3]

    ds = DataSource(kb)

    controller = Controller(data_source=ds,
                            pre_processors=[pre_processor['method'] for pre_processor in config.pre_processors],
                            distance_evaluator=config.distance_evaluator.value['method'],
                            distance_threshold=lambda d: d <= config.distance_threshold,
                            target_file=target_file)

    questions = []
    for question in f_utils.read_lines(questions_file):
        question = re.sub('^( | \t)*$', '', question)
        if len(question) > 0:
            questions.append(question)
    controller.process(questions)



if __name__ == "__main__":
    main()
