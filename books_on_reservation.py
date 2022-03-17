from tkinter import *
from connection import *
from get_facultyid import *
from tkinter import messagebox
import pymysql
from datetime import date
from PIL import Image, ImageTk


def reservation_report():
    reserved = Toplevel()
    reserved.title('Books on Reservation Report')
    loadImg = Image.open('sky.png')
    backgroundImage = ImageTk.PhotoImage(loadImg)
    reserved.background_label = Label(reserved, image=backgroundImage)
    reserved.background_label.place(x=0, y=0)

    con = connection()

    Accession_num_Label = Label(reserved, text="Accession Number")
    title_label = Label(reserved, text="Title")
    memberID_label = Label(reserved, text='Member ID')
    memberName_label = Label(reserved, text="Member Name")


    Accession_num_Label.grid(row=0, column=0)
    title_label.grid(row=0, column=1)
    memberID_label.grid(row=0, column=2)
    memberName_label.grid(row=0, column=3)

    '''
    select r.AccessionNumber, b.Title, r.MemberID, CONCAT( m.FirstName, " ", m.LastName) as MemberName
    from reserve r
    left join 
    (select AccessionNumber, Title from Book) b
    ON r.AccessionNumber = b.AccessionNumber
    left join
    (select MemberID, FirstName, LastName from member) m
    on m.MemberID = r.MemberID
    '''

    query = 'select r.AccessionNumber, b.Title, r.MemberID, CONCAT( m.FirstName, " ", m.LastName) as MemberName from ' \
            'reserve r left join (select AccessionNumber, Title from Book) b ON r.AccessionNumber = b.AccessionNumber ' \
            'left join (select MemberID, FirstName, LastName from member) m on m.MemberID = r.MemberID '
    with con.cursor() as cur:
        cur.execute(query)
        result = cur.fetchall()



    for row_count in range(len(result)):
        row = result[row_count]
        AccessionNumber, Title, MemberID, MemberName = row[0], row[1], row[2], row[3]
        Accession_num_Label = Label(reserved, text=AccessionNumber)
        title_label = Label(reserved, text=Title)
        memberID_label = Label(reserved, text=MemberID)
        memberName_label = Label(reserved, text=MemberName)

        Accession_num_Label.grid(row=row_count +1, column=0)
        title_label.grid(row=row_count +1, column=1)
        memberID_label.grid(row=row_count +1, column=2)
        memberName_label.grid(row=row_count +1, column=3)


    exit_button = Button(reserved, text='Back to Reports Menu', command=reserved.destroy, bg='skyblue1')
    exit_button.grid(row = len(result)+1, column = 3)


    reserved.mainloop()

