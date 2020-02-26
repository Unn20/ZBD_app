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

        self.ownersWindow = None
        self.findWindow = None

        self.addWindow = None
        self.modifyWindow = None
        self.modifyWindow2 = None
        self.table = None
        self.table2 = None

        self.tableData = self.database.getLibraryData()
        self.data = dict()
        self.data2 = dict()
        self.model = TableModel()
        self.model2 = TableModel()

        self.refreshTable()

        # Widgets
        self.content = Frame(self.themeWindow, bg="#B7B9B8", bd=4, relief=RAISED,
                             width=self.themeWindow.winfo_width() - 80,
                             height=self.themeWindow.winfo_height() - 80)
        self.content.place(x=40, y=40)
        self.content.bind("<<goback>>", lambda _: returnEvent(None))
        self.content.update()


        self.tabControl = ttk.Notebook(self.content)
        self.tab1 = Frame(self.tabControl)
        self.tabControl.add(self.tab1, text="Biblioteki")
        self.tab2 = Frame(self.tabControl)
        self.tabControl.add(self.tab2, text="Właściciele")

        self.tabControl.pack(expand=1, fill='both')


        ### LIBRARIES
        # Canvas with options menu
        self.topCanvas = Canvas(self.tab1, bg="white", bd=1, relief=RAISED,
                                width=int(self.content.winfo_width()),
                                height=int(self.content.winfo_height() / 12))
        self.topCanvas.pack(fill='both', side=TOP)

        self.backButton = Button(self.topCanvas, text=" < ", command=self.back, width=9)
        self.backButton.pack(fill='both', side=LEFT)
        self.showButton = Button(self.topCanvas, text="Refresh table", command=self.refreshTable, width=22)
        self.showButton.pack(fill='both', side=LEFT)
        self.findButton = Button(self.topCanvas, text="Owners", command=self.checkOwners, width=22)
        self.findButton.pack(fill='both', side=LEFT)
        self.findButton = Button(self.topCanvas, text="Find by owner", command=self.findByOwner, width=22)
        self.findButton.pack(fill='both', side=LEFT)


        # Canvas with data
        self.middleFrame = Frame(self.tab1)
        self.middleFrame.pack(fill='both', side=TOP)
        self.table = CustomTable(self.middleFrame, model=self.model)
        self.table.show()

        # Canvas with DML buttons
        self.bottomCanvas = Canvas(self.tab1, bg="white", bd=1, relief=FLAT,
                                   width=int(self.content.winfo_width()),
                                   height=int(self.content.winfo_height() / 5))
        self.bottomCanvas.pack(fill='both', side=TOP)
        self.buttonAdd = Button(self.bottomCanvas, text=" ADD ", command=self.add, width=24, height=3, bd=5)
        self.buttonAdd.pack(side=LEFT)
        self.buttonModify = Button(self.bottomCanvas, text=" MODIFY ", command=self.modify, width=25, height=3, bd=5)
        self.buttonModify.pack(side=LEFT)
        self.buttonDelete = Button(self.bottomCanvas, text=" DELETE ",
                                   command=lambda: self.delete(), width=25, height=3, bd=5)
        self.buttonDelete.pack(side=LEFT)

        ### OWNERS
        # Canvas with options menu
        self.topCanvas2 = Canvas(self.tab2, bg="white", bd=1, relief=RAISED,
                                width=int(self.content.winfo_width()),
                                height=int(self.content.winfo_height() / 12))
        self.topCanvas2.pack(fill='both', side=TOP)

        self.backButton2 = Button(self.topCanvas2, text=" < ", command=self.back, width=9)
        self.backButton2.pack(fill='both', side=LEFT)
        self.showButton2 = Button(self.topCanvas2, text="Refresh table", command=self.refreshTable, width=22)
        self.showButton2.pack(fill='both', side=LEFT)
        self.findButton2 = Button(self.topCanvas2, text="Libraries", command=self.checkLibraries, width=22)
        self.findButton2.pack(fill='both', side=LEFT)
        self.findButton2 = Button(self.topCanvas2, text="Find by library", command=self.findByLibrary, width=22)
        self.findButton2.pack(fill='both', side=LEFT)

        # Canvas with data
        self.middleFrame2 = Frame(self.tab2)
        self.middleFrame2.pack(fill='both', side=TOP)
        self.table2 = CustomTable(self.middleFrame2, model=self.model2)
        self.table2.show()

        # Canvas with DML buttons
        self.bottomCanvas2 = Canvas(self.tab2, bg="white", bd=1, relief=FLAT,
                                   width=int(self.content.winfo_width()),
                                   height=int(self.content.winfo_height() / 5))
        self.bottomCanvas2.pack(fill='both', side=TOP)
        self.buttonModify2 = Button(self.bottomCanvas2, text=" MODIFY ", command=self.modify2, width=25, height=3, bd=5)
        self.buttonModify2.pack(side=LEFT)
        self.buttonDelete2 = Button(self.bottomCanvas2, text=" DELETE ",
                                   command=lambda: self.delete2(), width=25, height=3, bd=5)
        self.buttonDelete2.pack(side=LEFT)


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
        if self.modifyWindow2 is not None:
            self.modifyWindow2.modifyWindow.destroy()
            self.modifyWindow2 = None
        self.refreshTable()

    def add(self):
        """ Go to add window """
        if self.addWindow is None:
            self.logger.debug("Starting add window.")
            self.addWindow = AddController(self.themeWindow, self.database, self.backEvent)

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

    def modify2(self):
        """ Go to modify window """
        pass
        if self.table2.startrow != self.table2.endrow:
            messagebox.showwarning('Modify error', 'Please select only one record!')
            self.themeWindow.focus_set()
        else:
            selectedRow = self.table2.currentrow
            if self.modifyWindow2 is None:
                self.logger.debug("Starting modify window.")
                self.modifyWindow2 = ModifyController2(self.themeWindow, self.database,
                                                       self.model2.getRecName(selectedRow),
                                                       self.data2, self.backEvent)

    def delete(self):
        """ Delete selected records """
        for no, i in enumerate(self.table.multiplerowlist):
            recName = self.model.getRecName(i)
            deletedRecord = list()
            deletedRecord.append(self.data[recName]["nazwa"])
            try:
                print(f"Deleted record = {deletedRecord}")
                self.database.deleteLibraryRecord(deletedRecord[0])
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
                                      f"Possible data loss. Are you sure?")
        if confirm:
            self.database.connection.commit()
        else:
            self.database.connection.rollback()
        self.themeWindow.focus_set()
        self.refreshTable()
        return

    def delete2(self):
        """ Delete selected records """
        for no, i in enumerate(self.table2.multiplerowlist):
            recName = self.model.getRecName(i)
            deletedRecord = list()
            deletedRecord.append(self.data2[recName]["NIP"])
            try:
                self.database.deleteOwner(deletedRecord[0])
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
                                      f"Possible data loss. Are you sure?")
        if confirm:
            self.database.connection.commit()
        else:
            self.database.connection.rollback()
        self.themeWindow.focus_set()
        self.refreshTable()
        return

    def refreshTable(self):
        self.model.createEmptyModel()
        self.tableData = self.database.getLibraryData()

        self.data = self.tableData
        self.model.importDict(self.data)
        if self.table is not None:
            self.table.redraw()

        self.model2.createEmptyModel()
        self.tableData = self.database.getOwnersData()

        self.data2 = self.tableData
        self.model2.importDict(self.data2)
        if self.table2 is not None:
            self.table2.redraw()

    def refreshTableWithOwner(self, nip):
        self.model.createEmptyModel()
        self.tableData = self.database.getLibraryDataByOwner(nip)
        self.data = dict()

        self.data = self.tableData
        self.model.importDict(self.data)
        if self.table is not None:
            self.table.redraw()
        self.findWindow.destroy()
        self.findWindow = None

    def refreshTableWithLibrary(self, libraryName):
        self.model2.createEmptyModel()
        self.tableData = self.database.getOwnerDataByLibrary(libraryName)

        self.data2 = self.tableData
        self.model2.importDict(self.data2)
        if self.table2 is not None:
            self.table2.redraw()
        self.findWindow.destroy()
        self.findWindow = None

    def findByOwner(self):
        if self.findWindow is not None:
            self.themeWindow.focus_set()
            return
        def exit_function():
            self.findWindow.destroy()
            self.findWindow = None
            self.themeWindow.focus_set()
        self.findWindow = Toplevel(self.themeWindow)
        self.findWindow.title("Search libraries by Owner's NIP.")
        self.findWindow.protocol('WM_DELETE_WINDOW', exit_function)

        vals = list()
        temp_vals = self.database.executeStatement("SELECT * FROM `wlasciciele`")
        for val1, val2, val3, val4 in temp_vals:
            owner = f"{val1}"
            if val2 is not None:
                owner += f" {val2}"
            if val3 is not None:
                owner += f" {val3}"
            if val4 is not None:
                owner += f" {val4}"
            vals.append(owner)

        self.listbox = Listbox(self.findWindow, width=50)
        self.listbox.pack(side=TOP)

        for val in vals:
            self.listbox.insert("end", val)

        self.button = Button(self.findWindow, text="Select",
                             command=lambda: self.refreshTableWithOwner(self.listbox.get(self.listbox.curselection()).split(" ")[0]))
        self.button.pack(side=TOP)

    def findByLibrary(self):
        if self.findWindow is not None:
            self.themeWindow.focus_set()
            return
        def exit_function():
            self.findWindow.destroy()
            self.findWindow = None
            self.themeWindow.focus_set()

        self.findWindow = Toplevel(self.themeWindow)
        self.findWindow.title("Search owners by library's name.")
        self.findWindow.protocol('WM_DELETE_WINDOW', exit_function)

        vals = list()
        temp_vals = self.database.executeStatement("SELECT * FROM `biblioteki`")
        for val1, val2 in temp_vals:
            owner = f"{val1}"
            owner += f" {val2}"
            vals.append(owner)

        self.listbox = Listbox(self.findWindow, width=50)
        self.listbox.pack(side=TOP)

        for val in vals:
            self.listbox.insert("end", val)

        self.button = Button(self.findWindow, text="Select",
                             command=lambda: self.refreshTableWithLibrary(self.listbox.get(self.listbox.curselection()).split(" ")[0]))
        self.button.pack(side=TOP)

    def checkOwners(self):
        if self.ownersWindow is not None:
            self.themeWindow.focus_set()
            return
        def exit_function():
            self.ownersWindow.destroy()
            self.ownersWindow = None
            self.themeWindow.focus_set()

        if self.table.startrow != self.table.endrow:
            messagebox.showwarning('Owners', 'Please select only one record!')
            self.themeWindow.focus_set()
            return

        recName = self.model.getRecName(self.table.currentrow)
        self.ownersWindow = Toplevel(self.themeWindow)
        self.ownersWindow.title(f"Owners of library {self.data[recName]['nazwa']}")
        self.ownersWindow.protocol('WM_DELETE_WINDOW', exit_function)

        Label(self.ownersWindow, text=f"Owners of {self.data[recName]['nazwa']}").pack(side=TOP)

        owners = self.database.executeStatement(f"SELECT w.`nip`, w.`imie`, w.`nazwisko`, w.`nazwa_firmy` "
                                                f"FROM `wlasciciele` w "
                                                f"JOIN `wlasciciel_biblioteka` wb ON w.`nip` = wb.`wlasciciel_nip` "
                                                f"WHERE wb.`biblioteka_nazwa` = \"{self.data[recName]['nazwa']}\"")
        ownersModel = TableModel()
        ownersModel.createEmptyModel()
        ownersData = dict()
        for no, owner in enumerate(owners):
            ownersData[f"rec {no+1}"] = dict()
            ownersData[f"rec {no + 1}"]["NIP"] = owner[0]
            if owner[1] is None:
                ownersData[f"rec {no + 1}"]["Imię"] = ""
            else:
                ownersData[f"rec {no + 1}"]["Imię"] = owner[1]
            if owner[2] is None:
                ownersData[f"rec {no + 1}"]["Nazwisko"] = ""
            else:
                ownersData[f"rec {no + 1}"]["Nazwisko"] = owner[2]
            if owner[3] is None:
                ownersData[f"rec {no + 1}"]["Nazwa Firmy"] = ""
            else:
                ownersData[f"rec {no + 1}"]["Nazwa Firmy"] = owner[3]

        ownersModel.importDict(ownersData)
        ownersFrame = Frame(self.ownersWindow)
        ownersFrame.pack(fill='both', side=TOP)
        ownersTable = CustomTable(ownersFrame, model=ownersModel)
        ownersTable.show()

        Button(self.ownersWindow, text="Close", command=exit_function).pack(side=TOP)

    def checkLibraries(self):
        if self.ownersWindow is not None:
            self.themeWindow.focus_set()
            return
        def exit_function():
            self.ownersWindow.destroy()
            self.ownersWindow = None
            self.themeWindow.focus_set()

        if self.table2.startrow != self.table2.endrow:
            messagebox.showwarning('Owners', 'Please select only one record!')
            self.themeWindow.focus_set()
            return

        recName = self.model2.getRecName(self.table2.currentrow)
        self.ownersWindow = Toplevel(self.themeWindow)
        self.ownersWindow.title(f"Library of owner {self.data2[recName]['NIP']}")
        self.ownersWindow.protocol('WM_DELETE_WINDOW', exit_function)

        Label(self.ownersWindow, text=f"Library of owner {self.data2[recName]['NIP']}").pack(side=TOP)

        libraries = self.database.executeStatement(f"SELECT * "
                                                f"FROM `biblioteki` b "
                                                f"JOIN `wlasciciel_biblioteka` wb ON b.`nazwa` = wb.`biblioteka_nazwa` "
                                                f"WHERE wb.`wlasciciel_nip` = \"{self.data2[recName]['NIP']}\"")
        libraryModel = TableModel()
        libraryModel.createEmptyModel()
        libraryData = dict()
        for no, library in enumerate(libraries):
            libraryData[f"rec {no+1}"] = dict()
            libraryData[f"rec {no + 1}"]["Nazwa"] = library[0]
            libraryData[f"rec {no + 1}"]["Lokalizacja"] = library[1]


        libraryModel.importDict(libraryData)
        libraryFrame = Frame(self.ownersWindow)
        libraryFrame.pack(fill='both', side=TOP)
        libraryTable = CustomTable(libraryFrame, model=libraryModel)
        libraryTable.show()

        Button(self.ownersWindow, text="Close", command=exit_function).pack(side=TOP)


class AddController:
    def __init__(self, themeWindow, database, backEvent):
        self.themeWindow = themeWindow
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
        self.assignWindow = None
        self.addWindow1 = None

        self.colFrame = Frame(self.addWindow, bd=4, relief=RAISED,
                              width=self.themeWindow.winfo_width(),
                              height=self.themeWindow.winfo_height() - 40)
        self.colFrame.pack(fill='both', side=TOP)

        self.entries = list()
        self.oldAssigments = list()

        Label(self.colFrame, text="Nazwa", font=("Arial Bold", 12)).grid(row=0, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=0, column=1, columnspan=2)
        self.entries.append(entry)

        Label(self.colFrame, text="Lokalizacja", font=("Arial Bold", 12)).grid(row=1, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=1, column=1, columnspan=2)
        self.entries.append(entry)

        self.button = Button(self.colFrame, text="Assign owners", command=self.assignOwners)
        self.button.grid(row=2, column=1)

        self.buttonFrame = Frame(self.addWindow, bd=4, relief=RAISED,
                                 width=self.themeWindow.winfo_width(),
                                 height=40)
        self.buttonFrame.pack(fill='both', side=TOP)
        self.addButton = Button(self.buttonFrame, text="Add", command=self.checkEntry)
        self.addButton.pack(side=LEFT)
        self.cancelButton = Button(self.buttonFrame, text="Cancel", command=self.goBack)
        self.cancelButton.pack(side=LEFT)

    def assignOwners(self):
        if self.assignWindow is not None:
            self.addWindow.focus_set()
            return

        def acceptOwners():
            self.oldAssigments = self.assigments.copy()
            self.assignWindow.destroy()
            self.assignWindow = None
            self.addWindow.focus_set()

        def exit_function():
            self.assignWindow.destroy()
            self.assignWindow = None
            self.addWindow.focus_set()

        def refresh():
            self.vals = list()
            temp_vals = self.database.executeStatement("SELECT * FROM `wlasciciele`")
            for val1, val2, val3, val4 in temp_vals:
                owner = f"{val1}"
                if val2 is not None:
                    owner += f" {val2}"
                if val3 is not None:
                    owner += f" {val3}"
                if val4 is not None:
                    owner += f" {val4}"
                self.vals.append(owner)

            self.listboxUnAssigned.delete(0,'end')
            self.listboxAssigned.delete(0, 'end')

            unAssigment = [val for val in self.vals if val not in self.assigments]
            for val in unAssigment:
                self.listboxUnAssigned.insert("end", val)
            for val in self.assigments:
                self.listboxAssigned.insert("end", val)

        self.assigments = self.oldAssigments.copy()

        self.assignWindow = Toplevel(self.addWindow)
        self.assignWindow.title("Assign owners.")
        self.assignWindow.protocol('WM_DELETE_WINDOW', exit_function)
        self.vals = list()

        self.listboxAssigned = Listbox(self.assignWindow, width=50, bd=4)
        self.listboxAssigned.pack(side=LEFT)

        self.listboxUnAssigned = Listbox(self.assignWindow, width=50)
        self.listboxUnAssigned.pack(side=LEFT)

        refresh()

        buttonFrame = Frame(self.assignWindow)
        buttonFrame.pack(side=RIGHT)

        addButton = Button(buttonFrame, text="Add owner", command=lambda: self.newOwner(refresh))
        addButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text=" < Assign", command=lambda: self.assignOwner(refresh))
        assignButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text=" > Unassign", command=lambda: self.unAssignOwner(refresh))
        assignButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text="Delete owner", command=lambda: self.deleteOwner(refresh))
        assignButton.pack(side=TOP)

        Button(buttonFrame, text="Accept", command=acceptOwners).pack(side=BOTTOM)
        Button(buttonFrame, text="Cancel", command=exit_function).pack(side=BOTTOM)

    def newOwner(self, func):
        if self.addWindow1 is not None:
            self.assignWindow.focus_set()
            return

        def exit_function():
            self.addWindow1.destroy()
            self.addWindow1 = None
            self.assignWindow.focus_set()

        def addOwner():
            if entry1.get() == "" or (entry4.get() == "" and (entry2.get() == "" or entry3.get() == "")):
                messagebox.showerror("Error", "Please fill all mandatory fields!")
                self.addWindow1.focus_set()
                return
            if len(entry1.get()) != 10 or not entry1.get().isdigit():
                messagebox.showerror("Error", "NIP field must contains 10 digits!")
                self.addWindow1.focus_set()
                return
            confirm = messagebox.askyesno("New owner", "Are you sure that you want add new owner?")
            if not confirm:
                self.addWindow1.focus_set()
                return
            try:
                self.database.addOwner(entry1.get(), entry2.get(), entry3.get(), entry4.get())
            except Exception as e:
                messagebox.showerror("Error", e)
                self.addWindow1.focus_set()
                return
            self.database.connection.commit()
            window.destroy()
            self.addWindow1 = None
            self.assignWindow.focus_set()
            func()

        window = Toplevel(self.assignWindow)
        self.addWindow1 = window
        window.title("New owner.")
        window.protocol('WM_DELETE_WINDOW', exit_function)

        Label(window, text="NIP").grid(row=0, column=0)
        entry1 = Entry(window)
        entry1.grid(row=0, column=1)
        Label(window, text="Imię").grid(row=1, column=0)
        entry2 = Entry(window)
        entry2.grid(row=1, column=1)
        Label(window, text="Nazwisko").grid(row=2, column=0)
        entry3 = Entry(window)
        entry3.grid(row=2, column=1)
        Label(window, text="Nazwa Firmy").grid(row=3, column=0)
        entry4 = Entry(window)
        entry4.grid(row=3, column=1)

        Button(window, text="Add", command=addOwner).grid(row=4, column=0)
        Button(window, text="Cancel", command=exit_function).grid(row=4, column=1)


    def assignOwner(self, func):
        if len(self.listboxUnAssigned.curselection()) == 0:
            return
        self.assigments.append(self.listboxUnAssigned.get(self.listboxUnAssigned.curselection()))
        func()

    def unAssignOwner(self, func):
        if len(self.listboxAssigned.curselection()) == 0:
            return
        self.assigments.remove(self.listboxAssigned.get(self.listboxAssigned.curselection()))
        func()

    def deleteOwner(self, func):
        if len(self.listboxAssigned.curselection()) == 0 and len(self.listboxUnAssigned.curselection()) == 0:
            messagebox.showerror("Delete problem", "Please select an owner to remove!")
            return
        confirm = messagebox.askyesno("Deleting", "Possible data loss. Are you sure?")
        if confirm:
            if len(self.listboxAssigned.curselection()) != 0:
                nip = self.listboxAssigned.get(self.listboxAssigned.curselection()).split(" ")[0]
                other = self.listboxAssigned.get(self.listboxAssigned.curselection())[10:]
                assigned = True
            else:
                nip = self.listboxUnAssigned.get(self.listboxUnAssigned.curselection()).split(" ")[0]
                other = self.listboxUnAssigned.get(self.listboxUnAssigned.curselection())[10:]
                assigned = False
            self.database.deleteOwner(nip)
            self.database.connection.commit()
            if assigned:
                self.assigments.remove(nip + other)
        else:
            return
        self.assignWindow.focus_set()
        func()


    def goBack(self):
        self.addWindow.event_generate("<<back>>")

    def checkEntry(self):
        self.newRecord.clear()
        # Library name
        self.newRecord.append(self.entries[0].get())
        # Library localization
        self.newRecord.append(self.entries[1].get())

        try:
            self.database.addLibrary(self.newRecord[0], self.newRecord[1], self.oldAssigments)
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
            self.addWindow.focus_set()
            return
        confirm = messagebox.askyesno("Add record confirmation",
                                      "Are You sure that You want to add this record to database?")

        if confirm:
            self.database.connection.commit()
            self.goBack()
        else:
            self.database.connection.rollback()
            self.addWindow.focus_set()

class ModifyController:
    def __init__(self, themeWindow, database, selectedRecord, data, backEvent):
        self.oldRecord = list()
        self.data = data
        self.oldRecord.append(self.data[selectedRecord]["nazwa"])
        self.themeWindow = themeWindow
        self.database = database
        self.backEvent = backEvent
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("AddController logger has started.")

        self.modifyWindow = Toplevel(self.themeWindow)
        self.modifyWindow.title("Add a new record to database.")
        self.modifyWindow.protocol('WM_DELETE_WINDOW', self.goBack)
        self.modifyWindow.bind("<<back>>", lambda _: self.backEvent(None))

        self.newRecord = list()

        ass = self.database.executeStatement(f"SELECT wb.`wlasciciel_nip`, w.`imie`, w.`nazwisko`, w.`nazwa_firmy` "
                                             f"FROM `wlasciciel_biblioteka` wb "
                                             f"JOIN `wlasciciele` w ON wb.`wlasciciel_nip` = w.`nip`"
                                             f"WHERE wb.`biblioteka_nazwa` = \"{self.oldRecord[0]}\"")
        self.oldAssigments = list()
        for val1, val2, val3, val4 in ass:
            owner = f"{val1}"
            if val2 is not None:
                owner += f" {val2}"
            if val3 is not None:
                owner += f" {val3}"
            if val4 is not None:
                owner += f" {val4}"
            self.oldAssigments.append(owner)


        self.helpWindow = None
        self.assignWindow = None
        self.addWindow1 = None

        self.colFrame = Frame(self.modifyWindow, bd=4, relief=RAISED,
                              width=self.themeWindow.winfo_width(),
                              height=self.themeWindow.winfo_height() - 40)
        self.colFrame.pack(fill='both', side=TOP)

        self.entries = list()

        Label(self.colFrame, text="Nazwa", font=("Arial Bold", 12)).grid(row=0, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=0, column=1, columnspan=2)
        entry.insert(END, self.data[selectedRecord]["nazwa"])
        self.entries.append(entry)

        Label(self.colFrame, text="Lokalizacja", font=("Arial Bold", 12)).grid(row=1, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=1, column=1, columnspan=2)
        entry.insert(END, self.data[selectedRecord]["lokalizacja"])
        self.entries.append(entry)

        self.button = Button(self.colFrame, text="Assign owners", command=self.assignOwners)
        self.button.grid(row=2, column=1)

        self.buttonFrame = Frame(self.modifyWindow, bd=4, relief=RAISED,
                                 width=self.themeWindow.winfo_width(),
                                 height=40)
        self.buttonFrame.pack(fill='both', side=TOP)
        self.addButton = Button(self.buttonFrame, text="Modify", command=self.checkEntry)
        self.addButton.pack(side=LEFT)
        self.cancelButton = Button(self.buttonFrame, text="Cancel", command=self.goBack)
        self.cancelButton.pack(side=LEFT)

    def assignOwners(self):
        if self.assignWindow is not None:
            self.modifyWindow.focus_set()
            return

        def acceptOwners():
            self.oldAssigments = self.assigments.copy()
            self.assignWindow.destroy()
            self.assignWindow = None
            self.modifyWindow.focus_set()

        def exit_function():
            self.assignWindow.destroy()
            self.assignWindow = None
            self.modifyWindow.focus_set()

        def refresh():
            self.vals = list()
            temp_vals = self.database.executeStatement("SELECT * FROM `wlasciciele`")
            for val1, val2, val3, val4 in temp_vals:
                owner = f"{val1}"
                if val2 is not None:
                    owner += f" {val2}"
                if val3 is not None:
                    owner += f" {val3}"
                if val4 is not None:
                    owner += f" {val4}"
                self.vals.append(owner)

            self.listboxUnAssigned.delete(0, 'end')
            self.listboxAssigned.delete(0, 'end')

            unAssigment = [val for val in self.vals if val not in self.assigments]
            for val in unAssigment:
                self.listboxUnAssigned.insert("end", val)
            for val in self.assigments:
                self.listboxAssigned.insert("end", val)

        self.assigments = self.oldAssigments.copy()

        self.assignWindow = Toplevel(self.modifyWindow)
        self.assignWindow.title("Assign owners.")
        self.assignWindow.protocol('WM_DELETE_WINDOW', exit_function)
        self.vals = list()

        self.listboxAssigned = Listbox(self.assignWindow, width=50, bd=4)
        self.listboxAssigned.pack(side=LEFT)

        self.listboxUnAssigned = Listbox(self.assignWindow, width=50)
        self.listboxUnAssigned.pack(side=LEFT)

        refresh()

        buttonFrame = Frame(self.assignWindow)
        buttonFrame.pack(side=RIGHT)

        addButton = Button(buttonFrame, text="Add owner", command=lambda: self.newOwner(refresh))
        addButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text="< Assign", command=lambda: self.assignOwner(refresh))
        assignButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text="> Unassign", command=lambda: self.unAssignOwner(refresh))
        assignButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text="Delete owner", command=lambda: self.deleteOwner(refresh))
        assignButton.pack(side=TOP)

        Button(buttonFrame, text="Accept", command=acceptOwners).pack(side=BOTTOM)
        Button(buttonFrame, text="Cancel", command=exit_function).pack(side=BOTTOM)

    def newOwner(self, func):
        if self.addWindow1 is not None:
            self.assignWindow.focus_set()
            return

        def exit_function():
            self.addWindow1.destroy()
            self.addWindow1 = None
            self.assignWindow.focus_set()

        def addOwner():
            if entry1.get() == "" or (entry4.get() == "" and (entry2.get() == "" or entry3.get() == "")):
                messagebox.showerror("Error", "Please fill all mandatory fields!")
                self.addWindow1.focus_set()
                return
            if len(entry1.get()) != 10 or not entry1.get().isdigit():
                messagebox.showerror("Error", "NIP field must contains 10 digits!")
                self.addWindow1.focus_set()
                return
            confirm = messagebox.askyesno("New owner", "Are you sure that you want add new owner?")
            if not confirm:
                self.addWindow1.focus_set()
                return
            try:
                self.database.addOwner(entry1.get(), entry2.get(), entry3.get(), entry4.get())
            except Exception as e:
                messagebox.showerror("Error", e)
                self.addWindow1.focus_set()
                return

            self.database.connection.commit()
            window.destroy()
            self.addWindow1 = None
            self.assignWindow.focus_set()
            func()

        window = Toplevel(self.assignWindow)
        self.addWindow1 = window
        window.title("New owner.")
        window.protocol('WM_DELETE_WINDOW', exit_function)

        Label(window, text="NIP").grid(row=0, column=0)
        entry1 = Entry(window)
        entry1.grid(row=0, column=1)
        Label(window, text="Imię").grid(row=1, column=0)
        entry2 = Entry(window)
        entry2.grid(row=1, column=1)
        Label(window, text="Nazwisko").grid(row=2, column=0)
        entry3 = Entry(window)
        entry3.grid(row=2, column=1)
        Label(window, text="Nazwa Firmy").grid(row=3, column=0)
        entry4 = Entry(window)
        entry4.grid(row=3, column=1)

        Button(window, text="Add", command=addOwner).grid(row=4, column=0)
        Button(window, text="Cancel", command=exit_function).grid(row=4, column=1)

    def assignOwner(self, func):
        if len(self.listboxUnAssigned.curselection()) == 0:
            return
        self.assigments.append(self.listboxUnAssigned.get(self.listboxUnAssigned.curselection()))
        func()

    def unAssignOwner(self, func):
        if len(self.listboxAssigned.curselection()) == 0:
            return
        self.assigments.remove(self.listboxAssigned.get(self.listboxAssigned.curselection()))
        func()

    def deleteOwner(self, func):
        if len(self.listboxAssigned.curselection()) == 0 and len(self.listboxUnAssigned.curselection()) == 0:
            messagebox.showerror("Delete problem", "Please select an owner to remove!")
            self.assignWindow.focus_set()
            return
        confirm = messagebox.askyesno("Deleting", "Possible data loss. Are you sure?")
        if confirm:
            if len(self.listboxAssigned.curselection()) != 0:
                nip = self.listboxAssigned.get(self.listboxAssigned.curselection()).split(" ")[0]
                other = self.listboxAssigned.get(self.listboxAssigned.curselection())[10:]
                assigned = True
            else:
                nip = self.listboxUnAssigned.get(self.listboxUnAssigned.curselection()).split(" ")[0]
                other = self.listboxUnAssigned.get(self.listboxUnAssigned.curselection())[10:]
                assigned = False
            self.database.deleteOwner(nip)
            self.database.connection.commit()
            if assigned:
                self.assigments.remove(nip + other)
        else:
            self.assignWindow.focus_set()
            return
        self.assignWindow.focus_set()
        func()

    def checkEntry(self):
        try:
            self.database.modifyLibrary(self.oldRecord[0], self.entries[0].get(), self.entries[1].get(), self.oldAssigments)
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
            self.modifyWindow.focus_set()
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


class ModifyController2:
    def __init__(self, themeWindow, database, selectedRecord, data, backEvent):
        self.oldRecord = list()
        self.data = data
        self.oldRecord.append(self.data[selectedRecord]["NIP"])
        self.themeWindow = themeWindow
        self.database = database
        self.backEvent = backEvent
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("ModifyController2 logger has started.")

        self.modifyWindow = Toplevel(self.themeWindow)
        self.modifyWindow.title("Modify a record in database.")
        self.modifyWindow.protocol('WM_DELETE_WINDOW', self.goBack)
        self.modifyWindow.bind("<<back>>", lambda _: self.backEvent(None))

        self.newRecord = list()

        # ass = self.database.executeStatement(f"SELECT wb.`wlasciciel_nip`, w.`imie`, w.`nazwisko`, w.`nazwa_firmy` "
        #                                      f"FROM `wlasciciel_biblioteka` wb "
        #                                      f"JOIN `wlasciciele` w ON wb.`wlasciciel_nip` = w.`nip`"
        #                                      f"WHERE wb.`biblioteka_nazwa` = \"{self.oldRecord[0]}\"")
        # self.oldAssigments = list()
        # for val1, val2, val3, val4 in ass:
        #     owner = f"{val1}"
        #     if val2 is not None:
        #         owner += f" {val2}"
        #     if val3 is not None:
        #         owner += f" {val3}"
        #     if val4 is not None:
        #         owner += f" {val4}"
        #     self.oldAssigments.append(owner)

        self.helpWindow = None

        self.colFrame = Frame(self.modifyWindow, bd=4, relief=RAISED,
                              width=self.themeWindow.winfo_width(),
                              height=self.themeWindow.winfo_height() - 40)
        self.colFrame.pack(fill='both', side=TOP)

        self.entries = list()

        Label(self.colFrame, text="NIP", font=("Arial Bold", 12)).grid(row=0, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=0, column=1, columnspan=2)
        entry.insert(END, self.data[selectedRecord]["NIP"])
        self.entries.append(entry)

        Label(self.colFrame, text="Nazwa firmy", font=("Arial Bold", 12)).grid(row=1, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=1, column=1, columnspan=2)
        if self.data[selectedRecord]["Nazwa firmy"] is not None:
            entry.insert(END, self.data[selectedRecord]["Nazwa firmy"])
        self.entries.append(entry)

        Label(self.colFrame, text="Imię", font=("Arial Bold", 12)).grid(row=2, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=2, column=1, columnspan=2)
        if self.data[selectedRecord]["Imię"] is not None:
            entry.insert(END, self.data[selectedRecord]["Imię"])
        self.entries.append(entry)

        Label(self.colFrame, text="Nazwisko", font=("Arial Bold", 12)).grid(row=3, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=3, column=1, columnspan=2)
        if self.data[selectedRecord]["Nazwisko"] is not None:
            entry.insert(END, self.data[selectedRecord]["Nazwisko"])
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
        try:
            self.database.modifyOwner(self.oldRecord[0], self.entries[0].get(), self.entries[1].get(),
                                      self.entries[2].get(), self.entries[3].get())
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
            self.modifyWindow.focus_set()
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

