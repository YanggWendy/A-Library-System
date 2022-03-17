from tkinter import *
from connection import *
from get_facultyid import *
from tkinter import messagebox
import pymysql
from datetime import date
from PIL import Image, ImageTk



def reserve_page():
    root = Toplevel()
    root.geometry('400x300')
    loadImg = Image.open('blueblossom.png')
    backgroundImage = ImageTk.PhotoImage(loadImg)
    root.background_label = Label(root, image=backgroundImage)
    root.background_label.place(x =0, y = 0)

    root.title('Reservations')

    welcome_label = Label(root, text='Make the Reservations!', font='Bold20')
    welcome_label.place(x=110, y = 30)


    member_label = Label(root, text='Enter the Member ID')
    member_label.place(x= 128, y =70)
    book_label = Label(root, text='Enter the Book Accession ID')
    book_label.place(x=110, y=140)

    member_id = Entry(root, width=20, fg="black")
    member_id.place(x = 120, y = 105)
    book_id = Entry(root, width=20, fg='black')
    book_id.place(x= 120, y = 175)

    #member_label.pack()
    #member_id.pack()
    #book_label.pack()
    #book_id.pack()

    def reserve():
        con = connection()
        mem_ID = member_id.get()
        bk_id = book_id.get()

        '''
        check condition:
            1. Book ID exist; Book ID not in the borrow table
            2. Member exists; Member fine == 0
            3. number of reserved books <2
        '''
        with con.cursor() as cur:
            select_fine = 'SELECT FineAmount from Member WHERE MemberID LIKE ' + '\'' + mem_ID + '\''
            cur.execute(select_fine)
            fine = cur.fetchall()
            try:
                if fine[0][0] > 0:
                    return messagebox.showerror('', 'Member has an outstanding fine of $' + str(fine[0][0]) + ' !')
            except IndexError:
                return messagebox.showerror('', 'Member does not exist!')

            # check if book inside book table but not inside borrow table
            check_book = 'SELECT AccessionNumber from book where AccessionNumber LIKE' + '\'' + bk_id + '\''
            cur.execute(check_book)
            book = cur.fetchall()
            if not book:
                return messagebox.showerror('', 'The book does not exist!')

            # check if the member has made 2 reservations
            check_reserve = 'SELECT ReserveDate from reserve where MemberID LIKE' + '\'' + mem_ID + '\''
            cur.execute(check_reserve)
            reserve_record = cur.fetchall()
            if len(reserve_record) > 1:
                return messagebox.showerror('', 'The member has already made 2 reservations!')

            check_already_reserved = 'SELECT ReserveDate from reserve where MemberID LIKE' + '\'' + mem_ID + '\'' + 'AND AccessionNumber LIKE' + '\'' + bk_id + '\''
            cur.execute(check_already_reserved)
            reserve_already_record = cur.fetchall()
            if len(reserve_already_record) > 0:
                return messagebox.showerror('', 'The member has already made the reservation for this book!')

            # if the conditions were all met, add the reserve record into the reserve table
            today = date.today()
            # get book title:
            query = 'SELECT Title FROM Book WHERE AccessionNumber LIKE ' + '\'' + bk_id + '\''
            cur.execute(query)
            book_title = cur.fetchall()[0][0]

            # get member name
            query = 'SELECT concat(FirstName, " ", LastName) FROM Member WHERE MemberID LIKE ' + '\'' + mem_ID + '\''
            cur.execute(query)
            member_name = cur.fetchall()[0][0]

        confirm_window = Toplevel()
        confirm_window.geometry('300x300')
        #confirm_window.title('Confirm Reservation')

        Img = Image.open('green_flowers_final.png')
        confirm_backgroundImage = ImageTk.PhotoImage(Img)
        confirm_window.background_label = Label(confirm_window, image=confirm_backgroundImage)
        confirm_window.background_label.place(x=0, y=0)
        confirm_window.background_label.image = confirm_backgroundImage

        confirm_window.title('Confirm Reservation')

        reserve_detail_label = Label(confirm_window, text='Reservation Details', font='bold20')
        reserve_detail_label.place(x=70,y=20)

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

        def reserve_execute():
            q = 'INSERT INTO Reserve VALUES (' + '\'' + bk_id + '\'' + ',' + '\'' + mem_ID + '\'' + ',' + '\'' + str(
                today) + '\')'
            try:
                with con.cursor() as cur:
                    cur.execute(q)
                    con.commit()
                    messagebox.showinfo('Success!', 'The reservation is done!')

            finally:
                con.close
            # return messagebox.showinfo('Success!', 'Reservation is done!')

        button1 = Button(confirm_window, text="Confirm Reservations", padx=20, \
                         command=reserve_execute)
        button1.place(x=65, y=220)
        exit_button = Button(confirm_window, text='Back to Reserve Function', command=confirm_window.destroy)
        exit_button.place(x=70, y =260)

    button1 = Button(root, text="Reserve Book", padx=20, \
                     command=reserve)
    button1.place(x = 130, y = 210)
    exit_button = Button(root, text='Back to Reservations Menu', command=root.destroy)
    exit_button.place(x = 110, y = 255)

    root.mainloop()


'''self.reservaiton_win_bn = Button(self.root, text="Reservation", compound='center', border=0,
                                   command=self.open_reservations, height=100, \
                                   width=166, image=self.buttonImage, activeforeground='black', font='bold30')'''

'''self.reservaiton_win_bn = Button(self.root, text="Reservation", 
                                   command=self.open_reservations, compound='center', border=0, height=100, \
                                   width=166, image=self.buttonImage, activeforeground='black', font='bold30')

                                       exit_button = Button(root, text = 'Back to Reservations  Menu', command = root.destroy, compound='center', border=0, height=100, \
                                   width=166, image=background, activeforeground='black', font='bold30')'''
