from tkinter import *
from tkinter import ttk
from src.Logger import Logger
from src.DataBase import Database

class ProcedureController:
    def __init__(self, rootWindow, database, backEvent):
        self.rootWindow = rootWindow
        self.backEvent = backEvent
        self.database = database
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("ProcedureController logger has started.")

        self.mainLabels = ["Library", "Book title", "Genre", "Publishing date"]
        self.personalLabels = ["Reader's name: ", "Reader's surname:", "Employee's name: ", "Employee's surname: ", "Comment: "]

        self.procedureWindow = Toplevel(self.rootWindow)
        self.procedureWindow.title("Check a book.")
        self.procedureWindow.protocol('WM_DELETE_WINDOW', self.goBack)
        self.procedureWindow.bind("<<back>>", lambda _: self.backEvent())

        self.mainFrame = Frame(self.procedureWindow, bd=4, relief=RAISED,
                               width=self.procedureWindow.winfo_width() - 40,
                               height=self.procedureWindow.winfo_height() - 40)
        self.mainFrame.pack(fill='both', side=TOP)

        self.comboBoxes = list()
        self.frames = list()
        for lab in self.mainLabels:
            self.frames.append(Frame(self.mainFrame))
            if len(self.comboBoxes) == 0:
                self.comboBoxes.append(extendedComboBox(self.database, self.frames[-1], lab))
            else:
                self.comboBoxes.append(extendedComboBox(self.database, self.frames[-1], lab))
                self.comboBoxes[-2].setChild(self.comboBoxes[-1])
                self.comboBoxes[-1].disable()
            self.frames[-1].pack(fill='both', side=TOP)
            # self.frames.append(Frame(self.mainFrame,
            #                          width=self.procedureWindow.winfo_width() - 40,
            #                          height=20 * 4
            #                          ))
            # Label(self.frames[no], text=lab, font=("Arial Bold", 12)).grid(row=0, column=0, columnspan=3)
            # entry = Entry(self.frames[no], width=20)
            # entry.grid(row=0, column=3, columnspan=2)
            # self.entries.append(entry)
            # self.frames[no].pack(fill='both', side=TOP)

        self.restFrame = Frame(self.mainFrame,
                               width=self.procedureWindow.winfo_width() - 40,
                               height=20 * 6
                               )
        self.entries = list()
        for no, lab in enumerate(self.personalLabels):
            Label(self.restFrame, text=lab, font=("Arial Bold", 12)).grid(row=no, column=0, columnspan=3)
            entry = Entry(self.restFrame, width=20)
            entry.grid(row=no, column=3, columnspan=2)
            self.entries.append(entry)
        self.restFrame.pack(fill='both', side=BOTTOM)

        self.buttonFrame = Frame(self.procedureWindow, bd=4, relief=RAISED,
                                 width=self.procedureWindow.winfo_width() - 40,
                                 height=40)
        self.buttonFrame.pack(fill='both', side=TOP)

        self.hireButton = Button(self.buttonFrame, text="Hire", command=self.applyProcedure)
        self.hireButton.pack(side=LEFT)
        self.cancelButton = Button(self.buttonFrame, text="Cancel", command=self.goBack)
        self.cancelButton.pack(side=LEFT)

    def goBack(self):
        self.procedureWindow.event_generate("<<back>>")

    def applyProcedure(self):
        for entry in self.entries:
            if entry.get() == "":
                print("wypelnij wszystkie pola")
                return
            print(entry.get())
        for combo in self.comboBoxes:
            if combo.combo.get() == "":
                print("wypelnij wszystkie pola")
                return
            print(combo.combo.get())
        # try:
        #     # Do a hire procedure
        #     pass
        # except:
        #     # show something on exceptions
        #     pass
        self.goBack()


class extendedComboBox:
    def __init__(self, database, frame, lab):
        self.database = database
        self.child = None
        self.frame = frame
        self.lab = lab
        self.bookName = None
        self.genre = None
        self.values = self.refreshValues()

        self.combo = ttk.Combobox(self.frame, values=self.values)
        self.combo.grid(row=0, column=0, columnspan=2)
        self.combo.bind("<<ComboboxSelected>>", self.selected)

        self.label = Label(self.frame, text=self.lab, font=("Arial Bold", 12))
        self.label.grid(row=0, column=2, columnspan=2)


    def enableChild(self):
        if self.child is not None:
            self.child.combo.configure(state='readonly')
            self.child.combo.set("")
            self.child.combo.configure(values=self.child.refreshValues())
            self.child.recurDisable()
            return True
        else:
            return False

    def setChild(self, child):
        self.child = child

    def disable(self):
        self.combo.configure(state="disabled")
        self.combo.set("")

    def recurDisable(self):
        if self.child is None:
            return
        else:
            self.child.combo.configure(state="disabled")
            self.child.combo.set("")
            self.child.recurDisable()

    def selected(self, event):
        if self.lab == "Book title":
            self.child.bookName = self.combo.get()
            self.child.child.bookName = self.combo.get()
        elif self.lab == "Genre":
            self.child.genre = str(self.combo.get())
        self.enableChild()

    def refreshValues(self):
        if self.lab == "Library":
            values = self.database.executeStatement("SELECT `nazwa` FROM `biblioteki`;")
        elif self.lab == "Book title":
            values = self.database.executeStatement("SELECT `tytul` FROM `ksiazki`;")
        elif self.lab == "Genre" and self.bookName is not None:
            values = self.database.executeStatement(f"SELECT DISTINCT `gatunek` FROM `ksiazki` " +
                                                    f"WHERE `tytul` = \"{self.bookName}\";")
        elif self.lab == "Publishing date" and self.genre is not None:
            values = self.database.executeStatement(f"SELECT DISTINCT `data_opublikowania` FROM `ksiazki` " +
                                                    f"WHERE `tytul` = \"{self.bookName}\" AND `gatunek` = \"{self.genre}\";")
        else:
            values = []
        return values

