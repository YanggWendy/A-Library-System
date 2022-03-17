from cProfile import label
from errno import EROFS
from logging import root
from optparse import check_builtin
from tkinter import*
from connection import*
from PIL import Image, ImageTk


def books_on_loan():

    on_loan = Toplevel()
    on_loan.title("Books on Loan Report")
    loadImg = Image.open('sky.png')
    backgroundImage = ImageTk.PhotoImage(loadImg)
    on_loan.image = backgroundImage
    background_label = Label(on_loan, image=backgroundImage)
    background_label.place(x=0, y=0)

    # create labels and pack
    Accession_num_Label = Label(on_loan, text = "Accession Number")
    title_label = Label(on_loan, text = "Title")
    ISBN_label = Label(on_loan, text = "ISBN")
    Publisher_label = Label(on_loan, text = "Publisher")
    PublicationYear_label = Label(on_loan, text = "Publication Year")
    author_label = Label(on_loan, text = "Authors")
    Accession_num_Label.grid(row=0, column=0)
    title_label.grid(row=0, column=1)
    ISBN_label.grid(row=0, column=2)
    Publisher_label.grid(row=0, column=3)
    PublicationYear_label.grid(row=0, column=4)
    author_label.grid(row=0, column=5)

    # find the AccessionNumber of all books on loan
    all_books_on_loan_command = "SELECT AccessionNumber from Borrow"
    con = connection()
    with con.cursor() as cur:
        cur.execute(all_books_on_loan_command)
        AccessionNumbers_result = cur.fetchall()
        con.close

    # row count for grid
    row_count = 0

    # find the info related to each book
    for ANtpl in AccessionNumbers_result:
        row_count += 1
        AccessionNumber = ANtpl[0]
        book_info_command = '''SELECT AccessionNumber, Title, ISBN, 
        Publisher, PublicationYear
        FROM Book
        WHERE AccessionNumber = ''' + '\'' + AccessionNumber + '\''
        #print(book_info_command)
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
        author_id_command = 'SELECT AuthorID FROM Writes WHERE AccessionNumber = ' + '\'' +  AccessionNumber + '\''
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
        Accession_num_Label = Label(on_loan, text = AccessionNumber)
        title_label = Label(on_loan, text = title)
        ISBN_label = Label(on_loan, text = ISBN)
        Publisher_label = Label(on_loan, text = Publisher)
        PublicationYear_label = Label(on_loan, text = PublicationYear)
        author_label = Label(on_loan, text = author_text)
        Accession_num_Label.grid(row=row_count, column=0)
        title_label.grid(row=row_count, column=1)
        ISBN_label.grid(row=row_count, column=2)
        Publisher_label.grid(row=row_count, column=3)
        PublicationYear_label.grid(row=row_count, column=4)
        author_label.grid(row=row_count, column=5)

    return_button = Button(on_loan, text = "Back to Reports Menu", \
    command = on_loan.destroy, bg='skyblue1')
    return_button.grid(row=row_count+1, column=3)
