from tkinter import *
from tkinter import filedialog
import sqlite3
from billiard.five import string
import numpy as np
import cv2
import dlib
import Face_Recognition


def add_to_database(name, reg, image):
    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()
    print(name)
    print(reg)
    print(image)
    print("Connected to SQLite")

    sqlite_insert_with_param = """INSERT INTO students
                              ( name, reg, image) 
                              VALUES ( ?, ?, ?);"""

    data_tuple = (name, reg, image)
    cursor.execute(sqlite_insert_with_param, data_tuple)
    conn.commit()
    print("Python Variables inserted successfully into students table")

    cursor.close()


def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents
    label_file_explorer.configure(text=filename)


# Create the root window
window = Tk()

# Set window title
window.title('File Explorer')

# Set window size
window.geometry("750x500")

# Set window background color

# Create a File Explorer label
label_file_explorer = Label(window,
                            text="File Explorer using Tkinter",
                            width=100, height=4,
                            fg="blue")

button_explore = Button(window,
                        text="Browse from Files",
                        command=browseFiles)

username_label = Label(window, text="Student Name", width=50, height=2)

username = Entry()

reg_label = Label(window, text="Registration number", width=50, height=2)

reg = Entry()

face_label = Label(window, text="Student's Image", width=50, height=2)

button_submit = Button(window,
                       text="Submit",
                       width=15, height=2, bg="#20bebe",
                       command=lambda: add_to_database(string(username.get()), string(reg.get()),
                                                       label_file_explorer.cget("text"))
                       )

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column=1, row=1)

username_label.grid(column=1, row=2)

username.grid(column=1, row=3)

reg_label.grid(column=1, row=4)
reg.grid(column=1, row=5)

face_label.grid(column=1, row=6)

button_explore.grid(column=1, row=7)

button_submit.grid(column=1, row=8)

# ==============================Recognition interface===============================

heading = Label(window, text="Recognize Students", height=2, fg="blue",
                font=('Raleway', 10, 'bold'))

heading.grid(column=0, row=9)

hidden = Label(window, text="")


def browseFiles2():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents
    hidden.configure(text=filename)


unknown_image = Button(window,
                       text="Browse from Files",
                       command=browseFiles2, width=15, height=2)

pk = []


def recognition(path):
    print(path)
    unknown_image = cv2.imread(path)
    enc1 = Face_Recognition.whirldata_face_encodings(unknown_image)

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()
    print("Connected to SQLite")

    sqlite_insert_with_param = """select image from students"""

    image_knowns = cursor.execute(sqlite_insert_with_param)
    conn.commit()

    print("This is", type(image_knowns))

    for i in image_knowns:
        counter = 1
        image2 = cv2.imread(','.join(i))
        enc2 = Face_Recognition.whirldata_face_encodings(image2)
        distance = Face_Recognition.return_euclidean_distance(enc1, enc2)

        if distance < 0.5:
            pk.append(counter)
            print("RECOGNIZED")
        else:
            print("NOT RECOGNIZED")

        counter += 1

    cursor.close()
    return


unknown_image.grid(column=0, row=10)
recognize_button = button_submit = Button(window,
                                          text="Submit",
                                          width=15, height=2, bg="#20bebe",
                                          command=lambda: recognition(hidden.cget("text"))
                                          )
recognize_button.grid(column=1, row=10)
# Let the window wait for any events
window.mainloop()
