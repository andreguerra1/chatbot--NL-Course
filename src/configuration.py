from helpers.chat_bot_utils import DistanceEvaluators as de
from functools import partial

from helpers.chat_bot_utils import ChatBotUtils as cb_utils


class Configuration:

    # Stopword to remove.
    stopWords = [
        'o', 'teu', 'seu',
        'se', 'caso', 'quando', 'qual', 'como',  # Conjunções
        'a', 'após', 'até', 'de', 'em', 'para',  # Preposições
        'que', 'com',
        'é',
    ]
    # Portuguese stop words example: https://gist.github.com/alopes/5358189

    # Leave uncommented the filters to be applied to the data source and user's questions
    pre_processors = (
    #    {'name': 'Letter marks removal', 'method': cb_utils.normalize_alphabet},  # Remove letter marks
        {'name': 'Tokenization and Stemming', 'method': cb_utils.stemming},  # Stemming sentences
        {'name': 'Stop-words removal', 'method': partial(cb_utils.removeStopWords, stopWordList=stopWords)},
    )

    # Maximum acceptable distance
    distance_threshold = 0.62

    # Distance metric
    distance_evaluator = de.JACCARD
