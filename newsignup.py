#Modules
import tkinter as tk
from tkinter import *
from tkinter import messagebox as msg
import os
import math
import random
import smtplib
import mysql.connector as sql
OTP = ""

##Clear Window
def clear_everything():
    for i in MainWin.winfo_children():
        i.destroy()

##Login_verifcation
def check_details(email, password):
    flag = 0
    connection = sql.connect(host = "localhost", user = "root", password = "root", database = "dds_user")
    mysql = connection.cursor()
    mysql.execute("Select * from users")
    for i in mysql:
        if i[0] == email:
            if i[1] == password:
                print("Found it!!")
                flag = 0
                MainWin.destroy()
                break
        else:
            print("I am at wrong place")
            flag = 1
    if flag == 1:
        print("Details not found!!")

##Login_Page
def login_widget():
##    MainWin = tk.Tk()
    MainWin.geometry("500x400")
    #MainWin.resizable(False,False)
    MainWin.title("Login..")
##    MainWin.iconbitmap("doc.ico")

    #properly centers the window
    '''MainWin.eval('tk::PlaceWindow . center')'''

    #Labels and Textboxes
    tk.Label(MainWin, text = "Disease Detection System").pack()
    tk.Label(MainWin, text = "Log In Page").pack()
    

    empty()
    #email
    E_mail = tk.Label(MainWin,text = "Email ID ")
    E_mail.pack()
    email_text = tk.Entry()
    email_text.pack()

    #password
    Pass_word = tk.Label(MainWin, text = "Password")
    Pass_word.pack()
    pass_text = tk.Entry(show = '*')
    pass_text.pack()
    empty()

    tk.Button(MainWin, text = "Login", command = lambda:check_details(email_text.get(), pass_text.get())).pack()

    
##OTP widget
def show_otp_widget(email, paswrd):
    if validate(email,paswrd):
        #OTP generation
        global OTP
        dig = "0123456789"
        for i in range(6):
            OTP += dig[math.floor(random.random()*10)]
            
        gen_OTP = "Welcome to \"Disease Detection System\" \nPlease verify your,\nEmail Id : " + email + "\nPassword : " + paswrd + " \nwith this OTP : " + OTP + "."
##        msg = gen_OTP
##        smtp = smtplib.SMTP('smtp.gmail.com',587)
##        smtp.starttls()
##        user_email = email.get()
##        smtp.login("aadarshprem82@gmail.com","icyekhmzqjncxpqd")
##        smtp.sendmail('Aadarsh',user_email,msg)
        print(gen_OTP)
        
        #OTP Widget
        empty()
        One_tp.pack()
        otp.pack()
        submit_otp.pack()

def verification(temp, email, passwrd):
    global OTP
    if temp.get() == OTP:
        go_ahead(email,passwrd)
    else:
        tk.Label(MainWin, text = "Entered Wrong OTP!!").pack()

    
#empty line
def empty():
    tk.Label(MainWin, text = " ").pack()

def validate(email, pswrd):
    print("I am into validation..")
    em_txt = email
    if em_txt == "":
        msg.showwarning("Empty!!","Email ID cannot be empty.")
    elif em_txt[len(em_txt)-9:len(em_txt)] != 'gmail.com':
        msg.showwarning("Invalid!!","Please Enter a valid Email ID.")
    elif '@' not in em_txt:
        msg.showwarning("Invalid!!","Please Enter a valid Email ID.")
        
    elif pswrd == "":
        msg.showwarning("Empty!!","Password cannot be empty.")
    else:
        return True

def go_ahead(email, passwrd):
    connection = sql.connect(host = 'localhost', user = 'root', password = 'root', database="dds_user")
    point = connection.cursor()
    sql_query = "insert into users (email, password) values(%s,%s)"
    
    point.execute(sql_query,(email, passwrd))
    connection.commit()
    if point.rowcount != 0:
        print("Data inserted successfully!!")
        clear_everything()
        
        login_widget()
    else:
        print("Something went wrong!!")
    

#MainWin(Login or SignUp Page)
MainWin = tk.Tk()
MainWin.geometry("1000x500")
MainWin.resizable(False,False)
MainWin.title("Sign Up..")
#MainWin.iconbitmap("doc.ico")

#properly centers the window
'''MainWin.eval('tk::PlaceWindow . center')'''

#Labels and Textboxes
tk.Label(MainWin, text = "Disease Detection System",font=('Times New Roman Bold',30)).pack(side=TOP,pady=10)
tk.Label(MainWin, text = "Sign Up Page",font=('verdana',15)).pack(side =TOP,pady=10)
empty()

#email
E_mail = tk.Label(MainWin,text = "Email ID ",font=('Roboto Bold',30))
E_mail.pack()
email_tex = tk.Entry(font=('Times ',20))
#Entry(root,font=('Times',20))  
email_tex.pack()

#password
Pass_word = tk.Label(MainWin, text = "Password",font=('Roboto Bold',30))
Pass_word.pack()
pass_wrd = tk.Entry(show = '*',font=('Times',20))
pass_wrd.pack()

One_tp = tk.Label(MainWin, text = "OTP ",font=('Roboto Bold',30))
otp = tk.Entry()
submit_otp = tk.Button(MainWin, text = "Submit", command = lambda:verification(otp,email_tex.get(), pass_wrd.get()))#verification(otp, email_tex.get(), pass_wrd.get())

empty()

#lambda is important here.

tk.Button(MainWin, text = "Sign Up",font=('Roboto Bold',20), command = lambda:show_otp_widget(email_tex.get(),pass_wrd.get())).pack()
#command = lambda:show_otp_widget(email_tex,pass_wrd)) || command = lambda:validate(email_tex,pass_wrd)

print(email_tex.get())
print(pass_wrd.get())
