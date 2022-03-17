from tkinter import*
from connection import*
from get_facultyid import*
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql

def member_page():
    root = Toplevel()
    root.geometry('400x300')
    loadImg1 = Image.open('blueblossom.png')
    backgroundImage = ImageTk.PhotoImage(loadImg1)
    loadImg2 = Image.open('green_flowers_final.png')
    bgi = ImageTk.PhotoImage(loadImg2)
    background_label = Label(root, image=backgroundImage)
    background_label.place(x = 0, y = 0)
    root.title('Create Member')

    page_title = Label(root, text = "Please Enter Requested Information Below")
    page_title.place(x = 50, y = 25)

    member_label = Label(root, text='Enter your ID')
    fname_label = Label(root, text='Enter your first name')
    lname_label = Label(root, text='Enter your last name')
    faculty_label = Label(root, text='Enter your faculty')
    phone_label = Label(root, text='Enter your phone number')
    email_label = Label(root, text='Enter your email')

    member_id = Entry(root, width=20)
    fname = Entry(root, width=20)
    lname = Entry(root, width=20)
    faculty = Entry(root, width=20)
    phone = Entry(root, width=20)
    email = Entry(root, width=20)


    member_label.place(x= 50, y =70)
    member_id.place(x= 210, y =70)
    fname_label.place(x= 50, y =100)
    fname.place(x= 210, y =100)
    lname_label.place(x= 50, y =130)
    lname.place(x= 210, y =130)
    faculty_label.place(x= 50, y =160)
    faculty.place(x= 210, y =160)
    phone_label.place(x= 50, y =190)
    phone.place(x= 210, y =190)
    email_label.place(x= 50, y =220)
    email.place(x= 210, y =220)


        
    def insert_member():
        con = connection()
        ID = member_id.get()
        f_name = fname.get()
        l_name = lname.get()
        faculty_name = faculty.get()
        phone_no = phone.get()
        email_add = email.get()
        faculty_id = get_facultyid(faculty_name)
        if ID == "" or f_name == '' or faculty_name == '' \
           or phone_no=='' or email_add=='':
            return messagebox.showerror('', 'Missing Field!')
        with con.cursor() as cur:
            view = 'SELECT MemberID from Member'
            cur.execute(view)
            results = cur.fetchall()
            for result in results:
                if ID in result:
                    return messagebox.showerror('', 'Membrer already exists!')

                
        insert = str((ID,f_name, l_name, faculty_id, phone_no, email_add))
        insert = 'INSERT INTO Member (MemberID, FirstName, LastName, FacultyID, PhoneNo,\
    Email) VALUES ' +insert 
        try:
            with con.cursor() as cur:
                cur.execute(insert)
                con.commit()
                messagebox.showinfo('', 'Member Successfully Added!')
        finally:
            con.close

    

    button1 = Button(root, text="Create new Member", \
                     command = insert_member)
    button1.place(x = 50, y =260)
    exit_button = Button(root, text = 'Back to main menu', command = root.destroy)
    exit_button.place(x = 218, y =260)


    root.mainloop()


