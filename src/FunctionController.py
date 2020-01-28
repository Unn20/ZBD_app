from tkinter import *
from tkinter import ttk
from src.Logger import Logger
from tkinter import messagebox


class FunctionController:
    def __init__(self, rootWindow, database, backEvent, year):
        self.rootWindow = rootWindow
        self.backEvent = backEvent
        self.database = database
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("FunctionController logger has started.")

        self.functionWindow = Toplevel(self.rootWindow)
        self.functionWindow.title("Check a book.")
        self.functionWindow.protocol('WM_DELETE_WINDOW', self.goBack)
        self.functionWindow.bind("<<back>>", lambda _: self.backEvent())

        print(year)
        self.data = self.database.findBestBook(year)
        print(self.data)
        values = self.database.executeStatement(f"SELECT * FROM `ksiazki` WHERE `ksiazka_id` = 1992")
        print(values)

        self.mainFrame = Frame(self.functionWindow,  bd=4, relief=RAISED,
                               width=self.functionWindow.winfo_width(),
                               height=self.functionWindow.winfo_height())
        self.mainFrame.pack(fill='both', side=TOP)





    def goBack(self):
        self.functionWindow.event_generate("<<back>>")