import tkinter as tk
from tkcalendar import *


if __name__ == '__main__':
    win = tk.Tk()
    win.title('DateEntry demo')

    #dentry = DateEntry(win, font=('Helvetica', 40, tk.NORMAL), border=0)
    #dentry.pack()

    #win.bind('<Return>', lambda e: print(dentry.get()))

    #cal = Calendar(win)
    #cal.pack()

    cal2 = DateEntry(win)
    cal2.pack()



    win.mainloop()