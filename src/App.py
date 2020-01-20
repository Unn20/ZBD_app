from src.DataBase import Database
from src.Logger import Logger
from tkinter import *
from src.LogonController import LogonController


class App:
    def __init__(self):
        # Initialize logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("===================================================================")
        self.logger.debug("Application logger has started.")

        # Initialize app window
        self.logger.debug("Initializing application window.")
        self.window = Tk()
        self.window.title("Database Application.")
        self.logger.debug("Application window has been initialized.")

        self.window.geometry('640x480')

        self.dataBase = Database(host="localhost", user="root", password="")

    def __del__(self):
        # Delete dataBase object to close connection with database
        self.logger.debug("Deleting database object.")
        del self.dataBase
        self.logger.info("Closing application.")
        self.logger.debug("===================================================================")

    def run(self):
        logon = LogonController(self.window)
        self.window.mainloop()


if __name__ == "__main__":
    application = App()
    application.run()
