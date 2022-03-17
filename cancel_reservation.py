from tkinter import *
from connection import *
from get_facultyid import *
from tkinter import messagebox
import pymysql
from datetime import date
from PIL import Image, ImageTk


def cancel_reservation():
    root = Toplevel()
    root.geometry('400x300')
    loadImg = Image.open('blueblossom.png')
    backgroundImage = ImageTk.PhotoImage(loadImg)
    root.background_label = Label(root, image=backgroundImage)
    root.background_label.place(x=0, y=0)

    root.title('Cancel Reservations')

    welcome_label = Label(root, text='Cancel Reservation', font='Bold20')
    welcome_label.place(x=121, y=30)

    member_label = Label(root, text='Enter the Member ID')
    member_label.place(x= 127, y =80)
    book_label = Label(root, text='Enter the Book Accession ID')
    book_label.place(x=107, y=140)

    member_id = Entry(root, width=20, fg="black")
    member_id.place(x = 120, y = 110)
    book_id = Entry(root, width=20, fg='black')
    book_id.place(x= 120, y = 170)

    def cancel_reserve():
        con = connection()
        mem_ID = member_id.get()
        bk_id = book_id.get()

        with con.cursor() as cur:
            find_reservation = 'select * from Reserve where MemberID Like ' + '\'' + str(
                mem_ID) + '\'' + ' AND AccessionNumber LIKE ' + '\'' + str(bk_id) + '\''
            cur.execute(find_reservation)
            result = cur.fetchall()
            if len(result) < 1:
                return messagebox.showerror(str(result), 'This reservation record does not exist!')

            query = 'SELECT Title FROM Book WHERE AccessionNumber LIKE ' + '\'' + bk_id + '\''
            cur.execute(query)
            book_title = cur.fetchall()[0][0]

            # get member name
            query = 'SELECT concat(FirstName, " ", LastName) FROM Member WHERE MemberID LIKE ' + '\'' + mem_ID + '\''
            cur.execute(query)
            member_name = cur.fetchall()[0][0]

        def execute_cancel_reservation():
            delete_reservation = 'DELETE FROM Reserve WHERE MemberID LIKE ' + '\'' + mem_ID + '\'' + ' and AccessionNumber LIKE ' + '\'' + bk_id + '\''

            try:
                with con.cursor() as cur:
                    cur.execute(delete_reservation)
                    con.commit()
                    return messagebox.showinfo('Success!', 'The Reservation record is deleted.')
            finally:
                con.close

        today = date.today()

        confirm_window = Toplevel()
        confirm_window.geometry('300x300')


        Img = Image.open('green_flowers_final.png')
        confirm_backgroundImage = ImageTk.PhotoImage(Img)
        confirm_window.background_label = Label(confirm_window, image=confirm_backgroundImage)
        confirm_window.background_label.place(x=0, y=0)
        confirm_window.background_label.image = confirm_backgroundImage
        confirm_window.title('Confirm Cancellation')
        reserve_detail_label = Label(confirm_window, text='Reservation Details', font='bold20')
        reserve_detail_label.place(x=65, y=20)

        book_label = Label(confirm_window, text='Accession Number: ' + bk_id)
        title_label = Label(confirm_window, text='Book Title: ' + book_title)
        member_label = Label(confirm_window, text='Member ID: ' + mem_ID)
        member_name_label = Label(confirm_window, text='Member Name: ' + member_name)
        date_label = Label(confirm_window, text='Reserve Date: ' + str(today))

        book_label.place(x = 65, y=60)
        title_label.place(x = 65, y=90)
        member_label.place(x = 65, y=120)
        member_name_label.place(x = 65, y = 150)
        date_label.place(x = 65, y= 180)

        confirm_button = Button(confirm_window, text="Confirm Cancellation", padx=20, \
                                command=execute_cancel_reservation)
        confirm_button.place(x=65, y=220)
        exit_button = Button(confirm_window, text='Back to Cancellation Function', command=confirm_window.destroy)
        exit_button.place(x=60, y =255)

    button1 = Button(root, text="Delete Reservation", padx=20, \
                     command=cancel_reserve)
    button1.place(x = 115, y = 210)
    exit_button = Button(root, text='Back to reservation menu', command=root.destroy)
    exit_button.place(x = 115, y = 255)

    root.mainloop()
