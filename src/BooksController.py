from tkinter import *
from tkinter import messagebox
from src.Logger import Logger
from tkinter import ttk
from tkintertable.Tables import TableCanvas
from src.CustomTable import CustomTable
from tkintertable.TableModels import TableModel
import datetime
from datetime import date
from tkcalendar import DateEntry


class BooksController:
    def __init__(self, database, themeWindow, returnEvent):
        self.database = database
        self.themeWindow = themeWindow
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("TableController logger has started.")

        self.addWindow = None
        self.modifyWindow = None
        self.table = None

        self.rackHelpWindow = None
        self.departmentHelpWindow = None

        self.tableData = self.database.getBooksData()
        self.data = dict()
        self.booksModel = TableModel()

        self.currentModel = self.booksModel

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

        self.backButton = Button(self.topCanvas, text=" < ", command=self.back, width=6)
        self.backButton.pack(fill='both', side=LEFT)
        self.showButton = Button(self.topCanvas, text="Refresh table", command=self.refreshTable, width=17)
        self.showButton.pack(fill='both', side=LEFT)
        self.showButton = Button(self.topCanvas, text="Authors", command=self.checkAuthors, width=17)
        self.showButton.pack(fill='both', side=LEFT)
        self.findButton = Button(self.topCanvas, text="Find by author", command=self.findByAuthor, width=17)
        self.findButton.pack(fill='both', side=LEFT)
        self.specimenButton = Button(self.topCanvas, text="Specimens", command=self.bookSpecimens, width=17)
        self.specimenButton.pack(fill='both', side=LEFT)

        # Canvas with data
        self.middleFrame = Frame(self.content)
        self.middleFrame.pack(fill='both', side=TOP)
        self.table = CustomTable(self.middleFrame, model=self.currentModel)
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

    def bookSpecimens(self):
        if self.table.startrow != self.table.endrow:
            messagebox.showwarning('Specimens', 'Please select only one record!')
            return
        self.specimenData = dict()
        def refresh():
            specimens = self.database.getSpecimensByBookId(self.bookId)
            specimenModel.createEmptyModel()
            self.specimenData = dict()
            for no, specimen in enumerate(specimens):
                self.specimenData[f"rec {no + 1}"] = dict()
                self.specimenData[f"rec {no + 1}"]["Egzemplarz ID"] = specimen[0]
                self.specimenData[f"rec {no + 1}"]["Numer regału"] = specimen[1]
                self.specimenData[f"rec {no + 1}"]["Nazwa działu"] = specimen[2]
                self.specimenData[f"rec {no + 1}"]["Lokalizacja działu"] = specimen[3]

            specimenModel.importDict(self.specimenData)
            self.specimenTable.redraw()

        recName = self.currentModel.getRecName(self.table.currentrow)

        self.specimenWindow = Toplevel(self.themeWindow)
        self.specimenWindow.title(f"Specimens of book {self.data[recName]['Tytuł']}")
        self.specimenWindow.protocol('WM_DELETE_WINDOW', self.specimenWindow.destroy)

        Label(self.specimenWindow, text=f"Specimens of {self.data[recName]['Tytuł']}").pack(side=TOP)

        self.bookId = self.database.executeStatement(f"SELECT `ksiazka_id` FROM `ksiazki` "
                                                f"WHERE `tytul` = \"{self.data[recName]['Tytuł']}\"")[0][0]

        specimenFrame = Frame(self.specimenWindow)
        specimenFrame.pack(fill='both', side=TOP)
        specimenModel = TableModel()
        self.specimenTable = CustomTable(specimenFrame, model=specimenModel)
        self.specimenTable.show()
        refresh()

        buttonFrame = Frame(self.specimenWindow)
        buttonFrame.pack(side=TOP)

        Button(buttonFrame, text="Add", command=lambda: self.addSpecimen(refresh)).pack(side=LEFT)
        Button(buttonFrame, text="Delete", command=lambda: self.deleteSpecimen(refresh)).pack(side=LEFT)
        Button(buttonFrame, text="Cancel", command=self.specimenWindow.destroy).pack(side=LEFT)

    def addSpecimen(self, func):
        def checkSpecimenEntry():
            if entry1.get() == "" or entry2.get() == "":
                messagebox.showerror("Error", "Fill all mandatory fields!")
                return

            tmp_racks = self.database.executeStatement(f"SELECT `numer` FROM `regaly` "
                                                       f"WHERE `dzial_nazwa` = \"{entry1.get()}\"")
            racks = list()
            for r in tmp_racks:
                racks.append(str(r[0]))

            if entry2.get() in racks:
                confirm = messagebox.askyesno("Add", "You want to add new specimen?")
                if confirm:
                    try:
                        self.database.addSpecimen(self.bookId, entry2.get())
                    except Exception as e:
                        messagebox.showerror("Can not delete selected records!",
                                             f"Error {e}")
                        return
                    self.database.connection.commit()
                    func()
                else:
                    return
            else:
                confirm = messagebox.askyesno("Add", "Given rack doesn't exists. Would You like to create a new rack?")
                if confirm:
                    try:
                        self.newRack(entry2.get(), 100, entry1.get())
                    except Exception as e:
                        messagebox.showerror("Can not delete selected records!",
                                             f"Error {e}")
                        return
                    try:
                        self.database.addSpecimen(self.bookId, entry2.get())
                    except Exception as e:
                        messagebox.showerror("Can not delete selected records!",
                                             f"Error {e}")
                        return
                    self.database.connection.commit()
                    func()
                else:
                    return

        window = Toplevel(self.specimenWindow)
        window.title(f"New specimen")
        window.protocol('WM_DELETE_WINDOW', window.destroy)

        Label(window, text="Dział").grid(row=0, column=0)
        entry1 = Entry(window)
        entry1.grid(row=0, column=1, columnspan=2)
        entry1.config(state="readonly")
        valueHelper = Button(window, text="?", command=lambda en=entry1: self.showDepartmentHelp(en))
        valueHelper.grid(row=0, column=3)
        new = Button(window, text="New", command=lambda en=entry1: self.newDepartment(en))
        new.grid(row=0, column=4)

        Label(window, text="Regał").grid(row=1, column=0)
        entry2 = Entry(window)
        entry2.grid(row=1, column=1, columnspan=2)
        entry2.config(state="normal")
        valueHelper = Button(window, text="?", command=lambda en1=entry1, en2=entry2: self.showRackHelp(en2, en1))
        valueHelper.grid(row=1, column=3)

        Button(window, text="Add", command=checkSpecimenEntry).grid(row=2, column=0)
        Button(window, text="Cancel", command=window.destroy).grid(row=2, column=1)

    def newRack(self, no, capability, dep):
        self.database.executeStatement(f"INSERT INTO `regaly` "
                                       f"VALUES ({no}, {capability}, {0}, \"{dep}\")")
        self.database.connection.commit()


    def newDepartment(self, entry):
        def addDep():
            if entry1.get() == "" or entry2.get() == "":
                messagebox.showerror("Error", "Fill all mandatory fields!")
                return
            confirm = messagebox.askyesno("Add", "You want to add new department?")
            if confirm:
                try:
                    self.database.addDepartment(entry1.get(), entry2.get())
                except Exception as e:
                    messagebox.showerror("Can not delete selected records!",
                                         f"Error {e}")
                    return
                self.database.connection.commit()
                entry.set(entry1.get())
            else:
                return

        window = Toplevel(self.specimenWindow)
        window.title(f"New department")
        window.protocol('WM_DELETE_WINDOW', window.destroy)

        Label(window, text="Nazwa", font=("Arial Bold", 12)).grid(row=0, column=0)
        entry1 = Entry(window, width=20)
        entry1.grid(row=0, column=1, columnspan=2)

        Label(window, text="Lokalizacja", font=("Arial Bold", 12)).grid(row=1, column=0)
        entry2 = Entry(window, width=20)
        entry2.grid(row=1, column=1, columnspan=2)

        Button(window, text="Add", command=addDep).grid(row=2, column=0)
        Button(window, text="Cancel", command=window.destroy).grid(row=2, column=1)


    def showRackHelp(self, entry, depEntry):
        if self.rackHelpWindow is not None:
            return

        def select():
            try:
                atr = self.rackListbox.get(self.rackListbox.curselection())
            except:
                return
            entry.config(state="normal")
            entry.delete("0", "end")
            entry.insert("end", atr)
            #entry.config(state="readonly")
            exit()
            return

        def exit():
            self.rackHelpWindow.destroy()
            self.rackHelpWindow = None

        self.rackHelpWindow = Toplevel(self.specimenWindow)
        self.rackHelpWindow.title("Choose rack")
        self.rackHelpWindow.protocol('WM_DELETE_WINDOW', exit)

        vals = list()
        temp_vals = self.database.executeStatement(f"SELECT `numer` FROM `regaly` "
                                                   f"WHERE `dzial_nazwa` = \"{depEntry.get()}\"")
        for val1 in temp_vals:
            vals.append(f"{val1[0]}")

        self.rackListbox = Listbox(self.rackHelpWindow)
        self.rackListbox.pack(side=TOP)
        for val in vals:
            self.rackListbox.insert("end", val)

        button = Button(self.rackHelpWindow, text="Select", command=select, bd=4)
        button.pack(side=BOTTOM)

    def showDepartmentHelp(self, entry):
        if self.departmentHelpWindow is not None:
            return

        def select():
            atr = self.departmentListbox.get(self.departmentListbox.curselection())
            entry.config(state="normal")
            entry.delete("0", "end")
            entry.insert("end", atr.split(" ")[0])
            entry.config(state="readonly")
            exit()
            return

        def exit():
            self.departmentHelpWindow.destroy()
            self.departmentHelpWindow = None

        self.departmentHelpWindow = Toplevel(self.addWindow)
        self.departmentHelpWindow.title("Choose genre")
        self.departmentHelpWindow.protocol('WM_DELETE_WINDOW', exit)

        vals = list()
        temp_vals = self.database.executeStatement("SELECT `nazwa`, `lokalizacja` FROM `dzialy`")
        for val1, val2 in temp_vals:
            vals.append(f"{val1} {val2}")

        self.departmentListbox = Listbox(self.departmentHelpWindow)
        self.departmentListbox.pack(side=TOP)
        for val in vals:
            self.departmentListbox.insert("end", val)

        button = Button(self.departmentHelpWindow, text="Select", command=select, bd=4)
        button.pack(side=BOTTOM)


    def deleteSpecimen(self, func):
        for no, i in enumerate(self.specimenTable.multiplerowlist):
            recName = self.currentModel.getRecName(i)
            try:
                self.database.deleteSpecimen(self.specimenData[recName]["Egzemplarz ID"])
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
                                      f"Are You sure that You want to delete {len(self.specimenTable.multiplerowlist)} records?")
        if confirm:
            self.database.connection.commit()
        else:
            self.database.connection.rollback()
        func()
        return

    def findByAuthor(self):
        self.findWindow = Toplevel(self.themeWindow)
        self.findWindow.title("Search book by author's personal data.")
        self.findWindow.protocol('WM_DELETE_WINDOW', self.findWindow.destroy)

        vals = list()
        temp_vals = self.database.executeStatement("SELECT * FROM `autorzy`")
        for val1, val2, val3, val4, val5 in temp_vals:
            author = f"{val1} {val2} {val3} {val4}"
            if val5 is not None:
                author += f"-{val5}"
            vals.append(author)

        self.listbox = Listbox(self.findWindow, width=50)
        self.listbox.pack(side=TOP)

        for val in vals:
            self.listbox.insert("end", val)

        self.button = Button(self.findWindow, text="Select",
                             command=lambda: self.refreshTableWithAuthor(
                                 self.listbox.get(self.listbox.curselection()).split(" ")[0]))
        self.button.pack(side=TOP)

    def refreshTableWithAuthor(self, author):
        self.currentModel.createEmptyModel()
        self.tableData = self.database.getBooksDataByAuthor(author)
        self.data = dict()
        for no, key in enumerate(self.tableData.keys()):
            self.data[f"rec {no + 1}"] = dict()
            self.data[f"rec {no + 1}"]["Tytuł"] = self.tableData[key]["tytul"]
            self.data[f"rec {no + 1}"]["Data opublikowania"] = str(self.tableData[key]["data_opublikowania"])
            self.data[f"rec {no + 1}"]["Gatunek"] = self.tableData[key]["gatunek"]
            self.data[f"rec {no + 1}"]["Liczba egzemplarzy"] = self.tableData[key]["liczba_ksiazek"]

        self.currentModel.importDict(self.data)
        if self.table is not None:
            self.table.redraw()
        self.findWindow.destroy()

    def checkAuthors(self):
        if self.table.startrow != self.table.endrow:
            messagebox.showwarning('Authors', 'Please select only one record!')
            return

        recName = self.currentModel.getRecName(self.table.currentrow)
        self.authorsWindow = Toplevel(self.themeWindow)
        self.authorsWindow.title(f"Authors of book {self.data[recName]['Tytuł']}")
        self.authorsWindow.protocol('WM_DELETE_WINDOW', self.authorsWindow.destroy)

        Label(self.authorsWindow, text=f"Authors of {self.data[recName]['Tytuł']}").pack(side=TOP)

        bookId = self.database.executeStatement(f"SELECT `ksiazka_id` FROM `ksiazki` "
                                                f"WHERE `tytul` = \"{self.data[recName]['Tytuł']}\"")
        authors = self.database.executeStatement(f"SELECT a.`imie`, a.`nazwisko`, a.`data_urodzenia`, a.`data_smierci` "
                                                f"FROM `autorzy` a "
                                                f"JOIN `autor_ksiazka` ak ON a.`autor_id` = ak.`autorzy_autor_id` "
                                                f"WHERE ak.`ksiazki_ksiazka_id` = \"{bookId[0][0]}\"")
        authorsModel = TableModel()
        authorsModel.createEmptyModel()
        authorsData = dict()
        for no, author in enumerate(authors):
            authorsData[f"rec {no+1}"] = dict()
            authorsData[f"rec {no + 1}"]["Imię"] = author[0]
            authorsData[f"rec {no + 1}"]["Nazwisko"] = author[1]
            authorsData[f"rec {no + 1}"]["Data urodzenia"] = str(author[2])
            if author[3] is None:
                authorsData[f"rec {no + 1}"]["Data śmierci"] = ""
            else:
                authorsData[f"rec {no + 1}"]["Data śmierci"] = str(author[3])

        authorsModel.importDict(authorsData)
        authorsFrame = Frame(self.authorsWindow)
        authorsFrame.pack(fill='both', side=TOP)
        authorsTable = CustomTable(authorsFrame, model=authorsModel)
        authorsTable.show()

        Button(self.authorsWindow, text="Close", command=self.authorsWindow.destroy).pack(side=TOP)

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
                                                     self.currentModel.getRecName(selectedRow),
                                                     self.data, self.backEvent)

    def delete(self):
        """ Delete selected records """
        for no, i in enumerate(self.table.multiplerowlist):
            recName = self.currentModel.getRecName(i)
            deletedRecord = list()
            deletedRecord.append(self.data[recName]["Tytuł"])
            id = self.database.executeStatement(f"SELECT `ksiazka_id` FROM `ksiazki` "
                                                f"WHERE `tytul` = \"{deletedRecord[0]}\"")
            try:
                self.database.deleteBookRecord(id[0][0])
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
        self.currentModel.createEmptyModel()
        self.tableData = self.database.getBooksData()
        self.data = dict()
        for no, key in enumerate(self.tableData.keys()):
            self.data[f"rec {no + 1}"] = dict()
            self.data[f"rec {no + 1}"]["Tytuł"] = self.tableData[key]["tytul"]
            self.data[f"rec {no + 1}"]["Data opublikowania"] = str(self.tableData[key]["data_opublikowania"])
            self.data[f"rec {no + 1}"]["Gatunek"] = self.tableData[key]["gatunek"]
            self.data[f"rec {no + 1}"]["Liczba egzemplarzy"] = self.tableData[key]["liczba_ksiazek"]

        self.currentModel.importDict(self.data)
        if self.table is not None:
            self.table.redraw()

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
        self.oldAssigments = list()

        self.helpWindow = None

        self.colFrame = Frame(self.addWindow, bd=4, relief=RAISED,
                              width=self.themeWindow.winfo_width(),
                              height=self.themeWindow.winfo_height() - 40)
        self.colFrame.pack(fill='both', side=TOP)

        self.entries = list()

        Label(self.colFrame, text="Tytuł", font=("Arial Bold", 12)).grid(row=0, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=0, column=1, columnspan=2)
        self.entries.append(entry)

        Label(self.colFrame, text="Data opublikowania", font=("Arial Bold", 12)).grid(row=1, column=0)
        entry = DateEntry(self.colFrame, date_pattern='y-mm-dd')
        entry.grid(row=1, column=1, columnspan=2)
        self.entries.append(entry)

        Label(self.colFrame, text="Gatunek", font=("Arial Bold", 12)).grid(row=2, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=2, column=1, columnspan=2)
        entry.config(state="normal")
        self.entries.append(entry)
        valueHelper = Button(self.colFrame, text="?", command=lambda _=entry: self.showHelp(_))
        valueHelper.grid(row=2, column=3)

        self.button = Button(self.colFrame, text="Assign authors", command=self.assignAuthors)
        self.button.grid(row=3, column=1)

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
            entry.config(state="normal")
            entry.delete("0", "end")
            entry.insert("end", atr)
            entry.config(state="readonly")
            exit()
            return

        def exit():
            self.helpWindow.destroy()
            self.helpWindow = None

        self.helpWindow = Toplevel(self.addWindow)
        self.helpWindow.title("Choose genre")
        self.helpWindow.protocol('WM_DELETE_WINDOW', exit)

        vals = list()
        temp_vals = self.database.executeStatement("SELECT `gatunek` FROM `gatunki`")
        for val1 in temp_vals:
            vals.append(f"{val1[0]}")

        self.listbox = Listbox(self.helpWindow)
        self.listbox.pack(side=TOP)
        for val in vals:
            self.listbox.insert("end", val)

        self.button = Button(self.helpWindow, text="Select", command=select, bd=4)
        self.button.pack(side=BOTTOM)

    def assignAuthors(self):
        def acceptAuthors():
            self.oldAssigments = self.assigments.copy()
            self.assignWindow.destroy()

        def refresh():
            self.vals = list()
            temp_vals = self.database.executeStatement("SELECT `autor_id`, `imie`, `nazwisko`, `data_urodzenia`, `data_smierci` "
                                                       "FROM `autorzy`")
            for val0, val1, val2, val3, val4 in temp_vals:
                author = f"{val0} {val1} {val2} {val3}"
                if val4 is not None:
                    author += f"-{val4}"
                self.vals.append(author)

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

        addButton = Button(buttonFrame, text="Add author", command=lambda: self.newAuthor(refresh))
        addButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text=" < Assign", command=lambda: self.assignAuthor(refresh))
        assignButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text=" > Unassign", command=lambda: self.unAssignAuthor(refresh))
        assignButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text="Delete author", command=lambda: self.deleteAuthor(refresh))
        assignButton.pack(side=TOP)

        Button(buttonFrame, text="Accept", command=acceptAuthors).pack(side=BOTTOM)
        Button(buttonFrame, text="Cancel", command=self.assignWindow.destroy).pack(side=BOTTOM)

    def newAuthor(self, func):
        def clicked():
            if empty.get() == 1:
                entry4.delete(0, "end")
                entry4.config(state='disabled')
            else:
                entry4.config(state='normal')

        def addAuthor():
            if entry1.get() == "" or entry2.get() == "" or entry3.get() == "":
                messagebox.showerror("Error", "Please fill all mandatory fields!")
                return


            confirm = messagebox.askyesno("New author", "Are you sure that you want add new author?")
            if not confirm:
                return
            try:
                self.database.addAuthor(entry1.get(), entry2.get(), entry3.get(), entry4.get())
            except Exception as e:
                messagebox.showerror("Can not delete selected records!",
                                     f"Error {e}")
                return
            self.database.connection.commit()
            window.destroy()
            func()

        window = Toplevel(self.assignWindow)
        window.title("New owner.")
        window.protocol('WM_DELETE_WINDOW', window.destroy)

        Label(window, text="Imię").grid(row=0, column=0)
        entry1 = Entry(window)
        entry1.grid(row=0, column=1)
        Label(window, text="Nazwisko").grid(row=1, column=0)
        entry2 = Entry(window)
        entry2.grid(row=1, column=1)
        Label(window, text="Data urodzenia").grid(row=2, column=0)
        entry3 = DateEntry(window, date_pattern='y-mm-dd')
        entry3.grid(row=2, column=1)
        Label(window, text="Data śmierci").grid(row=3, column=0)
        entry4 = DateEntry(window, date_pattern='y-mm-dd')
        entry4.grid(row=3, column=1)
        empty = IntVar()
        emptyButton = Checkbutton(window, text="Empty", variable=empty, command=clicked)
        emptyButton.grid(row=3, column=2)

        Button(window, text="Add", command=addAuthor).grid(row=4, column=0)
        Button(window, text="Cancel", command=window.destroy).grid(row=4, column=1)

    def assignAuthor(self, func):
        if len(self.listboxUnAssigned.curselection()) == 0:
            return
        self.assigments.append(self.listboxUnAssigned.get(self.listboxUnAssigned.curselection()))
        func()

    def unAssignAuthor(self, func):
        if len(self.listboxAssigned.curselection()) == 0:
            return
        self.assigments.remove(self.listboxAssigned.get(self.listboxAssigned.curselection()))
        func()

    def deleteAuthor(self, func):
        if len(self.listboxAssigned.curselection()) == 0 and len(self.listboxUnAssigned.curselection()) == 0:
            messagebox.showerror("Delete problem", "Please select an author to remove!")
            return
        confirm = messagebox.askyesno("Deleting", "Are you sure that you want to delete selected author?")
        if confirm:
            if len(self.listboxAssigned.curselection()) != 0:
                id = self.listboxAssigned.get(self.listboxAssigned.curselection()).split(" ")[0]
            else:
                id = self.listboxUnAssigned.get(self.listboxUnAssigned.curselection()).split(" ")[0]
            try:
                self.database.deleteAuthor(id)
            except Exception as e:
                messagebox.showerror("Can not delete selected records!",
                                     f"Error {e}")
                return
            self.database.connection.commit()
        else:
            return
        func()

    def goBack(self):
        self.addWindow.event_generate("<<back>>")

    def checkEntry(self):
        self.newRecord.clear()
        # Book title
        self.newRecord.append(self.entries[0].get())
        # Book date
        self.newRecord.append(self.entries[1].get())
        # Book genre
        self.newRecord.append(self.entries[2].get())
        # Assigments
        # ...
        if datetime.date(int(self.newRecord[1].split("-")[0]), int(self.newRecord[1].split("-")[1]),
                             int(self.newRecord[1].split("-")[2])) > date.today():
            messagebox.showerror("Wrong date", "Publishing date can not be bigger than today's date!")
            return

        if len(self.oldAssigments) == 0:
            messagebox.showerror("Error", "Book can't be withour authors!")
            return


        try:
            self.database.addBook(self.newRecord[0], self.newRecord[1], self.newRecord[2], self.oldAssigments)
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
        self.themeWindow = themeWindow
        self.database = database
        self.backEvent = backEvent
        self.data = data
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("ModifyController logger has started.")

        self.oldRecord = list()
        # Book's id
        bookId = self.database.executeStatement(f"SELECT `ksiazka_id` FROM `ksiazki` "
                                                f"WHERE `tytul` = \"{data[selectedRecord]['Tytuł']}\"")
        self.oldRecord.append(bookId[0][0])

        self.modifyWindow = Toplevel(self.themeWindow)
        self.modifyWindow.title("Add a new record to database.")
        self.modifyWindow.protocol('WM_DELETE_WINDOW', self.goBack)
        self.modifyWindow.bind("<<back>>", lambda _: self.backEvent(None))

        self.newRecord = list()

        ass = self.database.executeStatement(f"SELECT a.`imie`, a.`nazwisko`, a.`data_urodzenia`, a.`data_smierci` "
                                             f"FROM `autor_ksiazka` ak "
                                             f"JOIN `autorzy` a ON ak.`autorzy_autor_id` = a.`autor_id`"
                                             f"WHERE ak.`ksiazki_ksiazka_id` = {self.oldRecord[0]}")
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

        Label(self.colFrame, text="Tytuł", font=("Arial Bold", 12)).grid(row=0, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=0, column=1, columnspan=2)
        entry.insert(END, data[selectedRecord]['Tytuł'])
        self.entries.append(entry)

        Label(self.colFrame, text="Data opublikowania", font=("Arial Bold", 12)).grid(row=1, column=0)
        entry = DateEntry(self.colFrame, date_pattern='y-mm-dd')
        entry.grid(row=1, column=1, columnspan=2)
        entry.set_date(data[selectedRecord]['Data opublikowania'])
        self.entries.append(entry)

        Label(self.colFrame, text="Gatunek", font=("Arial Bold", 12)).grid(row=2, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=2, column=1, columnspan=2)
        entry.insert(END, data[selectedRecord]['Gatunek'])
        entry.config(state="normal")
        self.entries.append(entry)
        valueHelper = Button(self.colFrame, text="?", command=lambda _=entry: self.showHelp(_))
        valueHelper.grid(row=2, column=3)

        self.button = Button(self.colFrame, text="Assign authors", command=self.assignAuthors)
        self.button.grid(row=3, column=1)

        self.buttonFrame = Frame(self.modifyWindow, bd=4, relief=RAISED,
                                 width=self.themeWindow.winfo_width(),
                                 height=40)
        self.buttonFrame.pack(fill='both', side=TOP)
        self.modifyButton = Button(self.buttonFrame, text="Modify", command=self.checkEntry)
        self.modifyButton.pack(side=LEFT)
        self.cancelButton = Button(self.buttonFrame, text="Cancel", command=self.goBack)
        self.cancelButton.pack(side=LEFT)


    def showHelp(self, entry):
        if self.helpWindow is not None:
            return

        def select():
            atr = self.listbox.get(self.listbox.curselection())
            entry.config(state="normal")
            entry.delete("0", "end")
            entry.insert("end", atr)
            entry.config(state="readonly")
            exit()
            return

        def exit():
            self.helpWindow.destroy()
            self.helpWindow = None

        self.helpWindow = Toplevel(self.modifyWindow)
        self.helpWindow.protocol('WM_DELETE_WINDOW', exit)

        vals = list()
        temp_vals = self.database.executeStatement("SELECT `gatunek` FROM `gatunki`")
        for val1 in temp_vals:
            vals.append(f"{val1[0]}")

        self.listbox = Listbox(self.helpWindow)
        self.listbox.pack(side=TOP)
        for val in vals:
            self.listbox.insert("end", val)

        self.button = Button(self.helpWindow, text="Select", command=select, bd=4)
        self.button.pack(side=BOTTOM)

    def assignAuthors(self):

        def acceptAuthors():
            self.oldAssigments = self.assigments.copy()
            self.assignWindow.destroy()

        def refresh():
            self.vals = list()
            temp_vals = self.database.executeStatement("SELECT `autor_id`, `imie`, `nazwisko`, `data_urodzenia`, `data_smierci` "
                                                       "FROM `autorzy`")
            for val0, val1, val2, val3, val4 in temp_vals:
                author = f"{val0} {val1} {val2} {val3}"
                if val4 is not None:
                    author += f"-{val4}"
                self.vals.append(author)

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

        addButton = Button(buttonFrame, text="Add author", command=lambda: self.newAuthor(refresh))
        addButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text=" < Assign", command=lambda: self.assignAuthor(refresh))
        assignButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text=" > Unassign", command=lambda: self.unAssignAuthor(refresh))
        assignButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text="Delete author", command=lambda: self.deleteAuthor(refresh))
        assignButton.pack(side=TOP)

        Button(buttonFrame, text="Accept", command=acceptAuthors).pack(side=BOTTOM)
        Button(buttonFrame, text="Cancel", command=self.assignWindow.destroy).pack(side=BOTTOM)


    def newAuthor(self, func):
        def clicked():
            if empty.get() == 1:
                entry4.delete(0, "end")
                entry4.config(state='disabled')
            else:
                entry4.config(state='normal')

        def addAuthor():
            if entry1.get() == "" or entry2.get() == "" or entry3.get() == "":
                messagebox.showerror("Error", "Please fill all mandatory fields!")
                return

            confirm = messagebox.askyesno("New author", "Are you sure that you want add new author?")
            if not confirm:
                return
            try:
                self.database.addAuthor(entry1.get(), entry2.get(), entry3.get(), entry4.get())
            except Exception as e:
                messagebox.showerror("Can not delete selected records!",
                                     f"Error {e}")
                return
            self.database.connection.commit()
            window.destroy()
            func()

        window = Toplevel(self.assignWindow)
        window.title("New owner.")
        window.protocol('WM_DELETE_WINDOW', window.destroy)

        Label(window, text="Imię").grid(row=0, column=0)
        entry1 = Entry(window)
        entry1.grid(row=0, column=1)
        Label(window, text="Nazwisko").grid(row=1, column=0)
        entry2 = Entry(window)
        entry2.grid(row=1, column=1)
        Label(window, text="Data urodzenia").grid(row=2, column=0)
        entry3 = DateEntry(window, date_pattern='y-mm-dd')
        entry3.grid(row=2, column=1)
        Label(window, text="Data śmierci").grid(row=3, column=0)
        entry4 = DateEntry(window, date_pattern='y-mm-dd')
        entry4.grid(row=3, column=1)
        empty = IntVar()
        emptyButton = Checkbutton(window, text="Empty", variable=empty, command=clicked)
        emptyButton.grid(row=3, column=2)

        Button(window, text="Add", command=addAuthor).grid(row=4, column=0)
        Button(window, text="Cancel", command=window.destroy).grid(row=4, column=1)


    def assignAuthor(self, func):
        if len(self.listboxUnAssigned.curselection()) == 0:
            return
        self.assigments.append(self.listboxUnAssigned.get(self.listboxUnAssigned.curselection()))
        func()


    def unAssignAuthor(self, func):
        if len(self.listboxAssigned.curselection()) == 0:
            return
        self.assigments.remove(self.listboxAssigned.get(self.listboxAssigned.curselection()))
        func()

    def deleteAuthor(self, func):
        if len(self.listboxAssigned.curselection()) == 0 and len(self.listboxUnAssigned.curselection()) == 0:
            messagebox.showerror("Delete problem", "Please select an author to remove!")
            return
        confirm = messagebox.askyesno("Deleting", "Are you sure that you want to delete selected author?")
        if confirm:
            if len(self.listboxAssigned.curselection()) != 0:
                id = self.listboxAssigned.get(self.listboxAssigned.curselection()).split(" ")[0]
            else:
                id = self.listboxUnAssigned.get(self.listboxUnAssigned.curselection()).split(" ")[0]
            try:
                self.database.deleteAuthor(id)
            except Exception as e:
                messagebox.showerror("Can not delete selected records!",
                                     f"Error {e}")
                return
            self.database.connection.commit()
        else:
            return
        func()

    def goBack(self):
        self.modifyWindow.event_generate("<<back>>")

    def checkEntry(self):
        self.newRecord.clear()
        # Book title
        self.newRecord.append(self.entries[0].get())
        # Book date
        self.newRecord.append(self.entries[1].get())
        # Book genre
        self.newRecord.append(self.entries[2].get())
        # Assigments

        if datetime.date(int(self.newRecord[1].split("-")[0]), int(self.newRecord[1].split("-")[1]),
                         int(self.newRecord[1].split("-")[2])) > date.today():
            messagebox.showerror("Wrong date", "Publishing date can not be bigger than today's date!")
            return

        if len(self.oldAssigments) == 0:
            messagebox.showerror("Error", "Book can't be withour authors!")
            return

        try:
            self.database.modifyBook(self.oldRecord[0], self.entries[0].get(), self.entries[1].get(),
                                     self.entries[2].get(), self.oldAssigments)
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
