from tkinter import *
from src.Logger import Logger
from src.DataBase import Database


class TableController:
    """ Class that contains all methods to handle with choosen table menu with
    following functionality: add, modify, delete record, sort by columns, find record"""
    def __init__(self, tableName, database, themeWindow, returnEvent):
        self.tableName = tableName
        self.database = database
        self.themeWindow = themeWindow
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("TableController logger has started.")

        columns = ('NIP', 'Firma', "Imie", "Nazwisko")
        rows = self.database.executeStatement("SELECT * FROM wlasciciele")

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
        self.sortButton = Button(self.topCanvas, text=" Sort ", command=self.sort, width=22)
        self.sortButton.pack(fill='both', side=LEFT)
        self.findButton = Button(self.topCanvas, text=" Find ", command=self.find, width=22)
        self.findButton.pack(fill='both', side=LEFT)
        self.showButton = Button(self.topCanvas, text=" Show all ", command=self.showAll, width=22)
        self.showButton.pack(fill='both', side=LEFT)

        # Canvas with data
        # TODO: zrob to kiedy indziej
        self.middleCanvas = Canvas(self.content, bg="white", bd=1, relief=FLAT,
                                   width=int(self.content.winfo_width()),
                                   height=int(self.content.winfo_height() / 1.5))
        self.middleCanvas.pack(fill='both', side=TOP)

        self.columnRow = Canvas(self.middleCanvas,
                                width=int(self.middleCanvas.winfo_width()),
                                height=20)
        self.columnRow.pack(fill='both', side=TOP)
        self.checkbuttonAll = Checkbutton(self.columnRow, text="")
        self.checkbuttonAll.grid(row=0, column=0)
        columnrows = list()
        for i in range(3):
            columnrows.append(Entry(self.columnRow, text="").grid(row=1, column=1+i))

        self.tableCanvas = Canvas(self.middleCanvas,
                                width=int(self.middleCanvas.winfo_width()),
                                height=100)
        self.tableCanvas.pack(fill='both', side=TOP)
        table = list()
        for i in range(5):
            Checkbutton(self.tableCanvas, text="").grid(row=i, column=0)
            table.append(list())
            for j in range(3):
                table[i].append(Entry(self.columnRow, text="").grid(row=i, column=1+j))
        ############
        # Canvas with DML buttons
        self.bottomCanvas = Canvas(self.content, bg="white", bd=1, relief=FLAT,
                                   width=int(self.content.winfo_width()),
                                   height=int(self.content.winfo_height() / 5))
        self.bottomCanvas.pack(fill='both', side=TOP)
        self.buttonAdd = Button(self.bottomCanvas, text=" ADD ", command=self.add, width=24, height=3, bd=5)
        self.buttonAdd.pack(side=LEFT)
        self.buttonModify = Button(self.bottomCanvas, text=" MODIFY ", command=self.modify, width=25, height=3, bd=5)
        self.buttonModify.pack(side=LEFT)
        self.buttonDelete = Button(self.bottomCanvas, text=" DELETE ", command=self.delete, width=25, height=3, bd=5)
        self.buttonDelete.pack(side=LEFT)



    def back(self):
        """ Go back to main window """
        self.content.event_generate("<<goback>>")

    def add(self):
        """ Go to add window """
        print('add')

    def modify(self):
        print('modify')

    def delete(self):
        print('delete')

    def sort(self):
        print('sort')

    def find(self):
        print('find')

    def showAll(self):
        print('show all')
