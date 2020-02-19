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
        self.table = None

        self.tableData = self.database.getLibraryData()
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
        self.findButton = Button(self.topCanvas, text="Owners", command=self.checkOwners, width=22)
        self.findButton.pack(fill='both', side=LEFT)
        self.showButton = Button(self.topCanvas, text="Refresh table", command=self.refreshTable, width=22)
        self.showButton.pack(fill='both', side=LEFT)
        self.findButton = Button(self.topCanvas, text="Find by owner", command=self.findByOwner, width=22)
        self.findButton.pack(fill='both', side=LEFT)


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

    def add(self):
        """ Go to add window """
        if self.addWindow is None:
            self.logger.debug("Starting add window.")
            self.addWindow = AddController(self.themeWindow, self.database, self.backEvent)

    def modify(self):
        """ Go to modify window """
        if self.table.startrow != self.table.endrow:
            messagebox.showwarning('Modify error', 'Please select only one record!')
        else:
            selectedRow = self.table.currentrow
            if self.modifyWindow is None:
                self.logger.debug("Starting modify window.")
                self.modifyWindow = ModifyController(self.themeWindow, self.database,
                                                     self.model.getRecName(selectedRow),
                                                     self.data, self.backEvent)

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

                return
        confirm = messagebox.askyesno("Deleting record confirmation",
                                      f"Possible data loss. Are you sure?")
        if confirm:
            self.database.connection.commit()
        else:
            self.database.connection.rollback()
        self.refreshTable()
        return

    def refreshTable(self):
        self.model.createEmptyModel()
        self.tableData = self.database.getLibraryData()
        self.data = dict()

        self.data = self.tableData
        self.model.importDict(self.data)
        if self.table is not None:
            self.table.redraw()

    def refreshTableWithOwner(self, nip):
        self.model.createEmptyModel()
        self.tableData = self.database.getLibraryDataByOwner(nip)
        self.data = dict()

        self.data = self.tableData
        self.model.importDict(self.data)
        if self.table is not None:
            self.table.redraw()
        self.findWindow.destroy()

    def findByOwner(self):
        self.findWindow = Toplevel(self.themeWindow)
        self.findWindow.title("Search libraries by Owner's NIP.")
        self.findWindow.protocol('WM_DELETE_WINDOW', self.findWindow.destroy)

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

    def checkOwners(self):
        if self.table.startrow != self.table.endrow:
            messagebox.showwarning('Owners', 'Please select only one record!')
            return

        recName = self.model.getRecName(self.table.currentrow)
        self.ownersWindow = Toplevel(self.themeWindow)
        self.ownersWindow.title(f"Owners of library {self.data[recName]['nazwa']}")
        self.ownersWindow.protocol('WM_DELETE_WINDOW', self.ownersWindow.destroy)

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

        Button(self.ownersWindow, text="Close", command=self.ownersWindow.destroy).pack(side=TOP)


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
        def acceptOwners():
            self.oldAssigments = self.assigments.copy()
            self.assignWindow.destroy()

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

        self.assignWindow = Toplevel(self.themeWindow)
        self.assignWindow.title("Assign owners.")
        self.assignWindow.protocol('WM_DELETE_WINDOW', self.assignWindow.destroy)
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
        Button(buttonFrame, text="Cancel", command=self.assignWindow.destroy).pack(side=BOTTOM)

    def newOwner(self, func):
        def addOwner():
            if entry1.get() == "" or (entry4.get() == "" and (entry2.get() == "" or entry3.get() == "")):
                messagebox.showerror("Error", "Please fill all mandatory fields!")
                return
            if len(entry1.get()) != 10 or not entry1.get().isdigit():
                messagebox.showerror("Error", "NIP field must contains 10 digits!")
                return
            confirm = messagebox.askyesno("New owner", "Are you sure that you want add new owner?")
            if not confirm:
                return
            try:
                self.database.addOwner(entry1.get(), entry2.get(), entry3.get(), entry4.get())
            except Exception as e:
                messagebox.showerror("Error", e)
            self.database.connection.commit()
            window.destroy()
            func()

        window = Toplevel(self.assignWindow)
        window.title("New owner.")
        window.protocol('WM_DELETE_WINDOW', window.destroy)

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
        Button(window, text="Cancel", command=window.destroy).grid(row=4, column=1)


    def assignOwner(self, func):
        if len(self.listboxUnAssigned.curselection()) == 0:
            return
        self.assigments.append(self.listboxUnAssigned.get(self.listboxUnAssigned.curselection()))
        func()

    def unAssignOwner(self, func):
        if len(self.listboxAssigned.curselection()) == 0:
            return
        self.assigments.remove()
        func()

    def deleteOwner(self, func):
        if len(self.listboxAssigned.curselection()) == 0 and len(self.listboxUnAssigned.curselection()) == 0:
            messagebox.showerror("Delete problem", "Please select an owner to remove!")
            return
        confirm = messagebox.askyesno("Deleting", "Are you sure that you want to delete selected owner?")
        if confirm:
            if len(self.listboxAssigned.curselection()) != 0:
                nip = self.listboxAssigned.get(self.listboxAssigned.curselection()).split(" ")[0]
            else:
                nip = self.listboxUnAssigned.get(self.listboxUnAssigned.curselection()).split(" ")[0]
            self.database.deleteOwner(nip)
            self.database.connection.commit()
        else:
            return
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
        def acceptOwners():
            self.oldAssigments = self.assigments.copy()
            self.assignWindow.destroy()

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

        self.assignWindow = Toplevel(self.themeWindow)
        self.assignWindow.title("Assign owners.")
        self.assignWindow.protocol('WM_DELETE_WINDOW', self.assignWindow.destroy)
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
        Button(buttonFrame, text="Cancel", command=self.assignWindow.destroy).pack(side=BOTTOM)

    def newOwner(self, func):
        def addOwner():
            if entry1.get() == "" or (entry4.get() == "" and (entry2.get() == "" or entry3.get() == "")):
                messagebox.showerror("Error", "Please fill all mandatory fields!")
                return
            if len(entry1.get()) != 10 or not entry1.get().isdigit():
                messagebox.showerror("Error", "NIP field must contains 10 digits!")
                return
            confirm = messagebox.askyesno("New owner", "Are you sure that you want add new owner?")
            if not confirm:
                return
            self.database.addOwner(entry1.get(), entry2.get(), entry3.get(), entry4.get())
            self.database.connection.commit()
            window.destroy()
            func()

        window = Toplevel(self.assignWindow)
        window.title("New owner.")
        window.protocol('WM_DELETE_WINDOW', window.destroy)

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
        Button(window, text="Cancel", command=window.destroy).grid(row=4, column=1)

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
        confirm = messagebox.askyesno("Deleting", "Are you sure that you want to delete selected owner?")
        if confirm:
            if len(self.listboxAssigned.curselection()) != 0:
                nip = self.listboxAssigned.get(self.listboxAssigned.curselection()).split(" ")[0]
            else:
                nip = self.listboxUnAssigned.get(self.listboxUnAssigned.curselection()).split(" ")[0]
            self.database.deleteOwner(nip)
            self.database.connection.commit()
        else:
            return
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

