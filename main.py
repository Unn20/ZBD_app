import pymysql
from tkinter import *

if __name__ == '__main__':
    print("Hello")

    window = Tk()
    window.title("HELLO TK")



    connection = pymysql.connect(host="localhost", user="root", passwd="", database="zbd_project")
    cursor = connection.cursor()

    retrieve = "SELECT * FROM wlasciciele;"

    cursor.execute(retrieve)

    result = cursor.fetchall()

    lbl = Label(window, text=result)
    lbl.grid(column=0, row=0)
    window.mainloop()
    for row in result:
        print(row)


    connection.close()
    print("end")