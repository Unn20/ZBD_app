from tkinter import *
from src.Logger import Logger
from src.DataBase import Database

class LogonController:
    def __init__(self, mainWindow, eventF, width=300, height=200):
        # Initialize logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("LogonController logger has started.")

        # Create sub window with signing info
        self.tlLogon = Toplevel(mainWindow)
        self.tlLogon.title("Sign In")
        mainWindow.update()
        # Calculate offset of sub window
        xOffset = (mainWindow.winfo_width() / 2) - (width / 2)
        yOffset = (mainWindow.winfo_height() / 2) - (height / 2)

        self.tlLogon.geometry(f"{width}x{height}+{int(xOffset)}+{int(yOffset)}")
        self.tlLogon.lift()
        self.tlLogon.resizable(0, 0)
        self.tlLogon.attributes("-topmost", True)
        self.tlLogon.bind("<FocusIn>", self.eventHandleFocus)
        self.tlLogon.protocol('WM_DELETE_WINDOW', self.doNothing)
        self.tlLogon.bind('<<signed>>', lambda database: eventF(self.dataBase))

        # Other widgets
        self.content = Frame(self.tlLogon)
        self.content.place(x=self.tlLogon.winfo_width()/12, y=self.tlLogon.winfo_height()/6)

        self.labelAddress = Label(self.content, text="Adress:", font=("Arial Bold", 12))
        self.labelAddress.grid(row=0, column=0)

        self.textAddress = Entry(self.content, width=20)
        self.textAddress.grid(row=0, column=1)
        self.textAddress.insert(END, "localhost")  # TODO: REMOVE IT LATER

        self.labelUser = Label(self.content, text="Username:", font=("Arial Bold", 12))
        self.labelUser.grid(row=1, column=0)

        self.textUser = Entry(self.content, width=20)
        self.textUser.grid(row=1, column=1)
        self.textUser.insert(END, "root") # TODO: REMOVE IT LATER

        self.labelPassword = Label(self.content, text="Password:", font=("Arial Bold", 12))
        self.labelPassword.grid(row=2, column=0)

        self.textPassword = Entry(self.content, show='*', width=20)
        self.textPassword.grid(row=2, column=1)

        self.labelDatabase = Label(self.content, text="Database Name:", font=("Arial Bold", 12))
        self.labelDatabase.grid(row=3, column=0)

        self.textDatabase = Entry(self.content, width=20)
        self.textDatabase.grid(row=3, column=1)
        self.textDatabase.insert(END, "ZBD_project")

        self.buttonLogin = Button(self.content, text="Sign in", command=self.clickLogin)
        self.buttonLogin.grid(row=4, column=1)

        self.labelDatabase = Label(self.content, text="Incorrect login input!", font=("Arial Bold", 8), fg="red")
        self.labelDatabase.grid(row=5, column=1)
        self.labelDatabase.grid_remove()


    def clickLogin(self):
        self.logger.debug("Attempt to sign in.")
        address = self.textAddress.get()
        user = self.textUser.get()
        password = self.textPassword.get()
        databaseName = self.textDatabase.get()
        if self.signInToDatabase(address, user, password, databaseName):
            self.labelDatabase.grid_remove()
            self.logger.info("Signed in!")
            self.tlLogon.event_generate("<<signed>>")
        else:
            self.labelDatabase.grid()

    def signInToDatabase(self, address, user, password, databaseName):
        try:
            dataBase = Database(host=address, user=user, password=password, database=databaseName)
        except ConnectionRefusedError:
            self.logger.error("Could not connect to data base system!")
            return False
        self.dataBase = dataBase
        return True

    def eventHandleFocus(self, event):
        if event.widget == self.tlLogon:
            self.tlLogon.focus_set()

    def doNothing(self):
        pass
