from tkinter import *
from tkinter import messagebox
from src.Logger import Logger
from tkinter import ttk
from tkintertable.Tables import TableCanvas
from src.CustomTable import CustomTable
from tkintertable.TableModels import TableModel
import datetime


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

        self.backButton = Button(self.topCanvas, text=" < ", command=self.back, width=9)
        self.backButton.pack(fill='both', side=LEFT)
        self.showButton = Button(self.topCanvas, text="Refresh table", command=self.refreshTable, width=22)
        self.showButton.pack(fill='both', side=LEFT)
        self.showButton = Button(self.topCanvas, text="Authors", command=self.checkAuthors, width=22)
        self.showButton.pack(fill='both', side=LEFT)
        self.findButton = Button(self.topCanvas, text="Find by author", command=self.findByAuthor, width=22)
        self.findButton.pack(fill='both', side=LEFT)

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
                                   command=lambda: self.delete(None), width=25, height=3, bd=5)
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
            #self.addWindow = AddController(self.themeWindow, self.tableName, self.database, self.backEvent)

    def modify(self):
        """ Go to modify window """
        if self.table.startrow != self.table.endrow:
            messagebox.showwarning('Modify error', 'Please select only one record!')
        else:
            selectedRow = self.table.currentrow
            if self.modifyWindow is None:
                self.logger.debug("Starting modify window.")
                # self.modifyWindow = ModifyController(self.themeWindow, self.tableName, self.database,
                #                                      self.model.getRecName(selectedRow),
                #                                      self.data, self.backEvent)

    def delete(self, tableName):
        """ Delete selected records """
        for no, i in enumerate(self.table.multiplerowlist):
            recName = self.currentModel.getRecName(i)
            deletedRecord = list()
            deletedRecord.append(self.data[recName]["ID"])
            deletedRecord.append(self.data[recName]["Imię"])
            deletedRecord.append(self.data[recName]["Nazwisko"])
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
    pass

class ModifyController:
    pass