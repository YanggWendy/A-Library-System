from tkinter import *
from connection import *
from get_facultyid import *
from tkinter import messagebox
import pymysql
from datetime import date
from PIL import Image, ImageTk

def fine_report_page():
    fine_window = Toplevel()
    fine_window.title('Fine Report')
    loadImg = Image.open('sky.png')
    backgroundImage = ImageTk.PhotoImage(loadImg)
    fine_window.background_label = Label(fine_window, image=backgroundImage)
    fine_window.background_label.place(x=0, y=0)
    con = connection()

    memID_Label = Label(fine_window, text="Member ID")
    name_label = Label(fine_window, text="Member Name")
    faculty_label = Label(fine_window, text = 'Faculty Name')
    phone_label = Label(fine_window, text='Phone Number')
    email_label = Label(fine_window, text="Email")
    fine_label = Label(fine_window, text= 'Fine Amount')

    memID_Label.grid(row=0, column=0)
    name_label.grid(row=0, column=1)
    faculty_label.grid(row=0, column=2)
    phone_label.grid(row=0, column=3)
    email_label.grid(row=0, column=4)
    fine_label.grid(row = 0, column = 5)

    '''
    select MemberID, concat(FirstName, " ", LastName) as name, FacultyID, PhoneNo, Email, FineAmount 
    from member
    where FineAmount > 0
    '''

    query = 'SELECT MemberID, concat(FirstName, " ", LastName) AS name, FacultyID, PhoneNo, Email, FineAmount FROM member WHERE FineAmount > 0'
    with con.cursor() as cur:
        cur.execute(query)
        result = cur.fetchall()

    for row_count in range(len(result)):
        row = result[row_count]
        member_ID, member_name, facultyID, phone, email, fine = row[0], row[1], row[2], row[3], row[4], row[5]
        faculty = get_faculty_name(facultyID)

        memID_Label = Label(fine_window, text=member_ID)
        name_label = Label(fine_window, text=member_name)
        faculty_label = Label(fine_window, text=faculty)
        phone_label = Label(fine_window, text=phone)
        email_label = Label(fine_window, text=email)
        fine_label = Label(fine_window, text=fine)

        memID_Label.grid(row=row_count +1, column=0)
        name_label.grid(row=row_count +1, column=1)
        faculty_label.grid(row=row_count +1, column=2)
        phone_label.grid(row=row_count +1, column=3)
        email_label.grid(row=row_count +1, column=4)
        fine_label.grid(row=row_count +1, column=5)

    exit_button = Button(fine_window, text='Back to Reports Menu', command=fine_window.destroy, bg='skyblue1')
    exit_button.grid(row = len(result)+2, column = 5)


    fine_window.mainloop()

