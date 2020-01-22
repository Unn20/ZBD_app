from src.DataBase import Database
from src.Logger import Logger
from tkinter import *
from src.LogonController import LogonController
from src.MainController import MainController
import json

class App:
    def __init__(self, configPath, width=640, height=480):
        # Initialize logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("===================================================================")
        self.logger.debug("Application logger has started.")

        self.config = dict()
        try:
            with open(configPath) as f:
                self.config = {**self.config, **json.load(f)}
        except IOError as e:
            self.logger.error(f"Error occured while reading config from .json file!. Error = {e}")
            exit(-1)
        self.logger.debug("Config has been read.")

        # Initialize app window
        self.logger.debug("Initializing application window.")
        self.window = Tk()
        self.window.title("Database Application.")
        self.logger.debug("Application window has been initialized.")

        self.window.geometry(f"{int(width)}x{int(height)}+0+0")
        self.window.resizable(0, 0)
        self.window.attributes("-topmost", True)

        # Setting a theme picture
        self.theme = Canvas(width=width, height=height, bg='black')
        self.theme.grid(column=0, row=0)
        self.imagesDict = dict()
        self.imagesDict["themeC"] = PhotoImage(file="theme.gif")
        self.imagesDict["themeG"] = PhotoImage(file="grayscale_theme.gif")
        self.logger.debug("Images has been loaded.")
        self.imageOnCanvas = self.theme.create_image(0, 0, image=self.imagesDict["themeG"], anchor=NW)
        self.logger.debug("Setting grayscale theme.")

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
            self.logger.error(f"An error occurred while destroying logon window! Exception = {e}")
        self.window.attributes("-topmost", True)
        self.window.attributes("-topmost", False)
        self.theme.itemconfig(self.imageOnCanvas, image=self.imagesDict["themeC"])
        self.logger.debug("Setting coloured theme.")

        self.database = database

        self.mainWindow = MainController(self.window, self.database, self.logoutEvent)

    def logoutEvent(self, _):
        try:
            self.mainWindow.content.destroy()
        except Exception as e:
            self.logger.error(f"An error occurred while destroying logon window! Exception = {e}")
        self.logger.info("Signed out")
        self.theme.itemconfig(self.imageOnCanvas, image=self.imagesDict["themeG"])

        self.database = None

        self.logonWindow = LogonController(self.window, self.logonEvent)

