from tkinter import *
from tkinter import ttk
from src.Logger import Logger
from tkinter import messagebox
from tkinter import scrolledtext

class ProcedureController:
    def __init__(self, rootWindow, database, backEvent):
        self.rootWindow = rootWindow
        self.backEvent = backEvent
        self.database = database
        # Start logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("ProcedureController logger has started.")

        self.mainLabels = ["Library", "Book title"]
        self.personalLabels = ["Reader's surname", "Reader's name", "Employee's surname", "Employee's name",
                               "Comment(optional)"]

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
                self.comboBoxes[-1].combo.configure(state='readonly')
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
            #print(no, lab)
            l = Label(self.restFrame, text=lab, font=("Arial Bold", 12))
            l.grid(row=no, column=0, columnspan=3)
            if lab == "Comment(optional)":
                # self.commentEntry = Entry(self.restFrame, width=20)
                # self.commentEntry.grid(row=no, column=3, columnspan=2)
                self.commentEntry = scrolledtext.ScrolledText(self.restFrame, width=40, height=10)
                self.commentEntry.grid(row=no, column=3, columnspan=2)
                continue
            if lab == "Reader's surname":
                val = database.executeStatement("SELECT `nazwisko` FROM `pracownicy`")
            elif lab == "Reader's name":
                val = database.executeStatement("SELECT `imie` FROM `pracownicy`")
            elif lab == "Employee's surname":
                val = database.executeStatement("SELECT `nazwisko` FROM `pracownicy`")
            elif lab == "Employee's name":
                val = database.executeStatement("SELECT `imie` FROM `pracownicy`")
            entry = ttk.Combobox(self.restFrame, values=([""] + list(val)))
            entry.configure(state='readonly')
            entry.grid(row=no, column=3, columnspan=2, padx=5, pady=10)
            entry.bind("<<ComboboxSelected>>", lambda _: self.refreshValues())
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
            if entry.get() == "":
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
        args["Comment(optional)"] = self.commentEntry.get('1.0', END).replace("\n", "")
        try:
            self.database.borrowBook(args["Library"], args["Employee's name"], args["Employee's surname"],
                                     args["Reader's name"], args["Reader's surname"], args["Book title"],
                                     args["Comment(optional)"])
        except Exception as e:
            errorNo = int(e.__str__().split()[0][1:-1])
            if errorNo == 1644:
                self.logger.error(f"{e.__str__().split(',')[1][:-2]}")
                messagebox.showerror("Error while hiring a book.",
                                     f"{e.__str__().split(',')[1][:-2]}")
                return
            else:
                self.logger.error(f"{e}")
                messagebox.showerror("Error while hiring a book.",
                                     f"{e}")
                return
        self.database.connection.commit()
        self.procedureWindow.focus_set()
        messagebox.showinfo("Borrow", "Book has been borrowed succesfully!")
        self.goBack()

    def refreshValues(self):
        for lab, en in self.entries.items():
            if lab == "Reader's surname":
                if en.get() is not "":
                    val = self.database.executeStatement(f"SELECT DISTINCT `imie` FROM `czytelnicy` " +
                                                         f"WHERE `nazwisko` = \"{en.get()}\"")
                else:
                    val = self.database.executeStatement(f"SELECT DISTINCT `imie` FROM `czytelnicy`")
                self.entries["Reader's name"].configure(values=([""] + list(val)))
                #self.entries[lab].set("")
            elif lab == "Reader's name":
                if en.get() is not "":
                    val = self.database.executeStatement(f"SELECT DISTINCT `nazwisko` FROM `czytelnicy` " +
                                                         f"WHERE `imie` = \"{en.get()}\"")
                else:
                    val = self.database.executeStatement(f"SELECT DISTINCT `nazwisko` FROM `czytelnicy`")
                self.entries["Reader's surname"].configure(values=([""] + list(val)))
                # self.entries[lab].set("")
            elif lab == "Employee's surname":
                if en.get() is not "":
                    val = self.database.executeStatement(f"SELECT DISTINCT `imie` FROM `pracownicy` " +
                                                         f"WHERE `nazwisko` = \"{en.get()}\"")
                else:
                    val = self.database.executeStatement(f"SELECT DISTINCT `imie` FROM `pracownicy`")
                self.entries["Employee's name"].configure(values=([""] + list(val)))
                # self.entries[lab].set("")
            elif lab == "Employee's name":
                if en.get() is not "":
                    val = self.database.executeStatement(f"SELECT DISTINCT `nazwisko` FROM `pracownicy` " +
                                                         f"WHERE `imie` = \"{en.get()}\"")
                else:
                    val = self.database.executeStatement(f"SELECT DISTINCT `nazwisko` FROM `pracownicy`")
                self.entries["Employee's surname"].configure(values=([""] + list(val)))
                # self.entries[lab].set("")



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
        # if self.lab == "Book title":
        #     #self.child.bookName = self.combo.get()
        #     #self.child.child.bookName = self.combo.get()
        #     pass
        # elif self.lab == "Genre":
        #     self.child.genre = str(self.combo.get())
        self.enableChild()
    def selected(self, event):
        # if self.lab == "Book title":
        #     #self.child.bookName = self.combo.get()
        #     #self.child.child.bookName = self.combo.get()
        #     pass
        # elif self.lab == "Genre":
        #     self.child.genre = str(self.combo.get())
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

