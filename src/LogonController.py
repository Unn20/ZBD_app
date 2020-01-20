from tkinter import *


class LogonController:
    def __init__(self, window):
        self.labelUser = Label(window, text="Username:")
        self.labelUser.grid(row=0)

        self.textUser = Entry(window, width=10)
        self.textUser.grid(row=1)

        self.labelPassword = Label(window, text="Password:")
        self.labelPassword.grid(row=2)

        self.textPassword = Entry(window, width=10)
        self.textPassword.grid(row=3)

        self.buttonLogin = Button(window, text="Sign in", command=self.clickLogin)
        self.buttonLogin.grid(row=4)

    def clickLogin(self):
        res = self.textUser.get()
        self.labelUser.configure(text=res)

    def signInToDatabase(self):
        pass
