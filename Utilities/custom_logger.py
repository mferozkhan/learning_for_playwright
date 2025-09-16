import logging
import os
from datetime import datetime


class Logger:
    def get_logger(self):
        # Create logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # Create logs directory if it doesn't exist
        log_dir = "Logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create file handler
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = os.path.join(log_dir, f"test_log_{current_time}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger