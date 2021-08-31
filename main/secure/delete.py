'''
This function takes username,service name and email.It will check for the parameters in the database and delete the record .
PLEASE CHANGE DATABASE NAME TARUN
'''

import mysql.connector
from tkinter import messagebox
import tkinter as tk

root = tk.Tk()
root.withdraw()

def delete_rec(un,serv,mail):
    try:
        check = mysql.connector.connect(user='root', passwd='root', host='localhost', database='master_password')
        cursor = check.cursor()
        cursor.execute('select * from {}'.format(un))
        data = cursor.fetchall()
        lg = len(data)
        try:
            for record in data:
                if record[0] == mail and record[2] == serv:
                    break
            else:
                messagebox.showerror('Error','Record Not Found, Please Check!')
            
            a = 0
            for k in data:
                a += 1
                em = k[0]
                sn = k[2]
                if em == mail:
                    if serv == sn:
                        res = messagebox.askokcancel('Confirm', 'DELETE RECORD?')
                        if res == 1:
                            cursor.execute('DELETE FROM {} where email="{}" and service="{}"'.format(un,em,serv))
                            check.commit()
                            messagebox.showinfo('Success', 'Delete Successful!')
                            break
                else:
                    if a == lg:
                        messagebox.showerror('ERROR',"Records don't match!")
                    else:
                        continue
        except:
            messagebox.showerror('Failed','Something Went wrong. Please try again')
    except:
        messagebox.showerror('Failed','Connection problem ')


