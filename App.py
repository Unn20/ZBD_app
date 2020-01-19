from DataBase import Database
from Logger import Logger
from tkinter import *


class App:
    def __init__(self):
        # Initialize logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("Application logger has started.")

        # Initialize app window
        self.logger.debug("Initializing application window.")
        self.window = Tk()
        self.window.title("Database Application.")
        self.logger.debug("Application window has been initialized.")

        self.dataBase = Database(host="localhost", user="root", password="")

    def __del__(self):
        # Delete dataBase object to close connection with database
        self.logger.debug("Deleting database object.")
        del self.dataBase
        self.logger.info("Closing application.")

    def run(self):
        res = self.dataBase.executeStatement("SELECT * FROM wlasciciele")
        lbl = Label(self.window, text=res)
        lbl.grid(column=0, row=0)
        self.window.mainloop()


if __name__ == "__main__":
    application = App()
    application.run()
