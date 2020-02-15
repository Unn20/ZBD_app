from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from src.Logger import Logger
from tkintertable.Tables import TableCanvas
from src.CustomTable import CustomTable
from tkintertable.TableModels import TableModel


class HistoryController:
    def __init__(self, database, themeWindow, returnEvent):
        self.database = database
        self.themeWindow = themeWindow
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("TableController logger has started.")

        self.addWindow = None
        self.modifyWindow = None
        self.table = None

        tableName = "historia_operacji"
        self.tableName = tableName

        self.tableData = self.database.getRawData(tableName)
        self.data = dict()
        self.model = TableModel()

        if len(self.tableData) == 0:
            messagebox.showwarning("Empty table", "This table has no records!")
            self.data["_"] = dict()
            self.data["_"]["_"] = "Empty table"
        else:
            self.refreshTable()

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
        # TODO: do zrobenia (Maciek)
        for no, i in enumerate(self.table.multiplerowlist):
            recName = self.model.getRecName(i)
            deletedRecord = list()
            deletedRecord.append(self.data[recName]["ID"])
            if self.data[recName]["Nazwisko przełożonego"] == "":
                deletedRecord.append("")
            else:
                deletedRecord.append("")
            deletedRecord.append(self.data[recName]["Imię"])
            deletedRecord.append(self.data[recName]["Nazwisko"])
            deletedRecord.append(self.data[recName]["Funkcja"])
            try:
                print(f"Deleted record = {deletedRecord}")
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
        self.tableData = self.database.getRawData(self.tableName)
        self.data = dict()
        ''' Tutaj trzeba dopasowac wlasciwe dane z krotki do kolumn '''
        for no, record in enumerate(self.tableData):
            self.data[f"rec {no}"] = dict()
            # self.data[f"rec {no}"]["Data"] = record[0]
            # self.data[f"rec {no}"]["Rodzaj"] = record[2]
            # self.data[f"rec {no}"]["Opoźnienie"] = record[3]
            # self.data[f"rec {no}"]["Uwagi"] = record[4]
            # self.data[f"rec {no}"]["Tytuł książki"] = record[4]
            # self.data[f"rec {no}"]["ID egzemplarza"] = record[4]
            # self.data[f"rec {no}"]["Nazwa działu"] = record[4]
            # self.data[f"rec {no}"]["Numer regału"] = record[4]
            # self.data[f"rec {no}"]["Imię pracownika"] = record[4]
            # self.data[f"rec {no}"]["Nazwisko pracownika"] = record[4]
            # self.data[f"rec {no}"]["Imię czytelnika"] = record[4]
            # self.data[f"rec {no}"]["Nazwisko czytelnika"] = record[4]
            # self.data[f"rec {no}"]["Nazwa biblioteki"] = record[4]


        self.model.importDict(self.data)
        if self.table is not None:
            self.table.redraw()



#TODO: Ponizej do zrobienia jak juz bedzie data model
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

        self.helpWindow = None

        self.colFrame = Frame(self.addWindow, bd=4, relief=RAISED,
                              width=self.themeWindow.winfo_width(),
                              height=self.themeWindow.winfo_height() - 40)
        self.colFrame.pack(fill='both', side=TOP)

        self.entries = list()

        Label(self.colFrame, text="Imię", font=("Arial Bold", 12)).grid(row=0, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=0, column=1, columnspan=2)
        self.entries.append(entry)

        Label(self.colFrame, text="Nazwisko", font=("Arial Bold", 12)).grid(row=1, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=1, column=1, columnspan=2)
        self.entries.append(entry)

        Label(self.colFrame, text="Funkcja", font=("Arial Bold", 12)).grid(row=2, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=2, column=1, columnspan=2)
        self.entries.append(entry)

        Label(self.colFrame, text="Przełożony", font=("Arial Bold", 12)).grid(row=3, column=0)
        entry = Entry(self.colFrame, width=20, state="readonly")
        entry.grid(row=3, column=1, columnspan=2)
        self.entries.append(entry)
        valueHelper = Button(self.colFrame, text="?", command=lambda _=entry: self.showHelp(_))
        valueHelper.grid(row=3, column=3)

        self.buttonFrame = Frame(self.addWindow, bd=4, relief=RAISED,
                                 width=self.themeWindow.winfo_width(),
                                 height=40)
        self.buttonFrame.pack(fill='both', side=TOP)
        self.addButton = Button(self.buttonFrame, text="Add", command=self.checkEntry)
        self.addButton.pack(side=LEFT)
        self.cancelButton = Button(self.buttonFrame, text="Cancel", command=self.goBack)
        self.cancelButton.pack(side=LEFT)

    def showHelp(self, entry):
        if self.helpWindow is not None:
            return

        def select():
            atr = self.listbox.get(self.listbox.curselection())
            if atr == "<brak>":
                boss_id = ""
            else:
                boss_id = atr.split(" ")[0]
            entry.config(state="normal")
            entry.delete("0", "end")
            entry.insert("end", boss_id)
            entry.config(state="disabled")
            exit()
            return

        def exit():
            self.helpWindow.destroy()
            self.helpWindow = None

        self.helpWindow = Toplevel(self.addWindow)
        self.helpWindow.protocol('WM_DELETE_WINDOW', exit)

        vals = list()
        temp_vals = self.database.executeStatement("SELECT `pracownik_id`, `imie`, `nazwisko` FROM `pracownicy`")
        for val1, val2, val3 in temp_vals:
            vals.append(f"{val1} {val2} {val3}")

        self.listbox = Listbox(self.helpWindow)
        self.listbox.pack(side=TOP)
        self.listbox.insert("end", "<brak>")

        for val in vals:
            self.listbox.insert("end", val)

        self.button = Button(self.helpWindow, text="Select", command=select)
        self.button.pack(side=TOP)

    def goBack(self):
        self.addWindow.event_generate("<<back>>")

    def checkEntry(self):
        self.newRecord.clear()
        # Employee's id
        self.newRecord.append("")
        # Employee's boss_id
        self.newRecord.append(self.entries[3].get())
        # Employee's name
        self.newRecord.append(self.entries[0].get())
        # Employee's surname
        self.newRecord.append(self.entries[1].get())
        # Employee's function
        self.newRecord.append(self.entries[2].get())

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

class ModifyController:
    def __init__(self, themeWindow, tableName, database, selectedRecord, data, backEvent):

        self.oldRecord = list()
        # Employee's id
        self.oldRecord.append(data[selectedRecord]["ID"])
        # Employee's boss_id
        #TODO: Metoda getBossID(name, surname)
        self.oldRecord.append("")
        # Employee's name
        self.oldRecord.append(data[selectedRecord]["Imię"])
        # Employee's surname
        self.oldRecord.append(data[selectedRecord]["Nazwisko"])
        # Employee's function
        self.oldRecord.append(data[selectedRecord]["Funkcja"])

        self.themeWindow = themeWindow
        self.tableName = tableName
        self.database = database
        self.backEvent = backEvent
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("ModifyController logger has started.")

        self.modifyWindow = Toplevel(self.themeWindow)
        self.modifyWindow.title("Modify an existing record.")
        self.modifyWindow.protocol('WM_DELETE_WINDOW', self.goBack)
        self.modifyWindow.bind("<<back>>", lambda _: self.backEvent(None))

        self.newRecord = list()

        self.helpWindow = None

        self.colFrame = Frame(self.modifyWindow, bd=4, relief=RAISED,
                              width=self.themeWindow.winfo_width(),
                              height=self.themeWindow.winfo_height() - 40)
        self.colFrame.pack(fill='both', side=TOP)

        self.entries = list()

        Label(self.colFrame, text="Imię", font=("Arial Bold", 12)).grid(row=0, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=0, column=1, columnspan=2)
        entry.insert(END, self.oldRecord[2])
        self.entries.append(entry)

        Label(self.colFrame, text="Nazwisko", font=("Arial Bold", 12)).grid(row=1, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=1, column=1, columnspan=2)
        entry.insert(END, self.oldRecord[3])
        self.entries.append(entry)

        Label(self.colFrame, text="Funkcja", font=("Arial Bold", 12)).grid(row=2, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=2, column=1, columnspan=2)
        entry.insert(END, self.oldRecord[4])
        self.entries.append(entry)

        Label(self.colFrame, text="Przełożony", font=("Arial Bold", 12)).grid(row=3, column=0)
        entry = Entry(self.colFrame, width=20, state="normal")
        entry.insert(END, self.oldRecord[1])
        entry.config(state="readonly")
        entry.grid(row=3, column=1, columnspan=2)
        self.entries.append(entry)
        valueHelper = Button(self.colFrame, text="?", command=lambda _=entry: self.showHelp(_))
        valueHelper.grid(row=3, column=3)

        self.buttonFrame = Frame(self.modifyWindow, bd=4, relief=RAISED,
                                 width=self.themeWindow.winfo_width(),
                                 height=40)
        self.buttonFrame.pack(fill='both', side=TOP)
        self.modifyButton = Button(self.buttonFrame, text="Modify", command=self.checkEntry)
        self.modifyButton.pack(side=LEFT)
        self.cancelButton = Button(self.buttonFrame, text="Cancel", command=self.goBack)
        self.cancelButton.pack(side=LEFT)


    def checkEntry(self):
        self.newRecord.clear()
        # Employee's id
        self.newRecord.append(self.oldRecord[0])
        # Employee's boss_id
        self.newRecord.append(self.entries[3].get())
        # Employee's name
        self.newRecord.append(self.entries[0].get())
        # Employee's surname
        self.newRecord.append(self.entries[1].get())
        # Employee's function
        self.newRecord.append(self.entries[2].get())

        try:
            print(f"old record = {self.oldRecord}")
            print(f"new record = {self.newRecord}")
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

    def showHelp(self, entry):
        if self.helpWindow is not None:
            return

        def select():
            atr = self.listbox.get(self.listbox.curselection())
            if atr == "<brak>":
                boss_id = ""
            else:
                boss_id = atr.split(" ")[0]
            entry.config(state="normal")
            entry.delete("0", "end")
            entry.insert("end", boss_id)
            entry.config(state="disabled")
            exit()
            return

        def exit():
            self.helpWindow.destroy()
            self.helpWindow = None

        self.helpWindow = Toplevel(self.modifyWindow)
        self.helpWindow.protocol('WM_DELETE_WINDOW', exit)

        vals = list()
        temp_vals = self.database.executeStatement("SELECT `pracownik_id`, `imie`, `nazwisko` FROM `pracownicy`")
        for val1, val2, val3 in temp_vals:
            vals.append(f"{val1} {val2} {val3}")

        self.listbox = Listbox(self.helpWindow)
        self.listbox.pack(side=TOP)
        self.listbox.insert("end", "<brak>")

        for val in vals:
            self.listbox.insert("end", val)

        self.button = Button(self.helpWindow, text="Select", command=select)
        self.button.pack(side=TOP)
