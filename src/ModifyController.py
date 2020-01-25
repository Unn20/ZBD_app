from src.Logger import Logger
from tkinter import *


class ModifyController:
    def __init__(self, themeWindow, tableName, database, selectedRecord, data, backEvent):
        self.themeWindow = themeWindow
        self.tableName = tableName
        self.database = database
        self.selectedRecord = selectedRecord
        self.data = data
        self.backEvent = backEvent
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("ModifyController logger has started.")

        self.modifyWindow = Toplevel(self.themeWindow)
        self.modifyWindow.title("Modify an existing record.")
        self.modifyWindow.protocol('WM_DELETE_WINDOW', self.goBack)
        self.modifyWindow.bind("<<back>>", lambda _: self.backEvent(None))

        self.colNames = self.database.getColumns(self.tableName)
        self.colFrame = Frame(self.modifyWindow, bd=4, relief=RAISED,
                              width=self.themeWindow.winfo_width(),
                              height=self.themeWindow.winfo_height() - 40)
        self.colFrame.pack(fill='both', side=TOP)

        self.entries = list()
        for no, col in enumerate(self.colNames):
            Label(self.colFrame, text=col[0], font=("Arial Bold", 12)).grid(row=no, column=0)
            entry = Entry(self.colFrame, width=20)
            entry.grid(row=no, column=1, columnspan=2)
            if data[selectedRecord][col[0]] is not None:
                entry.insert(END, data[selectedRecord][col[0]])
            self.entries.append(entry)

        self.buttonFrame = Frame(self.modifyWindow, bd=4, relief=RAISED,
                                 width=self.themeWindow.winfo_width(),
                                 height=40)
        self.buttonFrame.pack(fill='both', side=TOP)
        self.addButton = Button(self.buttonFrame, text="Modify", command=self.checkEntry)
        self.addButton.pack(side=LEFT)
        self.cancelButton = Button(self.buttonFrame, text="Cancel", command=self.goBack)
        self.cancelButton.pack(side=LEFT)

    def checkEntry(self):
        print(self.selectedRecord)

    def modifyRecordInDatabase(self):
        pass

    def goBack(self):
        self.modifyWindow.event_generate("<<back>>")