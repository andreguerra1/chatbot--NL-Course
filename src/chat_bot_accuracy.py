import re
from textwrap import dedent, fill

from nltk.metrics.scores import accuracy

from datasources.kb import KbDataSource as G15DataSource
from helpers.chat_bot_utils import ChatBotUtils as cb_utils
from helpers.chat_bot_utils import DistanceEvaluators as de
from configuration import Configuration as config
from viewers.chat_bot_doc_viewer import ChatBotViewer as Viewer


def main(is_looping=False, is_not_first=False):
    ds_g15 = G15DataSource()

    header_body_msg = (
        'This script evaluates the accuracy of the assigned data set.',
        f'- Distance metric: {config.distance_evaluator.value["name"]}',
        f'- Applied filters: {str([pre_processor["name"] for pre_processor in config.pre_processors])}',
    )

    viewer = Viewer(None if is_not_first else header_body_msg)

    for pre_process in config.pre_processors:
        ds_g15.questions_apply(pre_process['method'])

    # ----- Test the model -----
    train_questions = list(ds_g15.train_questions)
    train_tags = list(ds_g15.train_tags)
    dev_questions = list(ds_g15.dev_questions)
    dev_tags = list(ds_g15.dev_tags)

    stats = []
    # ----- Show evaluation -----
    expected_tags, closest_question = cb_utils.evaluation(train_tags, train_questions, dev_questions,
                                                          distance_evaluator=config.distance_evaluator.value['method'])
    # ----- Find accuracy -----
    loop_accuracy = round(accuracy(list(ds_g15.dev_tags), expected_tags), 2)
    viewer.post(f'Accuracy: {loop_accuracy}')
    stats.append(loop_accuracy)

    if is_looping:
        return loop_accuracy
    else:
        viewer.post('-' * viewer.line_len)

        # ----- Output -----
        label_size = 24
        subsequent_indent = ' ' * label_size

        for dev_question, expected_tag, dev_tag, closest_question in zip(dev_questions, expected_tags, dev_tags,
                                                                         closest_question):
            sanitize = re.compile('[ \t\n]+')
            viewer.post('')
            viewer.post_direct(fill(dedent(sanitize.sub(" ", dev_question)), viewer.line_len,
                                    initial_indent='Question to evaluate:'.ljust(label_size),
                                    subsequent_indent=subsequent_indent,
                                    drop_whitespace=True))
            viewer.post(f'{"Suggested/Correct tags:".ljust(label_size)}{expected_tag}/{dev_tag}')
            viewer.post_direct(fill(dedent(sanitize.sub(" ", closest_question)), viewer.line_len,
                                    initial_indent='Closest question:'.ljust(label_size),
                                    subsequent_indent=subsequent_indent,
                                    drop_whitespace=True))


if __name__ == "__main__":
    loops = 10
    averages = []
    for count in range(loops):
        averages.append(main(is_looping=loops != 1, is_not_first=count > 0))
    if loops > 1:
        print('-' * 14)
        print(f'Average:  {round(sum(averages) / loops, 2)}')
        print(f'Loops:    {loops}')
