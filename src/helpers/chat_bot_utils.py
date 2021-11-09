import re
from enum import Enum

import nltk
from nltk.metrics.distance import edit_distance as levenshtein_distance
from nltk.metrics.distance import jaccard_distance

from functools import partial



class Similarity:

    @staticmethod
    def jaccard_distance(sentence_a, sentence_b):
        """
        Jaccard distance derived from the code in nltk.
        :param sentence_a:
        :param sentence_b:
        :return: a float representing the Jaccard distance.
        """
        set_a = set(sentence_a.split())
        set_b = set(sentence_b.split())
        distance = (len(set_a.union(set_b)) - len(set_a.intersection(set_b))) / len(set_a.union(set_b))
        return distance

    @staticmethod
    def sorensen_dice_distance(sentence_a, sentence_b):
        """
        Calculation of Sorensen-Dice from Jaccard distance.
        Jaccard index calculated as per
        https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient
        :param sentence_a:
        :param sentence_b:
        :return:
        """
        j_index = 1 - Similarity.jaccard_distance(sentence_a, sentence_b)
        s_index = 2 * j_index / (1 + j_index)
        distance = 1 - s_index
        return distance

    @staticmethod
    def sorensen_dice_distance_1(sentence_a, sentence_b):
        set_a = set(sentence_a.split())
        set_b = set(sentence_b.split())
        sd_index = 2 * len(set_a.intersection(set_b)) / (len(set_a) + len(set_b))
        distance = 1 - sd_index
        return distance


class DistanceEvaluators(Enum):
    EDIT = {
        'name': 'Edit index',
        'method': lambda train_sentence, dev_sentence: levenshtein_distance(train_sentence.split(),
                                                                            dev_sentence.split())
    }
    JACCARD_NLTK = {
        'name': 'Jaccard index',
        'method': lambda train_sentence, dev_sentence: jaccard_distance(set(train_sentence.split()),
                                                                        set(dev_sentence.split()))
    }
    JACCARD = {
        'name': 'Jaccard index (1)',
        'method': lambda train_sentence, dev_sentence: Similarity.jaccard_distance(train_sentence, dev_sentence)
    }
    DICE = {
        'name': 'Sørensen-Dice index',
        'method': lambda train_sentence, dev_sentence: Similarity.sorensen_dice_distance(train_sentence, dev_sentence)
    }


class ChatBotUtils:

    @staticmethod
    def stemming(sentence):
        stemmer = nltk.stem.RSLPStemmer()
        sentence = nltk.word_tokenize(sentence)
        words = []
        for word in sentence:
            word = stemmer.stem(word)
            words.append(word)
        sentence = ' '.join(words)
        return sentence

    @staticmethod
    def normalize_alphabet(sentence):
        """
        Removes letter marks in sentences.
        :param sentence: line of text
        :return: line of text
        """
        marks = (
            ('á', 'a'), ('â', 'a'), ('ã', 'a'), ('à', 'a'),
            ('Á', 'A'), ('Â', 'A'), ('Ã', 'A'), ('À', 'A'),
            ('é', 'e'), ('ê', 'e'),
            ('É', 'E'), ('Ê', 'E'),
            ('í', 'i'),
            ('Í', 'I'),
            ('ó', 'o'), ('ô', 'o'), ('õ', 'o'),
            ('Ó', 'O'), ('Ô', 'O'), ('Õ', 'O'),
            ('ú', 'u'),
            ('Ú', 'U'),
            ('ç', 'c'),
            ('Ç', 'C'),
        )
        for mark in marks:
            sentence = re.sub(mark[0], mark[1], sentence)
        sentence = sentence.lower()
        sentence = re.sub(r'[?|\.|!|:|,|;]', '', sentence)
        sentence = re.sub(r'^\w+\t+[^\w]', '', sentence)  # Drop tags (?!?)
        return str(sentence)

    @staticmethod
    def removeStopWords(sentence, stopWordList):
        segments = sentence.split()
        pieces = []
        target_sentence = ''
        for word in segments:
            if word.lower() not in stopWordList:
                pieces.append(word)
            target_sentence = ' '.join(pieces)
        return target_sentence

    @staticmethod
    def search_sentence(target, sentences, tags, distance_evaluator=DistanceEvaluators.JACCARD):
        """
        Searches for the best match of target in sentences, according to the selected evaluator
        """
        tag_id = 'VOID'
        best_sentence = ''
        best_distance = float('Infinity')
        x = list(zip(sentences, tags))
        for sentence, tag in zip(sentences, tags):
            #print(sentence)
            #print("\n\n\n" + tag)
            distance = distance_evaluator(sentence, target)
            if distance < best_distance:
                tag_id = tag
                best_sentence = sentence
                best_distance = distance
        return tag_id, best_sentence, best_distance

    @staticmethod
    def evaluation(training_tags, training_sentences, dev_sentences,
                   distance_evaluator=DistanceEvaluators.JACCARD):
        training_tags = list(training_tags)
        training_sentences = list(training_sentences)
        dev_sentences = list(dev_sentences)
        tag_ids = []
        best_sentences = []
        search_sentence = partial(ChatBotUtils.search_sentence, sentences=training_sentences, tags=training_tags,
                                  distance_evaluator=distance_evaluator)
        for dev_sentence in dev_sentences:
            tag_id, best_sentence, best_distance = search_sentence(dev_sentence)
            
            if best_distance >= 0.62:
                tag_id = 0
                best_sentence = ""

            tag_ids.append(tag_id)
            best_sentences.append(best_sentence)
        return tag_ids, best_sentences
