from tkinter import *
from src.Logger import Logger
from src.DataBase import Database


class TableController:
    """ Class that contains all methods to handle with choosen table menu with
    following functionality: add, modify, delete record, sort by columns, find record"""
    def __init__(self, tableName, database, themeWindow):
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
        self.content.update()

        # Canvas with options menu
        self.topCanvas = Canvas(self.content, bg="white", bd=1, relief=RAISED,
                                   width=int(self.content.winfo_width()),
                                   height=int(self.content.winfo_height() / 12))
        self.topCanvas.pack(fill='both', side=TOP)

        self.backButton = Button(self.topCanvas, text=" < ", command=self.back,
                                      width=7)
        self.backButton.pack(fill='both', side=LEFT)
        self.sortButton = Button(self.topCanvas, text=" Sort ", command=self.back,
                                      width=21)
        self.sortButton.pack(fill='both', side=LEFT)
        self.findButton = Button(self.topCanvas, text=" Find ", command=self.back,
                                        width=21)
        self.findButton.pack(fill='both', side=LEFT)
        self.showButton = Button(self.topCanvas, text=" Show all ", command=self.back,
                                        width=21)
        self.showButton.pack(fill='both', side=LEFT)

        # Canvas with data
        self.middleCanvas = Canvas(self.content, bg="white", bd=1, relief=FLAT,
                                   width=int(self.content.winfo_width()),
                                   height=int(self.content.winfo_height() / 2))
        self.topCanvas.pack(fill='both', side=TOP)

        #self.columnRow
        #TODO: Rest of that controller



    def back(self):
        pass
