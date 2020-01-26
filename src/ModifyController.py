from src.Logger import Logger
from tkinter import *
from tkinter import messagebox


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
            if data[self.selectedRecord][col[0]] is not None:
                entry.insert(END, data[self.selectedRecord][col[0]])
            self.entries.append(entry)

        self.oldRecord = list()
        for entry in self.entries:
            self.oldRecord.append(entry.get())

        self.buttonFrame = Frame(self.modifyWindow, bd=4, relief=RAISED,
                                 width=self.themeWindow.winfo_width(),
                                 height=40)
        self.buttonFrame.pack(fill='both', side=TOP)
        self.addButton = Button(self.buttonFrame, text="Modify", command=self.checkEntry)
        self.addButton.pack(side=LEFT)
        self.cancelButton = Button(self.buttonFrame, text="Cancel", command=self.goBack)
        self.cancelButton.pack(side=LEFT)

    def checkEntry(self):
        newRecord = list()
        for entry in self.entries:
            newRecord.append(entry.get())
        try:
            self.database.modifyRecord(self.tableName, self.oldRecord, newRecord)
        except Exception as e:
            self.logger.error(f"Exception! e = {e}")
            messagebox.showerror("Can not modify record in database!",
                                 f"Error {e}")
            return
        confirm = messagebox.askyesno("Modify record confirmation",
                                      "Are You sure that You want to modify this record in database?")

        if confirm:
            self.database.connection.commit()
            self.goBack()
        else:
            self.database.connection.rollback()
            self.themeWindow.focus_set()

    def goBack(self):
        self.modifyWindow.event_generate("<<back>>")