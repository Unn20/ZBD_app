from tkinter import *
from tkinter import ttk
from src.Logger import Logger
from tkinter import messagebox


class FunctionController:
    def __init__(self, rootWindow, database, backEvent, year):
        self.rootWindow = rootWindow
        self.backEvent = backEvent
        self.database = database
        self.year = year
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("FunctionController logger has started.")

        self.functionWindow = Toplevel(self.rootWindow)
        self.functionWindow.title("Check a book.")
        self.functionWindow.protocol('WM_DELETE_WINDOW', self.goBack)
        self.functionWindow.bind("<<back>>", lambda _: self.backEvent())

        self.data = self.database.findBestBook(self.year)
        values = self.database.executeStatement(f"SELECT * FROM `ksiazki` WHERE `ksiazka_id` = {self.data[0][0][0]}")
        self.finalData = dict()
        self.finalData["Title"] = values[0][1]
        self.finalData["Date"] = str(values[0][2])
        self.finalData["Genre"] = values[0][3]
        self.finalData["Amount"] = self.data[1][0][0]

        self.mainFrame = Frame(self.functionWindow,  bd=4, relief=RAISED,
                               width=self.functionWindow.winfo_width(),
                               height=self.functionWindow.winfo_height())
        self.mainFrame.pack(fill='both', side=TOP)

        titleLabel = Label(self.mainFrame, text=f"Most hired book in year {year} is..", font=("Arial Bold", 18))
        titleLabel.grid(row=0, column=0, columnspan=3, padx=40, pady=20)

        rowNo = 1
        for no, val in self.finalData.items():
            l1 = Label(self.mainFrame, text=f"{no}: {val}", font=("Arial Bold", 14))
            l1.grid(row=rowNo, column=0, columnspan=3, padx=10, pady=10)
            rowNo+=1

    def goBack(self):
        self.functionWindow.event_generate("<<back>>")