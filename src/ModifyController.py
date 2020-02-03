from src.Logger import Logger
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *


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
        self.colTypes = self.database.getColumnTypes(self.tableName)
        self.colKeys = self.database.getColumnKeys(self.tableName)
        self.colFrame = Frame(self.modifyWindow, bd=4, relief=RAISED,
                              width=self.themeWindow.winfo_width(),
                              height=self.themeWindow.winfo_height() - 40)
        self.colFrame.pack(fill='both', side=TOP)

        self.entries = list()

        if self.tableName in ["autor_ksiazka", "wlasciciel_biblioteka"]:
            for no, col in enumerate(self.colNames):
                Label(self.colFrame, text=col, font=("Arial Bold", 12)).grid(row=no, column=0)
                combo = ttk.Combobox(self.colFrame, values=self.initComboValues(self.tableName, col[0]))
                combo.grid(row=no, column=1, columnspan=2, padx=20, pady=10)
                if data[self.selectedRecord][col[0]] is not None:
                    combo.set(data[self.selectedRecord][col[0]])
                self.entries.append(combo)

        else:
            for no, col in enumerate(self.colNames):
                if col[0][-2:] == "id" and self.colKeys[col[0]][0] == 'PRI':
                    continue
                Label(self.colFrame, text=col, font=("Arial Bold", 12)).grid(row=no, column=0)
                if self.colTypes[col[0]] == 'date':
                    entry = DateEntry(self.colFrame, date_pattern='y/mm/dd')
                    entry.grid(row=no, column=1, columnspan=2, padx=20, pady=10)
                else:
                    if self.colKeys[col[0]][0] == 'MUL':
                        vals = self.database.executeStatement(
                            f"SELECT {self.colKeys[col[0]][2]} FROM {self.colKeys[col[0]][1]}")
                        entry = ttk.Combobox(self.colFrame, values=vals)
                        entry.grid(row=no, column=1, columnspan=2, padx=20, pady=10)
                    else:
                        entry = Entry(self.colFrame, width=20)
                        entry.grid(row=no, column=1, columnspan=2, padx=20, pady=10)

                if data[self.selectedRecord][col[0]] is not None:
                    if self.colTypes[col[0]] == 'date':
                        entry.set_date(data[self.selectedRecord][col[0]])
                    else:
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
            errorNo = int(e.__str__().split()[0][1:-1])
            if errorNo == 1048 or 1062:
                messagebox.showerror("Can not delete selected records!",
                                     f"{e.__str__().split(',')[1][:-2]}")
            else:
                messagebox.showerror("Can not modify record in database!",
                                     f"{e}")
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

    def initComboValues(self, tableName, col):
        return self.database.executeStatement(f"SELECT DISTINCT `{col}` FROM `{tableName}`")