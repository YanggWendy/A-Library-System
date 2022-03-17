from cProfile import label
from errno import EROFS
from optparse import check_builtin
from tkinter import*
from connection import*
from PIL import Image, ImageTk

def withdraw_book():
    # the following code works for page 20, 21, 22, 23
    BWPage = Toplevel()
    BWPage.geometry('400x300')
    loadImg1 = Image.open('blueblossom.png')
    backgroundImage = ImageTk.PhotoImage(loadImg1)
    loadImg2 = Image.open('green_flowers_final.png')
    bgi = ImageTk.PhotoImage(loadImg2)
    background_label = Label(BWPage, image=backgroundImage)
    background_label.place(x = 0, y = 0)
    BWPage.title("Book Withdrawal")

    # create title of the page
    page_title = Label(BWPage, text = '''To Remove Outdated Books From System, 
Please Enter Required Information Below:''')
    page_title.place(x = 70, y = 40)

    # enquire accession number of the book to be withdrawn
    accession_num_label = Label(BWPage, text = "Accession Number:")
    accession_num_label.place(x = 140, y = 105)

    accession_num_entry = Entry(BWPage, width = 20)
    accession_num_entry.place(x = 126, y = 150)

    # pop new windows based on the accession number entered
    def withdraw_book():
        accession_num = accession_num_entry.get()
        con = connection()
        with con.cursor() as cur:
            # check if the accession number entered exists in the database
            check_book_table = 'SELECT AccessionNumber FROM Book'
            # exist will be set to be True if the book is found in the database
            exist_check = False
            cur.execute(check_book_table)
            book_results = cur.fetchall()
            con.close
        for result in book_results:
            if accession_num in result:
                exist_check = True
        # return an error message pop-up if the book is not found in the database
        if exist_check == False:
            not_found_error = Toplevel()
            not_found_error.title("Book not Found")
            not_found_error.geometry('300x300')
            background_label = Label(not_found_error, image=bgi)
            background_label.place(x = 0, y = 0)
            error_message = Label(not_found_error, text = "Book not Found!")
            error_message.place(x = 103, y = 100)
            return_button = Button(not_found_error, text = "Return to Withdrawal Function", \
            command = not_found_error.destroy)
            return_button.place(x = 57, y = 190)
        # otherwise, the book exists
        # check if the book is on loan
        check_loan_table = 'SELECT AccessionNumber FROM Borrow'
        loan_check = False
        con = connection()
        with con.cursor() as cur:
            cur.execute(check_loan_table)
            loan_results = cur.fetchall()
            con.close
        for result in loan_results:
            if accession_num in result:
                loan_check = True
        # return an error message pop-up if the book is found in the loan table        
        if loan_check == True:
            loan_found_error = Toplevel()
            loan_found_error.title("Book not Found")
            loan_found_error.geometry('300x300')
            background_label = Label(loan_found_error, image=bgi)
            background_label.place(x = 0, y = 0)
            error_message = Label(loan_found_error, text = "Book is currently on Loan!")
            error_message.place(x = 70, y = 100)
            return_button = Button(loan_found_error, text = "Return to Withdrawal Function", \
            command = loan_found_error.destroy)
            return_button.place(x = 57, y = 190)
        # check if the book is on reservation
        check_reservation_table = 'SELECT AccessionNumber FROM Reserve'
        reservation_check = False
        con = connection()
        with con.cursor() as cur:
            cur.execute(check_reservation_table)
            reservation_results = cur.fetchall()
            con.close
        for result in reservation_results:
            if accession_num in result:
                reservation_check = True
        # return an error message pop-up if the book is found in the reservation table        
        if reservation_check == True:
            reservation_found_error = Toplevel()
            reservation_found_error.title("Book not Found")
            error_message = Label(reservation_found_error, text = "Book is currently Reserved!")
            error_message.pack()
            return_button = Button(reservation_found_error, text = "Return to Withdrawal Function", \
            command = reservation_found_error.destroy)
            return_button.pack()
        # after checking all the conditions, no problems are found
        # return the book information and confirm if the book will be withdrawn
        # now find all the information about the book from the book table
        if reservation_check == False and loan_check == False and exist_check == True:
            book_info_page = Toplevel()
            book_info_page.geometry('300x300')
            background_label = Label(book_info_page, image=bgi)
            background_label.place(x = 0, y = 0)
            book_info_page.title("Please Confirm Details to Be Correct")
            book_info_command = '''SELECT AccessionNumber, Title, ISBN, 
            Publisher, PublicationYear
            FROM Book
            WHERE AccessionNumber = ''' + "'" + accession_num + "'"
            con = connection()
            with con.cursor() as cur:
                cur.execute(book_info_command)
                book_info = cur.fetchall()
                con.close
            title = book_info[0][1]
            ISBN = book_info[0][2]
            Publisher = book_info[0][3]
            PublicationYear = book_info[0][4]
            # find the AuthorIDs related to the book from the write table
            author_id_command = 'SELECT AuthorID FROM Writes WHERE AccessionNumber = ' + "'" + accession_num + "'"
            con = connection()
            with con.cursor() as cur:
                cur.execute(author_id_command)
                author_id_result = cur.fetchall()
                con.close
            # create a tuple of AuthorIDs
            author_id = ()
            for id in author_id_result:
                author_id = author_id + id
            # find the names of each existing author in a tuple
            author_names = ()
            for id in author_id:
                author_command = 'SELECT FirstName, LastName FROM Author WHERE AuthorID = ' + str(id)
                con = connection()
                with con.cursor() as cur:
                    cur.execute(author_command)
                    author_names_result = cur.fetchall()
                    con.close
                for names in author_names_result:
                    if names[0] is not None:
                        author_names = author_names + (names[0] + " " + names[1],)
                    else:
                        author_names = author_names + (names[1],)
            # create labels for each piece of info
            Accession_num_Label = Label(book_info_page, text = ("Accession Number: " + accession_num))
            title_label = Label(book_info_page, text = ("Title: " + title))
            ISBN_label = Label(book_info_page, text = ("ISBN: " + ISBN))
            Publisher_label = Label(book_info_page, text = ("Publisher: " + Publisher))
            PublicationYear_label = Label(book_info_page, text = ("Publication Year: " + PublicationYear))
            author_text = "Author(s):"
            author_num = len(author_names)
            author_count = 0
            for author in author_names:
                author_count += 1
                if author_count == author_num:
                    author_text = author_text + " " + author
                else:
                    author_text = author_text + " " + author + ","
            author_label = Label(book_info_page, text = author_text)
            # pack all the labels
            Accession_num_Label.place(x = 30, y = 30)
            title_label.place(x = 30, y = 60)
            ISBN_label.place(x = 30, y = 90)
            Publisher_label.place(x = 30, y = 120)
            PublicationYear_label.place(x = 30, y = 150)
            author_label.place(x = 30, y = 180)
            # create function to confirm withdrawal
            def withdrawal():
                # firstly, delete the write record from the Writes table
                con = connection()
                with con.cursor() as cur: 
                    delete_writes_command = 'DELETE FROM Writes WHERE AccessionNumber =' + "'" + accession_num + "'"
                    cur.execute(delete_writes_command)
                    con.commit()
                    con.close
                # secondly, delete the book from the Book table
                con = connection()
                with con.cursor() as cur: 
                    delete_book_command = 'DELETE FROM Book WHERE AccessionNumber =' + "'" + accession_num + "'"
                    cur.execute(delete_book_command)
                    con.commit()
                    con.close      
                # thirdly, delete the author from the author table if the author does not write other books
                # find the remaining AuthorIDs in the writes table
                con = connection()
                with con.cursor() as cur: 
                    find_remaining_command = 'SELECT AuthorID FROM Writes'
                    cur.execute(find_remaining_command)
                    remaining = cur.fetchall()
                    con.close
                # use the tuple of AuthorID created previously, find remaining authors who will not be deleted
                remaining_author = ()
                for id in author_id:
                    for record in remaining:
                        if id in record:
                            remaining_author += (id,)
                # compare and find out the authors to be deleted from the author table
                author_to_delete = ()
                for id in author_id:
                    if id not in remaining_author:
                        author_to_delete += (id,)
                # delete authors in the author table
                for id in author_to_delete:
                    con = connection()
                    with con.cursor() as cur: 
                        delete_author_command = 'DELETE FROM Author WHERE AuthorID = ' + str(id)
                        cur.execute(delete_author_command)
                        con.commit()
                        con.close
                success = Toplevel()
                success.title("Success")
                success.geometry('300x300')
                background_label = Label(success, image=bgi)
                background_label.place(x = 0, y = 0)
                success_message = Label(success, text = "Book successfully removed!")
                success_message.place(x = 70, y = 100)    
                return_button = Button(success, text = "Return to Withdrawal Function", \
                command = success.destroy)
                return_button.place(x = 62, y = 170)               
            # button to confirm withdrawal               
            confirm_button = Button(book_info_page, text = "Confirm Withdrawal", \
            command = withdrawal)
            confirm_button.place(x = 30, y = 215)

            # create button to return to withdrawal function
            return_button = Button(book_info_page, text = "Return to Withdrawal Function", \
            command = book_info_page.destroy)
            return_button.place(x = 30, y = 255)
            
    # create button to verify book information
    withdraw_button = Button(BWPage, text = "Withdraw Book", \
                        command = withdraw_book)
    withdraw_button.place(x = 145, y = 190)

    # create back to book menu button
    return_button = Button(BWPage, text = "Back to Books Menu", \
                        command = BWPage.destroy)
    return_button.place(x = 131, y = 240)
    BWPage.mainloop()
