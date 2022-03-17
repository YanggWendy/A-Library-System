from tkinter import*
from connection import*
from get_facultyid import*
from tkinter import messagebox
import pymysql
from PIL import Image, ImageTk

def fine_page():
    root = Toplevel()
    root.title('Fine Payment')
    root.geometry('400x300')

    loadImg = Image.open('blueblossom.png')
    backgroundImage = ImageTk.PhotoImage(loadImg)
    root.background_label = Label(root, image=backgroundImage)
    root.background_label.place(x=0, y=0)
    loadImg2 = Image.open('green_flowers_final.png')
    bgi = ImageTk.PhotoImage(loadImg2)

    welcome_label = Label(root, text = "Please Enter Information Below", font='Bold20')
    welcome_label.place(x=80, y=27)

    member_label = Label(root, text='Enter Membership ID')
    member_id = Entry(root, width=20)
    date_label = Label(root, text='Payment Date')
    date = Entry(root, width=20)
    fine_label = Label(root, text='Payment Amount')
    fine = Entry(root, width=20)
    
    member_label.place(x=100, y=70)
    member_id.place(x=100, y=100)
    date_label.place(x=100, y=130)
    date.place(x=100, y=160)
    fine_label.place(x=100, y=190)
    fine.place(x=100, y=220)



    def pay_fine():
        con = connection()
        ID = member_id.get()
        if ID == '' or date.get()=='' or fine.get()=='':
            return messagebox.showerror('', 'Missing Field!')
        with con.cursor() as cur:
            member = 'SELECT MemberID FROM Member'
            cur.execute(member)
            results = cur.fetchall()
            if (ID,) not in results:
                return messagebox.showerror('', 'Member Does not Exist!')

            get_fine = 'SELECT FineAmount FROM Member WHERE MemberID = \'' + ID + '\''
            cur.execute(get_fine)
            results = cur.fetchall()[0][0]


        
        root = Toplevel()
        root.geometry('230x250')
        root.title('Confirm Details')
        background_label = Label(root, image=bgi)
        background_label.place(x = 0, y = 0)
        amount_txt = 'Payment Due: \n$' + str(results)
        title_label = Label(root, text='Please Confirm Your Details \n')
        amount_label = Label(root, text=amount_txt)
        id_label = Label(root, text='Membership ID: \n'+ID)
        date_label = Label(root, text='Payment date: \n'+date.get())
        confirm_label = Label(root, text='Exact Fee Only')
        title_label.pack()
        amount_label.pack()
        id_label.pack()
        date_label.pack()
        confirm_label.pack()

        def fine_execute():
            con = connection()
            with con.cursor() as cur:
                get_fine = 'SELECT FineAmount FROM Member WHERE MemberID = \'' + ID + '\''
                cur.execute(get_fine)
                actl_fine = cur.fetchall()[0][0]
                if actl_fine == 0:
                    return messagebox.showerror('', 'Member has no fine!')
                elif actl_fine != int(fine.get()):
                    return messagebox.showerror('', 'Incorrect Fine Payment Amount!')
                else:
                    update_fine = 'UPDATE Member SET FineAmount = 0 WHERE MemberID = \'' + ID + '\''
                    cur.execute(update_fine)
                    con.commit()
                    return messagebox.showinfo('', 'Payment Successful!')

        button1 = Button(root, text="Pay Fine", padx = 20, \
                     command = fine_execute)
        button1.pack()
        exit_button = Button(root, text = 'Back to Payment', command = root.destroy)
        exit_button.pack()
                
        

    

    button1 = Button(root, text="Pay Fine", padx = 20, \
                     command = pay_fine)
    button1.place(x = 60, y =260)
    exit_button = Button(root, text = 'Back to main menu', command = root.destroy)
    exit_button.place(x = 205, y =260)



    root.mainloop()

