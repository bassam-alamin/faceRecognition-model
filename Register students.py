from tkinter import *
from tkinter import filedialog
import sqlite3
from billiard.five import string
import numpy as np
import cv2
import dlib
import Face_Recognition

import csv



def add_to_database(name, reg, image):
    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    print(name)
    print(reg)
    print(image)
    if name != " " and reg != " " and image != " ":
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO students
                                  ( name, reg, image,attended) 
                                  VALUES ( ?, ?, ?,0);"""

        data_tuple = (name, reg, image)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
        print("Python Variables inserted successfully into students table")

        cursor.close()
    else:
        print("Make sure you input Name,Registration number and a valid image")


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


def open_camera():
    global uk_image
    vid = cv2.VideoCapture(0)
    while True:
        ret, frame = vid.read()
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            uk_image = frame
            break

    enc1 = Face_Recognition.whirldata_face_encodings(uk_image)
    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()
    print("Connected to SQLite")

    sqlite_insert_with_param = """select id,image from students"""

    image_knowns = cursor.execute(sqlite_insert_with_param)
    conn.commit()

    print("This is", type(image_knowns))

    for i in image_knowns.fetchall():
        print(i)
        counter = 1
        image2 = cv2.imread(i[1])
        print("This is Image of abdulaziz",image2)
        enc2 = Face_Recognition.whirldata_face_encodings(image2)
        distance = Face_Recognition.return_euclidean_distance(enc1, enc2)

        if distance < 0.5:
            pk.append(counter)
            print(distance)
            sqlite_insert_with_param = """update students set attended=? where id=?"""

            cursor.execute(sqlite_insert_with_param,(i[0],++1))
            conn.commit()
            print("RECOGNIZED increased attendance")

        else:
            print(distance)
            print("NOT RECOGNIZED")

        counter += 1

    cursor.close()

    vid.release()
    cv2.destroyAllWindows()






# def recognition(path):
#     print(path)
#     unknown_image = cv2.imread(path)
#     enc1 = Face_Recognition.whirldata_face_encodings(unknown_image)
#
#     conn = sqlite3.connect('students.db')
#
#     cursor = conn.cursor()
#     print("Connected to SQLite")
#
#     sqlite_insert_with_param = """select image from students"""
#
#     image_knowns = cursor.execute(sqlite_insert_with_param)
#     conn.commit()
#
#     print("This is", type(image_knowns))
#
#     for i in image_knowns:
#         counter = 1
#         image2 = cv2.imread(','.join(i))
#         enc2 = Face_Recognition.whirldata_face_encodings(image2)
#         distance = Face_Recognition.return_euclidean_distance(enc1, enc2)
#
#         if distance < 0.5:
#             pk.append(counter)
#             print("RECOGNIZED")
#         else:
#             print("NOT RECOGNIZED")
#
#         counter += 1
#
#     cursor.close()
#     return

def create_csv():
    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()
    print("Connected to SQLite")
    sqlite_insert_with_param = """select name,reg from students where attended=1"""
    name = cursor.execute(sqlite_insert_with_param)

    all = name.fetchall()
    print(all)
    conn.commit()

    with open('recognized_student.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name"])
        for i in all:
            print(i)
            writer.writerow([i[0], ''.join(i[1])])



unknown_image.grid(column=0, row=10)
recognize_button = button_submit = Button(window,
                                          text="Submit",
                                          width=15, height=2, bg="#20bebe",
                                          command=lambda: open_camera())


recognize_button.grid(column=1, row=10)

get_csv = Button(window,
                 text="Get Attendance",
                 width=15, height=2, bg="#20bebe",
                 command=lambda: create_csv()
                 )
get_csv.grid(column=1, row=11)

# Let the window wait for any events
window.mainloop()
