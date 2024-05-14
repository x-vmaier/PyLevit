class BaseSink:
    def __init__(self):
        self.messages = []

    def process(self, message, color):
        raise NotImplementedError("Subclasses must implement process_log method")