import mysql.connector as mysql
import re
db = mysql.connect(user='root',
        passwd='Jndl@123',
        host='localhost',
        database='minipro')
cursor = db.cursor(buffered=True)

def insert_user(user_name,email,password):
    formula = "INSERT INTO users(user_name,email,password) VALUES(%s,%s,%s)"
    cursor.execute(formula,(user_name,email,password))
    db.commit()
    cursor.execute('SELECT * FROM users WHERE email=%s',(email,))
    return cursor.fetchone()

def insert_comment(comment_text,user_id,device_id):
    formula = "INSERT INTO comments(comment_text,user_id,device_id) VALUES(%s,%s,%s)"
    cursor.execute(formula,(comment_text,user_id,device_id))
    db.commit()
    cursor.execute("SELECT comment_text,created_on,device_id FROM comments ORDER BY ID DESC")
    return cursor.fetchone()

def insert_device(device_name,query):
    formula = "INSERT INTO devices(device_name,query) VALUES(%s,%s)"
    cursor.execute(formula,(device_name,query))
    db.commit()
    cursor.execute('SELECT * FROM devices ORDER BY ID DESC LIMIT 1')
    return cursor.fetchone()
