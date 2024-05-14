from datetime import datetime
from logger.sinks.base_sink import BaseSink


class ConsoleSink(BaseSink):
    def __init__(self):
        self.colors = {
            'green': '\033[92m',
            'orange': '\033[93m',
            'red': '\033[91m'
        }

    def process(self, message, color):
        """Print the message to the console with color."""
        console_color = self.colors.get(color.lower(), '')
        print(f"{datetime.now()} - {console_color}{message}\033[0m")