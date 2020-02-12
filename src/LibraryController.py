from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from src.Logger import Logger
from tkintertable.Tables import TableCanvas
from src.CustomTable import CustomTable
from tkintertable.TableModels import TableModel
import datetime


class LibraryController:
    def __init__(self, database, themeWindow, returnEvent):
        self.database = database
        self.themeWindow = themeWindow
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("TableController logger has started.")

        self.addWindow = None
        self.modifyWindow = None

        tableName = "biblioteki"
        self.tableName = tableName

        self.columnNames = self.database.getColumns(tableName)
        self.tableData = self.database.getRawData(tableName)
        self.data = self.database.getData(tableName)
        self.model = TableModel()

        if len(self.data) == 0:
            messagebox.showwarning("Empty table", "This table has no records!")
            self.back()
        else:
            for key, records in self.data.items():
                for col, value in records.items():
                    if isinstance(value, datetime.date):
                        self.data[key][col] = str(value)
        self.model.importDict(self.data)

        # Widgets
        self.content = Frame(self.themeWindow, bg="#B7B9B8", bd=4, relief=RAISED,
                             width=self.themeWindow.winfo_width() - 80,
                             height=self.themeWindow.winfo_height() - 80)
        self.content.place(x=40, y=40)
        self.content.bind("<<goback>>", lambda _: returnEvent(None))
        self.content.update()

        # Canvas with options menu
        self.topCanvas = Canvas(self.content, bg="white", bd=1, relief=RAISED,
                                width=int(self.content.winfo_width()),
                                height=int(self.content.winfo_height() / 12))
        self.topCanvas.pack(fill='both', side=TOP)

        self.backButton = Button(self.topCanvas, text=" < ", command=self.back, width=9)
        self.backButton.pack(fill='both', side=LEFT)
        self.showButton = Button(self.topCanvas, text="Refresh table", command=self.refreshTable, width=22)
        self.showButton.pack(fill='both', side=LEFT)

        # Canvas with data
        self.middleFrame = Frame(self.content)
        self.middleFrame.pack(fill='both', side=TOP)
        self.table = CustomTable(self.middleFrame, model=self.model)
        self.table.show()

        # Canvas with DML buttons
        self.bottomCanvas = Canvas(self.content, bg="white", bd=1, relief=FLAT,
                                   width=int(self.content.winfo_width()),
                                   height=int(self.content.winfo_height() / 5))
        self.bottomCanvas.pack(fill='both', side=TOP)
        self.buttonAdd = Button(self.bottomCanvas, text=" ADD ", command=self.add, width=24, height=3, bd=5)
        self.buttonAdd.pack(side=LEFT)
        self.buttonModify = Button(self.bottomCanvas, text=" MODIFY ", command=self.modify, width=25, height=3, bd=5)
        self.buttonModify.pack(side=LEFT)
        self.buttonDelete = Button(self.bottomCanvas, text=" DELETE ",
                                   command=lambda: self.delete(self.tableName), width=25, height=3, bd=5)
        self.buttonDelete.pack(side=LEFT)

    def back(self):
        """ Go back to main window """
        self.content.event_generate("<<goback>>")

    def backEvent(self, event):
        if self.addWindow is not None:
            self.addWindow.addWindow.destroy()
            self.addWindow = None
        if self.modifyWindow is not None:
            self.modifyWindow.modifyWindow.destroy()
            self.modifyWindow = None
        self.refreshTable()

    def add(self):
        """ Go to add window """
        if self.addWindow is None:
            self.logger.debug("Starting add window.")
            self.addWindow = AddController(self.themeWindow, self.tableName, self.database, self.backEvent)

    def modify(self):
        """ Go to modify window """
        if self.table.startrow != self.table.endrow:
            messagebox.showwarning('Modify error', 'Please select only one record!')
        else:
            selectedRow = self.table.currentrow
            if self.modifyWindow is None:
                self.logger.debug("Starting modify window.")
                self.modifyWindow = ModifyController(self.themeWindow, self.tableName, self.database,
                                                     self.model.getRecName(selectedRow),
                                                     self.data, self.backEvent)

    def delete(self, tableName):
        """ Delete selected records """
        for no, i in enumerate(self.table.multiplerowlist):
            recName = self.model.getRecName(i)
            deletedRecord = list()
            for column, value in self.data[recName].items():
                deletedRecord.append(value)
            try:
                self.database.deleteRecord(tableName, deletedRecord)
            except Exception as e:
                self.logger.error(f"Can not delete selected records! Error = {e}")
                errorNo = int(e.__str__().split()[0][1:-1])
                if errorNo == 1451:
                    messagebox.showerror("Can not delete selected records!",
                                         f"There are bounds including selected record.")
                else:
                    messagebox.showerror("Can not delete selected records!",
                                         f"Error {e}")

                return
        confirm = messagebox.askyesno("Deleting record confirmation",
                                      f"Are You sure that You want to delete {len(self.table.multiplerowlist)} records?")
        if confirm:
            self.database.connection.commit()
        else:
            self.database.connection.rollback()
        self.refreshTable()
        return

    def refreshTable(self):
        self.model.createEmptyModel()
        self.data = self.database.getData(self.tableName)
        if len(self.data) == 0:
            messagebox.showwarning("Empty table", "This table has no records!")
            self.data["_"] = dict()
            self.data["_"]["_"] = "Empty table"
        else:
            for key, records in self.data.items():
                for col, value in records.items():
                    if isinstance(value, datetime.date):
                        self.data[key][col] = str(value)
        self.model.importDict(self.data)
        self.table.redraw()

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
        self.colConstraints = self.database.getTableCheckConstraint(self.tableName)
        print(f"DEBUG = {self.colConstraints}")
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
                        if col[0] in self.colConstraints.keys():
                            entry = ttk.Combobox(self.colFrame, values=self.colConstraints[col[0]])
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

        self.helpWindow = None

        self.newRecord = list()
        self.emptyCols = 0
        self.emptyButton = IntVar()

        self.colNames = self.database.getColumns(self.tableName)
        self.colTypes = self.database.getColumnTypes(self.tableName)
        self.colKeys = self.database.getColumnKeys(self.tableName)
        self.colNulls = self.database.getColumnNullable(self.tableName)
        self.colConstraints = self.database.getTableCheckConstraint(self.tableName)
        print(f"DEBUG = {self.colConstraints}")
        self.colFrame = Frame(self.modifyWindow, bd=4, relief=RAISED,
                              width=self.themeWindow.winfo_width(),
                              height=self.themeWindow.winfo_height() - 40)
        self.colFrame.pack(fill='both', side=TOP)

        self.entries = list()

        if self.tableName in ["wlasciciel_biblioteka"]:
            for no, col in enumerate(self.colNames):
                Label(self.colFrame, text=col, font=("Arial Bold", 12)).grid(row=no, column=0)
                combo = ttk.Combobox(self.colFrame, values=self.initComboValues(self.tableName, col[0]))
                combo.grid(row=no, column=1, columnspan=2, padx=20, pady=10)
                if data[self.selectedRecord][col[0]] is not None:
                    combo.set(data[self.selectedRecord][col[0]])
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
                        if col[0] in self.colConstraints.keys():
                            entry = ttk.Combobox(self.colFrame, values=self.colConstraints[col[0]])
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

        if self.emptyCols > 0:
            if self.tableName == "pracownicy":
                self.oldRecord.insert(0, self.database.executeStatement(
                    f"SELECT `{self.colNames[0][0]}` FROM `{self.tableName}`" +
                    f"WHERE `{self.colNames[2][0]}` = \"{self.oldRecord[1]}\" AND" +
                    f"`{self.colNames[3][0]}` = \"{self.oldRecord[2]}\"")[0][0])

            else:
                self.oldRecord.insert(0, self.database.executeStatement(
                    f"SELECT `{self.colNames[0][0]}` FROM `{self.tableName}`" +
                    f"WHERE `{self.colNames[1][0]}` = \"{self.oldRecord[0]}\" AND" +
                    f"`{self.colNames[2][0]}` = \"{self.oldRecord[1]}\"")[0][0])

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


        if self.emptyCols == 1:
            self.newRecord[0] = self.oldRecord[0]

        if self.tableName == "autorzy" and self.database.executeStatement(f"SELECT `data_smierci`" +
                                                                          f"FROM `autorzy` WHERE `autor_id` = \"{self.newRecord[0]}\"")[0][0] == None:
            self.oldRecord[-1] = ""
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
            self.newRecord = list()
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

        self.helpWindow = Toplevel(self.modifyWindow)
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



