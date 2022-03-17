from tkinter import *
from connection import*
import datetime
from book_return import*
import pymysql
from tkinter import messagebox
from datetime import datetime, timedelta
from PIL import Image, ImageTk

#def open_loans():
#    loans_win = Toplevel()
#    #loans_win.geometry('800x500')
#    loans_win.title("Loans Menu")
#    borrow_btn = Button(loans_win, text="Book Borrowing", command=borrow_page)
#    borrow_btn.pack()
#    return_btn = Button(loans_win, text="Book Returning", command = return_page)
#    return_btn.pack()
#    close_btn = Button(loans_win, text="Back to Main Menu", command= loans_win.destroy)
#    close_btn.pack()


def borrow_page():
    borrow_win = Toplevel()
    borrow_win.geometry('400x300')
    loadImg = Image.open('blueblossom.png')
    backgroundImage = ImageTk.PhotoImage(loadImg)
    borrow_win.image = backgroundImage
    background_label = Label(borrow_win, image=backgroundImage)
    background_label.place(x =0, y = 0)
    borrow_win.title("Borrow Menu")

    welcome_label = Label(borrow_win, text= "To Borrow a Book, Please Enter Information Below:")
    welcome_label.place(x=55, y = 30)

    Accession_label = Label(borrow_win, text='Enter Accession Number')
    Accession = Entry(borrow_win, width=20, bg="white")
    Membership_label = Label(borrow_win, text='Enter Membership ID')
    Membership_id = Entry(borrow_win, width=20, bg="white")

    Accession_label.place(x= 127, y =140)
    Accession.place(x = 129, y = 165)
    Membership_label.place(x=135, y=80)
    Membership_id.place(x= 129, y = 105)

    def create_borrow_detail():
        Accession_info = Accession.get()
        Membership_id_info = Membership_id.get()
        BorrowDate = datetime.today().date()
        delta = timedelta(days=14)
        Duedate = BorrowDate+delta
        book_title = ''
        member_name = ''


        if Accession_info == '' or Membership_id_info=='':
            return messagebox.showwarning('',"Please complete your information")
            #Label(borrow_win,text = response).pack()
        else:
            con = connection()
            # check if the accession number already exits
            check_AN = True
            check_AN_command = 'SELECT AccessionNumber FROM Book'
            with con.cursor() as cur:
                cur.execute(check_AN_command)
                AN_result = cur.fetchall()
                con.close
            for AN in AN_result:
                if Accession_info in AN:
                    check_AN = False

            # check if the membership already exits
            check_MID = True
            check_command = 'SELECT MemberID FROM Member'
            with con.cursor() as cur:
                cur.execute(check_command)
                results = cur.fetchall()
                con.close
            for result in results:
                if Membership_id_info in result:
                    check_MID = False

            if check_AN or check_MID:
                return messagebox.showwarning('',"Your information is invalid, please check!")
                #Label(borrow_win, text=response).pack()
            else:
                borrow_detail = Toplevel()
                borrow_detail.geometry('300x300')
                Img = Image.open('green_flowers_final.png')
                borrow_detail.title("Confirm Details")


                confirm_backgroundImage = ImageTk.PhotoImage(Img)
                borrow_detail.background_label = Label(borrow_detail, image=confirm_backgroundImage)
                borrow_detail.background_label.place(x=0, y=0)
                borrow_detail.background_label.image = confirm_backgroundImage
                with con.cursor() as cur:
                    view = 'SELECT Title from Book WHERE AccessionNumber = "' + str(Accession_info)+'"'
                    cur.execute(view)
                    results = cur.fetchall()
                    for result in results:
                        for title in result:
                            book_title = title

                    view = 'SELECT FirstName, LastName from Member WHERE MemberID = "' + str(Membership_id_info)+'"'
                    cur.execute(view)
                    results = cur.fetchall()
                    for (FirstName,LastName) in results:
                        member_name = ' '.join((FirstName,LastName))
                    con.close
                
                borrow_detail_label = Label(borrow_detail, text='Borrowing Details', font='bold20')
                borrow_detail_label.place(x=80,y=15)
                
                bd_Accession = Label(borrow_detail, text='Accession Number: '+str(Accession_info))
                bd_Booktitle = Label(borrow_detail, text='Book Title: ' + str(book_title))
                bd_borrowdate = Label(borrow_detail, text='Borrow Date: ' + str(BorrowDate))
                bd_MemberName = Label(borrow_detail, text='Membership ID: ' + str(Membership_id_info))
                bd_Membership = Label(borrow_detail, text='Member Name: ' + str(member_name))
                bd_duedate = Label(borrow_detail, text='Due Date: ' + str(Duedate))

                bd_Accession.place(x = 65, y=50)
                bd_Booktitle.place(x = 65, y=80)
                bd_borrowdate.place(x = 65, y=110)
                bd_Membership.place(x = 65, y = 140)
                bd_MemberName.place(x = 65, y= 170)
                bd_duedate.place(x = 65, y= 200)

                borrow_confirm_btn = Button(borrow_detail, text="Confirm Loan", command=insert_borrow)
                borrow_confirm_btn.place(x = 65, y= 235)
                close_detail_btn = Button(borrow_detail, text="Back to Loan Menu", command=borrow_detail.destroy)
                close_detail_btn.place(x = 65, y= 270)


    def insert_borrow():
        con = connection()
        Accession_info = Accession.get()
        Membership_id_info = Membership_id.get()
        BorrowDate = datetime.today().date()
        borrow_num = 0
        check_fine = 0

        #check if already be borrowed
        check_command = 'SELECT AccessionNumber FROM Borrow'
        check_b = False
        get_rdate = ''
        with con.cursor() as cur:
            cur.execute(check_command)
            results = cur.fetchall()
            con.close
        for result in results:
            if Accession_info in result:
                check_b = True
        #check loan number
        command = 'SELECT COUNT(*) FROM Borrow WHERE MemberID ="' + str(Membership_id_info)+'"'
        with con.cursor() as cur:
            cur.execute(command)
            results = cur.fetchall()
            con.close
        for result in results:
            for num in result:
                borrow_num = num
                #print("borrow_num",borrow_num)

        #check fine
        check_command = 'SELECT FineAmount FROM Member WHERE MemberID ="' + str(Membership_id_info)+'"'
        with con.cursor() as cur:
            cur.execute(check_command)
            results = cur.fetchall()
            con.close
        for result in results:
            for num in result:
                check_fine = num

        # check reservation
        check_reserv = False
        check_reserv_exist = False

        check_rv_command = 'SELECT AccessionNumber FROM Reserve WHERE MemberID ="' + str(Membership_id_info) + '"'
        check_rv_exist_command = 'SELECT AccessionNumber FROM Reserve'
        with con.cursor() as cur:
            cur.execute(check_rv_command)
            rv_result = cur.fetchall()
            cur.execute(check_rv_exist_command)
            rv_exist_result = cur.fetchall()
            con.close
        for rv in rv_result:
            if Accession_info in rv:
                check_reserv = True
        for rv in rv_exist_result:
            if Accession_info in rv:
                check_reserv_exist = True

        #print("check_reserv",check_reserv)
        #print("check_reserv_exist",check_reserv_exist)
        # if any errors occur, pop the error message window
        if check_b:
            check_command = 'SELECT BorrowDate FROM Borrow WHERE AccessionNumber ="' + str(Accession_info)+'"'
            with con.cursor() as cur:
                cur.execute(check_command)
                results = cur.fetchall()
                con.close
            for result in results:
                for date in result:
                    get_rdate = date+timedelta(days=14)

            return messagebox.showerror('',"The book has been borrowed until "+ str(get_rdate))
            #Label(borrow_win, text=response).pack()
        elif borrow_num>=2:
            return messagebox.showerror('',"Member loan quota exceeded!")
            #Label(borrow_win, text=response).pack()
        elif check_fine>0:
            return messagebox.showerror('',"Member has outstanding fines!")
            #Label(borrow_win, text=response).pack()
        elif check_reserv == False and check_reserv_exist == True:
            return messagebox.showerror('',"The Book has been reserved by someone else!")
            #Label(borrow_win, text=response).pack()
        else:

            # delete reserve after borrow
            if check_reserv and check_reserv_exist:
                delete_reserv_insert = 'DELETE FROM Reserve WHERE AccessionNumber ="' + str(Accession_info) + '" AND MemberID = "' + str(Membership_id_info) + '"'
                try:
                    with con.cursor() as cur:
                        cur.execute(delete_reserv_insert)
                        con.commit()
                finally:
                    con.close

            insert = str((Accession_info,Membership_id_info,str(BorrowDate)))
            insert = 'INSERT INTO Borrow (AccessionNumber,MemberID,BorrowDate) VALUES ' + insert
            try:
                with con.cursor() as cur:
                    cur.execute(insert)
                    con.commit()
                    messagebox.showinfo('',"The borrow has been confirmed!")
            finally:
                con.close
            #Label(borrow_win, text=response).pack()

    borrow_btn = Button(borrow_win, text="Borrow Book", command=create_borrow_detail)
    borrow_btn.place(x = 158, y = 210)
    close_btn = Button(borrow_win, text="Back to Loan Menu", command=borrow_win.destroy)
    close_btn.place(x = 140, y = 245)
