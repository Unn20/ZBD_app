from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from src.Logger import Logger
from src.TableController import TableController
from src.ProcedureController import ProcedureController
from src.FunctionController import FunctionController


class MainController:
    """ A class that contains all methods to handle main window with table names """

    def __init__(self, themeWindow, database, logoutEvent):
        self.database = database
        self.themeWindow = themeWindow
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("MainController logger has started.")
        # Read table names from database object
        self.tableNames = self.database.getTableNames()
        if len(self.tableNames) != 0:
            self.logger.debug("Table names are loaded")
        else:
            self.logger.warning("No table names has been loaded!")

        self.procedureController = None
        self.functionController = None
        self.choiceWindow = None

        # Widgets
        # Main frame of this window
        self.content = Frame(self.themeWindow, bg="#B7B9B8", bd=4, relief=RAISED,
                             width=self.themeWindow.winfo_width() - 80, height=self.themeWindow.winfo_height() - 80)
        self.content.place(x=40, y=40)
        self.content.grid(row=0, column=0)
        self.content.bind("<<signout>>", lambda _: logoutEvent(None))
        self.content.update()

        self.listFrame = Frame(self.content, bg="white", bd=1, relief=FLAT,
                               width=int(self.content.winfo_width() / 2 + 20),
                               height=int(self.content.winfo_height() - 60))
        self.listFrame.place(x=20, y=20)

        # Canvas which contains whole list of table names with their buttons
        self.tablesCanvas = Canvas(self.listFrame, bg="white", bd=1, relief=FLAT,
                                   width=int(self.content.winfo_width() / 2),
                                   height=int(self.content.winfo_height() - 60))
        self.tablesCanvas.update()
        self.tablesScrollY = Scrollbar(self.listFrame, orient="vertical", command=self.tablesCanvas.yview)

        self.tablesFrame = Frame(self.tablesCanvas, bg="white", bd=0, relief=FLAT,
                                 width=self.tablesCanvas.winfo_width(), height=self.tablesCanvas.winfo_height())

        self.selectionVar = IntVar()  # Int variable which contains current selection
        for no, table in enumerate(self.tableNames):
            Radiobutton(self.tablesFrame, bg="white", text=f"{table}", variable=self.selectionVar,
                        value=no, command=lambda: self.selection(self.tableNames[self.selectionVar.get()])
                        ).pack(anchor=W)

        self.tablesCanvas.place(x=40, y=30)
        self.tablesCanvas.create_window(0, 0, anchor='nw', window=self.tablesFrame)
        self.tablesCanvas.configure(scrollregion=self.tablesCanvas.bbox('all'),
                                    yscrollcommand=self.tablesScrollY.set)
        self.tablesCanvas.pack(fill='both', expand=True, side='left')
        self.tablesScrollY.pack(fill='y', side='left')

        # Frame which contain buttons
        self.buttonsFrame = Frame(self.content, bg="#B7B9B8", relief=RAISED,
                                  width=int(self.content.winfo_width() / 4),
                                  height=int(self.content.winfo_height() - 60))

        self.buttonsFrame.place(x=380, y=20)

        # Button to view selected table
        self.buttonViewTable = Button(self.buttonsFrame, text="View Table", command=self.viewTable,
                                      width=20, height=5)
        self.buttonViewTable.grid(row=0, column=0)
        # Button with SQL defined procedure
        self.buttonViewTable = Button(self.buttonsFrame, text="Hire a book", command=self.customProcedure,
                                      width=20, height=5)
        self.buttonViewTable.grid(row=1, column=0)
        # Button with SQL defined function
        self.buttonViewTable = Button(self.buttonsFrame, text="Top book", command=self.functionEntry,
                                      width=20, height=5)
        self.buttonViewTable.grid(row=2, column=0)
        # Button to log out
        self.buttonViewTable = Button(self.buttonsFrame, text="Log out", command=self.logout,
                                      width=20, height=5)
        self.buttonViewTable.grid(row=3, column=0)

    def selection(self, tabName):
        self.logger.debug(f"Choosed `{tabName}` table.")

    def customProcedure(self):
        if self.procedureController is None:
            self.procedureController = ProcedureController(self.themeWindow, self.database, self.backEvent)

    def customFunction(self, year):
        self.year = year
        if self.functionController is None:
            self.functionController = FunctionController(self.themeWindow, self.database, self.backEvent, self.year)
            self.choiceWindow.destroy()
            self.choiceWindow = None

    def functionEntry(self):
        if self.choiceWindow is not None:
            return
        years = self.database.executeStatement("SELECT DISTINCT `data` FROM `historia_operacji` " +
                                               "WHERE `rodzaj_operacji` = \"wypozyczenie\"")
        new_years = list()
        if len(years) == 0:
            messagebox.showwarning("No hired books", "There are no hired books yet!")
            return
        for no, y in enumerate(years):
            new_years.append(y[0].year)

        self.choiceWindow = Toplevel(self.themeWindow)
        self.choiceWindow.protocol('WM_DELETE_WINDOW', self.backEvent)

        titleLabel = Label(self.choiceWindow, text="What is best hired book in selected year?")
        titleLabel.grid(row=0, column=0, columnspan=2)
        label = Label(self.choiceWindow, text="Choose year: ")
        label.grid(row=1, column=0)
        combo = ttk.Combobox(self.choiceWindow, values=new_years)
        combo.grid(row=1, column=1, columnspan=2)
        combo.configure(state="readonly")
        button = Button(self.choiceWindow, text="Select", command=lambda: self.customFunction(combo.get()))
        button.grid(row=2, column=0)

    def backEvent(self):
        if self.procedureController is not None:
            self.procedureController.procedureWindow.destroy()
            self.procedureController = None
        if self.functionController is not None:
            self.functionController.functionWindow.destroy()
            self.functionController = None
        if self.choiceWindow is not None:
            self.choiceWindow.destroy()
            self.choiceWindow = None

    def logout(self):
        """ Generate an event to sign out """
        self.content.event_generate("<<signout>>")

    def viewTable(self):
        """ Go to selected table screen """
        self.content.grid_forget()
        self.tableController = TableController(self.tableNames[self.selectionVar.get()],
                                               self.database, self.themeWindow, self.chooseTableEvent)

    def chooseTableEvent(self, _):
        self.tableController.content.destroy()
        self.content.grid(row=0, column=0)
