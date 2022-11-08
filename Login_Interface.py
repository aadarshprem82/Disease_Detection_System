#Modules
import tkinter as tk
from tkinter import messagebox as msg
import os
import math
import random
import smtplib

OTP = ""

#hidden OTP widget
def show_otp_widget(email, paswrd):
    if validate(email,paswrd):
        #OTP generation
        global OTP
        dig = "0123456789"
        for i in range(6):
            OTP += dig[math.floor(random.random()*10)]
            
        gen_OTP = "Welcome to \"Title\" \nPlease verify your,\nEmail Id : " + email.get() + "\nPassword : " + paswrd.get() + " \nwith this OTP : " + OTP + "."
        msg = gen_OTP
        smtp = smtplib.SMTP('smtp.gmail.com',587)
        smtp.starttls()
        user_email = email.get()
        smtp.login("aadarshprem82@gmail.com","icyekhmzqjncxpqd")
        smtp.sendmail('Aadarsh',user_email,msg)
        
        #OTP Widget
        empty()
        One_tp.pack()
        otp.pack()
        submit_otp.pack()

def verification(temp):
    global OTP
    if temp.get() == OTP:
        print("Verified, Go Main to Window!!")
    else:
        print("Wrong OTP!!")

    
#empty line
def empty():
    tk.Label(MainWin, text = " ").pack()

def validate(email, pswrd):
    print("I am into validation..")
    em_txt = email.get()
    if em_txt == "":
        msg.showwarning("Empty!!","Email ID cannot be empty.")
    elif em_txt[len(em_txt)-4:len(em_txt)] != '.com':
        msg.showwarning("Invalid!!","Please Enter a valid Email ID.")
    elif '@' not in em_txt:
        msg.showwarning("Invalid!!","Please Enter a valid Email ID.")
        
    elif pswrd.get() == "":
        msg.showwarning("Empty!!","Password cannot be empty.")
    else:
        return True

#MainWin(Login or SignUp Page)
MainWin = tk.Tk()
MainWin.geometry("550x350+150+150")
MainWin.resizable(False,False)
MainWin.title("Log in..")

#properly centers the window
'''MainWin.eval('tk::PlaceWindow . center')'''

#Labels and Textboxes
tk.Label(MainWin, text = "Title").pack()
tk.Label(MainWin, text = "Login Page").pack()
empty()

#email
E_mail = tk.Label(MainWin,text = "Email ID ")
E_mail.pack()
email_tex = tk.Entry()
email_tex.pack()

#password
Pass_word = tk.Label(MainWin, text = "Password")
Pass_word.pack()
pass_wrd = tk.Entry(show = '*')
pass_wrd.pack()

One_tp = tk.Label(MainWin, text = "OTP ")
otp = tk.Entry()
submit_otp = tk.Button(MainWin, text = "Submit", command = lambda:verification(otp))

empty()

#lambda is way too important here.
tk.Button(MainWin, text = "Login", command = lambda:show_otp_widget(email_tex,pass_wrd)).pack()# command = lambda:validate(email_tex,pass_wrd)



print(email_tex.get())
print(pass_wrd.get())

