from src.Logger import Logger
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *

class AddController:
    def __init__(self, themeWindow, tableName, database, backEvent):
        self.themeWindow = themeWindow
        self.tableName = tableName
        self.database = database
        self.backEvent = backEvent
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("AddController logger has started.")

        self.addWindow = Toplevel(self.themeWindow)
        self.addWindow.title("Add a new record to database.")
        self.addWindow.protocol('WM_DELETE_WINDOW', self.goBack)
        self.addWindow.bind("<<back>>", lambda _: self.backEvent(None))

        self.newRecord = list()

        self.colNames = self.database.getColumns(self.tableName)
        self.colTypes = self.database.getColumnTypes(self.tableName)
        self.colKeys = self.database.getColumnKeys(self.tableName)
        self.colNulls = self.database.getColumnNullable(self.tableName)
        self.emptyCols = 0
        print(self.colNames)
        print(self.colTypes)
        print(self.colKeys)
        print(self.colNulls)

        self.colFrame = Frame(self.addWindow, bd=4, relief=RAISED,
                              width=self.themeWindow.winfo_width(),
                              height=self.themeWindow.winfo_height() - 40)
        self.colFrame.pack(fill='both', side=TOP)

        self.entries = list()

        if self.tableName in ["autor_ksiazka", "wlasciciel_biblioteka"]:
            for no, col in enumerate(self.colNames):
                Label(self.colFrame, text=col, font=("Arial Bold", 12)).grid(row=no, column=0)
                combo = ttk.Combobox(self.colFrame, values=self.initComboValues(self.tableName, col[0]))
                combo.grid(row=no, column=1, columnspan=2, padx=20, pady=10)
                self.entries.append(combo)

        else:
            for no, col in enumerate(self.colNames):
                if col[0][-2:] == "id" and self.colKeys[col[0]][0] == 'PRI':
                    self.emptyCols += 1
                    continue
                if self.colKeys[col[0]][0] == 'PRI':
                    _text = self.colNames[no][0] + "*"
                else:
                    _text = self.colNames[no][0]
                Label(self.colFrame, text=_text, font=("Arial Bold", 12)).grid(row=no, column=0)
                if self.colTypes[col[0]] == 'date':
                    entry = DateEntry(self.colFrame, date_pattern='y/mm/dd')
                    entry.grid(row=no, column=1, columnspan=2, padx=20, pady=10)
                else:
                    if self.colKeys[col[0]][0] == 'MUL':
                        vals = self.database.executeStatement(f"SELECT {self.colKeys[col[0]][2]} FROM {self.colKeys[col[0]][1]}")
                        entry = ttk.Combobox(self.colFrame, values=vals)
                        entry.grid(row=no, column=1, columnspan=2, padx=20, pady=10)
                    else:
                        entry = Entry(self.colFrame, width=20)
                        entry.grid(row=no, column=1, columnspan=2, padx=20, pady=10)
                self.entries.append(entry)

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

    def checkEntry(self):
        self.newRecord.clear()
        for i in range(self.emptyCols):
            self.newRecord.append("")
        for entry in self.entries:
            value = entry.get()
            if len(value) == 10 and value[4] == "/" and value[7] == "/":
                value = value.replace("/", "-", 2)
            self.newRecord.append(value)
        try:
            self.database.addRecord(self.tableName, self.newRecord)
        except Exception as e:
            self.logger.error(f"Exception! e = {e}")
            try:
                errorNo = int(e.__str__().split()[0][1:-1])
            except:
                errorNo = 0
            if errorNo == 1048:
                messagebox.showerror("Can not add a record to database!",
                                     f"{e.__str__().split(',')[1][:-2]}")
            elif errorNo == 1062:
                messagebox.showerror("Can not add a record to database!",
                                     f"Primary column value (with '*') is duplicate!")
            elif errorNo == 0:
                messagebox.showerror("Can not add a record to database!",
                                     f"{e}")
            else:
                messagebox.showerror("Can not add a record to database!",
                                     f"{e.__str__().split(',')[1][:-2]}")
            return
        confirm = messagebox.askyesno("Add record confirmation",
                                      "Are You sure that You want to add this record to database?")


        if confirm:
            self.database.connection.commit()
            self.goBack()
        else:
            self.database.connection.rollback()
            self.themeWindow.focus_set()

    def initComboValues(self, tableName, col):
        return self.database.executeStatement(f"SELECT DISTINCT `{col}` FROM `{tableName}`")