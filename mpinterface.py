from tkinter import*
from tkinter.ttk import *

root= Tk()
style=Style()


def camwindow():
    cam=Toplevel(root)
    Label(cam,text="Your camera are ready?",font=('Times New Roman',30)).pack(side =TOP,pady=10)
    
def imgwindow():
    img=Toplevel(root)
    Label(img,text="Select or insert any Images",font=('Times New Roman',30)).pack(side=TOP,pady=10)

def txtwindow():
    txt=Toplevel(root)
    Label(txt,text="Type your details ",font=('Times New Roman',30)).pack(side=TOP,pady=10)


style.configure('TButton',font=('calibri',30,'bold'),borderwidth='25')
style.map('TButton',foreground=[('active','green')],background=[('active','Blue')])

Label(root,text ='One App For All Your Health Needs',font=('Times New Roman',30)).pack(side =TOP,pady=10)
Label(root,text ='Welcome User ',font=('verdana',15)).pack(side =TOP,pady=10)

Button(root,text = 'Detect your Disease By Using Camera',command=camwindow).pack(side=TOP,pady=50,padx=100)
Button(root,text = 'Detect your Disease By Using Images',command=imgwindow).pack(side=TOP,pady=50,padx=100)
Button(root,text = 'Detect your Disease By Using Text',command=txtwindow).pack(side=TOP,pady=50,padx=100)
Button(root,text='Exit', command=root.destroy).pack(side=RIGHT,pady=25,padx=50)


root.mainloop()
