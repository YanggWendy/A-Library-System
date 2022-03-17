from cProfile import label
from errno import EROFS
from optparse import check_builtin
from tkinter import*
from connection import*
from PIL import Image, ImageTk

# this root is just for testing

def ask_info():
    info = Toplevel()
    info.title("Search Book")
    loadImg = Image.open('sky.png')
    backgroundImage = ImageTk.PhotoImage(loadImg)
    info.image = backgroundImage
    background_label = Label(info, image=backgroundImage)
    background_label.place(x=0, y=0)
    page_title = Label(info, text = "Search based on the one of the categories below:")
    page_title.grid(row=0, column=0)

    title_label = Label(info, text='Title')
    authors_label = Label(info, text='Authors')
    ISBN_label = Label(info, text='ISBN')
    publisher_label = Label(info, text='Publisher')
    publication_year_label = Label(info, text='Publication Year')

    title_entry = Entry(info, width=20)
    authors_entry = Entry(info, width=20)
    ISBN_entry = Entry(info, width=20)
    publisher_entry = Entry(info, width=20)
    publication_year_entry = Entry(info, width=20)

    # pack all the labels and entries in order
    title_label.grid(row=1, column=0)
    title_entry.grid(row=2, column=0)
    authors_label.grid(row=3, column=0)
    authors_entry.grid(row=4, column=0)
    ISBN_label.grid(row=5, column=0)
    ISBN_entry.grid(row=6, column=0)
    publisher_label.grid(row=7, column=0)
    publisher_entry.grid(row=8, column=0)
    publication_year_label.grid(row=9, column=0)
    publication_year_entry.grid(row=10, column=0)

    def search_book():
        titlein = title_entry.get()
        authorsin = authors_entry.get()
        ISBNin = ISBN_entry.get()
        publisherin = publisher_entry.get()
        publication_yearin = publication_year_entry.get()
        # create checks for input values
        title_check = False
        authors_check = False
        ISBN_check = False
        publisher_check = False
        publication_year_check = False
        if titlein != "":
            if " " not in titlein:
                title_check = True
        if authorsin != "":
            if " " not in authorsin:
                authors_check = True
        if ISBNin != "":
            if " " not in ISBNin:
                ISBN_check = True
        if publisherin != "":
            if " " not in publisherin:
                publisher_check = True
        if publication_yearin != "":
            if " " not in publication_yearin:
                publication_year_check = True
        input_checks = [title_check, authors_check, ISBN_check, publisher_check, publication_year_check]
        # pop error if the inputs have issues
        if input_checks.count(True) != 1:
            error = Toplevel()
            error.title("Error in Book Search")
            error.image = backgroundImage
            background_label = Label(error, image=backgroundImage)
            background_label.place(x=0, y=0)
            error_message1 = Label(error, text = "Error in Book Search!")
            error_message1.pack()
            error_message2 = Label(error, text = "Missing or illegal inputs")
            error_message2.pack()
            return_button = Button(error, text = "Back to Book Search Function", \
            command = error.destroy, bg='skyblue1')
            return_button.pack()
        else:
            books = Toplevel()
            books.title("Book Search Results")
            # create labels and pack
            books.image = backgroundImage
            background_label = Label(books, image=backgroundImage)
            background_label.place(x=0, y=0)
            Accession_num_Label = Label(books, text = "Accession Number")
            title_label = Label(books, text = "Title")
            ISBN_label = Label(books, text = "ISBN")
            Publisher_label = Label(books, text = "Publisher")
            PublicationYear_label = Label(books, text = "Publication Year")
            author_label = Label(books, text = "Authors")
            Accession_num_Label.grid(row=0, column=0)
            title_label.grid(row=0, column=1)
            ISBN_label.grid(row=0, column=2)
            Publisher_label.grid(row=0, column=3)
            PublicationYear_label.grid(row=0, column=4)
            author_label.grid(row=0, column=5)
            # row count for grid
            row_count = 0
            if title_check == True:
                book_info_command = '''SELECT AccessionNumber, Title, ISBN, 
                Publisher, PublicationYear
                FROM Book
                WHERE Title = ''' + "'" + titlein + "' OR Title LIKE" + "'% " + titlein + "' OR Title LIKE" + "'" + titlein + " %' OR Title LIKE" + "'% " + titlein + " %'"
                con = connection()
                with con.cursor() as cur:
                    cur.execute(book_info_command)
                    book_info = cur.fetchall()
                    con.close
                for book in book_info:
                    row_count += 1
                    AN = book[0]
                    title = book[1]
                    ISBN = book[2]
                    Publisher = book[3]
                    PublicationYear = book[4]
                    # find the AuthorIDs related to the book from the write table
                    author_id_command = 'SELECT AuthorID FROM Writes WHERE AccessionNumber = ' + "'" + AN + "'" 
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
                        author_command = 'SELECT FirstName, LastName FROM Author WHERE AuthorID = ' + "'" + str(id) + "'" 
                        con = connection()
                        with con.cursor() as cur:
                            cur.execute(author_command)
                            author_names_result = cur.fetchall()
                            con.close
                        for names in author_names_result:
                            author_names = author_names + (names[0] + " " + names[1],)

                    # find names of all authors of the book
                    author_text = ""
                    author_num = len(author_names)
                    author_count = 0
                    for author in author_names:
                        author_count += 1
                        if author_count == author_num:
                            author_text = author_text + " " + author
                        else:
                            author_text = author_text + " " + author + ","
                    # for each piece of info of the book, create labels and pack them
                    Accession_num_Label1 = Label(books, text = AN)
                    title_label1 = Label(books, text = title)
                    ISBN_label1 = Label(books, text = ISBN)
                    Publisher_label1 = Label(books, text = Publisher)
                    PublicationYear_label1 = Label(books, text = PublicationYear)
                    author_label1 = Label(books, text = author_text)
                    Accession_num_Label1.grid(row=row_count, column=0)
                    title_label1.grid(row=row_count, column=1)
                    ISBN_label1.grid(row=row_count, column=2)
                    Publisher_label1.grid(row=row_count, column=3)
                    PublicationYear_label1.grid(row=row_count, column=4)
                    author_label1.grid(row=row_count, column=5)
            if ISBN_check == True:
                book_info_command = '''SELECT AccessionNumber, Title, ISBN, 
                Publisher, PublicationYear
                FROM Book
                WHERE ISBN = ''' + "'" + ISBNin + "'"
                con = connection()
                with con.cursor() as cur:
                    cur.execute(book_info_command)
                    book_info = cur.fetchall()
                    con.close
                for book in book_info:
                    row_count += 1
                    AN = book[0]
                    title = book[1]
                    ISBN = book[2]
                    Publisher = book[3]
                    PublicationYear = book[4]
                    # find the AuthorIDs related to the book from the write table
                    author_id_command = 'SELECT AuthorID FROM Writes WHERE AccessionNumber = ' + "'" + AN + "'" 
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
                        author_command = 'SELECT FirstName, LastName FROM Author WHERE AuthorID = ' + "'" + str(id) + "'" 
                        con = connection()
                        with con.cursor() as cur:
                            cur.execute(author_command)
                            author_names_result = cur.fetchall()
                            con.close
                        for names in author_names_result:
                            author_names = author_names + (names[0] + " " + names[1],)

                    # find names of all authors of the book
                    author_text = ""
                    author_num = len(author_names)
                    author_count = 0
                    for author in author_names:
                        author_count += 1
                        if author_count == author_num:
                            author_text = author_text + " " + author
                        else:
                            author_text = author_text + " " + author + ","
                    # for each piece of info of the book, create labels and pack them
                    Accession_num_Label1 = Label(books, text = AN)
                    title_label1 = Label(books, text = title)
                    ISBN_label1 = Label(books, text = ISBN)
                    Publisher_label1 = Label(books, text = Publisher)
                    PublicationYear_label1 = Label(books, text = PublicationYear)
                    author_label1 = Label(books, text = author_text)
                    Accession_num_Label1.grid(row=row_count, column=0)
                    title_label1.grid(row=row_count, column=1)
                    ISBN_label1.grid(row=row_count, column=2)
                    Publisher_label1.grid(row=row_count, column=3)
                    PublicationYear_label1.grid(row=row_count, column=4)
                    author_label1.grid(row=row_count, column=5)
            if publisher_check == True:
                book_info_command = '''SELECT AccessionNumber, Title, ISBN, 
                Publisher, PublicationYear
                FROM Book
                WHERE Publisher = ''' + "'" + publisherin + "' OR Publisher LIKE" + "'% " + publisherin + "' OR Publisher LIKE" + "'" + publisherin + " %' OR Publisher LIKE" + "'% " + publisherin + " %'"
                con = connection()
                with con.cursor() as cur:
                    cur.execute(book_info_command)
                    book_info = cur.fetchall()
                    con.close
                for book in book_info:
                    row_count += 1
                    AN = book[0]
                    title = book[1]
                    ISBN = book[2]
                    Publisher = book[3]
                    PublicationYear = book[4]
                    # find the AuthorIDs related to the book from the write table
                    author_id_command = 'SELECT AuthorID FROM Writes WHERE AccessionNumber = ' + "'" + AN + "'" 
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
                        author_command = 'SELECT FirstName, LastName FROM Author WHERE AuthorID = ' + "'" + str(id) + "'" 
                        con = connection()
                        with con.cursor() as cur:
                            cur.execute(author_command)
                            author_names_result = cur.fetchall()
                            con.close
                        for names in author_names_result:
                            author_names = author_names + (names[0] + " " + names[1],)

                    # find names of all authors of the book
                    author_text = ""
                    author_num = len(author_names)
                    author_count = 0
                    for author in author_names:
                        author_count += 1
                        if author_count == author_num:
                            author_text = author_text + " " + author
                        else:
                            author_text = author_text + " " + author + ","
                    # for each piece of info of the book, create labels and pack them
                    Accession_num_Label1 = Label(books, text = AN)
                    title_label1 = Label(books, text = title)
                    ISBN_label1 = Label(books, text = ISBN)
                    Publisher_label1 = Label(books, text = Publisher)
                    PublicationYear_label1 = Label(books, text = PublicationYear)
                    author_label1 = Label(books, text = author_text)
                    Accession_num_Label1.grid(row=row_count, column=0)
                    title_label1.grid(row=row_count, column=1)
                    ISBN_label1.grid(row=row_count, column=2)
                    Publisher_label1.grid(row=row_count, column=3)
                    PublicationYear_label1.grid(row=row_count, column=4)
                    author_label1.grid(row=row_count, column=5)
            if publication_year_check == True:
                book_info_command = '''SELECT AccessionNumber, Title, ISBN, 
                Publisher, PublicationYear
                FROM Book
                WHERE PublicationYear = ''' + "'" + publication_yearin + "'"
                con = connection()
                with con.cursor() as cur:
                    cur.execute(book_info_command)
                    book_info = cur.fetchall()
                    con.close
                for book in book_info:
                    row_count += 1
                    AN = book[0]
                    title = book[1]
                    ISBN = book[2]
                    Publisher = book[3]
                    PublicationYear = book[4]
                    # find the AuthorIDs related to the book from the write table
                    author_id_command = 'SELECT AuthorID FROM Writes WHERE AccessionNumber = ' + "'" + AN + "'" 
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
                        author_command = 'SELECT FirstName, LastName FROM Author WHERE AuthorID = ' + "'" + str(id) + "'" 
                        con = connection()
                        with con.cursor() as cur:
                            cur.execute(author_command)
                            author_names_result = cur.fetchall()
                            con.close
                        for names in author_names_result:
                            author_names = author_names + (names[0] + " " + names[1],)

                    # find names of all authors of the book
                    author_text = ""
                    author_num = len(author_names)
                    author_count = 0
                    for author in author_names:
                        author_count += 1
                        if author_count == author_num:
                            author_text = author_text + " " + author
                        else:
                            author_text = author_text + " " + author + ","
                    # for each piece of info of the book, create labels and pack them
                    Accession_num_Label1 = Label(books, text = AN)
                    title_label1 = Label(books, text = title)
                    ISBN_label1 = Label(books, text = ISBN)
                    Publisher_label1 = Label(books, text = Publisher)
                    PublicationYear_label1 = Label(books, text = PublicationYear)
                    author_label1 = Label(books, text = author_text)
                    Accession_num_Label1.grid(row=row_count, column=0)
                    title_label1.grid(row=row_count, column=1)
                    ISBN_label1.grid(row=row_count, column=2)
                    Publisher_label1.grid(row=row_count, column=3)
                    PublicationYear_label1.grid(row=row_count, column=4)
                    author_label1.grid(row=row_count, column=5)
            if authors_check == True:
                author_info_command = "SELECT AuthorID FROM Author WHERE FirstName =" + "'" + authorsin + "' OR FirstName LIKE" + "'% " + authorsin + "' OR FirstName LIKE" + "'" + authorsin + " %' OR FirstName LIKE" + "'% " + authorsin + " %' OR LastName =" + "'" + authorsin + "' OR LastName LIKE" + "'% " + authorsin + "' OR LastName LIKE" + "'" + authorsin + " %' OR LastName LIKE" + "'% " + authorsin + " %'"
                con = connection()
                with con.cursor() as cur:
                    cur.execute(author_info_command)
                    found_author_id_result = cur.fetchall()
                    con.close
                # create a tuple for all AN related to the authors
                AN_results = ()
                for id in found_author_id_result:
                    find_AN_command = "SELECT AccessionNumber FROM Writes WHERE AuthorID = " + str(id[0])
                    with con.cursor() as cur:
                        cur.execute(find_AN_command)
                        found_AN_result = cur.fetchall()
                        con.close
                    for AN in found_AN_result:
                        AN_results += AN
                for ANum in AN_results:
                    book_info_command = '''SELECT AccessionNumber, Title, ISBN, 
                    Publisher, PublicationYear
                    FROM Book
                    WHERE AccessionNumber = ''' + "'" + ANum + "'"
                    con = connection()
                    with con.cursor() as cur:
                        cur.execute(book_info_command)
                        book_info = cur.fetchall()
                        con.close
                    for book in book_info:
                        row_count += 1
                        AN = book[0]
                        title = book[1]
                        ISBN = book[2]
                        Publisher = book[3]
                        PublicationYear = book[4]
                        # find the AuthorIDs related to the book from the write table
                        author_id_command = 'SELECT AuthorID FROM Writes WHERE AccessionNumber = ' + "'" + AN + "'" 
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
                            author_command = 'SELECT FirstName, LastName FROM Author WHERE AuthorID = ' + "'" + str(id) + "'" 
                            con = connection()
                            with con.cursor() as cur:
                                cur.execute(author_command)
                                author_names_result = cur.fetchall()
                                con.close
                            for names in author_names_result:
                                author_names = author_names + (names[0] + " " + names[1],)

                        # find names of all authors of the book
                        author_text = ""
                        author_num = len(author_names)
                        author_count = 0
                        for author in author_names:
                            author_count += 1
                            if author_count == author_num:
                                author_text = author_text + " " + author
                            else:
                                author_text = author_text + " " + author + ","
                        # for each piece of info of the book, create labels and pack them
                        Accession_num_Label1 = Label(books, text = AN)
                        title_label1 = Label(books, text = title)
                        ISBN_label1 = Label(books, text = ISBN)
                        Publisher_label1 = Label(books, text = Publisher)
                        PublicationYear_label1 = Label(books, text = PublicationYear)
                        author_label1 = Label(books, text = author_text)
                        Accession_num_Label1.grid(row=row_count, column=0)
                        title_label1.grid(row=row_count, column=1)
                        ISBN_label1.grid(row=row_count, column=2)
                        Publisher_label1.grid(row=row_count, column=3)
                        PublicationYear_label1.grid(row=row_count, column=4)
                        author_label1.grid(row=row_count, column=5)    
            return_button = Button(books, text = "Back to Reports Menu", \
            command = books.destroy, bg='skyblue1')
            return_button.grid(row=row_count+1, column=2)

    # create the add new book button back to menus button
    search_book_button = Button(info, text="Search Book", command = search_book, bg='skyblue1')
    search_book_button.grid(row=11, column=0)
    back_to_books_menu_button = Button(info, text="Back to Reports Menu", command = info.destroy, bg='skyblue1')
    back_to_books_menu_button.grid(row=12, column=0)
