class DataProvider:

    def __init__(self, tags, sentences, data_path):
        self._tags = tags
        self._sentences = sentences
        self._data_path = data_path

    @property
    def tags(self):
        return self._tags

    @property
    def sentences(self):
        return self._sentences

    @property
    def data_path(self):
        return self._data_path

    def sentences_apply(self, method):
        for i in range(len(self._sentences)):
            self._sentences[i] = method(self._sentences[i])
