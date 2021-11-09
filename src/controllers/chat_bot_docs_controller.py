from models.chat_bot_docs_model import ChatBotModel as Model
from viewers.chat_bot_docs_viewer import ChatBotViewer as Viewer


class ChatBotController:

    def __init__(self, data_source, pre_processors, distance_evaluator, distance_threshold, header_body_msgs=None, viewer_insights=True):
        self.model = Model(data_source, pre_processors, distance_evaluator, distance_threshold)
        self.viewer = Viewer(header_body_msgs, insights=viewer_insights)

    def process(self, questions):
        data = self.model.query(questions)
        self.viewer.view(data)

    def post(self, message):
        self.viewer.post(message)
