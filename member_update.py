from tkinter import *
from connection import *
from get_facultyid import *
from tkinter import messagebox
import pymysql
from member_creation import*
from PIL import Image, ImageTk


def update_mem_page():
    root = Toplevel()
    root.geometry('400x300')
    loadImg = Image.open('blueblossom.png')
    backgroundImage = ImageTk.PhotoImage(loadImg)
    root.background_label = Label(root, image=backgroundImage)
    root.background_label.place(x=0, y=0)
    root.title('Update')

    welcome_label = Label(root, text='Please Only Fill in the Fields that Need Changes')
    welcome_label.place(x=55, y=20)

    member_label = Label(root, text='Enter your ID')
    member_label.place(x=20, y=70)
    fname_label = Label(root, text='Enter the changed first name')
    fname_label.place(x=205, y=70)
    lname_label = Label(root, text='Enter the changed last name')
    lname_label.place(x=20, y = 125)
    faculty_label = Label(root, text='Enter the changed faculty name')
    faculty_label.place(x=205,y=125)
    phone_label = Label(root, text='Enter a new phone number')
    phone_label.place(x=20, y=180)
    email_label = Label(root, text='Enter a new email')
    email_label.place(x=205,y=180)

    member_id = Entry(root, width=20, fg="black")
    member_id.place(x=20, y=95)
    fname = Entry(root, width=20, fg='black')
    fname.place(x=205,y=95)
    lname = Entry(root, width=20, fg='black')
    lname.place(x=20,y=150)
    faculty = Entry(root, width=20, fg='black')
    faculty.place(x = 205,y=150)
    phone = Entry(root, width=20, fg='black')
    phone.place(x=20, y=205)
    email = Entry(root, width=20, fg='black')
    email.place(x=205, y=205)

    def update_info():
        con = connection()
        ID = member_id.get()
        f_name = fname.get()
        l_name = lname.get()
        faculty_name = faculty.get()
        phone_no = phone.get()
        email_add = email.get()
        
        if ID == '':
            return messagebox.showerror('','You haven\'t keyed in Membership ID!')

        else:
            with con.cursor() as cur:
                view = 'SELECT MemberID from Member'
                cur.execute(view)
                results = cur.fetchall()
                if (ID,) not in results:
                    return messagebox.showerror('', 'Member Does not Exist!')

        if f_name == '' and faculty_name == '' and phone_no=='' and email_add=='' and l_name == '':
           return messagebox.showerror('', 'You haven\'t keyed in a field!')

        elif faculty_name != "":
            faculty_id = get_facultyid(faculty_name)
        else:
            faculty_id = ""

        column_names = ['FirstName', 'LastName', 'FacultyID', 'PhoneNo', 'Email']
        user_input = [f_name, l_name, faculty_id, phone_no, email_add]
        update_dict = {}


        for i in range(len(user_input)):
            if user_input[i] != "":
                update_dict[i] = user_input[i]

        def update_execute():

            for index, info in update_dict.items():
                column = column_names[index]
                q = 'update member set ' + column + ' = ' + '\'' + str(
                    info) + '\'' + " where MemberID = " + '\'' + ID + '\''
                try:
                    with con.cursor() as cur:
                        cur.execute(q)
                        con.commit()


                finally:
                    con.close

            create_member_window = Toplevel()
            create_member_window.geometry('300x300')
            create_member_window.title('Success!')

            bg_img = Image.open('blueFlower.png')
            background = ImageTk.PhotoImage(bg_img)
            create_member_window.image = background
            create_member_window.background_label = Label(create_member_window, image=background)
            create_member_window.background_label.place(x=0, y=0)
            create_member_window.background_label.image = bg_img

            update_success_label = Label(create_member_window, text='ASL Membership Updated!', font='bold24')
            update_success_label.place(x=35, y=60)
            button = Button(create_member_window, text="Create a new member", padx=20, \
                            command= member_page)
            button.place(x=65, y= 150)
            exit_button = Button(create_member_window, text='Back to Update Function', command=create_member_window.destroy)
            exit_button.place(x =75,y=200)

        confirm_window = Toplevel()
        confirm_window.title('Confirm Updates')
        confirm_window.geometry('300x300')


        img = Image.open('green_flowers_final.png')
        confirm_background_image = ImageTk.PhotoImage(img)
        confirm_window.background_label = Label(confirm_window, image=confirm_background_image)
        confirm_window.background_label.place(x=0, y=0)
        confirm_window.background_label.image = confirm_background_image

        confirm_window.title('Confirm updates')

        #x_value = 50
        #y_value = 30
        for index, info in update_dict.items():
            column = column_names[index]
            globals()[f"{column}_label"] = Label(confirm_window, text=column + ' will be changed to: \n' + str(info))
            globals()[f"{column}_label"].pack()


        button1 = Button(confirm_window, text="Confirm Update", padx=20, \
                         command=update_execute)
        button1.place(x=85, y=220)
        exit_button = Button(confirm_window, text='Back to Membership Menu', command=confirm_window.destroy)
        exit_button.place(x=70, y =260)

        # return messagebox.showinfo("Success!", 'Information Updated!')

    button1 = Button(root, text="Update the information", padx=20, \
                     command=update_info, bg='lightblue3')
    button1.place(x = 110, y = 240)

    exit_button = Button(root, text='Back to Membership menu', command=root.destroy, bg='lightblue3')
    exit_button.place(x = 115, y = 270)

    root.mainloop()
