import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import *
from PIL import ImageTk,Image
import mysql.connector as mysql
from secure import retrieve,save,modify,delete
import re
import pyperclip
import hashlib



# saving master password for new user
def add_master(name,password):
    salt = 'LTC'
    passwd = password[0:1] + salt + password[1:]
    res=hashlib.md5(bytes(passwd,'utf-8')).hexdigest()

    mydb = mysql.connect(user='root',passwd='root',host='localhost',database='master_password')
    if mydb.is_connected:
        mycur = mydb.cursor()
        try:
            query = 'INSERT INTO password(name,password) VALUES(%s,%s)'
            values = (name,res)
            mycur.execute(query,values)
            make_table(name)
            mydb.commit()
        except Exception as e:
            mydb.rollback()
            messagebox.showerror('Error','User Already Exists, Please sign in')

    mydb.close()

# making table for new user
def make_table(name):
    mydb = mysql.connect(user='root',passwd='root',host='localhost',database='master_password')
    if mydb.is_connected:
        mycur = mydb.cursor()
        try:
            mycur.execute('CREATE TABLE {} (email varchar(225),password BLOB,service varchar(225),tkey varchar(225));'.format(name))
            mydb.commit()
        except Exception as e:
            messagebox.showerror('Error','User could not be added Try later')
            mydb.rollback()
    mydb.close()
            
            
    

# getting all master passwords
def get_master():
    mydb = mysql.connect(user='root',passwd='root',host='localhost',database='master_password')
    if mydb.is_connected:
        mycur = mydb.cursor()
        mycur.execute('SELECT * from password')
        passwords = mycur.fetchall()
    mydb.close()

    return passwords
    
# clearing entries
def forget_newuser():
    name_entry.delete(0,END)
    master_entry.delete(0,END)
    masterconfi_entry.delete(0,END)

# clear screen
def clear():
    item_list = exist_win.winfo_children()
    for widget in item_list:
        widget.destroy()

# getting existing users passwords
def get_exist_pass(username):
    mydb = mysql.connect(user='root',passwd='root',host='localhost',database='master_password')
    if mydb.is_connected:
        mycur = mydb.cursor()
        mycur.execute('select * from {}'.format(username))
        exist_passwords = mycur.fetchall()
    mydb.close()

    return exist_passwords

# getting passwords based on service

def get_pass_by_service():
    selected_service = service_listbox.get(tk.ANCHOR)
    passwords_by_service = retrieve.get_passwd(username,selected_service)
    
    return passwords_by_service




# displaying existing password for that service
def display():
    global trv
    passwords_by_services = get_pass_by_service()
    clear()
    style = ttk.Style(exist_win)

    # setting ttk theme to "clam" which support the fieldbackground option
    style.theme_use("clam")

    ttk.Style().configure("Treeview", background="black",foreground="white", fieldbackground="black")
    trv = ttk.Treeview(exist_win)
    # setting columns
    trv['columns'] = ('Email','Password','Service')

    # formatting columns
    # ! #0 is phantom column given by treeview 
    trv.column('#0',width=0,minwidth=0)
    trv.column('Email',anchor=W,width=120)
    trv.column('Password',anchor=CENTER,width=120)
    trv.column('Service',anchor=W,width=120)


    trv.heading('#0',text='')
    trv.heading('Email',text='Email')
    trv.heading('Password',text='Password')
    trv.heading('Service',text='Service')

    trv.pack()

    for row in passwords_by_services:
        trv.insert(parent='',index='end',values=row)
    
    # ? calling copying function 
    copy_button = ttk.Button(exist_win,text='Copy Password',command=select) 
    copy_button.pack(pady=10) 


    # ! Using lambda to do 2 fuctions with 1 command
    go_back_button = ttk.Button(exist_win,text='Go back',command=lambda :[clear(), show_details()])
    go_back_button.pack(pady=10)

    

    clear_button = ttk.Button(exist_win,text='Clear ClipBoard',command=clear_clipboard) 
    clear_button.pack(pady=10)

def clear_clipboard():
    pyperclip.copy(' ')
    messagebox.showinfo('Success','Clipboard Has been Cleared!')
   
 # Copying the password to computers clipboard
def select(): 
    global trv 
    try:
        curItem = trv.focus()
        value = trv.item(curItem)['values'][1] 
        print(curItem,value)
        messagebox.showinfo('WARNING','!!!COPYING PASSWORD WILL SAVE A COPY TO THE CLIPBOARD,REMEMBER TO CLEAR THE CLIPBOARD ONCE PASSWORD IS PASTED!!!')
        pyperclip.copy(value)
        messagebox.showinfo('Success','Password Copied to Clipboard')
    except:
        messagebox.showerror('Error','Please Select A Record to Copy!') 




# adding new passwords for existing users
def dis_pass():
    service_name = (service_entry.get())
    username_add = (username_entry.get())
    service_passwd = (masterpwd_entry.get())
    regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
    if(re.search(regex,username_add)):
        save.store_passwd(username,service_passwd,masterpassword,username_add,service_name)
        service_entry.delete(0,END)
        username_entry.delete(0,END)
        masterpwd_entry.delete(0,END)
        
    else:
        messagebox.showerror('Invalid Email Entered','Invalid Email Entered! Please check')
        new_add_win.destroy()
        add_new_passwd()

    # ! refreshing screen as a password is added 
    exit_button_add = ttk.Button(new_add_win, text='Close', command = lambda :[new_add_win.destroy(),clear(),show_details()])
    exit_button_add.grid(row=5, column=0, columnspan=2, pady=10, padx=20,ipadx=125)




# window for adding new passwords for existing users
def add_new_passwd():

    global new_add_win, username_entry, masterpwd_entry ,service_entry,sumbit_button
    new_add_win = tk.Toplevel()
    new_add_win.title("Store your password")
    new_add_win.geometry('400x400+500+300')
    new_add_win.resizable('false', 'false')
    new_add_win.configure(bg='black')

    # labels
    service_label = tk.Label(new_add_win, text='SERVICE NAME:',bg='black',fg='#39FF14',font=('helvetica',14))
    service_label.grid(row=0, column=0, pady=20)

    username_label = tk.Label(new_add_win, text='EMAIL :',bg='black',fg='#39FF14',font=('helvetica',14))
    username_label.grid(row=1, column=0, pady=20)

    dum_label1 = tk.Label(new_add_win, text='')
    dum_label1.grid(row=2, column=0, pady=20)

    masterpwd_label = tk.Label(new_add_win, text='PASSWORD :',bg='black',fg='#39FF14',font=('helvetica',14))
    masterpwd_label.grid(row=2, column=0, pady=20)

    # entry
    service_entry = tk.Entry(new_add_win)
    service_entry.grid(row=0, column=1, pady=20)
    username_entry = tk.Entry(new_add_win)
    username_entry.grid(row=1, column=1, pady=20)
    masterpwd_entry = tk.Entry(new_add_win,show='*')
    masterpwd_entry.grid(row=2, column=1, pady=20)

    # dummy label
    dum_label1 = tk.Label(new_add_win, text='',bg='black',fg='black')
    dum_label1.grid(row=3, column=1, pady=20)
    
    # sumbit button
    sumbit_button = ttk.Button(new_add_win, text='ADD RECORD', command=dis_pass)
    sumbit_button.grid(row=4, column=0, columnspan=2, pady=20, padx=30,ipadx=125)

    # focusing on entry box
    service_entry.focus()

def actually_modify_password():
    email_add = modify_username_entry.get()
    modify_service_name = modify_service_entry.get()
    modify_oldpassword = modify_masterpwd_entry.get()
    modify_newpwd = modify_newpwd_entry.get()
    modify.update(username,modify_service_name,email_add,modify_oldpassword,modify_newpwd)
    
    modify_username_entry.delete(0,END)
    modify_service_entry.delete(0,END)
    modify_masterpwd_entry.delete(0,END)
    modify_newpwd_entry.delete(0,END)

    modify_sumbit_button.config(text='Close',command=modify_win.destroy)


def actually_delete_password():
    del_service_name = delete_service_entry.get()
    del_email = delete_username_entry.get()
    delete.delete_rec(username,del_service_name,del_email)
    delete_service_entry.delete(0,END)
    delete_username_entry.delete(0,END)

    delete_sumbit_button.config(text='Close',command=delete_win.destroy)

# deleting password
def delete_password():
    global delete_win, delete_service_entry,delete_username_entry,delete_sumbit_button

    delete_win = tk.Toplevel()
    delete_win.title("Delete Password")
    delete_win.geometry('400x400+500+300')
    delete_win.resizable('false', 'false')
    delete_win.configure(bg='black')

    # labels
    delete_service_label = tk.Label(delete_win, text='SERVICE NAME:',bg='black',fg='#39FF14',font=('helvetica',14))
    delete_service_label.grid(row=0, column=0, pady=20)

    delete_username_label = tk.Label(delete_win, text='EMAIL :',bg='black',fg='#39FF14',font=('helvetica',14))
    delete_username_label.grid(row=1, column=0, pady=20)

    delete_dum_label1 = tk.Label(delete_win, text='',bg='black',fg='black')
    delete_dum_label1.grid(row=2, column=0, pady=20)


    # entry
    delete_service_entry = tk.Entry(delete_win)
    delete_service_entry.grid(row=0, column=1, pady=20)
    delete_username_entry = tk.Entry(delete_win)
    delete_username_entry.grid(row=1, column=1, pady=20)
    

   
    # sumbit button
    delete_sumbit_button = ttk.Button(delete_win, text='DELETE RECORD', command=actually_delete_password)
    delete_sumbit_button.grid(row=4, column=0, columnspan=2, pady=20, padx=30,ipadx=125)

    # focusing on entry box
    delete_service_entry.focus()
    
    

# modifying exisiting passwords
def modify_password():
    global modify_win, modify_username_entry, modify_masterpwd_entry ,modify_service_entry,modify_sumbit_button,modify_newpwd_entry
    modify_win = tk.Toplevel()
    modify_win.title("Change Password")
    modify_win.geometry('400x400+500+300')
    modify_win.resizable('false', 'false')
    modify_win.configure(bg='black')

    # labels
    modify_service_label = tk.Label(modify_win, text='SERVICE NAME:',bg='black',fg='#39FF14',font=('helvetica',14))
    modify_service_label.grid(row=0, column=0, pady=20)

    modify_username_label = tk.Label(modify_win, text='EMAIL :',bg='black',fg='#39FF14',font=('helvetica',14))
    modify_username_label.grid(row=1, column=0, pady=20)

    modify_dum_label1 = tk.Label(modify_win, text='',bg='black',fg='black')
    modify_dum_label1.grid(row=2, column=0, pady=20)

    modify_masterpwd_label = tk.Label(modify_win, text='OLD PASSWORD :',bg='black',fg='#39FF14',font=('helvetica',14))
    modify_masterpwd_label.grid(row=2, column=0, pady=20)

    modify_newpwd_label = tk.Label(modify_win, text='NEW PASSWORD :',bg='black',fg='#39FF14',font=('helvetica',14))
    modify_newpwd_label.grid(row=3, column=0, pady=20)

    # entry
    modify_service_entry = tk.Entry(modify_win)
    modify_service_entry.grid(row=0, column=1, pady=20)
    modify_username_entry = tk.Entry(modify_win)
    modify_username_entry.grid(row=1, column=1, pady=20)
    modify_masterpwd_entry = tk.Entry(modify_win,show='*')
    modify_masterpwd_entry.grid(row=2, column=1, pady=20)
    modify_newpwd_entry = tk.Entry(modify_win,show='*')
    modify_newpwd_entry.grid(row=3, column=1, pady=20)

   
    # sumbit button
    modify_sumbit_button = ttk.Button(modify_win, text='CHANGE PASSWORD', command=actually_modify_password)
    modify_sumbit_button.grid(row=4, column=0, columnspan=2, pady=20,padx=10,ipadx=125)

    # focusing on entry box
    modify_service_entry.focus()
    
    

# options in edit password
def edit_existing_passwd():
    global modify_button_image1,delete_pass_image,exit_button_image_1
    clear()
    modify_button_image1 = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/uppass.png',master=exist_win)
    modify_pass_button = tk.Button(exist_win,image=modify_button_image1, command= modify_password)
    modify_pass_button.pack(pady=20)

    delete_pass_image = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/deletepass.png',master=exist_win)
    delete_pass_button = tk.Button(exist_win, image=delete_pass_image, command= delete_password)
    delete_pass_button.pack(pady=20)

    exit_button_image_1 = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/CLOSE.png',master=exist_win)
    exit_button_add = tk.Button(exist_win, image=exit_button_image_1, command = lambda :[clear(),show_details()])
    exit_button_add.pack(pady=20)



# showing services
def show_details():
    global service_listbox,service_image,add_image,modify_image,log_out_image
    exist_win.title("Password Manager")
    total_details = get_exist_pass(username)
    if total_details:
        select_label = tk.Label(exist_win,text='Select Service to Show Password ',bg='black',fg='#39FF14',font=('helvetica',14))
        select_label.pack()
    else:
        select_label = tk.Label(exist_win,text='Please add Passwords!',bg='black',fg='#39FF14',font=('helvetica',14))
        select_label.pack()
    service_list = []
    for services in total_details:
        if services[2] not in service_list:
            service_list.append(services[2])
    service_listbox = tk.Listbox(exist_win,background="black", fg="white",selectbackground="blue",highlightcolor="Red")
    service_listbox.pack(pady=5)
    service_listbox.insert(tk.END,*service_list)

    service_image = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/showpasswords.png',master=exist_win)
    service_button = tk.Button(exist_win,image=service_image,command=display)
    service_button.pack(pady=5)

    add_image = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/addpass.png',master=exist_win)
    add_button = tk.Button(exist_win,image=add_image,command=add_new_passwd)
    add_button.pack(pady=5,expand=TRUE)

    modify_image = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/CHANGE.png',master=exist_win)
    modify_button = tk.Button(exist_win,image=modify_image,command=edit_existing_passwd)
    modify_button.pack(pady=5,expand=TRUE)

    log_out_image = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/logout.png',master=exist_win)
    log_out_button = tk.Button(exist_win,image=log_out_image,command=exist_win.destroy)
    log_out_button.pack(pady=5,expand=TRUE)
    





# checking master passsword
def checkpwd():
    global username,masterpassword
    username = username_entry.get()
    masterpassword = masterpwd_entry.get()
    salt = 'LTC'
    passwd = masterpassword[0:1] + salt + masterpassword[1:]
    res=hashlib.md5(bytes(passwd,'utf-8')).hexdigest()

    chktup=(username,res)
    for k in get_master():
        if k == chktup:
            messagebox.showinfo('Success!','Signed in Successfully')
            clear()
            show_details()
            break
    else:
        messagebox.showerror('Failed!','Master Password and Username dont match')
        masterpwd_entry.delete(0,tk.END)


    
    

def exist_user():
    global exist_win,username_entry,masterpwd_entry
    exist_win = tk.Toplevel()
    exist_win.title("Sign In")
    exist_win.geometry('400x400+500+300')
    exist_win.resizable('false','false')
    exist_win.configure(bg='black')

    # labels
    username_label = tk.Label(exist_win,text='USERNAME :',bg='black',fg='#39FF14',font=('helvetica',14))
    username_label.grid(row=0,column=0,pady=20)

    dum_label1 = tk.Label(exist_win,text='',bg='black',fg='green',font=('helvetica',14))
    dum_label1.grid(row=1,column=0,pady=20)

    masterpwd_label = tk.Label(exist_win,text='MASTER PASSWORD :',bg='black',fg='#39FF14',font=('helvetica',14))
    masterpwd_label.grid(row=2,column=0,pady=20)

    # entry
    username_entry=tk.Entry(exist_win)
    username_entry.grid(row=0,column=1,pady=20)
    masterpwd_entry=tk.Entry(exist_win,show="*")
    masterpwd_entry.grid(row=2,column=1,pady=20)
    
    # dummy label
    dum_label1 = tk.Label(exist_win,text='',bg='black',fg='white',font=('helvetica',10))
    dum_label1.grid(row=3,column=1,pady=20)
    
    # sumbit button 
    #sign_in_image = tk.PhotoImage(file='signin.png')
    sumbit_button = ttk.Button(exist_win,text='SIGN IN',command=checkpwd)
    sumbit_button.grid(row=5,column=0,columnspan=2,pady=10,padx=15,ipadx=150)

    # focusing on entry box
    username_entry.focus()


def sumbit():
    global exit_button_image,close_image
    name = name_entry.get()
    master = master_entry.get()
    chkmaster = masterconfi_entry.get()
    if name!= '' and master!='':
        if chkmaster == master:
            add_master(name,master)
            messagebox.showinfo('Success',f'New User {name} Created! ')
            forget_newuser()
            message_label.config(text='Sign Into Existing User Please')
        else:
            messagebox.showerror('Failed','Master Password error! Try later')
            forget_newuser()
    else:
        messagebox.showerror('Failed','Fields Are Empty! Please Fill in')
        forget_newuser()

    close_image = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/CLOSE.png',master=new_win)
    sumbit_button.config(image=close_image,command=new_win.destroy)



def new_user():
    global name_entry,master_entry,masterconfi_entry,sumbit_button,new_win,message_label,sumbit_user_image
    new_win = tk.Toplevel()
    new_win.title("New User")
    new_win.geometry('400x400+500+300')
    new_win.resizable('false','false')
    new_win.configure(bg='black')

    # labels
    name_label = tk.Label(new_win,text='USERNAME :',bg='black',fg='#39FF14',font=('helvetica',10))
    name_label.grid(row=0,column=0,pady=20,padx=20)
    master_label = tk.Label(new_win,text='MASTER PASSWORD :',bg='black',fg='#39FF14',font=('helvetica',10))
    master_label.grid(row=1,column=0,pady=20,padx=20)
    confi_label = tk.Label(new_win,text='CONFIRM MASTER PASSWORD :',bg='black',fg='#39FF14',font=('helvetica',10))
    confi_label.grid(row=2,column=0,pady=20,padx=20)

    # entry
    name_entry=tk.Entry(new_win)
    name_entry.grid(row=0,column=1,pady=20)
    master_entry=tk.Entry(new_win,show="*")
    master_entry.grid(row=1,column=1,pady=20)
    masterconfi_entry=tk.Entry(new_win,show="*")
    masterconfi_entry.grid(row=2,column=1,pady=20)

    # dummy label for grid
    #dum_label1 = tk.Label(new_win,text='')
    #dum_label1.grid(row=3,column=0,pady=20)
    message_label = tk.Label(new_win,text='',bg='black',fg='white',font=('helvetica',10))
    message_label.grid(row=4,column=0,pady=20)
   

    # sumbit button 
    sumbit_user_image = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/SUBMIT.png',master=new_win)
    sumbit_button = tk.Button(new_win,image=sumbit_user_image,command=sumbit)
    sumbit_button.grid(row=6,column=1,pady=10,padx=20)

    # focusing on entry box
    name_entry.focus()

def open_info():
    messagebox.showinfo('Information','''This is a GUI Password Manager, That uses Encryption to store passwords localy on your machine ensuring maximum privacy and giving you the option of having multiple users. A make in india initative.''')
    


def about_us():
    global about_Img 
    about_win = tk.Toplevel()
    about_win.title("ABOUT US")
    about_win.geometry('400x400+500+300')
    about_win.resizable('false','false')
    about_win.configure(bg='black')

    about_Img = ImageTk.PhotoImage(file="/home/kali/Downloads/Project_Password_Manager_12A/Main program/about_final.png",master=about_win)
    about_img_button = tk.Button(about_win, image=about_Img,command=open_info)
    about_img_button.pack()



def open():
    global Img,win,about_image,new_user_image,exist_user_image
    root.geometry('500x500+50+50')
    win = tk.Toplevel()
    win.title("PASSWORD MANAGER")
    win.geometry('400x400+500+300')
    win.resizable('false','false')
    win.configure(bg='black')

    #picture
    Img = ImageTk.PhotoImage(file="/home/kali/Downloads/Project_Password_Manager_12A/Main program/LOGODARKSMALL1.png",master=win)
    img_label = tk.Label(win, image=Img)
    img_label.pack()

    #main_buttons
    new_user_image = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/new.png',master=win)
    new_button = tk.Button(win,image=new_user_image,command=new_user)
    new_button.pack(side=LEFT)

    exist_user_image = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/exist2.png',master=win)
    exist_button = tk.Button(win,image=exist_user_image,command=exist_user)
    exist_button.pack(side=RIGHT)

    #about us
    about_image = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/about us.png',master=win)
    about_button = tk.Button(win,image=about_image,command=about_us)
    about_button.pack(side=LEFT,padx=40)

def delete_user_from_database(username_to_delete):
    db = mysql.connect(user='root',passwd='root',host='localhost',database='master_password')
    cur = db.cursor()
    statement = 'DROP table {}'.format(username_to_delete)
    state2 = '''DELETE from password 
    WHERE name = "{}" '''.format(username_to_delete)
    try:
        cur.execute(statement)
        cur.execute(state2)
        db.commit()
        messagebox.showinfo('Success',f'User {username_to_delete} successfully deleted!')
    except Exception as error:
        db.rollback()
        messagebox.showerror('Failed',f"Couldn't Delete User Data : {error}")
    

def check_for_del():
    user_data = get_master()
    print(user_data)
    del_username = del_username_entry.get()
    del_passwd = del_masterpwd_entry.get()
    salt = 'LTC'
    passwd = del_passwd[0:1] + salt + del_passwd[1:]
    res=hashlib.md5(bytes(passwd,'utf-8')).hexdigest()
    data = (del_username,res)
    print(data)
    if data in user_data:
        response = messagebox.askokcancel('User Found',f'{del_username} found, Proceed to Delete?')
        if response == 1:
            delete_user_from_database(del_username)
        else:
            messagebox.showinfo('Failed','User not deleted')
    else:
        messagebox.showerror('Error','User Not found!')
    del_username_entry.delete(0,END)
    del_masterpwd_entry.delete(0,END)
    

   
    

def delete_screen():
    global del_username_entry,del_masterpwd_entry,del_win,del_sumbit_button_image
    del_win = tk.Toplevel()
    del_win.title("Delete User")
    del_win.geometry('400x400+500+300')
    del_win.resizable('false','false')
    del_win.configure(bg='black')

    # labels
    del_label = tk.Label(del_win,text='USERNAME :',bg='black',fg='#39FF14',font=('helvetica',12))
    del_label.grid(row=0,column=0,pady=20,padx=20)

    del_dum_label1 = tk.Label(del_win,text='',bg='black',fg='#39FF14')
    del_dum_label1.grid(row=1,column=0,pady=20)

    del_masterpwd_label = tk.Label(del_win,text='MASTER PASSWORD :',bg='black',fg='#39FF14',font=('helvetica',12))
    del_masterpwd_label.grid(row=2,column=0,pady=20,padx=20)

    # entry
    del_username_entry=tk.Entry(del_win)
    del_username_entry.grid(row=0,column=1,pady=20)
    del_masterpwd_entry=tk.Entry(del_win,show="*")
    del_masterpwd_entry.grid(row=2,column=1,pady=20)
    
    # dummy label
    del_dum_label3 = tk.Label(del_win,text='',bg='black',fg='white')
    del_dum_label3.grid(row=3,column=1,pady=20)
    
    
    # sumbit button 
    
    del_sumbit_button_image = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/SUBMIT.png',master=del_win)
    del_sumbit_button = tk.Button(del_win,image=del_sumbit_button_image,command=check_for_del,borderwidth=2)
    del_sumbit_button.grid(row=4,column=1,pady=10,padx=50)

    # focusing on entry box
    del_username_entry.focus()


#main window
root = tk.Tk()
root.title("PASSWORD MANAGER")
root.geometry('500x500+500+150')
root.resizable('false','false')
root.configure(bg='black')
about_Img_1 = ImageTk.PhotoImage(file="/home/kali/Downloads/Project_Password_Manager_12A/Main program/about_final.png",master=root)
about_img_button = tk.Button(root, image=about_Img_1,command=open_info)
about_img_button.pack()

main_button_image = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/start.png',master=root)
main_button = tk.Button(root,image=main_button_image,command=open)
main_button.pack(side=LEFT)

exit_button_image = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/end.png',master=root)
exit_button = tk.Button(root,image=exit_button_image,command=root.quit)
exit_button.pack(side=LEFT,padx=90)

delete_button_image = tk.PhotoImage(file='/home/kali/Downloads/Project_Password_Manager_12A/Main program/delete.png',master=root)
delete_button = tk.Button(root,image=delete_button_image,command=delete_screen)
delete_button.pack(side=LEFT)

root.mainloop()