from tkinter import *
from tkinter import ttk
from src.Logger import Logger
from src.DataBase import Database
from tkinter import messagebox

class ProcedureController:
    def __init__(self, rootWindow, database, backEvent):
        self.rootWindow = rootWindow
        self.backEvent = backEvent
        self.database = database
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("ProcedureController logger has started.")

        self.mainLabels = ["Library", "Book title", "Genre", "Publishing date"]
        self.personalLabels = ["Reader's name", "Reader's surname", "Employee's name", "Employee's surname", "(opt)Comment"]

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
        self.entries = dict()
        for no, lab in enumerate(self.personalLabels):
            l = Label(self.restFrame, text=lab, font=("Arial Bold", 12))
            l.grid(row=no, column=0, columnspan=3)
            entry = Entry(self.restFrame, width=20)
            entry.grid(row=no, column=3, columnspan=2, padx=5, pady=10)
            self.entries[l.cget("text")] = entry

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
        args = dict()
        for label, entry in self.entries.items():
            if entry.get() == "" and label != "(opt)Comment":
                self.logger.error("Not all entries are filled")
                messagebox.showerror("Not all mandatory entries are filled!",
                                     "Not all mandatory entries are filled!")
                return
            else:
                args[label] = entry.get()

        for combo in self.comboBoxes:
            if combo.combo.get() == "":
                self.logger.error("Not all entries are filled")
                messagebox.showerror("Not all mandatory entries are filled!",
                                     "Not all mandatory entries are filled!")
                return
            else:
                args[combo.label.cget("text")] = combo.combo.get()

        print(args["Library"])
        print(args["Employee's name"])
        print(args["Employee's surname"])
        print(args["Reader's name"])
        print(args["Reader's surname"])
        print(args["Book title"])
        print(args["Publishing date"])
        print(args["Genre"])
        print(args["(opt)Comment"])

        try:
            self.database.borrowBook(args["Library"], args["Employee's name"], args["Employee's surname"],
                                     args["Reader's name"], args["Reader's surname"], args["Book title"],
                                     args["Publishing date"], args["Genre"], args["(opt)Comment"])
        except Exception as e:
            errorNo = int(e.__str__().split()[0][1:-1])
            if errorNo == 1644:
                self.logger.error(f"{e.__str__().split(',')[1][:-2]}")
                messagebox.showerror("Error while hiring a book.",
                                     f"{e.__str__().split(',')[1][:-2]}")
                return
            else:
        # show me dat exception
                print(f"EXCEPTION = {e}")
                return
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

