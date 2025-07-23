# 

# logger.py
import os
import logging

class Logger:
    def __init__(self, log_file):
        """
        Initialize the logger with a log file.
        
        Args:
            log_file (str): Path to the log file.
        """
        # Ensure the directory for the log file exists
        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)  # Create the directory if it doesn't exist

        # Configure logging
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger()

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)