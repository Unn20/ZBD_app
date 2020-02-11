from tkinter import *
from tkinter import messagebox
from src.Logger import Logger
from tkintertable.Tables import TableCanvas
from src.CustomTable import CustomTable
from tkintertable.TableModels import TableModel
from src.AddController import AddController
from src.ModifyController import ModifyController
import datetime


class BooksController:
    def __init__(self, database, themeWindow, returnEvent):
        self.database = database
        self.themeWindow = themeWindow
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("TableController logger has started.")
