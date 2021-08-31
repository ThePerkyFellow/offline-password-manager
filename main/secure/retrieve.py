'''
This function takes username and service.It will decrypt and provide the result in this form of all the passwords of that service 
PLEASE CHANGE DATABASE NAME TARUN
'''

import mysql.connector
from tkinter import messagebox
import tkinter as tk

root = tk.Tk()
root.withdraw()

def get_passwd(un,sn):
    final = []
    try:
        check = mysql.connector.connect(user='root', passwd='root', host='localhost', database='master_password')
        cursor = check.cursor()
        try:
            cursor.execute('select * from {}'.format(un))
            data = cursor.fetchall()
            for k in data:
                tk=k[3]
                em=k[0]
                sn=k[2]
                cursor.execute('select AES_DECRYPT(a.password,"{}") from {} a where a.email="{}" AND a.service="{}";'.format(tk,un,em,sn))
                res1 = cursor.fetchall()
                for response in res1:
                    if response:
                        for element in response:
                            line = f'{em}               {element}            {sn}'
                            final.append(line)
            return final
        except:
            messagebox.showerror('Failed','!!!!')
    except:
        messagebox.showerror('Failed','Connection problem ')



#get_passwd('tarun','google')