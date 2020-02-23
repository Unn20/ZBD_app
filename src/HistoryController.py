from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
from src.Logger import Logger
from tkintertable.Tables import TableCanvas
from tkinter import scrolledtext
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
        self.helpWindow = None

        self.tableData = self.database.getHistoryData()
        self.data = dict()
        self.model = TableModel()


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
        # self.buttonAdd = Button(self.bottomCanvas, text=" ADD ", command=self.add, width=24, height=3, bd=5)
        # self.buttonAdd.pack(side=LEFT)
        self.buttonModify = Button(self.bottomCanvas, text=" MODIFY ", command=self.modify, width=25, height=3, bd=5)
        self.buttonModify.pack(side=LEFT)
        self.buttonDelete = Button(self.bottomCanvas, text=" DELETE ",
                                   command=lambda: self.delete(), width=25, height=3, bd=5)
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


    def modify(self):
        """ Go to modify window """
        if self.table.startrow != self.table.endrow:
            messagebox.showwarning('Modify error', 'Please select only one record!')
            self.themeWindow.focus_set()
        else:
            selectedRow = self.table.currentrow
            if self.modifyWindow is None:
                self.logger.debug("Starting modify window.")
                self.modifyWindow = ModifyController(self.themeWindow, self.database,
                                                     self.model.getRecName(selectedRow),
                                                     self.data, self.backEvent)

    def delete(self, tableName="historia_operacji"):
        """ Delete selected records """
        for no, i in enumerate(self.table.multiplerowlist):
            recName = self.model.getRecName(i)
            try:
                self.database.deleteHistoryRecord(self.data[recName]['operacja_id'])
            except Exception as e:
                self.logger.error(f"Can not delete selected records! Error = {e}")
                errorNo = int(e.__str__().split()[0][1:-1])
                if errorNo == 1451:
                    messagebox.showerror("Can not delete selected records!",
                                         f"There are bounds including selected record.")
                else:
                    messagebox.showerror("Can not delete selected records!",
                                         f"Error {e}")
                self.themeWindow.focus_set()
                return
        confirm = messagebox.askyesno("Deleting record confirmation",
                                      f"Are You sure that You want to delete {len(self.table.multiplerowlist)} records?")
        if confirm:
            self.database.connection.commit()
        else:
            self.database.connection.rollback()
        self.themeWindow.focus_set()
        self.refreshTable()
        return

    def refreshTable(self):
        self.model.createEmptyModel()
        self.tableData = self.database.getHistoryData()
        self.data = dict()

        for key in self.tableData.keys():
            self.tableData[key]["data"] = str(self.tableData[key]["data"])
            del self.tableData[key]["pracownik_id"]
            del self.tableData[key]["czytelnik_id"]
        self.data = self.tableData
        self.model.importDict(self.data)
        if self.table is not None:
            self.table.redraw()


class ModifyController:
    def __init__(self, themeWindow, database, selectedRecord, data, backEvent):

        self.oldRecord = list()
        self.data = data
        self.oldRecord.append(data[selectedRecord]["operacja_id"])

        self.themeWindow = themeWindow
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

        self.delay = IntVar()
        if self.data[selectedRecord]["opoznienie"] == None:
            self.delay.set(0)
        else:
            self.delay.set(int(self.data[selectedRecord]["opoznienie"]))

        rowNo = 0

        Label(self.colFrame, text="Opoźnienie", font=("Arial Bold", 12)).grid(row=rowNo, column=0)
        entry = Spinbox(self.colFrame, from_=0, to=365, width=20, textvariable=self.delay)
        entry.grid(row=rowNo, column=1, columnspan=2)
        self.entries.append(entry)
        rowNo += 1

        """ Not used
        books = self.database.executeStatement("SELECT `tytul` FROM `ksiazki`")
        Label(self.colFrame, text="Tytuł książki", font=("Arial Bold", 12)).grid(row=rowNo, column=0)
        entry = ttk.Combobox(self.colFrame, width=20, values=books)
        entry.grid(row=rowNo, column=1, columnspan=2)
        entry.set(self.data[selectedRecord]["ksiazka_tytul"])
        self.entries.append(entry)
        rowNo += 1

        Label(self.colFrame, text="Dział", font=("Arial Bold", 12)).grid(row=rowNo, column=0)
        entry = Entry(self.colFrame, width=20, state="normal")
        entry.insert(END, self.data[selectedRecord]["dzial_nazwa"])
        entry.config(state="readonly")
        entry.grid(row=rowNo, column=1, columnspan=2)
        self.entries.append(entry)
        valueHelper = Button(self.colFrame, text="?", command=lambda _=entry: self.showHelp(_, "department"))
        valueHelper.grid(row=rowNo, column=4)
        rowNo += 1

        self.department = self.data[selectedRecord]['dzial_nazwa']
        self.racks = self.database.executeStatement(f"SELECT `numer` FROM `regaly` WHERE "
                                                    f"`dzial_nazwa` = \"{self.department}\"")
        Label(self.colFrame, text="Numer regału", font=("Arial Bold", 12)).grid(row=rowNo, column=0)
        self.rackEntry = ttk.Combobox(self.colFrame, width=20, values=self.racks)
        entry = self.rackEntry
        entry.grid(row=rowNo, column=1, columnspan=2)
        entry.set(self.data[selectedRecord]["regal_numer"])
        self.entries.append(entry)
        rowNo += 1
        """

        Label(self.colFrame, text="Pracownik", font=("Arial Bold", 12)).grid(row=rowNo, column=0)
        entry = Entry(self.colFrame, width=20, state="normal")
        entry.insert(END, self.data[selectedRecord]["pracownik_imie"] + " " + self.data[selectedRecord]["pracownik_nazwisko"])
        entry.config(state="readonly")
        entry.grid(row=rowNo, column=1, columnspan=2)
        self.entries.append(entry)
        valueHelper = Button(self.colFrame, text="?", command=lambda _=entry: self.showHelp(_, "employee"))
        valueHelper.grid(row=rowNo, column=4)
        rowNo += 1

        Label(self.colFrame, text="Czytelnik", font=("Arial Bold", 12)).grid(row=rowNo, column=0)
        entry = Entry(self.colFrame, width=20, state="normal")
        entry.insert(END, self.data[selectedRecord]["czytelnik_imie"] + " " + self.data[selectedRecord]["czytelnik_nazwisko"])
        entry.config(state="readonly")
        entry.grid(row=rowNo, column=1, columnspan=2)
        self.entries.append(entry)
        valueHelper = Button(self.colFrame, text="?", command=lambda _=entry: self.showHelp(_, "reader"))
        valueHelper.grid(row=rowNo, column=4)
        rowNo += 1

        libraries = self.database.executeStatement("SELECT `nazwa` FROM `biblioteki`")
        Label(self.colFrame, text="Nazwa biblioteki", font=("Arial Bold", 12)).grid(row=rowNo, column=0)
        entry = ttk.Combobox(self.colFrame, width=20, values=libraries)
        entry.grid(row=rowNo, column=1, columnspan=2)
        entry.set(self.data[selectedRecord]["biblioteka_nazwa"])
        self.entries.append(entry)
        rowNo += 1

        Label(self.colFrame, text="Uwagi", font=("Arial Bold", 12)).grid(row=rowNo, column=0)
        #entry = scrolledtext.ScrolledText(self.colFrame, width=40, height=10)
        entry = Entry(self.colFrame, width=40)
        entry.grid(row=rowNo, column=1, columnspan=2)
        #entry.insert(END, self.data[selectedRecord]["uwagi"])
        if self.data[selectedRecord]["uwagi"] == None:
            entry.insert(END, "")
        else:
            entry.insert(END, self.data[selectedRecord]["uwagi"])
        self.entries.append(entry)
        rowNo += 1

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

        # Delay
        self.newRecord.append(int(self.entries[0].get()))
        # Employee Id
        ns = self.entries[1].get().split(" ")
        id = self.database.executeStatement(f"SELECT `pracownik_id` FROM `pracownicy` "
                                            f"WHERE `imie` = \"{ns[0]}\" AND `nazwisko` = \"{ns[1]}\"")
        self.newRecord.append(id[0][0])
        # Reader
        ns = self.entries[2].get().split(" ")
        id = self.database.executeStatement(f"SELECT `czytelnik_id` FROM `czytelnicy` "
                                            f"WHERE `imie` = \"{ns[0]}\" AND `nazwisko` = \"{ns[1]}\"")
        self.newRecord.append(id[0][0])
        # Library Name
        self.newRecord.append(self.entries[3].get())
        # Comment
        #self.newRecord.append(self.entries[4].get('1.0', 'end'))
        self.newRecord.append(self.entries[4].get())

        try:
            self.database.modifyHistoryRecord(self.oldRecord, self.newRecord)
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
            self.modifyWindow.focus_set()
            self.newRecord = list()
            return
        confirm = messagebox.askyesno("Modify record confirmation",
                                      "Are You sure that You want to modify this record in database?")

        if confirm:
            self.database.connection.commit()
            self.goBack()
        else:
            self.database.connection.rollback()
            self.modifyWindow.focus_set()

    def goBack(self):
        self.modifyWindow.event_generate("<<back>>")

    def showHelp(self, entry, table):
        if self.helpWindow is not None:
            return

        def select():
            atr = self.listbox.get(self.listbox.curselection())
            entry.config(state="normal")
            entry.delete("0", "end")
            if table != "department":
                entry.insert("end", atr.split(" ")[0] + " " + atr.split(" ")[1])
            # else:
            #     entry.insert("end", atr.split(" ")[0])
            #     self.department = atr.split(" ")[0]
            #     self.racks = self.database.executeStatement(f"SELECT `numer` FROM `regaly` WHERE "
            #                                                 f"`dzial_nazwa` = \"{self.department}\"")
            #     #self.rackEntry.configure(values=self.racks)
            #     #self.rackEntry.set("")
            entry.config(state="readonly")
            self.helpWindow.focus_set()
            exit()
            return

        def exit():
            self.helpWindow.destroy()
            self.helpWindow = None

        self.helpWindow = Toplevel(self.modifyWindow)
        self.helpWindow.protocol('WM_DELETE_WINDOW', exit)

        vals = list()
        if table == "employee":
            temp_vals = self.database.executeStatement("SELECT `pracownik_id`, `imie`, `nazwisko` FROM `pracownicy`")
            for val1, val2, val3 in temp_vals:
                vals.append(f"{val2} {val3}")
        elif table == "reader":
            temp_vals = self.database.executeStatement("SELECT `czytelnik_id`, `imie`, `nazwisko` FROM `czytelnicy`")
            for val1, val2, val3 in temp_vals:
                vals.append(f"{val2} {val3}")
        else:
            temp_vals = self.database.executeStatement("SELECT `nazwa`, `lokalizacja` FROM `dzialy`")
            for val1, val2 in temp_vals:
                vals.append(f"{val1} {val2}")

        self.listbox = Listbox(self.helpWindow)
        self.listbox.pack(side=TOP)
        for val in vals:
            self.listbox.insert("end", val)

        self.button = Button(self.helpWindow, text="Select", command=select)
        self.button.pack(side=TOP)
