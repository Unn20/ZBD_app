from tkinter import *
from src.Logger import Logger
from src.DataBase import Database


class MainController:
    def __init__(self, themeWindow, database, width=300, height=200):
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("MainController logger has started.")
        self.themeWindow = themeWindow
        self.database = database

