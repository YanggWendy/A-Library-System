from connection import*
import pymysql


def insert_faculty(facultyname):
    con = connection()
    insert = 'INSERT INTO Faculty (FacultyName) VALUES (\'' + facultyname + '\')'
    try:
        with con.cursor() as cur:
            cur.execute(insert)
            con.commit()
        
    finally:
        con.close()

def get_facultyid(faculty):
    con = connection()
    query = 'SELECT * FROM Faculty'
    with con.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
    for result in results:
        if faculty in result:
            return result[0]
    
    insert_faculty(faculty)
    return get_facultyid(faculty)

def get_faculty_name(facultyid):
    con = connection()
    query = 'SELECT * FROM Faculty'
    with con.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
    for result in results:
        if facultyid in result:
            return result[1]

