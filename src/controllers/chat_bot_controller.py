from models.chat_bot_docs_model import ChatBotModel as Model
from viewers.chat_bot_viewer import ChatBotViewer as Viewer


class ChatBotController:

    def __init__(self, data_source, pre_processors, distance_evaluator, distance_threshold, target_file):
        self.model = Model(data_source, pre_processors, distance_evaluator, distance_threshold)
        self.viewer = Viewer(target_file)

    def process(self, questions):
        data = self.model.query(questions)
        self.viewer.view(data)
