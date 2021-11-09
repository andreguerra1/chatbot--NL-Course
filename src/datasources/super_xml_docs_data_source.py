import re
import random


class DataProvider:

    @property
    def root(self):
        return self.tree.getroot()

    def __load_faqs(self):
        faqs = []
        tag = 0
        for documento in self.root:
            for subelem in documento:
                for subsubelem in subelem:
                    source = ''
                    questions = []
                    tags = []
                    id = ''
                    answer = ''
                    for subsubsubelem in subsubelem:
                        if (subsubsubelem.tag == 'perguntas'):
                            for subsubsubelem in subsubsubelem:
                                if subsubsubelem.text is not None:
                                    if subsubsubelem.text not in questions:
                                        questions.append(subsubsubelem.text)
                                    else:
                                        # print('Duplicate found.')
                                        # print(subsubsubelem.text)
                                        pass
                                    tags.append(str(tag))
                        elif (subsubsubelem.tag == 'resposta'):
                            answer = subsubsubelem.text
                            id = subsubsubelem.attrib['id']
                            tag += 1
                        elif (subsubsubelem.tag == 'fonte'):
                            source = subsubsubelem.text
                        else:
                            raise Exception('UNEXPECTED TOKEN IN SOURCE DATA.')
                    faq = {'id': id, 'source': source, 'questions': questions, 'answer': answer, 'tags': tags}
                    faqs.append(faq)
        return faqs

    @staticmethod
    def __clean(line):
        line = re.sub('( |\n)+', '', line)
        return line

    @staticmethod
    def __compact_faqs(faqs):
        compact_faqs = []
        for faq in faqs:
            compact_faq = {}
            compact_faq['id'] = DataProvider.__clean(faq['id'])
            compact_faq['source'] = DataProvider.__clean(faq['source'])
            compact_faq['answer'] = DataProvider.__clean(faq['answer'])
            compact_faq['questions'] = [DataProvider.__clean(question) for question in faq['questions']]
            compact_faq['tags'] = faq['tags']
            compact_faqs.append(compact_faq)
        return compact_faqs

    @staticmethod
    def __clean_up(faqs):
        tag = 0
        cleaned_faqs = []
        compact_faqs = DataProvider.__compact_faqs(faqs)
        compact_questions = []
        for compact_faq, faq in zip(compact_faqs, faqs):
            faq_questions = []
            faq_tags = []
            for compact_question, question in zip(compact_faq['questions'], faq['questions']):
                stag = str(tag)
                if compact_question not in compact_questions:
                    compact_questions.append(compact_question)
                    faq_questions.append(question)
                    faq_tags.append(stag)
            if (len(faq_questions) > 0):
                faq['questions'] = faq_questions
                faq['tags'] = faq_tags
                cleaned_faqs.append(faq)
                tag += 1
            else:
                # print(faq['id'])
                pass
        return cleaned_faqs

    def __init__(self, tree, data_path):
        self.tree = tree
        self.data_path = data_path
        _faqs = self.__load_faqs()
        self._faqs = DataProvider.__clean_up(_faqs)
        self._dev_tag_idxs = [random.randrange(len(faq['questions'])) for faq in self._faqs]

    @property
    def faqs(self):
        return self._faqs

    @property
    def questions(self):
        for faq in self._faqs:
            for question in faq['questions']:
                yield question

    @property
    def tags(self):
        for faq in self._faqs:
            for tag in faq['tags']:
                yield tag

    @property
    def ids(self):
        for faq in self._faqs:
            yield faq['id']

    @property
    def answers(self):
        for faq in self._faqs:
            yield faq['answer']

    @property
    def faqs_count(self):
        return len(self._faqs)

    @property
    def train_tags(self):
        for faq, dev_tag_idx in zip(self._faqs, self._dev_tag_idxs):
            for tag, tag_idx in zip(faq['tags'], range(len(faq['tags']))):
                if tag_idx != dev_tag_idx:
                    yield tag

    @property
    def train_questions(self):
        for faq, dev_tag_idx in zip(self._faqs, self._dev_tag_idxs):
            for question, tag_idx in zip(faq['questions'], range(len(faq['questions']))):
                if tag_idx != dev_tag_idx:
                    yield question

    @property
    def dev_tags(self):
        for faq, dev_tag_idx in zip(self._faqs, self._dev_tag_idxs):
            yield faq['tags'][dev_tag_idx]

    @property
    def dev_questions(self):
        for faq, dev_tag_idx in zip(self._faqs, self._dev_tag_idxs):
            yield faq['questions'][dev_tag_idx]

    def questions_apply(self, method):
        for faq in self._faqs:
            for i in range(len(faq['questions'])):
                faq['questions'][i] = method(faq['questions'][i])
