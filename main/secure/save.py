'''
This function takes username,password,key(==master password),email,service name
It inserts space as passoword first and then updates it.PLEASE CHANGE DATABASE NAME TARUN

'''

import mysql.connector
from tkinter import messagebox
import tkinter as tk

root = tk.Tk()
root.withdraw()


def store_passwd(un,pw,tk,em,sn):
    try:
        check = mysql.connector.connect(user='root', passwd='root', host='localhost', database='master_password')
        cursor = check.cursor()
        df = ' '
        try:
            cursor.execute('INSERT INTO {} VALUES ("{}","{}","{}","{}");'.format(un,em,df,sn,tk))
            cursor.execute('update {} set password = AES_ENCRYPT("{}","{}") where email="{}" and service="{}";'.format(un,pw,tk,em,sn))
            check.commit()
            messagebox.showinfo('Success','Password Added Successfully')
        except:
            
            messagebox.showerror('Failed','Password could not be saved!')
    except:
        messagebox.showerror('Failed','User not found ')



#store_passwd('tarun','ff','y','mail@gm','google')
