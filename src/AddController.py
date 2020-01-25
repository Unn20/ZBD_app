from src.Logger import Logger
from tkinter import *


class AddController:
    def __init__(self, themeWindow, tableName, database, backEvent):
        self.themeWindow = themeWindow
        self.tableName = tableName
        self.database = database
        self.backEvent = backEvent
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("TableController logger has started.")

        self.addWindow = Toplevel(self.themeWindow)
        self.addWindow.title("Add a new record to database.")
        self.addWindow.protocol('WM_DELETE_WINDOW', self.goBack)
        self.addWindow.bind("<<back>>", lambda _: self.backEvent(None))

        self.colNames = self.database.getColumns(self.tableName)

        self.colFrame = Frame(self.addWindow, bd=4, relief=RAISED,
                               width=self.themeWindow.winfo_width(),
                               height=self.themeWindow.winfo_height() - 40)
        self.colFrame.pack(fill='both', side=TOP)

        self.entries = dict()
        for no, col in enumerate(self.colNames):
            Label(self.colFrame, text=col, font=("Arial Bold", 12)).grid(row=no, column=0)
            self.entries[col] = Entry(self.colFrame, width=20).grid(row=no, column=1, columnspan=2)

        self.buttonFrame = Frame(self.addWindow, bd=4, relief=RAISED,
                               width=self.themeWindow.winfo_width(),
                               height=40)
        self.buttonFrame.pack(fill='both', side=TOP)
        self.addButton = Button(self.buttonFrame, text="Add record", command=self.checkEntry)
        self.addButton.pack(side=LEFT)
        self.cancelButton = Button(self.buttonFrame, text="Cancel", command=self.goBack)
        self.cancelButton.pack(side=LEFT)

    def goBack(self):
        self.addWindow.event_generate("<<back>>")

    def addRecordToDatabase(self):
        pass

    def checkEntry(self):
        pass
