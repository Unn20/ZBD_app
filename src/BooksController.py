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
        self.modifyWindow2 = None
        self.modifyWindow3 = None
        self.table = None
        self.table2 = None
        self.table3 = None

        self.rackHelpWindow = None
        self.departmentHelpWindow = None
        self.findWindow = None
        self.authorsWindow = None
        self.specimenWindow = None
        self.addSpecimenWindow = None
        self.newDepartmentWindow = None

        #self.tableData = None
        self.data = dict()
        self.data2 = dict()
        self.data3 = dict()
        self.currentModel = TableModel()
        self.currentModel2 = TableModel()
        self.currentModel3 = TableModel()

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
        self.tabControl.add(self.tab1, text="Książki")
        self.tab2 = Frame(self.tabControl)
        self.tabControl.add(self.tab2, text="Autorzy")
        self.tab3 = Frame(self.tabControl)
        self.tabControl.add(self.tab3, text="Gatunki")

        self.tabControl.pack(expand=1, fill='both')

        ### BOOKS
        # Canvas with options menu
        self.topCanvas = Canvas(self.tab1, bg="white", bd=1, relief=RAISED,
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
        self.middleFrame = Frame(self.tab1)
        self.middleFrame.pack(fill='both', side=TOP)
        self.table = CustomTable(self.middleFrame, model=self.currentModel)
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

        ### AUTHORS
        self.topCanvas2 = Canvas(self.tab2, bg="#B7B9B8", bd=1, relief=RAISED,
                                width=int(self.content.winfo_width()),
                                height=int(self.content.winfo_height() / 12))
        self.topCanvas2.pack(fill='both', side=TOP)

        self.backButton2 = Button(self.topCanvas2, text=" < ", command=self.back, width=6)
        self.backButton2.pack(fill='both', side=LEFT)
        self.refreshButton2 = Button(self.topCanvas2, text="Refresh table", command=self.refreshTable, width=17)
        self.refreshButton2.pack(fill='both', side=LEFT)
        self.bookButton2 = Button(self.topCanvas2, text="Books", command=self.checkBooksByAuthor, width=17)
        self.bookButton2.pack(fill='both', side=LEFT)
        self.findButton2 = Button(self.topCanvas2, text="Find by book", command=self.findByBook, width=17)
        self.findButton2.pack(fill='both', side=LEFT)


        # Canvas with data
        self.middleFrame2 = Frame(self.tab2)
        self.middleFrame2.pack(fill='both', side=TOP)
        self.table2 = CustomTable(self.middleFrame2, model=self.currentModel2)
        self.table2.show()

        # Canvas with DML buttons
        self.bottomCanvas2 = Canvas(self.tab2, bg="#B7B9B8", bd=1, relief=FLAT,
                                   width=int(self.content.winfo_width()),
                                   height=int(self.content.winfo_height() / 5))
        self.bottomCanvas2.pack(fill='both', side=TOP)

        self.buttonModify2 = Button(self.bottomCanvas2, text=" MODIFY ", command=self.modify2, width=25, height=3, bd=5)
        self.buttonModify2.pack(side=LEFT)
        self.buttonDelete2 = Button(self.bottomCanvas2, text=" DELETE ",
                                   command=lambda: self.delete2(), width=25, height=3, bd=5)
        self.buttonDelete2.pack(side=LEFT)


        ### GENRES
        self.topCanvas3 = Canvas(self.tab3, bg="#B7B9B8", bd=1, relief=RAISED,
                                 width=int(self.content.winfo_width()),
                                 height=int(self.content.winfo_height() / 12))
        self.topCanvas3.pack(fill='both', side=TOP)

        self.backButton3 = Button(self.topCanvas3, text=" < ", command=self.back, width=6)
        self.backButton3.pack(fill='both', side=LEFT)
        self.refreshButton3 = Button(self.topCanvas3, text="Refresh table", command=self.refreshTable, width=17)
        self.refreshButton3.pack(fill='both', side=LEFT)
        self.findButton3 = Button(self.topCanvas3, text="Books", command=self.checkBooksByGenre, width=17)
        self.findButton3.pack(fill='both', side=LEFT)

        # Canvas with data
        self.middleFrame3 = Frame(self.tab3)
        self.middleFrame3.pack(fill='both', side=TOP)
        self.table3 = CustomTable(self.middleFrame3, model=self.currentModel3)
        self.table3.show()

        # Canvas with DML buttons
        self.bottomCanvas3 = Canvas(self.tab3, bg="#B7B9B8", bd=1, relief=FLAT,
                                    width=int(self.content.winfo_width()),
                                    height=int(self.content.winfo_height() / 5))
        self.bottomCanvas3.pack(fill='both', side=TOP)

        self.buttonModify3 = Button(self.bottomCanvas3, text=" MODIFY ", command=self.modify3, width=25, height=3, bd=5)
        self.buttonModify3.pack(side=LEFT)

    def bookSpecimens(self):
        if self.specimenWindow is not None:
            self.themeWindow.focus_set()
            return

        def exit_function():
            self.specimenWindow.destroy()
            self.specimenWindow = None
            self.addSpecimenWindow = None
            self.departmentHelpWindow = None
            self.rackHelpWindow = None
            self.newDepartmentWindow = None
            self.themeWindow.focus_set()

        if self.table.startrow != self.table.endrow:
            messagebox.showwarning('Specimens', 'Please select only one record!')
            self.themeWindow.focus_set()
            return
        self.specimenData = dict()
        def refresh():
            specimens = self.database.getSpecimensByBookId(self.bookId)
            if len(specimens) == 0:
                return
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
        self.specimenWindow.protocol('WM_DELETE_WINDOW', exit_function)

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
        Button(buttonFrame, text="Cancel", command=exit_function).pack(side=LEFT)

    def addSpecimen(self, func):
        if self.addSpecimenWindow is not None:
            self.specimenWindow.focus_set()
            return
        def exit_function():
            self.addSpecimenWindow.destroy()
            self.addSpecimenWindow = None
            self.departmentHelpWindow = None
            self.rackHelpWindow = None
            self.newDepartmentWindow = None
            self.specimenWindow.focus_set()

        def checkSpecimenEntry():
            if entry1.get() == "" or entry2.get() == "":
                messagebox.showerror("Error", "Fill all mandatory fields!")
                self.addSpecimenWindow.focus_set()
                return

            tmp_racks = self.database.executeStatement(f"SELECT `numer` FROM `regaly` "
                                                       f"WHERE `dzial_nazwa` = \"{entry1.get()}\"")
            racks = list()
            for r in tmp_racks:
                racks.append(str(r[0]))

            tmp_sections = self.database.executeStatement(f"SELECT `nazwa` FROM `dzialy` ")
            sections = list()
            for s in tmp_sections:
                sections.append(str(s[0]))

            if entry1.get() not in sections:
                messagebox.showerror("Error", "If you want to create new Section press New button.")
                self.addSpecimenWindow.focus_set()
                return
            else:
                if entry2.get() in racks:
                    confirm = messagebox.askyesno("Add", "You want to add new specimen?")
                    if confirm:
                        try:
                            self.database.addSpecimen(self.bookId, entry2.get())
                        except Exception as e:
                            messagebox.showerror("Can not delete selected records!",
                                                 f"Error {e}")
                            self.addSpecimenWindow.focus_set()
                            return
                        self.database.connection.commit()
                        func()
                    else:
                        self.addSpecimenWindow.focus_set()
                        return
                else:
                    confirm = messagebox.askyesno("Add", "Given rack doesn't exists. Would You like to create a new rack?")
                    if confirm:
                        try:
                            self.newRack(entry2.get(), 100, entry1.get())
                        except Exception as e:
                            messagebox.showerror("Can not delete selected records!",
                                                 f"Error {e}")
                            self.addSpecimenWindow.focus_set()
                            return
                        try:
                            self.database.addSpecimen(self.bookId, entry2.get())
                        except Exception as e:
                            messagebox.showerror("Can not delete selected records!",
                                                 f"Error {e}")
                            self.addSpecimenWindow.focus_set()
                            return
                        self.database.connection.commit()
                        self.addSpecimenWindow.destroy()
                        self.addSpecimenWindow = None
                        func()
                    else:
                        self.addSpecimenWindow.focus_set()
                        return

        window = Toplevel(self.specimenWindow)
        self.addSpecimenWindow = window
        window.title(f"New specimen")
        window.protocol('WM_DELETE_WINDOW', exit_function)

        Label(window, text="Dział").grid(row=0, column=0)
        entry1 = Entry(window)
        entry1.grid(row=0, column=1, columnspan=2)
        entry1.config(state="normal")
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
        Button(window, text="Cancel", command=exit_function).grid(row=2, column=1)

    def newRack(self, no, capability, dep):
        if not re.match('^[0-9]+$', no):
            raise Exception("Rack number need to be an intiger")
            return
        self.database.executeStatement(f"INSERT INTO `regaly` "
                                       f"VALUES (\'{no}\', \'{capability}\', \'{0}\', \"{dep}\")")
        self.database.connection.commit()


    def newDepartment(self, entry):
        if self.newDepartmentWindow is not None:
            self.addSpecimenWindow.focus_set()
            return
        def exit_function():
            self.newDepartmentWindow.destroy()
            self.newDepartmentWindow = None
            self.addSpecimenWindow.focus_set()

        def addDep():
            if entry1.get() == "" or entry2.get() == "":
                messagebox.showerror("Error", "Fill all mandatory fields!")
                self.newDepartmentWindow
                return
            confirm = messagebox.askyesno("Add", "You want to add new department?")
            if confirm:
                try:
                    self.database.addDepartment(entry1.get(), entry2.get())
                except Exception as e:
                    messagebox.showerror("Can not delete selected records!",
                                         f"Error {e}")
                    self.newDepartmentWindow
                    return
                self.database.connection.commit()
                self.newDepartmentWindow.destroy()
                self.newDepartmentWindow = None
                #entry.set(entry1.get())
            else:
                self.newDepartmentWindow
                return

        window = Toplevel(self.addSpecimenWindow)
        self.newDepartmentWindow = window
        window.title(f"New department")
        window.protocol('WM_DELETE_WINDOW', exit_function)

        Label(window, text="Nazwa", font=("Arial Bold", 12)).grid(row=0, column=0)
        entry1 = Entry(window, width=20)
        entry1.grid(row=0, column=1, columnspan=2)

        Label(window, text="Lokalizacja", font=("Arial Bold", 12)).grid(row=1, column=0)
        entry2 = Entry(window, width=20)
        entry2.grid(row=1, column=1, columnspan=2)

        Button(window, text="Add", command=addDep).grid(row=2, column=0)
        Button(window, text="Cancel", command=exit_function).grid(row=2, column=1)


    def showRackHelp(self, entry, depEntry):
        if self.rackHelpWindow is not None:
            self.addSpecimenWindow.focus_set()
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
            self.addSpecimenWindow.focus_set()

        self.rackHelpWindow = Toplevel(self.addSpecimenWindow)
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
            self.addSpecimenWindow.focus_set()
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
            self.addSpecimenWindow.focus_set()

        self.departmentHelpWindow = Toplevel(self.addSpecimenWindow)
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
            id = self.specimenData[recName]["Egzemplarz ID"]
            try:
                self.database.deleteSpecimen(self.specimenData[recName]["Egzemplarz ID"])
            except Exception as e:
                self.logger.error(f"Can not delete selected records! Error = {e}")
                errorNo = int(e.__str__().split()[0][1:-1])
                if errorNo == 1451:
                    confirm = messagebox.askyesno("Add",
                                                  "Possible data loss. Are you sure?")
                    if confirm:
                        self.database.executeStatement(f"DELETE FROM `historia_operacji` WHERE"
                                                       f"`egzemplarz_id` = \'{id}\'")
                        self.database.executeStatement(f"DELETE FROM `egzemplarze` WHERE"
                                                       f"`egzemplarz_id` = \'{id}\'")
                    else:
                        self.specimenWindow.focus_set()
                        return
                else:
                    messagebox.showerror("Can not delete selected records!",
                                         f"Error {e}")
                self.specimenWindow.focus_set()
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
        if self.findWindow is not None:
            self.themeWindow.focus_set()
            return
        def exit_function():
            self.findWindow.destroy()
            self.findWindow = None
            self.themeWindow.focus_set()
        self.findWindow = Toplevel(self.themeWindow)
        self.findWindow.title("Search book by author's personal data.")
        self.findWindow.protocol('WM_DELETE_WINDOW', exit_function)

        vals = list()
        temp_vals = self.database.executeStatement("SELECT * FROM `autorzy` "
                                                   "ORDER BY `nazwisko`, `imie`")
        for val1, val2, val3, val4, val5 in temp_vals:
            author = f"{val2} {val3} {val4}"
            if val5 is not None:
                author += f"-{val5}"
            vals.append(author)

        self.listbox = Listbox(self.findWindow, width=50)
        self.listbox.pack(side=TOP)

        for val in vals:
            self.listbox.insert("end", val)

        self.button = Button(self.findWindow, text="Select",
                             command=lambda: self.refreshTableWithAuthor(
                                 self.listbox.get(self.listbox.curselection()).split(" ")[0],
                                 self.listbox.get(self.listbox.curselection()).split(" ")[1]))
        self.button.pack(side=TOP)

    def findByBook(self):
        if self.findWindow is not None:
            self.themeWindow.focus_set()
            return
        def exit_function():
            self.findWindow.destroy()
            self.findWindow = None
            self.themeWindow.focus_set()
        self.findWindow = Toplevel(self.themeWindow)
        self.findWindow.title("Search authors by book.")
        self.findWindow.protocol('WM_DELETE_WINDOW', exit_function)

        vals = list()
        temp_vals = self.database.executeStatement("SELECT `tytul`, `data_opublikowania`, `gatunek` "
                                                   "FROM `ksiazki` "
                                                   "ORDER BY `tytul`")
        for val1, val2, val3 in temp_vals:
            book = f"{val1}"# {val2} {val3}"
            vals.append(book)

        self.listbox = Listbox(self.findWindow, width=50)
        self.listbox.pack(side=TOP)

        for val in vals:
            self.listbox.insert("end", val)

        self.button = Button(self.findWindow, text="Select",
                             command=lambda: self.refreshTableWithBook(
                                 self.listbox.get(self.listbox.curselection()).split(" ")[0]))
        self.button.pack(side=TOP)

    def refreshTableWithAuthor(self, authorName, authorSurname):
        authorId = self.database.executeStatement("SELECT `autor_id` FROM `autorzy` "
                                                  f"WHERE `imie` = \'{authorName}\' "
                                                  f"AND `nazwisko` = \'{authorSurname}\'")
        self.currentModel.createEmptyModel()
        try:
            self.tableData = self.database.getBooksDataByAuthor(authorId[0][0])
        except Exception as e:
            messagebox.showerror("Error", e)


        self.data = dict()
        if self.tableData != None:
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
        self.findWindow = None

    def refreshTableWithBook(self, book):
        bookId = self.database.executeStatement("SELECT `ksiazka_id` FROM `ksiazki` "
                                                f"WHERE `tytul` = \"{book}\"")
        try:
            self.tableData = self.database.getAuthorsData(bookId[0][0])
        except Exception as e:
            messagebox.showerror("Error", e)

        self.currentModel2.createEmptyModel()
        self.data2 = dict()
        for no, key in enumerate(self.tableData.keys()):
            self.data2[f"rec {no + 1}"] = dict()
            self.data2[f"rec {no + 1}"]["Imię"] = self.tableData[key]["imie"]
            self.data2[f"rec {no + 1}"]["Nazwisko"] = self.tableData[key]["nazwisko"]
            self.data2[f"rec {no + 1}"]["Data urodzenia"] = str(self.tableData[key]["data_urodzenia"])
            if self.tableData[key]["data_smierci"] is None:
                self.data2[f"rec {no + 1}"]["Data śmierci"] = ""
            else:
                self.data2[f"rec {no + 1}"]["Data śmierci"] = str(self.tableData[key]["data_smierci"])
            self.data2[f"rec {no + 1}"]["Liczba książek"] = str(self.tableData[key]["liczba_ksiazek"])
        self.currentModel2.importDict(self.data2)
        if self.table2 is not None:
            self.table2.redraw()
        self.findWindow.destroy()
        self.findWindow = None

    def checkAuthors(self):
        if self.table.startrow != self.table.endrow:
            messagebox.showwarning('Authors', 'Please select only one record!')
            self.themeWindow.focus_set()
            return
        if self.authorsWindow is not None:
            self.themeWindow.focus_set()
            return

        def exit_function():
            self.authorsWindow.destroy()
            self.authorsWindow = None
            self.themeWindow.focus_set()
        recName = self.currentModel.getRecName(self.table.currentrow)
        self.authorsWindow = Toplevel(self.themeWindow)
        self.authorsWindow.title(f"Authors of book {self.data[recName]['Tytuł']}")
        self.authorsWindow.protocol('WM_DELETE_WINDOW', exit_function)

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

        Button(self.authorsWindow, text="Close", command=exit_function).pack(side=TOP)

    def checkBooksByAuthor(self):
        if self.table2.startrow != self.table2.endrow:
            messagebox.showwarning('Books', 'Please select only one record!')
            self.themeWindow.focus_set()
            return
        if self.authorsWindow is not None:
            self.themeWindow.focus_set()
            return
        def exit_function():
            self.authorsWindow.destroy()
            self.authorsWindow = None
            self.themeWindow.focus_set()
        recName = self.currentModel.getRecName(self.table2.currentrow)

        self.authorsWindow = Toplevel(self.themeWindow)
        self.authorsWindow.title(f"Books of author {self.data2[recName]['Imię']} {self.data2[recName]['Nazwisko']}")
        self.authorsWindow.protocol('WM_DELETE_WINDOW', exit_function)

        Label(self.authorsWindow, text=f"Books of author {self.data2[recName]['Imię']} "
                                       f"{self.data2[recName]['Nazwisko']}").pack(side=TOP)

        authorId = self.database.executeStatement(f"SELECT `autor_id` FROM `autorzy` "
                                                f"WHERE `imie` = \"{self.data2[recName]['Imię']}\" "
                                                  f"AND `nazwisko` = \"{self.data2[recName]['Nazwisko']}\"")

        books = self.database.executeStatement(f"SELECT k.`tytul`, k.`data_opublikowania`, k.`gatunek`, "
                                               f"COUNT(*) AS `liczba_ksiazek` "
                                                f"FROM `ksiazki` k "
                                               f"LEFT JOIN `egzemplarze` e ON k.`ksiazka_id` = e.`ksiazka_id` "
                                                f"JOIN `autor_ksiazka` ak ON k.`ksiazka_id` = ak.`ksiazki_ksiazka_id` "
                                                f"WHERE ak.`autorzy_autor_id` = \"{authorId[0][0]}\" "
                                               f"GROUP BY k.`tytul`")

        booksModel = TableModel()
        booksModel.createEmptyModel()
        booksData = dict()
        for no, book in enumerate(books):
            booksData[f"rec {no+1}"] = dict()
            booksData[f"rec {no + 1}"]["Tytuł"] = book[0]
            booksData[f"rec {no + 1}"]["Data opublikowania"] = str(book[1])
            booksData[f"rec {no + 1}"]["Gatunek"] = book[2]
            booksData[f"rec {no + 1}"]["Liczba egzemplarzy"] = book[3]

        booksModel.importDict(booksData)
        booksFrame = Frame(self.authorsWindow)
        booksFrame.pack(fill='both', side=TOP)
        booksTable = CustomTable(booksFrame, model=booksModel)
        booksTable.show()

        Button(self.authorsWindow, text="Close", command=exit_function).pack(side=TOP)

    def checkBooksByGenre(self):
        if self.table3.startrow != self.table3.endrow:
            messagebox.showwarning('Books', 'Please select only one record!')
            self.themeWindow.focus_set()
            return
        if self.authorsWindow is not None:
            self.themeWindow.focus_set()
            return
        def exit_function():
            self.authorsWindow.destroy()
            self.authorsWindow = None
            self.themeWindow.focus_set()
        recName = self.currentModel.getRecName(self.table3.currentrow)

        self.authorsWindow = Toplevel(self.themeWindow)
        self.authorsWindow.title(f"Books by genre {self.data3[recName]['Gatunek']}")
        self.authorsWindow.protocol('WM_DELETE_WINDOW', exit_function)

        Label(self.authorsWindow, text=f"Books by genre {self.data3[recName]['Gatunek']}").pack(side=TOP)

        books = self.database.executeStatement(f"SELECT k.`tytul`, k.`data_opublikowania`, k.`gatunek`, "
                                               f"COUNT(egzemplarz_id) AS `liczba_ksiazek` "
                                                f"FROM `ksiazki` k "
                                               f"LEFT JOIN `egzemplarze` e ON k.`ksiazka_id` = e.`ksiazka_id` "
                                                f"WHERE k.`gatunek` = \"{self.data3[recName]['Gatunek']}\" "
                                               f"GROUP BY k.`tytul` ")

        booksModel = TableModel()
        booksModel.createEmptyModel()
        booksData = dict()
        for no, book in enumerate(books):
            booksData[f"rec {no+1}"] = dict()
            booksData[f"rec {no + 1}"]["Tytuł"] = book[0]
            booksData[f"rec {no + 1}"]["Data opublikowania"] = str(book[1])
            booksData[f"rec {no + 1}"]["Gatunek"] = book[2]
            booksData[f"rec {no + 1}"]["Liczba egzemplarzy"] = book[3]

        booksModel.importDict(booksData)
        booksFrame = Frame(self.authorsWindow)
        booksFrame.pack(fill='both', side=TOP)
        booksTable = CustomTable(booksFrame, model=booksModel)
        booksTable.show()

        Button(self.authorsWindow, text="Close", command=exit_function).pack(side=TOP)

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
        if self.modifyWindow3 is not None:
            self.modifyWindow3.modifyWindow.destroy()
            self.modifyWindow3 = None
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
                                                     self.currentModel.getRecName(selectedRow),
                                                     self.data, self.backEvent)

    def modify2(self):
        """ Go to modify window """
        if self.table2.startrow != self.table2.endrow:
            messagebox.showwarning('Modify error', 'Please select only one record!')
            self.themeWindow.focus_set()
        else:
            selectedRow = self.table2.currentrow
            if self.modifyWindow2 is None:
                self.logger.debug("Starting modify window.")
                self.modifyWindow2 = ModifyController2(self.themeWindow, self.database,
                                                     self.currentModel2.getRecName(selectedRow),
                                                     self.data2, self.backEvent)

    def modify3(self):
        """ Go to modify window """
        if self.table3.startrow != self.table3.endrow:
            messagebox.showwarning('Modify error', 'Please select only one record!')
            self.themeWindow.focus_set()
        else:
            selectedRow = self.table3.currentrow
            if self.modifyWindow3 is None:
                self.logger.debug("Starting modify window.")
                self.modifyWindow3 = ModifyController3(self.themeWindow, self.database,
                                                     self.currentModel3.getRecName(selectedRow),
                                                     self.data3, self.backEvent)

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
        pass
        """ Delete selected records """
        for no, i in enumerate(self.table2.multiplerowlist):
            recName = self.currentModel2.getRecName(i)

            id = self.database.executeStatement(f"SELECT `autor_id` FROM `autorzy` "
                                                f"WHERE `imie` = \"{self.data2[recName]['Imię']}\" "
                                                f"AND `nazwisko` = \"{self.data2[recName]['Nazwisko']}\"")
            try:
                self.database.deleteAuthorRecord(id[0][0])
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

        self.currentModel2.createEmptyModel()
        self.tableData = self.database.getAuthorsData()
        self.data2 = dict()
        for no, key in enumerate(self.tableData.keys()):
            self.data2[f"rec {no + 1}"] = dict()
            self.data2[f"rec {no + 1}"]["Imię"] = self.tableData[key]["imie"]
            self.data2[f"rec {no + 1}"]["Nazwisko"] = self.tableData[key]["nazwisko"]
            self.data2[f"rec {no + 1}"]["Data urodzenia"] = str(self.tableData[key]["data_urodzenia"])
            if self.tableData[key]["data_smierci"] is None:
                self.data2[f"rec {no + 1}"]["Data śmierci"] = ""
            else:
                self.data2[f"rec {no + 1}"]["Data śmierci"] = str(self.tableData[key]["data_smierci"])
            self.data2[f"rec {no + 1}"]["Liczba książek"] = str(self.tableData[key]["liczba_ksiazek"])

        self.currentModel2.importDict(self.data2)
        if self.table2 is not None:
            self.table2.redraw()

        self.currentModel3.createEmptyModel()
        self.tableData = self.database.getGenresData()
        self.data3 = dict()
        for no, key in enumerate(self.tableData.keys()):
            self.data3[f"rec {no + 1}"] = dict()
            self.data3[f"rec {no + 1}"]["Gatunek"] = self.tableData[key]["nazwa"]
            self.data3[f"rec {no + 1}"]["Liczność"] = self.tableData[key]["liczba"]

        self.currentModel3.importDict(self.data3)
        if self.table3 is not None:
            self.table3.redraw()

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
        self.assignWindow = None
        self.newAuthorWindow = None

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
            self.addWindow.focus_set()
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
            self.addWindow.focus_set()

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
        if self.assignWindow is not None:
            self.addWindow.focus_set()
            return

        def acceptAuthors():
            self.oldAssigments = self.assigments.copy()
            self.assignWindow.destroy()
            self.assignWindow = None
            self.newAuthorWindow = None
            self.addWindow.focus_set()

        def exit_function():
            self.assignWindow.destroy()
            self.assignWindow = None
            self.newAuthorWindow = None
            self.addWindow.focus_set()

        def refresh():
            self.vals = list()
            temp_vals = self.database.executeStatement("SELECT `autor_id`, `imie`, `nazwisko`, `data_urodzenia`, `data_smierci` "
                                                       "FROM `autorzy`")
            for val0, val1, val2, val3, val4 in temp_vals:
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

        addButton = Button(buttonFrame, text="Add author", command=lambda: self.newAuthor(refresh))
        addButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text=" < Assign", command=lambda: self.assignAuthor(refresh))
        assignButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text=" > Unassign", command=lambda: self.unAssignAuthor(refresh))
        assignButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text="Delete author", command=lambda: self.deleteAuthor(refresh))
        assignButton.pack(side=TOP)

        Button(buttonFrame, text="Accept", command=acceptAuthors).pack(side=BOTTOM)
        Button(buttonFrame, text="Cancel", command=exit_function).pack(side=BOTTOM)

    def newAuthor(self, func):
        if self.newAuthorWindow is not None:
            self.assignWindow.focus_set()
            return
        def exit_function():
            self.newAuthorWindow.destroy()
            self.newAuthorWindow = None
            self.assignWindow.focus_set()
        def clicked():
            if empty.get() == 1:
                entry4.delete(0, "end")
                entry4.config(state='disabled')
            else:
                entry4.config(state='normal')

        def addAuthor():
            if entry1.get() == "" or entry2.get() == "" or entry3.get() == "":
                messagebox.showerror("Error", "Please fill all mandatory fields!")
                self.newAuthorWindow.focus_set()
                return


            confirm = messagebox.askyesno("New author", "Are you sure that you want add new author?")
            if not confirm:
                self.newAuthorWindow.focus_set()
                return
            try:
                self.database.addAuthor(entry1.get(), entry2.get(), entry3.get(), entry4.get())
            except Exception as e:
                messagebox.showerror("Can not add selected record!",
                                     f"Error {e}")
                self.newAuthorWindow.focus_set()
                return
            self.database.connection.commit()
            window.destroy()
            func()

        window = Toplevel(self.assignWindow)
        self.newAuthorWindow = window
        window.title("New owner.")
        window.protocol('WM_DELETE_WINDOW', exit_function)

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
        Button(window, text="Cancel", command=exit_function).grid(row=4, column=1)

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
            self.assignWindow.focus_set()
            return
        confirm = messagebox.askyesno("Deleting", "Possible data loss. Are you sure?")
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
                self.assignWindow.focus_set()
                return
            self.database.connection.commit()
        else:
            return
        self.assignWindow.focus_set()
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

        if self.newRecord[1] in ('', 'NULL', None):
            messagebox.showerror("Wrong date.", "You need to set date.")
            self.addWindow.focus_set()
            return

        if str(self.newRecord[1].split("-")[1]) == '02' and int(self.newRecord[1].split("-")[2]) > 29:
            messagebox.showerror("Wrong date", "This date dosn't exists.")
            self.addWindow.focus_set()
            return

        if int(self.newRecord[1].split("-")[2]) > 31:
            messagebox.showerror("Wrong date", "This date dosn't exists.")
            self.addWindow.focus_set()
            return

        if str(self.newRecord[1].split("-")[1]) not in ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'):
            messagebox.showerror("Wrong date", "This date dosn't exists.")
            self.addWindow.focus_set()
            return

        if datetime.date(int(self.newRecord[1].split("-")[0]), int(self.newRecord[1].split("-")[1]),
                             int(self.newRecord[1].split("-")[2])) > date.today():
            messagebox.showerror("Wrong date", "Publishing date can not be bigger than today's date!")
            self.addWindow.focus_set()
            return

        if len(self.oldAssigments) == 0:
            messagebox.showerror("Error", "Book can't be withour authors!")
            self.addWindow.focus_set()
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
        self.themeWindow = themeWindow
        self.database = database
        self.backEvent = backEvent
        self.data = data
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("ModifyController logger has started.")

        self.assignWindow = None
        self.newAuthorWindow = None

        self.oldRecord = list()
        # Book's id
        bookId = self.database.executeStatement(f"SELECT `ksiazka_id` FROM `ksiazki` "
                                                f"WHERE `tytul` = \"{data[selectedRecord]['Tytuł']}\"")
        self.oldRecord.append(bookId[0][0])

        self.modifyWindow = Toplevel(self.themeWindow)
        self.modifyWindow.title("Modify record in database.")
        self.modifyWindow.protocol('WM_DELETE_WINDOW', self.goBack)
        self.modifyWindow.bind("<<back>>", lambda _: self.backEvent(None))

        self.newRecord = list()

        ass = self.database.executeStatement(f"SELECT a.`imie`, a.`nazwisko`, a.`data_urodzenia`, a.`data_smierci` "
                                             f"FROM `autor_ksiazka` ak "
                                             f"JOIN `autorzy` a ON ak.`autorzy_autor_id` = a.`autor_id`"
                                             f"WHERE ak.`ksiazki_ksiazka_id` = {self.oldRecord[0]}")

        self.oldAssigments = list()
        for val1, val2, val3, val4 in ass:
            id = self.database.executeStatement(f"SELECT `autor_id` FROM `autorzy` WHERE `imie` = \'{val1}\' AND `nazwisko` = \'{val2}\' AND `data_urodzenia` = \'{val3}\'")[0][0]
            owner = f"{val1}"
            if val2 is not None:
                owner += f" {val2}"
            if val3 is not None:
                owner += f" {val3}"
            if val4 is not None:
                owner += f"-{val4}"
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
            self.modifyWindow.focus_set()
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
            self.modifyWindow.focus_set()

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
        if self.assignWindow is not None:
            self.modifyWindow.focus_set()
            return

        def acceptAuthors():
            self.oldAssigments = self.assigments.copy()
            self.assignWindow.destroy()
            self.assignWindow = None
            self.newAuthorWindow = None
            self.modifyWindow.focus_set()

        def exit_function():
            self.assignWindow.destroy()
            self.assignWindow = None
            self.newAuthorWindow = None
            self.modifyWindow.focus_set()

        def refresh():
            self.vals = list()
            temp_vals = self.database.executeStatement("SELECT `autor_id`, `imie`, `nazwisko`, `data_urodzenia`, `data_smierci` "
                                                       "FROM `autorzy`")
            for val0, val1, val2, val3, val4 in temp_vals:
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

        addButton = Button(buttonFrame, text="Add author", command=lambda: self.newAuthor(refresh))
        addButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text=" < Assign", command=lambda: self.assignAuthor(refresh))
        assignButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text=" > Unassign", command=lambda: self.unAssignAuthor(refresh))
        assignButton.pack(side=TOP)
        assignButton = Button(buttonFrame, text="Delete author", command=lambda: self.deleteAuthor(refresh))
        assignButton.pack(side=TOP)

        Button(buttonFrame, text="Accept", command=acceptAuthors).pack(side=BOTTOM)
        Button(buttonFrame, text="Cancel", command=exit_function).pack(side=BOTTOM)


    def newAuthor(self, func):
        if self.newAuthorWindow is not None:
            self.assignWindow.focus_set()
            return
        def exit_function():
            self.newAuthorWindow.destroy()
            self.newAuthorWindow = None
            self.assignWindow.focus_set()

        def clicked():
            if empty.get() == 0:
                entry4.delete(0, "end")
                entry4.config(state='disabled')
            else:
                entry4.config(state='normal')

        def addAuthor():
            if entry1.get() == "" or entry2.get() == "" or entry3.get() == "":
                messagebox.showerror("Error", "Please fill all mandatory fields!")
                self.newAuthorWindow.focus_set()
                return

            confirm = messagebox.askyesno("New author", "Are you sure that you want add new author?")
            if not confirm:
                self.newAuthorWindow.focus_set()
                return
            try:
                self.database.addAuthor(entry1.get(), entry2.get(), entry3.get(), entry4.get())
            except Exception as e:
                messagebox.showerror("Can not delete selected records!",
                                     f"Error {e}")
                self.newAuthorWindow.focus_set()
                return
            self.database.connection.commit()
            window.destroy()
            func()

        window = Toplevel(self.assignWindow)
        self.newAuthorWindow = window
        window.title("New owner.")
        window.protocol('WM_DELETE_WINDOW', exit_function)

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
        emptyButton = Checkbutton(window, text="Zmarł", variable=empty, command=clicked)
        emptyButton.grid(row=3, column=2)
        entry4.delete(0, "end")
        entry4.config(state='disabled')

        Button(window, text="Add", command=addAuthor).grid(row=4, column=0)
        Button(window, text="Cancel", command=exit_function).grid(row=4, column=1)


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
            self.assignWindow.focus_set()
            return
        confirm = messagebox.askyesno("Deleting", "Possible data loss. Are you sure?")
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
        self.assignWindow.focus_set()
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

        if self.newRecord[1] in ('', 'NULL', None):
            messagebox.showerror("Wrong date.", "You need to set date.")
            self.modifyWindow.focus_set()
            return

        if str(self.newRecord[1].split("-")[1]) == '02' and int(self.newRecord[1].split("-")[2]) > 29:
            messagebox.showerror("Wrong date", "This date dosn't exists.")
            self.modifyWindow.focus_set()
            return

        if int(self.newRecord[1].split("-")[2]) > 31:
            messagebox.showerror("Wrong date", "This date dosn't exists.")
            self.modifyWindow.focus_set()
            return

        if str(self.newRecord[1].split("-")[1]) not in ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'):
            messagebox.showerror("Wrong date", "This date dosn't exists.")
            self.modifyWindow.focus_set()
            return

        if datetime.date(int(self.newRecord[1].split("-")[0]), int(self.newRecord[1].split("-")[1]),
                         int(self.newRecord[1].split("-")[2])) > date.today():
            messagebox.showerror("Wrong date", "Publishing date can not be bigger than today's date!")
            self.modifyWindow.focus_set()
            return

        if len(self.oldAssigments) == 0:
            messagebox.showerror("Error", "Book can't be withour authors!")
            self.modifyWindow.focus_set()
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


class ModifyController2:
    def __init__(self, themeWindow, database, selectedRecord, data, backEvent):
        self.themeWindow = themeWindow
        self.database = database
        self.backEvent = backEvent
        self.data = data
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("ModifyController2 logger has started.")

        self.oldRecord = list()
        # Book's id
        authorId = self.database.executeStatement(f"SELECT `autor_id` FROM `autorzy` "
                                                  f"WHERE `imie` = \"{data[selectedRecord]['Imię']}\" "
                                                  f"AND `nazwisko` = \"{data[selectedRecord]['Nazwisko']}\"")
        self.oldRecord.append(authorId[0][0])

        self.modifyWindow = Toplevel(self.themeWindow)
        self.modifyWindow.title("Modify record in database.")
        self.modifyWindow.protocol('WM_DELETE_WINDOW', self.goBack)
        self.modifyWindow.bind("<<back>>", lambda _: self.backEvent(None))

        self.newRecord = list()

        self.helpWindow = None

        self.colFrame = Frame(self.modifyWindow, bd=4, relief=RAISED,
                              width=self.themeWindow.winfo_width(),
                              height=self.themeWindow.winfo_height() - 40)
        self.colFrame.pack(fill='both', side=TOP)

        self.entries = list()

        def clicked():
            if empty.get() == 0:
                self.entries[-1].delete(0, "end")
                self.entries[-1].config(state='disabled')
            else:
                self.entries[-1].config(state='normal')

        Label(self.colFrame, text="Imię", font=("Arial Bold", 12)).grid(row=0, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=0, column=1, columnspan=2)
        entry.insert(END, data[selectedRecord]['Imię'])
        self.entries.append(entry)

        Label(self.colFrame, text="Nazwisko", font=("Arial Bold", 12)).grid(row=1, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=1, column=1, columnspan=2)
        entry.insert(END, data[selectedRecord]['Nazwisko'])
        self.entries.append(entry)

        Label(self.colFrame, text="Data urodzenia", font=("Arial Bold", 12)).grid(row=2, column=0)
        entry = DateEntry(self.colFrame, date_pattern='y-mm-dd')
        entry.grid(row=2, column=1, columnspan=2)
        entry.set_date(data[selectedRecord]['Data urodzenia'])
        self.entries.append(entry)

        empty = IntVar()
        Label(self.colFrame, text="Data śmierci", font=("Arial Bold", 12)).grid(row=3, column=0)
        entry = DateEntry(self.colFrame, date_pattern='y-mm-dd')
        entry.grid(row=3, column=1, columnspan=2)
        if data[selectedRecord]['Data śmierci'] != "":
            entry.set_date(data[selectedRecord]['Data śmierci'])
            empty.set(1)
        else:
            empty.set(0)
            entry.delete(0, "end")
            entry.config(state='disabled')
        self.entries.append(entry)

        emptyButton = Checkbutton(self.colFrame, text="Zmarł", variable=empty, command=clicked)
        emptyButton.grid(row=3, column=3)

        self.buttonFrame = Frame(self.modifyWindow, bd=4, relief=RAISED,
                                 width=self.themeWindow.winfo_width(),
                                 height=40)
        self.buttonFrame.pack(fill='both', side=TOP)
        self.modifyButton = Button(self.buttonFrame, text="Modify", command=self.checkEntry)
        self.modifyButton.pack(side=LEFT)
        self.cancelButton = Button(self.buttonFrame, text="Cancel", command=self.goBack)
        self.cancelButton.pack(side=LEFT)

    def goBack(self):
        self.modifyWindow.event_generate("<<back>>")

    def checkEntry(self):
        self.newRecord.clear()
        # Author's name
        self.newRecord.append(self.entries[0].get())
        # Author's surname
        self.newRecord.append(self.entries[1].get())
        # Author's birth date
        self.newRecord.append(self.entries[2].get())
        # Author's death date
        self.newRecord.append(self.entries[3].get())
        # Assigments


        try:
            self.database.modifyAuthor(self.oldRecord[0], self.entries[0].get(), self.entries[1].get(),
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

class ModifyController3:
    def __init__(self, themeWindow, database, selectedRecord, data, backEvent):
        self.themeWindow = themeWindow
        self.database = database
        self.backEvent = backEvent
        self.data = data
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("ModifyController3 logger has started.")

        self.oldRecord = list()
        # Book's id

        self.oldRecord.append(data[selectedRecord]['Gatunek'])

        self.modifyWindow = Toplevel(self.themeWindow)
        self.modifyWindow.title("Modify record in database.")
        self.modifyWindow.protocol('WM_DELETE_WINDOW', self.goBack)
        self.modifyWindow.bind("<<back>>", lambda _: self.backEvent(None))

        self.newRecord = list()

        self.helpWindow = None

        self.colFrame = Frame(self.modifyWindow, bd=4, relief=RAISED,
                              width=self.themeWindow.winfo_width(),
                              height=self.themeWindow.winfo_height() - 40)
        self.colFrame.pack(fill='both', side=TOP)

        self.entries = list()

        Label(self.colFrame, text="Gatunek", font=("Arial Bold", 12)).grid(row=0, column=0)
        entry = Entry(self.colFrame, width=20)
        entry.grid(row=0, column=1, columnspan=2)
        entry.insert(END, data[selectedRecord]['Gatunek'])
        self.entries.append(entry)

        self.buttonFrame = Frame(self.modifyWindow, bd=4, relief=RAISED,
                                 width=self.themeWindow.winfo_width(),
                                 height=40)
        self.buttonFrame.pack(fill='both', side=TOP)
        self.modifyButton = Button(self.buttonFrame, text="Modify", command=self.checkEntry)
        self.modifyButton.pack(side=LEFT)
        self.cancelButton = Button(self.buttonFrame, text="Cancel", command=self.goBack)
        self.cancelButton.pack(side=LEFT)

    def goBack(self):
        self.modifyWindow.event_generate("<<back>>")

    def checkEntry(self):
        self.newRecord.clear()
        # Genre
        self.newRecord.append(self.entries[0].get())

        try:
            self.database.modifyGenre(self.oldRecord[0], self.newRecord[0])
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

