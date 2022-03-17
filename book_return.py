from tkinter import *
from connection import*
import datetime
from tkinter import messagebox
import pymysql
from datetime import datetime
from PIL import Image, ImageTk

def return_page():
    return_win = Toplevel()
    return_win.title("Return Menu")
    return_win.geometry('400x300')
    loadImg = Image.open('blueblossom.png')
    backgroundImage = ImageTk.PhotoImage(loadImg)
    return_win.image = backgroundImage
    background_label = Label(return_win, image=backgroundImage)
    background_label.place(x=0, y=0)

    welcome_label = Label(return_win, text="To Return a Book, Please Enter Information Below:")

    welcome_label.place(x=25, y=30)

    Accession = Entry(return_win, width=20, bg="white")
    Return_id = Entry(return_win, width=20, bg="white")
    Accession_label = Label(return_win, text='Enter Accession Number:')
    Return_label = Label(return_win, text='Enter Return Date in YYYY-MM-DD Format:')

    Accession_label.place(x=127, y=75)
    Accession.place(x=130, y=105)
    Return_label.place(x=80, y=140)
    Return_id.place(x=130, y=170)

    close_btn = Button(return_win, text="Back to Loan Menu", command=return_win.destroy)
    close_btn.place(x = 140, y = 245)


    def create_return_detail():
        Accession_info = Accession.get()
        Return_info = Return_id.get()
        book_title = ''
        member_name = ''
        borrowdate = ''
        fine_amount = 0
        memberid = ''


        if Accession_info == '' or Return_info == '':
            response = messagebox.showwarning('',"Please complete your information")
            #Label(return_win, text=response).pack()
        else:
            con = connection()
            # check if the accession number already exits
            check_AN = True
            check_AN_command = 'SELECT AccessionNumber FROM Borrow'
            with con.cursor() as cur:
                cur.execute(check_AN_command)
                AN_result = cur.fetchall()
                con.close
            for AN in AN_result:
                if Accession_info in AN:
                    check_AN = False

            if check_AN:
                response = messagebox.showwarning('',"Your information is invalid, please check!")
                #Label(return_win, text=response).pack()
            else:
                return_detail = Toplevel()
                return_detail.title("Confirm Return Detail to be Correct")
                return_detail.geometry('300x300')
                Img = Image.open('green_flowers_final.png')

                confirm_backgroundImage = ImageTk.PhotoImage(Img)
                return_detail.background_label = Label(return_detail, image=confirm_backgroundImage)
                return_detail.background_label.place(x=0, y=0)
                return_detail.background_label.image = confirm_backgroundImage

                #get other details from database
                with con.cursor() as cur:
                    view = 'SELECT Title from Book WHERE AccessionNumber = "' + str(Accession_info)+'"'
                    cur.execute(view)
                    results = cur.fetchall()
                    for result in results:
                        for title in result:
                            book_title = title
                    view = 'SELECT MemberID from Borrow WHERE AccessionNumber = "' + str(Accession_info) + '"'
                    cur.execute(view)
                    results = cur.fetchall()
                    for result in results:
                        for id in result:
                            memberid = id

                    view = 'SELECT FirstName, LastName from Member WHERE MemberID = "' + str(memberid)+'"'
                    cur.execute(view)
                    results = cur.fetchall()
                    for (FirstName,LastName) in results:
                        member_name = ' '.join((FirstName,LastName))

                    view = 'SELECT BorrowDate from Borrow WHERE AccessionNumber = "' + str(Accession_info) + '"'
                    cur.execute(view)
                    results = cur.fetchall()
                    for result in results:
                        for date in result:
                            borrowdate = date
                    con.close
                #calculate fine
                Return_info = datetime.strptime(Return_info,'%Y-%m-%d').date()
                if (Return_info-borrowdate).days>14:
                    fine_amount = (Return_info-borrowdate).days -14
                rt_Accession = Label(return_detail, text='Accession Number '+str(Accession_info))
                rt_Booktitle = Label(return_detail, text='Book Title ' + str(book_title))
                rt_Membership = Label(return_detail, text='Membership ID ' + str(memberid))
                rt_Membername = Label(return_detail, text='Member Name ' + str(member_name))
                rt_returndate= Label(return_detail, text='Return Date ' + str(Return_info))
                rt_fine = Label(return_detail, text='Fine $' + str(fine_amount))

                rt_Accession.place(x=65, y=30)
                rt_Booktitle.place(x=65, y=60)
                rt_Membership.place(x=65, y=90)
                rt_Membername.place(x=65, y=120)
                rt_returndate.place(x=65, y=150)
                rt_fine.place(x=65, y=180)


                return_confirm_btn = Button(return_detail, text="Confirm Return", command=insert_return)
                return_confirm_btn.place(x=65, y=230)
                close_detail_btn = Button(return_detail, text="Back to Loan Menu", command=return_detail.destroy)
                close_detail_btn.place(x = 65, y= 265)

    def insert_return():
        con = connection()
        Accession_info = Accession.get()

        # calculate fine
        Return_info = Return_id.get()
        borrowdate = ''
        memberid = ''
        fine_amount = 0
        fine_amount_total = 0

        # check if the accession number  exits
        check_AN = True
        check_AN_command = 'SELECT AccessionNumber FROM Borrow'
        with con.cursor() as cur:
            cur.execute(check_AN_command)
            AN_result = cur.fetchall()
            con.close
        for AN in AN_result:
            if Accession_info in AN:
                check_AN = False
        if check_AN:
            response = messagebox.showinfo('',"The book is successfully returned!")

        view = 'SELECT BorrowDate from Borrow WHERE AccessionNumber = "' + str(Accession_info) + '"'
        with con.cursor() as cur:
            cur.execute(view)
            results = cur.fetchall()
            for result in results:
                for date in result:
                    borrowdate = date

            view = 'SELECT MemberID from Borrow WHERE AccessionNumber = "' + str(Accession_info) + '"'
            cur.execute(view)
            results = cur.fetchall()
            for result in results:
                for id in result:
                    memberid = id
            con.close

        Return_info = datetime.strptime(Return_info, '%Y-%m-%d').date()
        if (Return_info - borrowdate).days > 14:
            fine_amount = (Return_info - borrowdate).days - 14

        #check fine
        check_command = 'SELECT FineAmount FROM Member WHERE MemberID ="' + str(memberid)+'"'
        with con.cursor() as cur:
            cur.execute(check_command)
            results = cur.fetchall()
            con.close
        for result in results:
            for num in result:
                fine_orig = num
                fine_amount_total = fine_orig+fine_amount

        insert = 'DELETE FROM Borrow WHERE AccessionNumber ="' + str(Accession_info) + '"'
        update_fine = 'UPDATE Member SET FineAmount = ' + str(fine_amount_total) +' WHERE MemberID ="' + str(memberid)+'"'

        try:
            with con.cursor() as cur:
                cur.execute(insert)
                cur.execute(update_fine)
                con.commit()
        finally:
            con.close

        response = messagebox.showinfo('',"The Return has been confirmed!")
        #Label(return_win, text=response).pack()


    borrow_btn = Button(return_win, text="Return Book", command=create_return_detail)
    borrow_btn.place(x = 160, y = 210)
