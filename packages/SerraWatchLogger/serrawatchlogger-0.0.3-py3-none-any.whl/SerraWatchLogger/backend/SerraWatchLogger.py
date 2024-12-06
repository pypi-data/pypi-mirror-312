import logging
import os
from datetime import datetime


class SerraWatchLogger:
    _instance = None
    def __new__(cls, name: str = __name__):
        if cls._instance is None:
            cls._instance = super(SerraWatchLogger, cls).__new__(cls)
            cls._instance.logger = logging.getLogger(name)

            # Create the base log directory if it doesn't exist
            base_log_directory = "logs"
            if not os.path.exists(base_log_directory):
                os.makedirs(base_log_directory)

            # Create a new log folder with the current date and time inside the base log directory
            log_directory = os.path.join(base_log_directory, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            if not os.path.exists(log_directory):
                os.makedirs(log_directory)

            # Create handlers for logging
            log_filename = os.path.join(log_directory, "application.log")
            file_handler = logging.FileHandler(log_filename)
            stream_handler = logging.StreamHandler()

            # Set formatter for the handlers
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)

            # Store log directory for topic-specific logs
            cls._instance.log_directory = log_directory

            cls._instance.logger.addHandler(file_handler)
            cls._instance.logger.addHandler(stream_handler)
            cls._instance.logger.setLevel(logging.DEBUG)
        return cls._instance

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)

    def add_topic_log(self, topic: str, message: str):

        topic_log_directory = os.path.join(self.log_directory, topic)
        if not os.path.exists(topic_log_directory):
            os.makedirs(topic_log_directory)

        topic_log_filename = os.path.join(topic_log_directory, f"{topic}.log")
        with open(topic_log_filename, "a") as topic_log_file:
            topic_log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")