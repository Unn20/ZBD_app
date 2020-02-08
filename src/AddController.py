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
        self.colConstraints = self.database.getTableCheckConstraint(self.tableName)
        self.emptyCols = 0
        self.emptyButton = IntVar()

        self.helpWindow = None

        self.colFrame = Frame(self.addWindow, bd=4, relief=RAISED,
                              width=self.themeWindow.winfo_width(),
                              height=self.themeWindow.winfo_height() - 40)
        self.colFrame.pack(fill='both', side=TOP)

        self.entries = list()

        if self.tableName in ["wlasciciel_biblioteka"]:
            for no, col in enumerate(self.colNames):
                Label(self.colFrame, text=col, font=("Arial Bold", 12)).grid(row=no, column=0)
                combo = ttk.Combobox(self.colFrame, values=self.initComboValues(self.tableName, col[0]))
                combo.grid(row=no, column=1, columnspan=2, padx=20, pady=10)
                self.entries.append(combo)

        elif self.tableName in ["autor_ksiazka"]:
            for no, col in enumerate(self.colNames):
                Label(self.colFrame, text=col, font=("Arial Bold", 12)).grid(row=no, column=0)
                vals = self.initComboValues(self.tableName, col[0])
                combo = ttk.Combobox(self.colFrame, values=vals)
                combo.grid(row=no, column=1, columnspan=2, padx=20, pady=10)
                valueHelper = Button(self.colFrame, text="?", command=lambda b=col[0], c=combo:
                                                                            self.showHelp(b, c))
                valueHelper.grid(row=no, column=3)
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
                        vals = self.database.executeStatement(f"SELECT {self.colKeys[col[0]][2]} FROM {self.colKeys[col[0]][1]}")
                        entry = ttk.Combobox(self.colFrame, values=vals)
                        entry.grid(row=no, column=1, columnspan=2, padx=20, pady=10)
                    else:
                        #print(f"deb1 = {col}")
                        #print(f"deb2 = {self.colConstraints[0][0]}")
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
            if col == 'YES' and self.emptyButton.get() == 1:
                self.newRecord[no] = ""
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

    def showHelp(self, column, combo):
        if self.helpWindow is not None:
            return

        def select():
            atr = self.listbox.get(self.listbox.curselection())
            if self.column == "autorzy_autor_id":
                atr = atr.split(" ")
                id = self.database.executeStatement(f"SELECT `autor_id` " +
                                                    f"FROM `autorzy` WHERE `imie` = \"{atr[0]}\" " +
                                                    f"AND `nazwisko` = \"{atr[1]}\" ")
            else:
                id = self.database.executeStatement(f"SELECT `ksiazka_id` " +
                                                    f"FROM `ksiazki` WHERE `tytul` = \"{atr}\" ")
            self.combo.set(id)
            exit()
            return

        def exit():
            self.helpWindow.destroy()
            self.helpWindow = None

        self.column = column
        self.combo = combo

        self.helpWindow = Toplevel(self.addWindow)
        self.helpWindow.protocol('WM_DELETE_WINDOW', exit)

        vals = list()
        if self.column == "autorzy_autor_id":
            temp_vals = self.database.executeStatement(f"SELECT `imie`, `nazwisko` FROM `autorzy`")
            for val1, val2 in temp_vals:
                vals.append(val1 + " " + val2)
        else:
            temp_vals = self.database.executeStatement(f"SELECT `tytul` FROM `ksiazki`")
            for val1 in temp_vals:
                vals.append(val1[0])

        self.listbox = Listbox(self.helpWindow)
        self.listbox.pack(side=TOP)

        for val in vals:
            self.listbox.insert("end", val)

        self.button = Button(self.helpWindow, text="Select", command=select)
        self.button.pack(side=TOP)
