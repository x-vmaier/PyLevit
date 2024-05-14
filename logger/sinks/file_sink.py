import os
import shutil
from datetime import datetime
from logger.sinks.base_sink import BaseSink


class FileSink(BaseSink):
    def __init__(self, log_dir="logs/"):
        super().__init__()
        self.log_dir = log_dir
        self.create_log_dir()
        self.file_path = self.get_log_filename()

    def create_log_dir(self):
        """Create the log directory if it doesn't exist."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def get_log_filename(self):
        """Generate a log filename with the current datetime."""
        return f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_latest.log"

    def process(self, message, color):
        """Write the message to the log file."""
        if self.find_latest_log_file() is not None:
            self.rollback()
        with open(self.file_path, 'a') as file:
            file.write(f"{datetime.now()} - {message}\n")

    def rollback(self):
        """Rollback the latest log file to a backup file with a timestamped filename."""
        latest_log_file = self.find_latest_log_file()
        if latest_log_file:
            backup_file = self.create_backup_filename(latest_log_file)
            shutil.move(latest_log_file, backup_file)

    def find_latest_log_file(self):
        """Find the latest log file in the root directory."""
        for file in os.listdir('.'):
            if file.endswith("_latest.log"):
                return file
        return None

    def create_backup_filename(self, log_file):
        """Generate a backup filename with a timestamp."""
        filename = f"{os.path.splitext(log_file)[0].split('_latest')[0]}.log"
        return os.path.join(self.log_dir, filename)
