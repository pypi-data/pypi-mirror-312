import logging
import traceback

class Logger:
    def __init__(self, level=logging.INFO):
        self.logger = logging.getLogger('storify')
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(levelname)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(level)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def traceback(self, msg):
        self.logger.error(f"{msg}\n{traceback.format_exc()}")
