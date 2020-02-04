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

        self.newRecord = list()
        self.emptyCols = 0
        self.emptyButton = IntVar()

        self.colNames = self.database.getColumns(self.tableName)
        self.colTypes = self.database.getColumnTypes(self.tableName)
        self.colKeys = self.database.getColumnKeys(self.tableName)
        self.colNulls = self.database.getColumnNullable(self.tableName)
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
                    if self.colNulls[col[0]] == 'YES':
                        emptyButton = Checkbutton(self.colFrame, text="Empty", variable=self.emptyButton,
                                                  command=self.clicked)
                        emptyButton.grid(row=no, column=3)
                        self.emptyDate = entry
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

    def clicked(self):
        if self.emptyButton.get() == 0:
            self.emptyDate.configure(state='enabled')
        else:
            self.emptyDate.configure(state='disabled')

    def checkEntry(self):
        self.newRecord.clear()
        for i in range(self.emptyCols):
            self.newRecord.append("")
        for entry in self.entries:
            value = entry.get()
            if len(value) == 10 and value[4] == "/" and value[7] == "/":
                value = value.replace("/", "-", 2)
            self.newRecord.append(value)
        for no, col in enumerate(self.colNulls.values()):
            if col == 'YES':
                if self.emptyButton.get() == 1:
                    self.newRecord[no] = ""
                self.oldRecord[no-1] = ""

        if self.emptyCols == 1:
            self.newRecord[0] = self.database.executeStatement("SELECT `autor_id` FROM `autorzy`" +
                                                               f"WHERE `imie` = \"{self.oldRecord[0]}\" AND" +
                                                               f"`nazwisko` = \"{self.oldRecord[1]}\"")[0][0]
            self.oldRecord.insert(0, self.database.executeStatement("SELECT `autor_id` FROM `autorzy`" +
                                                               f"WHERE `imie` = \"{self.oldRecord[0]}\" AND" +
                                                               f"`nazwisko` = \"{self.oldRecord[1]}\"")[0][0])
        print(self.oldRecord)
        print(self.newRecord)
        try:
            self.database.modifyRecord(self.tableName, self.oldRecord, self.newRecord)
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