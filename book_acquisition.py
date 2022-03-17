from cProfile import label
from errno import EROFS
from optparse import check_builtin
from tkinter import*
from connection import*
from PIL import Image, ImageTk

# the following code works for page 17, 18, 19
def create_book():
    BAPage = Toplevel()
    BAPage.geometry('400x300')
    loadImg1 = Image.open('blueblossom.png')
    backgroundImage = ImageTk.PhotoImage(loadImg1)
    loadImg2 = Image.open('green_flowers_final.png')
    bgi = ImageTk.PhotoImage(loadImg2)
    background_label = Label(BAPage, image=backgroundImage)
    background_label.place(x = 0, y = 0)
    BAPage.title("Book Acquisition")


    # create title of the page
    page_title = Label(BAPage, text = "Please Enter Required Book Information Below:")
    page_title.place(x = 60, y = 25)

    # create labels for each entry
    accession_number_label = Label(BAPage, text='Accession Number')
    title_label = Label(BAPage, text='Title')
    authors_label = Label(BAPage, text='Author Name(s)')
    ISBN_label = Label(BAPage, text='ISBN')
    publisher_label = Label(BAPage, text='Publisher')
    publication_year_label = Label(BAPage, text='Publication Year')

    # create entries for all info
    accession_number_entry = Entry(BAPage, width=20, fg='black')
    title_entry = Entry(BAPage, width=20, fg='black')
    authors_entry = Entry(BAPage, width=20, fg='black')
    ISBN_entry = Entry(BAPage, width=20, fg='black')
    publisher_entry = Entry(BAPage, width=20, fg='black')
    publication_year_entry = Entry(BAPage, width=20, fg='black')

    # pack all the labels and entries in order
    accession_number_label.place(x= 60, y =70)
    accession_number_entry.place(x= 198, y =70)
    title_label.place(x= 60, y =100)
    title_entry.place(x= 198, y =100)
    authors_label.place(x= 60, y =130)
    authors_entry.place(x= 198, y =130)
    ISBN_label.place(x= 60, y =160)
    ISBN_entry.place(x= 198, y =160)
    publisher_label.place(x= 60, y =190)
    publisher_entry.place(x= 198, y =190)
    publication_year_label.place(x= 60, y =220)
    publication_year_entry.place(x= 198, y =220)

    def add_book():
        accession_number = accession_number_entry.get()
        title = title_entry.get()
        authors = authors_entry.get()
        # ***conversion to get AuthorIDs
        ISBN = ISBN_entry.get()
        publisher = publisher_entry.get()
        publication_year = publication_year_entry.get()

        # check if the accession number already exits
        check_AN = False
        check_AN_command = 'SELECT AccessionNumber FROM Book'
        con = connection()
        with con.cursor() as cur:
            cur.execute(check_AN_command)
            AN_result = cur.fetchall()
            con.close
        for AN in AN_result:
            if accession_number in AN:
                check_AN = True
        # check if any field input is empty
        check_input = False
        if accession_number == '':
            check_input = True
        if title == '':
            check_input = True
        if authors == '':
            check_input = True
        if ISBN == '':
            check_input = True
        if publisher == '':
            check_input = True
        if publication_year == '':
            check_input = True
        # if any errors occur, pop the error message window
        if check_AN == True or check_input == True:
            error = Toplevel()
            error.title("Error in Book Acquisition")
            error.geometry('300x300')
            background_label = Label(error, image=bgi)
            background_label.place(x = 0, y = 0)
            error_message1 = Label(error, text = "Error!")
            error_message1.place(x = 130, y =60)
            error_message2 = Label(error, text = '''Book already added; 
Duplicate, Missing or Incomplete fields!''')
            error_message2.place(x = 32, y = 130)
            return_button = Button(error, text = "Back to Acquisition Function", \
            command = error.destroy)
            return_button.place(x = 65, y = 230)
        # if no error occurs add the data into the database
        else:
            # add book to the Book table
            add_book_command = "INSERT INTO Book VALUES(" + "'" + accession_number + "'" + "," + "'" + title + "'" + ',' + "'" + ISBN + "'" + ',' + "'" + publisher + "'" + ',' + "'" + publication_year + "'" + ")"
            con = connection()
            try:
                with con.cursor() as cur:
                    cur.execute(add_book_command)
                    con.commit()
            finally:
                con.close
            # add author to the Author table
            while authors != "":
                if authors.find(",") != -1:
                    idxcomma = authors.find(",")
                    this_author = authors[:idxcomma]
                    authors = authors[idxcomma+2:]
                else:
                    this_author = authors
                    authors = ""
                if this_author.find(" ") != -1:
                    idxspace = this_author.rfind(" ")
                    this_first_name = this_author[:idxspace]
                    this_first_name_quote = "'" + this_first_name + "'"
                    this_last_name = this_author[idxspace+1:]
                    this_last_name_quote = "'" + this_last_name + "'"
                    # check if the author already exists in the Author table
                    find_author_command = 'SELECT FirstName, LastName FROM Author'
                    con = connection()
                    with con.cursor() as cur:
                        cur.execute(find_author_command)
                        author_names_result = cur.fetchall()
                        con.close
                    check_exist = False
                    if (this_first_name, this_last_name) in author_names_result:
                        check_exist = True
                    if check_exist == False:
                        add_author_command = 'INSERT INTO Author(FirstName, LastName) VALUES(' + this_first_name_quote + ',' + this_last_name_quote + ')'
                        con = connection()
                        try:
                            with con.cursor() as cur:
                                cur.execute(add_author_command)
                                con.commit()
                        finally:
                            con.close
                    # add record into the Writes table
                    find_authorid_command = 'SELECT AuthorID from Author WHERE FirstName = ' + this_first_name_quote + 'AND LastName = ' + this_last_name_quote 
                    with con.cursor() as cur:
                        cur.execute(find_authorid_command)
                        authorid_result = cur.fetchall()
                        con.close
                    authorid_result = authorid_result[0][0]
                    insert_write_command = 'INSERT INTO Writes VALUES(' + str(authorid_result) + "," + "'" + accession_number + "'" + ')'
                    try:
                        with con.cursor() as cur:
                            cur.execute(insert_write_command)
                            con.commit()
                    finally:
                        con.close
                else:
                    this_last_name = this_author
                    this_last_name_quote = "'" + this_last_name + "'"
                    # check if the author already exists in the Author table
                    find_author_command = 'SELECT FirstName, LastName FROM Author'
                    con = connection()
                    with con.cursor() as cur:
                        cur.execute(find_author_command)
                        author_names_result = cur.fetchall()
                        con.close
                    check_exist = False
                    if (None, this_last_name) in author_names_result:
                        check_exist = True
                    if check_exist == False:
                        add_author_command = 'INSERT INTO Author(LastName) VALUES(' + this_last_name_quote + ')'
                        con = connection()
                        try:
                            with con.cursor() as cur:
                                cur.execute(add_author_command)
                                con.commit()
                        finally:
                            con.close
                    # add record into the Writes table
                    find_authorid_command = "SELECT AuthorID from Author WHERE FirstName IS NULL "+ 'AND LastName = ' + this_last_name_quote
                    with con.cursor() as cur:
                        cur.execute(find_authorid_command)
                        authorid_result = cur.fetchall()
                        con.close
                    authorid_result = authorid_result[0][0]
                    insert_write_command = 'INSERT INTO Writes VALUES(' + str(authorid_result) + "," + "'" + accession_number + "'" + ')'
                    try:
                        with con.cursor() as cur:
                            cur.execute(insert_write_command)
                            con.commit()
                    finally:
                        con.close
            # pop the success message window
            success = Toplevel()
            success.title("Success")
            success.geometry('300x300')
            background_label = Label(success, image=bgi)
            background_label.place(x = 0, y = 0)
            success_message1 = Label(success, text = "Success!")
            success_message1.place(x = 130, y = 50)
            success_message2 = Label(success, text = "New Book added in Library!")
            success_message2.place(x = 70, y = 140)    
            return_button = Button(success, text = "Return to Acquisition Function", \
            command = success.destroy)
            return_button.place(x = 66, y = 230)

    # create the add new book button back to menus button
    add_new_book_button = Button(BAPage, text="Add New Book", command = add_book)
    add_new_book_button.place(x = 60, y =260)
    back_to_books_menu_button = Button(BAPage, text="Back to Books Menu", command = BAPage.destroy)
    back_to_books_menu_button.place(x = 205, y =260)

    BAPage.mainloop()
