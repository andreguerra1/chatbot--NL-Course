from helpers.chat_bot_utils import ChatBotUtils as cb_utils



class ChatBotModel:

    def __init__(self, data_source, pre_processors, distance_evaluator, distance_threshold):
        self.data_source = data_source
        self.pre_processors = pre_processors
        self.distance_evaluator = distance_evaluator
        self.distance_threshold = distance_threshold

        for pre_processor in pre_processors:
            data_source.questions_apply(pre_processor)

        self.train_questions = list(data_source.questions)
        self.train_tags = list(data_source.tags)
        self.answers = list(data_source.answers)
        self.ids = list(data_source.ids)

    def query(self, questions):
        for question in questions:
            for pre_processor in self.pre_processors:
                question = pre_processor(question)

            tag, closest_question, distance = cb_utils.search_sentence(question, self.train_questions, self.train_tags,
                                                                       distance_evaluator=self.distance_evaluator)
            idx = int(tag)
            id = self.ids[idx]
            answer = self.answers[idx]
            if not self.distance_threshold(distance):
                id = 0
                answer = "\nI don't know the answer to that question."
            yield (id, answer, distance, tag, closest_question)
