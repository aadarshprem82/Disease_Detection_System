from tkinter import*
from tkinter.ttk import *
#import cv2
#import os
import codecs
import webbrowser

root= Tk()
style=Style()

f= open('dds.html', 'w')
html_temp="""
<html>
<head></head>
<body>
<form>
<h2>Please complete this patient registration form with your information and a doctor will contact you shortly. </h2>
<label for="sname"> First Name</label>
<input type="text"><br><br>

<label for="sname">Last Name</label>
<input type="text"><br><br>

<label for="pn">Phone no.</label>
<input type="text"><br><br>

<label for="eid">E-mail Id</label>
<input type="text"><br><br>

<label for="dob">Date of Birth</label>
<input type="text"><br><br>

<label for="dob">Address</label>
<input type="text"><br><br>

<label for="mar">Past Medical History</label>

<input type="checkbox" id="ms1 name="ms1">
<label for="mar1">Anemia</label>

<input type="checkbox" id="ms2 name="ms2">
<label for="mar2">Asthma</label>

<input type="checkbox" id="ms3 name="ms3">
<label for="mar3">Diabetes</label>

<input type="checkbox" id="ms4 name="ms4">
<label for="mar4">Thyroid Disease</label>

<input type="checkbox" id="ms5 name="ms5">
<label for="mar5">Other</label><br><br>



<input type="submit" value="submit">

</form>
</body>
</html>
"""
f.write(html_temp)
f.close()
file=codecs.open("dds.html",'r',"utf-8")
print(file.read())

def camwindow():
    cam=Toplevel(root)
    Label(cam,text="Your camera are ready?",font=('Times New Roman',30)).pack(side =TOP,pady=10)
    #cam_port=0
    #cam=VideoCapture(cam_port)
    #result,image=cam.read()
    #if result:
        #imshow("Hello ",image)
        #waitKey(1)
        #destroyWindow("Hello")
    #else:
        #print("NO image detected")
    



def imgwindow():
    img=Toplevel(root)
    Label(img,text="Select or insert any Images",font=('Times New Roman',30)).pack(side=TOP,pady=10)
    #fileitem = form['filename']
    #if fileitem.filename:
     #   fn=os.path.basename(fileitem.filename)
      #  open(fn,'wb').write(fileitem.file.read())

def txtwindow():
    txt=Toplevel(root)
    Label(txt,text="Type your details ",font=('Times New Roman',30)).pack(side=TOP,pady=10)

def online():
    webbrowser.open('dds.html')
    


style.configure('TButton',font=('calibri',30,'bold'),borderwidth='25')
style.map('TButton',foreground=[('active','green')],background=[('active','Blue')])

Label(root,text ='One App For All Your Health Needs',font=('Times New Roman',30)).pack(side =TOP,pady=10)
Label(root,text ='Welcome User ',font=('verdana',15)).pack(side =TOP,pady=10)

Button(root,text = 'Detect your Disease By Using Camera',command=camwindow).pack(side=TOP,pady=50,padx=100)
Button(root,text = 'Detect your Disease By Using Images',command=imgwindow).pack(side=TOP,pady=50,padx=100)
Button(root,text = 'Detect your Disease By Using Text',command=txtwindow).pack(side=TOP,pady=50,padx=100)
Button(root,text='Exit', command=root.destroy).pack(side=RIGHT,pady=25,padx=50)

Button(root,text = 'Go Online',command=online).pack(side=LEFT,pady=25,padx=50)

root.mainloop()
