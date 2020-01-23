from src.Logger import Logger

class AddController:
    def __init__(self, event):
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("TableController logger has started.")
        pass