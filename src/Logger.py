import logging


def loggingLevels(string):
    if string.lower() == "debug":
        return logging.DEBUG
    elif string.lower() == "info":
        return logging.INFO
    elif string.lower() == "warning":
        return logging.WARNING
    elif string.lower() == "error":
        return logging.ERROR
    elif string.lower() == "critical":
        return logging.CRITICAL
    else:
        return logging.DEBUG

class Logger:
    def __init__(self, loggerName, loggingLevel):
        self.logger = logging.getLogger(loggerName)
        if not len(self.logger.handlers):
            self.logger = logging.getLogger(loggerName)
            self.logger.setLevel(logging.DEBUG)
            self.fileHandler = logging.FileHandler("logFile.log")
            self.streamHandler = logging.StreamHandler()
            self.formatter = logging.Formatter("%(asctime)s:%(name)s : %(levelname)s : %(message)s")
            self.fileHandler.setLevel(logging.DEBUG)
            self.fileHandler.setFormatter(self.formatter)
            self.streamHandler.setLevel(loggingLevels(loggingLevel))
            self.streamHandler.setFormatter(self.formatter)
            self.logger.addHandler(self.fileHandler)
            self.logger.addHandler(self.streamHandler)

    def debug(self, _message):
        return self.logger.debug(_message)

    def info(self, _message):
        return self.logger.info(_message)

    def warning(self, _message):
        return self.logger.warning(_message)

    def error(self, _message):
        return self.logger.error(_message)

    def critical(self, _message):
        return self.logger.critical(_message)
