'''This function takes username service name,email id and the old password.It will check each of the parameters
mentioned before and then runs the update command to change the password.Error will pop if nay of the parameters
are not matching!
Tell me if you need me to change the errors to messagebox
PLEASE CHANGE DATABASE NAME TARUN'''

import mysql.connector
from tkinter import messagebox
import tkinter as tk

root = tk.Tk()
root.withdraw()

def update(un,serv,mail,opass,pw):
    try:
        check = mysql.connector.connect(user='root', passwd='root', host='localhost', database='master_password')
        cursor = check.cursor()
        cursor.execute('select * from {}'.format(un))
        data = cursor.fetchall()
        lg=len(data)
        try:
            for record in data:
                if record[0] == mail and record[2] == serv:
                    break
            else:
                messagebox.showerror('Error','Record Not Found, Please Check!')
            
            a=0
            for k in data:
                a+=1
                em = k[0]
                sn = k[2]
                tk = k[3]
                cursor.execute('select AES_DECRYPT(a.password,"{}") from {} a where a.email="{}" AND a.service="{}";'.format(tk,un,em,sn))
                res1 = cursor.fetchall()
                pd=res1[0][0]
                if pd == opass:
                    if em == mail:
                        if serv==sn:
                            res = messagebox.askokcancel('Confirm','Confirm Changes?')
                            if res == 1: 
                                cursor.execute('update {} set password = AES_ENCRYPT("{}","{}") where email="{}";'.format(un, pw, tk, em))
                                check.commit()
                                messagebox.showinfo('Success','Changes Successful!')
                                break                        
                else:
                    if a == lg:
                        messagebox.showerror('ERROR',"Records don't match!")
                    else:
                        continue
        except:
            messagebox.showerror('Failed','Something Went Wrong Please try later')
    except:
        messagebox.showerror('Failed','Connection problem ')



