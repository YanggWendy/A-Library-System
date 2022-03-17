from tkinter import*
from connection import*
from get_facultyid import*
from tkinter import messagebox
import pymysql
from PIL import Image, ImageTk

def delete_page():
    root = Toplevel()
    root.geometry('400x220')
    root.title('Delete Member')
    loadImg = Image.open('blueblossom.png')
    backgroundImage = ImageTk.PhotoImage(loadImg)
    root.background_label = Label(root, image=backgroundImage)
    root.background_label.place(x=0, y=0)


    welcome_label = Label(root, text='To Delete Member, Please Enter Membership ID:')
    welcome_label.place(x =60, y = 20)


    member_label = Label(root, text='Enter the Member ID')
    member_id = Entry(root, width=20)
    member_label.place(x = 133, y = 65)
    member_id.place(x = 125, y = 100)

    
    def delete_member():
        con = connection()
        ID = member_id.get()
        if ID == "":
            return messagebox.showerror('', 'Missing Field!')
        with con.cursor() as cur:
            membership = 'SELECT MemberID FROM Member'
            cur.execute(membership)
            results = cur.fetchall()
            if (ID,) not in results:
                return messagebox.showerror('', 'Member does not exist')
        
            borrow = 'SELECT MemberID FROM Borrow'
            cur.execute(borrow)
            results = cur.fetchall()
            for result in results:
                if ID in result:
                    return messagebox.showerror('', 'Book not returned!')
            fine = 'SELECT FineAmount from Member WHERE MemberID = \'' + ID + '\''
            cur.execute(fine)
            results = cur.fetchall()[0][0]
            if results != 0:
                return messagebox.showerror('', 'Member has unpaied fine!')
            
            details = 'SELECT * from Member WHERE MemberID = \'' + ID + '\''
            cur.execute(details)
            details = cur.fetchall()[0]
            name = details[1] + " " + details[2]
            facultyid, phone, email = details[3], details[4], details[5]
            faculty = 'SELECT FacultyName from Faculty WHERE FacultyID = \'' + str(facultyid) + '\''
            cur.execute(faculty)
            faculty = cur.fetchall()[0][0]
        
        confirm_window = Toplevel()
        confirm_window.title('Confirm Deletion')
        confirm_window.geometry('300x300')
        # confirm_window.title('Confirm Reservation')

        img = Image.open('green_flowers_final.png')
        confirm_background_image = ImageTk.PhotoImage(img)
        confirm_window.background_label = Label(confirm_window, image=confirm_background_image)
        confirm_window.background_label.place(x=0, y=0)
        confirm_window.background_label.image = confirm_background_image

        confirm_window.title('Confirm Details')
        
        id_label = Label(confirm_window, text='Member ID: \n'+ID)
        name_label = Label(confirm_window, text='Name: \n'+name)
        faculty_label = Label(confirm_window, text='Faculty: \n'+faculty)
        phone_label = Label(confirm_window, text='Phone Number: \n'+phone)
        email_label = Label(confirm_window, text='Email Address: \n'+email)
        id_label.pack()
        name_label.pack()
        faculty_label.pack()
        phone_label.pack()
        email_label.pack()

        def delete_execute():
            delete = 'DELETE FROM Member WHERE MemberID = \'' + ID + '\''
            try:
                with con.cursor() as cur:
                    cur.execute(delete)
                    con.commit()
                    messagebox.showinfo('', 'Membrer Successfully Deleted!')
            finally:
                con.close
        button1 = Button(confirm_window, text="Concfirm Deletion", padx = 20, \
                     command = delete_execute)
        button1.place(x=72, y=220)
        exit_button = Button(confirm_window, text = 'Back to Member Deletion', command = confirm_window.destroy)
        exit_button.place(x=70, y =260)
        

    

    button1 = Button(root, text="Delete Member", padx = 20, \
                     command = delete_member)
    button1.place(x =130, y = 135)
    exit_button = Button(root, text = 'Back to Main Menu', command = root.destroy)
    exit_button.place(x =139, y = 175)



    root.mainloop()
