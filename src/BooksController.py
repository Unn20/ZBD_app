from tkinter import *
from tkinter import messagebox
from src.Logger import Logger
from tkinter import ttk
from tkintertable.Tables import TableCanvas
from src.CustomTable import CustomTable
from tkintertable.TableModels import TableModel
import datetime
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

        self.tableData = self.database.getBooksData()
        self.data = dict()
        self.booksModel = TableModel()
        #self.specimenModel = TableModel()

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
        self.specimenButton = Button(self.topCanvas, text="Specimens", command=self.findByAuthor, width=17)
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
            temp_vals = self.database.executeStatement("SELECT `imie`, `nazwisko`, `data_urodzenia`, `data_smierci` "
                                                       "FROM `autorzy`")
            for val1, val2, val3, val4 in temp_vals:
                author = f"{val1} {val2} {val3}"
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
            self.database.addAuthor(entry1.get(), entry2.get(), entry3.get(), entry4.get())
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
            self.database.deleteAuthor(id)
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
            temp_vals = self.database.executeStatement("SELECT `imie`, `nazwisko`, `data_urodzenia`, `data_smierci` "
                                                       "FROM `autorzy`")
            for val1, val2, val3, val4 in temp_vals:
                author = f"{val1} {val2} {val3}"
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

        Button(buttonFrame, text="Accept", command=self.acceptAuthors).pack(side=BOTTOM)
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
            self.database.addAuthor(entry1.get(), entry2.get(), entry3.get(), entry4.get())
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
            self.database.deleteAuthor(id)
            self.database.connection.commit()
        else:
            return
        func()

    def goBack(self):
        self.modifyWindow.event_generate("<<back>>")

    def checkEntry(self):
        self.newRecord.clear()
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
