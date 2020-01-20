from src.DataBase import Database
from src.Logger import Logger
from tkinter import *
from src.LogonController import LogonController
from src.MainController import MainController

class App:
    def __init__(self, width=640, height=480):
        # Initialize logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("===================================================================")
        self.logger.debug("Application logger has started.")

        # Initialize app window
        self.logger.debug("Initializing application window.")
        self.window = Tk()
        self.window.title("Database Application.")
        self.logger.debug("Application window has been initialized.")

        self.window.geometry(f"{int(width)}x{int(height)}+0+0")

        # Setting a theme picture
        self.theme = Canvas(width=width, height=height, bg='black')
        self.theme.grid(column=0, row=0)
        self.themePicture = PhotoImage(file="theme.gif")
        self.theme.create_image(0, 0, image=self.themePicture, anchor=NW)

    def __del__(self):
        # Delete dataBase object to close connection with database
        if self.database:
            self.logger.debug("Deleting database object.")
            try:
                del self.database
            except:
                pass
        self.logger.info("Closing application.")
        self.logger.debug("===================================================================")

    def main(self):
        self.logonWindow = LogonController(self.window, self.logonEvent)
        self.window.mainloop()

    def logonEvent(self, database):
        try:
            self.logonWindow.tlLogon.destroy()
        except Exception as e:
            self.logger.critical(f"An error occurred while destroying logon window! Exception = {e}")
        self.window.attributes("-topmost", True)

        self.database = database

        self.mainWindow = MainController(self.window, self.database)

