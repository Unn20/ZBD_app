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

        self.dataBase = False

    def __del__(self):
        # Delete dataBase object to close connection with database
        if self.dataBase:
            self.logger.debug("Deleting database object.")
            try:
                del self.dataBase
            except:
                pass
        self.logger.info("Closing application.")
        self.logger.debug("===================================================================")

    def run(self):
        self.logonWindow = LogonController(self.window, self.logonEvent)
        self.window.mainloop()

    def logonEvent(self, database):
        try:
            self.logonWindow.tlLogon.destroy()
        except Exception as e:
            self.logger.critical(f"An error occured while detroying logon window! Exception = {e}")
        self.window.attributes("-topmost", True)
        self.dataBase = database
        res = self.dataBase.executeStatement("SELECT * FROM wlasciciele")
        print(f"{res}")

