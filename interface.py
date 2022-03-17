from tkinter import *
from get_facultyid import*
from member_creation import*
from member_deletion import*
from member_update import*
from book_acquisition import*
from book_withdrawal import*
from book_loan import*
from book_return import*

from book_reservation import*
from cancel_reservation import*
from fine_payment import*
from books_on_loan import*
from books_on_reservation import*
from fine_report import*
from book_search import*
from books_on_loan_to_member import*

import numpy as np
import pandas as pd


# noinspection PyAttributeOutsideInit
class GuiWindow():
    def __init__(self):
        self.root = Tk()
        self.root.title('ALS System')
        self.root.geometry('800x500')
        self.root.resizable(height=None, width=None)

        # self.root.resizable(height=None, width=None)
        self.backgroundImage = PhotoImage(file='vangogh.png')
        self.buttonImage = PhotoImage(file='png_buttons_87348.png')
        self.subpageImage = PhotoImage(file='wheat.png')
        self.subpage_buttonImage = PhotoImage(file='button2.png')

        self.backGroundImageLabel = Label(self.root, image=self.backgroundImage)
        self.backGroundImageLabel.place(x=0, y=0)
        self.canvas = Canvas(self.root, width=500, height=200)
        self.canvas.place(x=150, y=150)
        self.title = Label(self.root, text='Welcome to the ALS System!', font='Bold 24')
        self.title.place(x=190, y=100)
        self.root.resizable(height=None, width=None)
        self.creat_manu()

    def open_membership(self):
        self.membership_win = Toplevel()
        self.membership_win.geometry('600x400')
        self.membership_win.title("Membership Menu")
        self.membership_win.label = Label(self.membership_win, image=self.subpageImage)
        self.membership_win.label.place(x=0, y=0)
        self.membership_win.intro_label = Label(self.membership_win, text='Membership', font='Bold24')
        self.membership_win.intro_label.place(x=240, y=50)

        self.create_btn = Button(self.membership_win, text="Create member", command=member_page, compound='center',
                                  border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.create_btn.place(x=217, y=120)

        self.delete_btn = Button(self.membership_win, text="Delete member", command=delete_page,
                                  compound='center', border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.delete_btn.place(x=217, y=180)

        self.update_btn = Button(self.membership_win, text="Update member Information", command=update_mem_page,
                                  compound='center', border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.update_btn.place(x=217, y=240)

        self.close_btn = Button(self.membership_win, text="Back to Main Menu", command=self.membership_win.destroy,
                                  compound='center', border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.close_btn.place(x=217, y=300)

    def open_book(self):
        self.book_win = Toplevel()
        self.book_win.geometry('600x400')
        self.book_win.title("Book Menu")
        self.book_win.label = Label(self.book_win, image=self.subpageImage)
        self.book_win.label.place(x=0, y=0)
        self.book_win.intro_label = Label(self.book_win, text='Book Management', font='Bold24')
        self.book_win.intro_label.place(x=217, y = 50)

        self.create_btn = Button(self.book_win, text="Book Acquisition", command=create_book, compound='center',
                                  border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.create_btn.place(x=217, y=120)

        self.delete_btn = Button(self.book_win, text="Book Withdrawal", command=withdraw_book,
                                  compound='center', border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.delete_btn.place(x=217, y=180)

        self.close_btn = Button(self.book_win, text="Back to Main Menu", command=self.book_win.destroy,
                                  compound='center', border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.close_btn.place(x=217, y=240)


    def open_loans(self):
        self.loans_win = Toplevel()
        self.loans_win.geometry('600x400')
        self.loans_win.title("Loans Menu")

        self.loans_win.label = Label(self.loans_win, image=self.subpageImage)
        self.loans_win.label.place(x=0, y=0)
        self.loans_win.intro_label = Label(self.loans_win, text='Book Loan Management', font='Bold24')
        self.loans_win.intro_label.place(x=217, y=50)

        self.close_btn = Button(self.loans_win, text="Borrow Book", command=borrow_page, compound='center', border=0, height=50, \
                               width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.close_btn.place(x=217, y=120)

        self.close_btn = Button(self.loans_win, text="Return Book", command=return_page,
                                  compound='center', border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.close_btn.place(x=217, y=180)

        self.close_btn = Button(self.loans_win, text="Back to Main Menu", command=self.loans_win.destroy,
                                  compound='center', border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.close_btn.place(x=217, y=240)
    
    def open_reservations(self):
        self.reservations = Toplevel()

        self.reservations.geometry('600x400')
        self.reservations.title("Reservations Menu")
        self.reservations.label = Label(self.reservations, image=self.subpageImage)
        self.reservations.label.place(x=0, y=0)
        self.reservations.intro_label = Label(self.reservations, text='Reservations Menu', font='Bold24')
        self.reservations.intro_label.place(x=217, y=50)

        self.reserve_btn = Button(self.reservations, text="Make Reservations", command=reserve_page, compound='center',
                                  border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.reserve_btn.place(x=217, y=120)

        self.reserve_btn = Button(self.reservations, text="Delete Reservations", command=cancel_reservation,
                                  compound='center', border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.reserve_btn.place(x=217, y=180)

        self.reserve_btn = Button(self.reservations, text="Back to Main Menu", command=self.reservations.destroy,
                                  compound='center', border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.reserve_btn.place(x=217, y=240)

    def open_fines(self):
        self.fines_win = Toplevel()
        self.fines_win.geometry('600x400')
        self.fines_win.title("Fines Menu")
        self.fines_win.label = Label(self.fines_win, image=self.subpageImage)
        self.fines_win.label.place(x=0, y=0)
        self.fines_win.intro_label = Label(self.fines_win, text='Fine Payment', font='Bold24')
        self.fines_win.intro_label.place(x=240, y=80)

        self.fine_btn = Button(self.fines_win, text="Fine Payment", command=fine_page, compound='center',
                                  border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.fine_btn.place(x=217, y=160)


        self.close_btn = Button(self.fines_win, text="Back to Main Menu", command=self.fines_win.destroy,
                                  compound='center', border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.close_btn.place(x=217, y=240)

    def open_reports(self):
        self.reports_win = Toplevel()
        self.reports_win.geometry('600x400')
        self.reports_win.title("Reports Menu")
        self.reports_win.label = Label(self.reports_win, image=self.subpageImage)
        self.reports_win.label.place(x=0, y=0)
        self.reports_win.intro_label = Label(self.reports_win, text='Reports Menu', font='Bold24')
        self.reports_win.intro_label.place(x=240, y=50)

        self.reports_btn = Button(self.reports_win, text="Book Search", command=ask_info, compound='center',
                                  border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.reports_btn.place(x=100, y=140)

        self.reports_btn = Button(self.reports_win, text="Books on Loan", command=books_on_loan,
                                  compound='center', border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.reports_btn.place(x=320, y=140)


        self.reports_btn = Button(self.reports_win, text="Books on Reservation", command=reservation_report,
                                  compound='center', border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.reports_btn.place(x=100, y=200)


        self.reports_btn = Button(self.reports_win, text="Outstanding Fines", command=fine_report_page,
                                  compound='center', border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.reports_btn.place(x=320, y=200)

        self.reports_btn = Button(self.reports_win, text="Books on Loan to Member", command=books_on_loan_to_member,
                                  compound='center', border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.reports_btn.place(x=100, y=260)


        self.close_btn = Button(self.reports_win, text="Back to Main Menu", command=self.reports_win.destroy,
                                  compound='center', border=0, height=50, \
                                  width=166, image=self.subpage_buttonImage, activeforeground='black')
        self.close_btn.place(x=320, y=260)


    def creat_manu(self):
        self.membership_win_bn = Button(self.root, text="Membership", compound='center', border=0,
                                        command=self.open_membership, height=100, \
                                        width=166, image=self.buttonImage, activeforeground='black', font='bold30')
        self.membership_win_bn.place(x=150, y=150)

        self.book_win_bn = Button(self.root, text="Book", compound='center', border=0,
                                  command=self.open_book, height=100, \
                                  width=166, image=self.buttonImage, activeforeground='black', font='bold30')
        self.book_win_bn.place(x=320, y=150)

        self.loans_win_bn = Button(self.root, text="Loans", compound='center', border=0,
                                   command=self.open_loans, height=100, \
                                   width=166, image=self.buttonImage, activeforeground='black', font='bold30')
        self.loans_win_bn.place(x=490, y=150)

        self.reservaiton_win_bn = Button(self.root, text="Reservation", compound='center', border=0,
                                         command=self.open_reservations, height=100, \
                                         width=166, image=self.buttonImage, activeforeground='black', font='bold30')
        self.reservaiton_win_bn.place(x=150, y=250)

        self.fines_win_bn = Button(self.root, text="Fine", compound='center', border=0,
                                   command=self.open_fines, height=100, \
                                   width=166, image=self.buttonImage, activeforeground='black', font='bold30')
        self.fines_win_bn.place(x=320, y=250)

        self.reports_win_bn = Button(self.root, text="Report", compound='center', border=0,
                                     command=self.open_reports, height=100, \
                                     width=166, image=self.buttonImage, activeforeground='black', font='bold30')
        self.reports_win_bn.place(x=490, y=250)


    def init_book(self):
        con = connection()
        book_info = pd.read_csv('LibBooks.txt')
        count = 1

        for i in range(book_info.shape[0]):
            for j in [2,3,4]:
                check_authorid = True
                check_Name = True
                if pd.isna(book_info.iloc[i,j]) == False:
                    AuthorID = count
                    FirstName = ' '.join(str(book_info.iloc[i,j]).split()[:-1])
                    LastName = str(book_info.iloc[i,j]).split()[-1]
                    #print(AuthorID,FirstName,LastName)
                    with con.cursor() as cur:
                        view = 'SELECT AuthorID from Author'
                        cur.execute(view)
                        results = cur.fetchall()
                        for result in results:
                            if AuthorID in result:
                                print("Author already exists!")
                                check_authorid = False

                        #check replicate author
                        view = 'SELECT FirstName, LastName from Author'
                        cur.execute(view)
                        names = cur.fetchall()
                        if (FirstName,LastName) in names:
                            print("Author already exists!")
                            check_Name = False
                    if check_Name and check_authorid:
                        insert = str((AuthorID, str(FirstName), LastName))
                        # print(insert)
                        insert = 'INSERT INTO Author(AuthorID,FirstName,LastName) VALUES ' + insert
                        try:
                            with con.cursor() as cur:
                                cur.execute(insert)
                                con.commit()
                        finally:
                            con.close
                    count += 1


        #for book data
        for i in range(book_info.shape[0]):
            check_AN = True
            AccessionNumber = book_info.iloc[i,0]
            Title = book_info.iloc[i,1]
            ISBN = book_info.iloc[i,5]
            Publisher = book_info.iloc[i,-2]
            PublicationYear = book_info.iloc[i, -1]
            with con.cursor() as cur:
                view = 'SELECT AccessionNumber from Book'
                cur.execute(view)
                results = cur.fetchall()
                for result in results:
                    if AccessionNumber in result:
                        print("Book already exists!")
                        check_AN = False
            if check_AN:
                insert = str((AccessionNumber,Title,ISBN,Publisher,PublicationYear))
                #print(insert)
                insert = 'INSERT INTO Book(AccessionNumber,Title,ISBN,Publisher,PublicationYear) VALUES ' + insert
                try:
                    with con.cursor() as cur:
                        cur.execute(insert)
                        con.commit()
                finally:
                    con.close

        #for write relationship
        for i in range(book_info.shape[0]):
            for j in [2, 3, 4]:
                if pd.isna(book_info.iloc[i, j]) == False:
                    AccessionNumber = book_info.iloc[i,0]
                    FirstName_c = ' '.join(str(book_info.iloc[i, j]).split()[:-1])
                    LastName_c = str(book_info.iloc[i, j]).split()[-1]

                    with con.cursor() as cur:
                        view = 'SELECT AuthorID from Author WHERE FirstName = "'+ FirstName_c+'" AND LastName= "' + LastName_c+'"'
                        cur.execute(view)
                        AuthorID_W = cur.fetchall()
                        AuthorID_W = AuthorID_W[0][0]

                        view = 'SELECT * from Writes'
                        cur.execute(view)
                        results = cur.fetchall()

                        if (AuthorID_W,AccessionNumber) in results:
                            print('Write relationship already exists!')
                            continue
                        else:
                            insert = str((AuthorID_W,AccessionNumber))
                            insert = 'INSERT INTO Writes(AuthorID,AccessionNumber) VALUES ' + insert
                            try:
                                with con.cursor() as cur:
                                    cur.execute(insert)
                                    con.commit()
                            finally:
                                con.close


if __name__ == "__main__":
    gw = GuiWindow()
    gw.root.mainloop()