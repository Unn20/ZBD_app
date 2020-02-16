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


        tableName = "ksiazki"
        self.tableName = tableName

        self.tableData = self.database.getRawData(tableName)
        self.data = dict()
        self.booksModel = TableModel()
        self.authorsModel = TableModel()
        self.specimenModel = TableModel()

        self.currentModel = self.booksModel

        self.notebookWidget = ttk.Notebook(self.themeWindow)
        self.booksTab = Frame(self.notebookWidget)
        self.authorsTab = Frame(self.notebookWidget)

        self.notebookWidget.add(self.booksTab, text="Książki")
        self.notebookWidget.add(self.authorsTab, text="Autorzy")
        #self.notebookWidget.pack(expand=1, fill='both')

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
        self.tableData = self.database.getRawData(self.tableName)
        self.data = dict()
        for no, record in enumerate(self.tableData):
            self.data[f"rec {no}"] = dict()
            self.data[f"rec {no}"]["Tytuł"] = record[0]
            self.data[f"rec {no}"]["Rok napisania"] = str(record[1])
            #self.data[f"rec {no}"]["Nazwisko"] = record[2]

        self.currentModel.importDict(self.data)
        if self.table is not None:
            self.table.redraw()

class AddController:
    pass

class ModifyController:
    pass