from connection import*
from get_facultyid import*
import pymysql
import numpy as np
import pandas as pd


def insert_member(ID, fname, lname, faculty, phone, email):
    con = connection()
    with con.cursor() as cur:
        view = 'SELECT MemberID from Member'
        cur.execute(view)
        results = cur.fetchall()
        for result in results:
            if ID in result:
                return 'Member already exists!'

    faculty_id = get_facultyid(faculty)
    insert = str((ID,fname, lname, faculty_id, phone, email))
    insert = 'INSERT INTO Member (MemberID, FirstName, LastName, FacultyID, PhoneNo,\
Email) VALUES ' +insert 
    try:
        with con.cursor() as cur:
            cur.execute(insert)
            con.commit()
    finally:
        con.close
insert_member('A101A', 'Hermione', 'Granger', 'Science', '33336663', 'flying@als.edu')
insert_member('A201B','Sherlock','Holmes','Law','44327676','elementarydrw@als.edu')
insert_member('A301C','Tintin','','Engineering','14358788','luvmilu@als.edu')
insert_member('A401D','Prinche','Hamlet','FASS','16091609','tobeornot@als.edu')
insert_member('A5101E','Willy','Wonka','FASS','19701970','choco1@als.edu')
insert_member('A601F','Holly','Golightly','Business','55548008','diamond@als.edu')
insert_member('A701G','Raskolnikov','','Law','18661866','oneaxe@als.edu')
insert_member('A801H','Patrick' ,'Bateman','Business','38548544','mice@als.edu')
insert_member('A901I','Captain','Ahab','Science','18511851','wwhale@als.edu')
print('Member Data Successfully Added!')


def init_book():
        con = connection()
        book_info = pd.read_csv('LibBooks.txt')
        count = 1

        for i in range(book_info.shape[0]):
            for j in [2,3,4]:
                check_authorid = True
                check_Name = True
                if pd.isna(book_info.iloc[i,j]) == False:
                    AuthorID = count
                    FirstName = ' '.join(str(book_info.iloc[i,j]).split()[:-1])
                    LastName = str(book_info.iloc[i,j]).split()[-1]
                    #print(AuthorID,FirstName,LastName)
                    with con.cursor() as cur:
                        view = 'SELECT AuthorID from Author'
                        cur.execute(view)
                        results = cur.fetchall()
                        for result in results:
                            if AuthorID in result:
                                check_authorid = False

                        #check replicate author
                        view = 'SELECT FirstName, LastName from Author'
                        cur.execute(view)
                        names = cur.fetchall()
                        if (FirstName,LastName) in names:
                            check_Name = False
                    if check_Name and check_authorid:
                        insert = str((AuthorID, str(FirstName), LastName))
                        # print(insert)
                        insert = 'INSERT INTO Author(AuthorID,FirstName,LastName) VALUES ' + insert
                        try:
                            with con.cursor() as cur:
                                cur.execute(insert)
                                con.commit()
                        finally:
                            con.close
                    count += 1


        #for book data
        for i in range(book_info.shape[0]):
            check_AN = True
            AccessionNumber = book_info.iloc[i,0]
            Title = book_info.iloc[i,1]
            ISBN = book_info.iloc[i,5]
            Publisher = book_info.iloc[i,-2]
            PublicationYear = book_info.iloc[i, -1]
            with con.cursor() as cur:
                view = 'SELECT AccessionNumber from Book'
                cur.execute(view)
                results = cur.fetchall()
                for result in results:
                    if AccessionNumber in result:
                        print("Book already exists!")
                        check_AN = False
            if check_AN:
                insert = str((AccessionNumber,Title,ISBN,Publisher,PublicationYear))
                #print(insert)
                insert = 'INSERT INTO Book(AccessionNumber,Title,ISBN,Publisher,PublicationYear) VALUES ' + insert
                try:
                    with con.cursor() as cur:
                        cur.execute(insert)
                        con.commit()
                finally:

                    con.close

        #for write relationship
        for i in range(book_info.shape[0]):
            for j in [2, 3, 4]:
                if pd.isna(book_info.iloc[i, j]) == False:
                    AccessionNumber = book_info.iloc[i,0]
                    FirstName_c = ' '.join(str(book_info.iloc[i, j]).split()[:-1])
                    LastName_c = str(book_info.iloc[i, j]).split()[-1]

                    with con.cursor() as cur:
                        view = 'SELECT AuthorID from Author WHERE FirstName = "'+ FirstName_c+'" AND LastName= "' + LastName_c+'"'
                        cur.execute(view)
                        AuthorID_W = cur.fetchall()
                        AuthorID_W = AuthorID_W[0][0]

                        view = 'SELECT * from Writes'
                        cur.execute(view)
                        results = cur.fetchall()

                        if (AuthorID_W,AccessionNumber) in results:
                            print('Write relationship already exists!')
                            continue
                        else:
                            insert = str((AuthorID_W,AccessionNumber))
                            insert = 'INSERT INTO Writes(AuthorID,AccessionNumber) VALUES ' + insert
                            try:
                                with con.cursor() as cur:
                                    cur.execute(insert)
                                    con.commit()
                            finally:

                                con.close
init_book()
print('Book Data Successfully Added!')
