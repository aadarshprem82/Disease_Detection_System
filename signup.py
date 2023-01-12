from tkinter import *

root = Tk()
root.geometry("400x400")
bg = PhotoImage(file = "C:\\Users\\USER\Pictures\\Screenshots\\New folder\\R.png")
canvas1 = Canvas( root, width = 300,height = 400)
canvas1.pack(fill = "both", expand = True)

canvas1.create_image( 0, 0, image = bg,anchor = "nw")


lb1= Label(root, text="Enter Name",width=10, font=("Times",30))  
lb1.place(x=200, y=120)  
en1= Entry(root,font=('Times',20))
en1.place(x=600, y=120)  

lb2= Label(root, text="Enter Emai-id", width=10, font=("Times",30))  
lb2.place(x=200, y=160)  
en2= Entry(root,font=('Times',20))  
en2.place(x=600, y=160)

lb3= Label(root, text="Enter Password", width=13,font=("Times",30))  
lb3.place(x=200, y=200)  
en3= Entry(root, show='*',font=('Times',20))  
en3.place(x=600, y=200)  

lb4= Label(root, text="Re-Enter Password", width=15,font=("Times",30))  
lb4.place(x=200, y=240)  
en4 = Entry(root,font=('Times',20))
en4.place(x=600, y=240)

lb5=Label(root, text ='New User acount',font=('verdana',15)).place(x=600,y=400)
B1=Button(root, font=("Times",20), text="SignUp").place(x=650,y=450)

lb5=Label(root, text ='I have alredy an acount',font=('verdana',15)).place(x=200,y=400)
B2=Button(root, font=("Times",20), text="Login").place(x=250,y=450)

root.mainloop()
