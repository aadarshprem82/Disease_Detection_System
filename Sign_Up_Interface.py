#Modules
import tkinter as tk
from tkinter import *
from tkinter import messagebox as msg
import os
import math
import random
import smtplib
import mysql.connector as sql

#ML_Modules
import numpy as np
import pandas as pd
from scipy.stats import mode
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

#Image_Modules
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk, ImageChops

OTP = ""
input_set = set()
mail = ""

#Clear Window
def clear_everything():
    for i in MainWin.winfo_children():
        i.destroy()
    
#Model Creation
def preparation(user_symptoms):
    data = pd.read_csv("Training.csv").dropna(axis = 1)
    encoder = LabelEncoder()
    data["prognosis"] = encoder.fit_transform(data["prognosis"])

    X = data.iloc[:,:-1]
    Y = data.iloc[:,-1]

    svm_model = SVC()
    nb_model = GaussianNB()
    rf_model = RandomForestClassifier(random_state = 18)
    svm_model.fit(X,Y)
    nb_model.fit(X,Y)
    rf_model.fit(X,Y)

    symptoms = X.columns.values
    symptoms_index = {}
    for i, val in enumerate(symptoms):
        temp = val.replace("_"," ").title()
        all_symptom = " ".join([temp])
        symptoms_index[all_symptom] = i
    data_dict = {"symptom_index":symptoms_index, "prediction_classes":encoder.classes_}
    return prediction(user_symptoms, data_dict, svm_model, nb_model, rf_model)

#Prediction
def prediction(user_symptoms, data_dict, svm_model, nb_model, rf_model):
    input_symptoms = user_symptoms.split(",")
    input = [0]*len(data_dict["symptom_index"])
    for i in input_symptoms:
        index = data_dict["symptom_index"][i]
        input[index] = 1
    input_data = np.array(input).reshape(1,-1)

    svm = data_dict["prediction_classes"][svm_model.predict(input_data)[0]]
    nb = data_dict["prediction_classes"][nb_model.predict(input_data)[0]]
    rf = data_dict["prediction_classes"][rf_model.predict(input_data)[0]]

    result = mode([svm, nb, rf])[0][0]
    return result

##Login_verifcation
def check_details(email, password):
    global mail
    mail = email
    if validate_login(email, password):
        flag = 0
        connection = sql.connect(host = "localhost", user = "root", password = "Dongle@123", database = "dds_user")
        mysql = connection.cursor()
        mysql.execute("Select * from users")
        for i in mysql:
            if i[0] == email:
                if i[1] == password:
                    flag = 0
                    main_page()
                    break
                else:
                    flag = 0
                    msg.showwarning("Wrong!", "You have entered a wrong password.\nTry Again!!")
                    break
            else:
                flag = 1
        if flag == 1:
            msg.showinfo("Not Registered","We can't find you in our database.\nTry Signing Up!!")
            
#End Message
def thank_you():
    clear_everything()
    tk.Label(MainWin, text="ThankYou for using our software.",height=7,width=30,
             font=("Roboto bold",25), bg="lightgreen").grid(row=0, column=0)
    tk.Label(MainWin, text="Your diagnosis has been sent to your email.",
             font=("Roboto bold",11),bg ="lightgreen").grid(row=1, column=0)
    tk.Button(MainWin, text="×", font=("Arial bold",10),
              bg="red",fg="white",command=lambda:exit()).grid(row=2,column=0)
    
#Submission of Data
def click(event):
    print("clicked")
    selected = event.curselection()
    for i in selected:
        global input_set
        if i not in input_set:
            input_set.add(event.get(i))
        print(event.get(i))

def text_predict():
    input_data = formatting()
    diagnosis = preparation(input_data.title())
    final_submit(diagnosis)

#Sending Diagnosis
def final_submit(diagnosis):
    check = msg.askokcancel("Continue!!",
    "Your diagnosis statement will be sent to you on your registered e-mail.\n(Please bear with us it can take few minutes.)")
    if check:
        message = f"Dear {mail},\nThis is a probable disease predicted by our ML model,\n\tThe result of detection is \"{diagnosis}\"\nNote:This is just a prediction based on stored data.\nYou can consult a concerned doctor with this \'link\'"

##        smtp = smtplib.SMTP('smtp.gmail.com',587)
##        smtp.starttls()
##        smtp.login("aadarshprem82@gmail.com","okmmhluijiaaoaqe")
##        smtp.sendmail('Aadarsh',mail,message)
        print(message)
        thank_you()
    else:
        MainWin.destroy()

def formatting():
    global input_set
    input_string = ",".join(input_set)
    print("Input String is ",input_string)
    diagnosis = preparation(input_string.title())
    final_submit(diagnosis)
##    return input_string

def upper_body_symptoms():
    clear_everything()
    msg.showinfo("Procedure","Please select all the symptoms you're having.\n(On the next page!!)")
    MainWin.title("Symptoms from Upper Body Parts")
    #Main Border after Main Window
    main_border = tk.Frame(MainWin, bd=2, relief="sunken", background="lightgreen")
    main_border.grid(row=0, column=0, padx=5, pady=4)
    
    eye_neck_border = tk.Frame(main_border, relief="sunken")
    eye_neck_border.grid(row=0, column=0, padx=5, pady=4)

    #Eye Symptoms
    eye_border = tk.Frame(eye_neck_border, bd=1, relief="sunken")
    eye_border.grid(row=0, column=0, padx=5, pady=4)
    tk.Label(eye_border, text="👀Eye", font=("Roboto bold",15)).grid(row=0, column=0)
    eye = tk.Listbox(eye_border, width=20, height=7, selectmode=tk.MULTIPLE,
                     borderwidth=0, highlightthickness=0,
                     background=eye_border.cget("background"))
    eye_sb = tk.Scrollbar(eye_border, orient="vertical", command=eye.yview)
    eye.configure(yscrollcommand=eye_sb)
    eye_sb.grid(row=1, column=1, sticky="ns")
    eye.grid(row=1, column=0)
    values = ['Sunken Eyes','Pain behind the eyes','Yellowing of eyes'
              ,'Blurred And Distorted Vision','Redness of eyes','Watering From Eyes'
              ,'Visual Disturbances']
    for i in values:
        eye.insert("end", i)

    tk.Button(eye_border, text="Submit",background="lightsalmon",
              font=("Roboto bold",10), width=10,
              command=lambda:click(eye)).grid(row=2, column=0)

    #Neck Symptoms
    neck_border = tk.Frame(eye_neck_border, bd=1, relief="sunken")
    neck_border.grid(row=1, column=0, padx=5, pady=2)

    tk.Label(neck_border, text="✨Neck", font=("Roboto bold",15)).grid(row=0, column=0)

    neck = tk.Listbox(neck_border, width=20, height=7, selectmode=tk.MULTIPLE,
                      borderwidth=0, highlightthickness=0,
                      background=neck_border.cget("background"))

    neck_sb = tk.Scrollbar(neck_border, orient="vertical", command=neck.yview)
    neck.configure(yscrollcommand=neck_sb)
    neck_sb.grid(row=1, column=1, sticky="ns")
    neck.grid(row=1, column=0)
    values = ['Neck Pain','Enlarged Thyroid','Stiff Neck','Patches in throat','Cough',
              'Phlegm','Throat irritation','Mucoid Sputum','Rusty Sputum',
              'Blood in Sputum','Ulcers on tongue']
    for i in values:
        neck.insert("end", i)

    tk.Button(neck_border, text="Submit",background="lightsalmon",
              font=("Roboto bold",10), width=10,
              command=lambda:click(neck)).grid(row=2, column=0)

    head_in_border = tk.Frame(main_border, relief="sunken")
    head_in_border.grid(row=0, column=1, padx=5, pady=4)
    ##Head Symptoms
    head_border = tk.Frame(head_in_border, bd=1, relief="sunken")
    head_border.grid(row=0, column=1, padx=5, pady=4)

    tk.Label(head_border, text="🧠Head", font=("Roboto bold",15)).grid(row=0, column=0)

    head = tk.Listbox(head_border, width=21, height=18, selectmode=tk.MULTIPLE,
                         borderwidth=0, highlightthickness=0,
                         background=head_border.cget("background"))

    head_sb = tk.Scrollbar(head_border, orient="vertical", command=head.yview)
    head.grid(row=1, column=0)
    head_sb.grid(row=1, column=1, sticky='ns')

    values = ['Headache','Sinus Pressure','Dizziness','Slurred Speech','Unsteadiness'
              ,'Depression','Irritability','Altered Sensorium','Lack of Concentration'
              ,'Anxiety','Mood swings']
    for i in values:
        head.insert("end", i)

    tk.Button(head_border, text="Submit",background="lightsalmon",
              font=("Roboto bold",10), width=10,
              command=lambda:click(head)).grid(row=2, column=0)

    nose_face_border = tk.Frame(main_border, relief="sunken")
    nose_face_border.grid(row=0, column=2, padx=5, pady=4)
    ##Nose Symptoms
    nose_border = tk.Frame(nose_face_border, bd=1, relief="sunken")
    nose_border.grid(row=0, column=0, padx=5, pady=4)

    tk.Label(nose_border, text="👃Nose", font=("Roboto bold",15)).grid(row=0, column=0)

    nose = tk.Listbox(nose_border, width=20, height=7, selectmode=tk.MULTIPLE,
                         borderwidth=0, highlightthickness=0,
                         background=nose_border.cget("background"))

    nose_sb = tk.Scrollbar(nose_border, orient="vertical", command=nose.yview)
    nose.configure(yscrollcommand=nose_sb)
    nose_sb.grid(row=1, column=1, sticky="ns")
    nose.grid(row=1, column=0)
    values = ['Continuous Sneezing','Breathlessness','Runny Nose','Loss of smell',
              'Red Sore around Nose']
    for i in values:
        nose.insert("end", i)

    tk.Button(nose_border, text="Submit",background="lightsalmon",
              font=("Roboto bold",10), width=10,
              command=lambda:click(nose)).grid(row=2, column=0)

    face_border = tk.Frame(nose_face_border, bd=1, relief="sunken")
    face_border.grid(row=1, column=0, padx=5, pady=4)
    ##Face Symptoms
    tk.Label(face_border, text="👩🏻‍🦲Face", font=("Roboto bold",15)).grid(row=0, column=0)

    face = tk.Listbox(face_border, width=20, height=7, selectmode=tk.MULTIPLE,
                         borderwidth=0, highlightthickness=0,
                         background=face_border.cget("background"))

    face_sb = tk.Scrollbar(face_border, orient="vertical", command=face.yview)
    face.configure(yscrollcommand=face_sb)
    face_sb.grid(row=1, column=1, sticky="ns")
    face.grid(row=1, column=0)
    values = ['Puffy Face and Eyes','Drying and Tingling Lips','Pus filled pimples',
              'Blackheads','Scarring','Skin Peeling']
    for i in values:
        face.insert("end", i)

    tk.Button(face_border, text="Submit",background="lightsalmon",
              font=("Roboto bold",10), width=10,
              command=lambda:click(face)).grid(row=2, column=0)

    ##Button goes to mid_body_symptoms
    tk.Button(MainWin, text="Next..",background="salmon",
              font=("Roboto bold",10),width=65,
              command=lambda:mid_body_symptoms()).grid(row=1, column=0)

def mid_body_symptoms():
    clear_everything()
    MainWin.title("Symptoms from Mid-Body Parts")

    mid_main_border = tk.Frame(MainWin, bd=2, relief="sunken", background="lightgreen")
    mid_main_border.grid(row=0, column=0, padx=5, pady=4)

    skin_chest_border = tk.Frame(mid_main_border, relief="sunken")
    skin_chest_border.grid(row=0, column=0, padx=5, pady=4)
    ##Skin Symptoms
    skin_border = tk.Frame(skin_chest_border, bd=1, relief="sunken")
    skin_border.grid(row=0, column=0, padx=5, pady=4)

    tk.Label(skin_border, text="✨Skin", font=("Roboto bold",15)).grid(row=0, column=0)

    skin = tk.Listbox(skin_border, width=20, height=7, selectmode=tk.MULTIPLE,
                         borderwidth=0, highlightthickness=0,
                         background=skin_border.cget("background"))

    skin_sb = tk.Scrollbar(skin_border, orient="vertical", command=skin.yview)
    skin.grid(row=1, column=0)
    skin_sb.grid(row=1, column=1, sticky='ns')

    values = ['Itching','Skin Rash','Nodal Skin Eruptions','Yellowish Skin',
              'Bruising','Internal Itching','Toxic Look (typhos)',
              'Dischromic  Patches','Blister','Yellow Crust Ooze']
    for i in values:
        skin.insert("end", i)

    tk.Button(skin_border, text="Submit",background="lightsalmon",
              font=("Roboto bold",10), width=10,
              command=lambda:click(skin)).grid(row=2, column=0)

    ##Chest Symptoms
    chest_border = tk.Frame(skin_chest_border, bd=1, relief="sunken")
    chest_border.grid(row=1, column=0, padx=5, pady=4)

    tk.Label(chest_border, text="✨Chest", font=("Roboto bold",15)).grid(row=0, column=0)

    chest = tk.Listbox(chest_border, width=20, height=7, selectmode=tk.MULTIPLE,
                         borderwidth=0, highlightthickness=0,
                         background=chest_border.cget("background"))

    chest_sb = tk.Scrollbar(chest_border, orient="vertical", command=chest.yview)
    chest.grid(row=1, column=0)
    chest_sb.grid(row=1, column=1, sticky='ns')

    values = ['Chest Pain', 'Fast heart Rate', 'Palpitations']
    for i in values:
        chest.insert("end", i)

    tk.Button(chest_border, text="Submit",background="lightsalmon",
              font=("Roboto bold",10), width=10,
              command=lambda:click(chest)).grid(row=2, column=0)

    body_in_border = tk.Frame(mid_main_border, relief="sunken")
    body_in_border.grid(row=0, column=1, padx=5, pady=4)
    ##Body Symptoms
    body_border = tk.Frame(body_in_border, bd=1, relief="sunken")
    body_border.grid(row=0, column=1, padx=5, pady=4)

    tk.Label(body_border, text="🏋🏻‍♂️Body", font=("Roboto bold",15)).grid(row=0, column=0)

    body = tk.Listbox(body_border, width=21, height=18, selectmode=tk.MULTIPLE,
                         borderwidth=0, highlightthickness=0,
                         background=body_border.cget("background"))

    body_sb = tk.Scrollbar(body_border, orient="vertical", command=body.yview)
    body.grid(row=1, column=0)
    body_sb.grid(row=1, column=1, sticky='ns')

    values = ['Shivering', 'Chills', 'Fatigue', 'Weight Gain',
              'Cold hands and Feets', 'Weight Loss', 'Restlessness', 'Lethargy',
              'High Fever', 'Sweating', 'Dehydration' ,'Back Pain',
              'Mild Fever', 'Fluid Overload', 'Swelled Lymph Nodes', 'Malaise',
              'Congestion', 'Swollen blood vessels', 'Movement Stiffness',
              'Spinning movements', 'Weakness of one body side',
              'Red Spots over body', 'Abnormal Menstruation']
    for i in sorted(values):
        body.insert("end", i)

    tk.Button(body_border, text="Submit",background="lightsalmon",
              font=("Roboto bold",10), width=10,
              command=lambda:click(body)).grid(row=2, column=0)


    stomach_muscle_border = tk.Frame(mid_main_border, relief="sunken")
    stomach_muscle_border.grid(row=0, column=2, padx=5, pady=4)
    ##Stomach Symptoms
    stomach_border = tk.Frame(stomach_muscle_border, bd=1, relief="sunken")
    stomach_border.grid(row=0, column=0, padx=5, pady=4)

    tk.Label(stomach_border, text="🍔Stomach", font=("Roboto bold",15)).grid(row=0, column=0)

    stomach = tk.Listbox(stomach_border, width=20, height=7, selectmode=tk.MULTIPLE,
                         borderwidth=0, highlightthickness=0,
                         background=stomach_border.cget("background"))

    stomach_sb = tk.Scrollbar(stomach_border, orient="vertical", command=stomach.yview)
    stomach.grid(row=1, column=0)
    stomach_sb.grid(row=1, column=1, sticky='ns')

    values = ['Stomach Pain', 'Acidity', 'Indigestion', 'Nausea',
              'Loss of appetite', 'Swelling of stomach', 'Excessive Hunger',
              'Belly Pain', 'Increased Appetite', 'Stomach Bleeding',
              'Distention of Abdomen']
    for i in values:
        stomach.insert("end", i)

    tk.Button(stomach_border, text="Submit",background="lightsalmon",
              font=("Roboto bold",10), width=10,
              command=lambda:click(stomach)).grid(row=2, column=0)

    ##Muscle Symptoms
    muscle_border = tk.Frame(stomach_muscle_border, bd=1, relief="sunken")
    muscle_border.grid(row=1, column=0, padx=5, pady=4)

    tk.Label(muscle_border, text="🦾Muscle", font=("Roboto bold",15)).grid(row=0, column=0)

    muscle = tk.Listbox(muscle_border, width=20, height=7, selectmode=tk.MULTIPLE,
                         borderwidth=0, highlightthickness=0,
                         background=muscle_border.cget("background"))

    muscle_sb = tk.Scrollbar(muscle_border, orient="vertical", command=muscle.yview)
    muscle.grid(row=1, column=0)
    muscle_sb.grid(row=1, column=1, sticky='ns')

    values = ['Muscle Wasting', 'Cramps', 'Obesity', 'Muscle Weakness',
              'Muscle Pain']
    for i in values:
        muscle.insert("end", i)

    tk.Button(muscle_border, text="Submit",background="lightsalmon",
              font=("Roboto bold",10), width=10,
              command=lambda:click(muscle)).grid(row=2, column=0)

    lower_border = tk.Frame(MainWin, relief="sunken", background="lightgreen")
    lower_border.grid(row=1, column=0, padx=5, pady=4)
    
    ##Button to lower_body_symptoms
    tk.Button(lower_border, text="Next..",background="salmon",
              font=("Roboto bold",10),width=30,
              command=lambda:lower_body_symptoms()).grid(row=0, column=0)

    tk.Label(lower_border, text="  ", background="lightgreen").grid(row=0, column=1)
    
    tk.Button(lower_border, text="Previous Menu",background="salmon",
              font=("Roboto bold",10),width=30,
              command=lambda:upper_body_symptoms()).grid(row=0, column=2)

def lower_body_symptoms():
    clear_everything()
    MainWin.title("Symptoms from Lower Body Parts")

    lower_main_border = tk.Frame(MainWin, bd=1, relief="sunken", bg="lightgreen")
    lower_main_border.grid(row=0, column=0, padx=5, pady=10)

    
    limbs_border = tk.Frame(lower_main_border, bd=1, relief="sunken")
    limbs_border.grid(row=0, column=0, padx=5, pady=5)
    ##limbs Symptoms
    tk.Label(limbs_border, text="🙋🏻‍♂️Limbs", font=("Roboto bold",15)).grid(row=0, column=0)

    limbs = tk.Listbox(limbs_border, width=21, height=18, selectmode=tk.MULTIPLE,
                         borderwidth=0, highlightthickness=0,
                         background=limbs_border.cget("background"))

    limbs_sb = tk.Scrollbar(limbs_border, orient="vertical", command=limbs.yview)
    limbs.grid(row=1, column=0)
    limbs_sb.grid(row=1, column=1, sticky='ns')

    values = ['Weakness in limbs', 'Swollen Legs', 'Brittle Nails',
              'Swollen Extremeties', 'Knee Pain', 'Hip Joint Pain',
              'Swelling Joints', 'Loss of balance', 'Prominent veins on calf',
              'Painful Walking', 'Small dents in nails', 'inflammatory nails',
              'Joint Pain']
    for i in values:
        limbs.insert("end", i)

    tk.Button(limbs_border, text="Submit",background="lightsalmon",
              font=("Roboto bold",10), width=10,
              command=lambda:click(limbs)).grid(row=2, column=0)

    excretion_border = tk.Frame(lower_main_border, bd=1, relief="sunken")
    excretion_border.grid(row=0, column=1, padx=5, pady=4)
    ##Excretion Symptoms
    tk.Label(excretion_border, text="🚽Excretion", font=("Roboto bold",15)).grid(row=0, column=0)

    excretion = tk.Listbox(excretion_border, width=22, height=18, selectmode=tk.MULTIPLE,
                         borderwidth=0, highlightthickness=0,
                         background=excretion_border.cget("background"))

    excretion_sb = tk.Scrollbar(excretion_border, orient="vertical", command=excretion.yview)
    excretion.grid(row=1, column=0)
    excretion_sb.grid(row=1, column=1, sticky='ns')

    values = ['Vomiting', 'Burning Micturition', 'Spotting  Urination',
              'Dark Urine', 'Yellow Urine', 'Pain during Bowel Movements',
              'Pain in Anal Region', 'Bloody Stool', 'Irritation in Anus',
              'Bladder discomfort', 'Foul Smell of Urine', 'Passage of Gases',
              'Polyuria']
    for i in values:
        excretion.insert("end", i)

    tk.Button(excretion_border, text="Submit",background="lightsalmon",
              font=("Roboto bold",10), width=10,
              command=lambda:click(excretion)).grid(row=2, column=0)

    ##Previous History Symptoms
    prev_border = tk.Frame(lower_main_border, bd=1, relief="sunken")
    prev_border.grid(row=0, column=2, padx=5, pady=4)

    tk.Label(prev_border, text="🔮Previous History", font=("Roboto bold",15)).grid(row=0, column=0)

    prev = tk.Listbox(prev_border, width=22, height=18, selectmode=tk.MULTIPLE,
                      borderwidth=0, highlightthickness=0,
                      background=prev_border.cget("background"))

    prev_sb = tk.Scrollbar(prev_border, orient="vertical", command=prev.yview)
    prev.grid(row=1, column=0)
    prev_sb.grid(row=1, column=1, sticky='ns')

    values = ['Irregular Sugar Level', 'Diarrhoea', 'Acute Liver failure',
              'Extra Marital Contacts', 'Family History',
              'Receiving blood transfusion', 'Receiving Unsterile Injections',
              'Coma', 'History of Alcohol Consumption']
    for i in values:
        prev.insert("end", i)

    tk.Button(prev_border, text="Submit",background="lightsalmon",
              font=("Roboto bold",10), width=10,
              command=lambda:click(prev)).grid(row=2, column=0)

    lower_border = tk.Frame(MainWin, relief="sunken", background="lightgreen")
    lower_border.grid(row=1, column=0, padx=5, pady=4)
    
    ##Button to Final Last Submit
    tk.Button(lower_border, text="Final Submit",background="salmon",
              font=("Roboto bold",10),width=30,
              command=lambda:formatting()).grid(row=0, column=0)

    tk.Label(lower_border, text="  ", background="lightgreen").grid(row=0, column=1)
    
    tk.Button(lower_border, text="Previous Menu",background="salmon",
              font=("Roboto bold",10),width=30,
              command=lambda:mid_body_symptoms()).grid(row=0, column=2)

def check_image(file):
    final = tk.Label(MainWin, text="Checking...", width=20,
             font=("Arial Bold", 24), padx=5, pady=0,bg="light green"
             ).grid(row=4, column = 0, padx=5, pady=10)
    image = Image.open(file)
    x = np.array(image.histogram())

    dis_dict = {}
    tally = {}
    for j in range(47):
        y_file = f"Eye_diseases/Cataracts/{j}.jpeg"
        rest = Image.open(y_file)
        y = np.array(rest.histogram())
        try:
            if len(x) == len(y):
                error = np.sqrt(((x-y) ** 2).mean())
                error = str(error)[:2]
                actual_error = float(100) - float(error)
            diff = ImageChops.difference(image, rest).getbbox()
            if diff:
                tally[j] = actual_error
            else:
                tally[j] = actual_error
                continue
        except ValueError as identifier:
            print("Matching Images in percentage : ", actual_error, " %")

    dis_dict["Cataract"] = max(tally.values())

    tally = {}
    for j in range(17):
        y_file = f"Eye_diseases/Glaucoma/{j}.jpeg"
        template = Image.open(y_file)
        y = np.array(template.histogram())
        try:
            if len(x) == len(y):
                error = np.sqrt(((x-y) ** 2).mean())
                error = str(error)[:2]
                actual_error = float(100) - float(error)
            diff = ImageChops.difference(image, template).getbbox()
            if diff:
                tally[j] = actual_error
            else:
                tally[j] = actual_error
                continue
        except ValueError as identifier:
            print("Matching Images in percentage : ", actual_error, " %")
            
    dis_dict["Glaucoma"] = max(tally.values())

    tally = {}
    for j in range(26):
        y_file = f"Eye_diseases/Uveitis/{j}.jpeg"
        template = Image.open(y_file)
        y = np.array(template.histogram())
        try:
            if len(x) == len(y):
                error = np.sqrt(((x-y) ** 2).mean())
                error = str(error)[:2]
                actual_error = float(100) - float(error)
            diff = ImageChops.difference(image, template).getbbox()
            if diff:
                tally[j] = actual_error
            else:
                tally[j] = actual_error
                continue
        except ValueError as identifier:
            print("Matching Images in percentage : ", actual_error, " %")

    dis_dict["Uveitis"] = max(tally.values())
    diagnosis = ""
    for i in dis_dict.keys():
        if dis_dict[i] == 100:
            diagnosis = i+" or"
            break
        if dis_dict[i] >= 85:
            diagnosis += i+" or "
    final_submit(diagnosis[:-3])

def get_image_dialog():
    global img
    types = [("Jpeg Files","*.jpeg"), ('Jpg Files','*.jpg')]
    filename = filedialog.askopenfilename(filetypes = types)
    img = ImageTk.PhotoImage(file=filename)
    b2=tk.Label(MainWin, image=img, bg="light green")
    b2.grid(row=2, column=0)
    submit_image = tk.Button(MainWin, text="Check", width=15,
            font=("Roboto bold", 12), command=lambda:check_image(filename)
            ).grid(row=3, column=0, padx=5, pady=10)

##Detection_through_Images
def main_image_page():
    clear_everything()
    tk.Label(MainWin, text = "Select the Image", width=29,
             font=("Arial Bold", 24), padx=5, pady=30,bg="light green"
             ).grid(row = 0, column = 0, pady=7)
    upload_button = tk.Button(MainWin, text="Upload Image", width=25,
            font=("Roboto bold", 12), command=lambda:get_image_dialog()
            ).grid(row=1, column=0, padx=5, pady=10)

def camera():
    msg.showwarning("Comming Soon", "This feature will get added on next update.")
##Main_Page
def main_page():
    clear_everything()
    MainWin.title(f"Logged in as {mail}")
    tk.Label(MainWin, text = "Disease Detection System", width=29,
             font=("Arial Bold", 24), padx=5, pady=30,bg="light green"
             ).grid(row = 0, column = 0, pady=7)
    tk.Button(MainWin, text="Detection through Inputs", width=25,
            font=("Roboto bold", 12), command=lambda:upper_body_symptoms()
            ).grid(row=1, column=0, padx=5, pady=10)
    tk.Button(MainWin, text="Detection through Images",  width=25,
            font=("Roboto bold", 12), command=lambda:main_image_page()
            ).grid(row=2, column=0, padx=5, pady=10)
    tk.Button(MainWin, text="Detection through Camera",  width=25,
            font=("Roboto bold", 12), command=lambda:camera()
            ).grid(row=3, column=0, padx=5, pady=10)

##Login_Page
def login_widget():
    MainWin.title("Login..")

    #Labels and Textboxes
    tk.Label(MainWin, text = "Disease Detection System", width=29,
             font=("Arial Bold", 24),
             bg="light green").grid(row = 0, column = 0, pady=7)
    tk.Label(MainWin, text = "Login Page", bg="light green",
             font=("Roboto Bold", 12)
             ).grid(row = 1, column = 0)

    main_border = tk.Frame(MainWin, bd=2, relief="sunken", bg="lightgreen")
    main_border.grid(row=2, column=0, padx=5, pady=10)

    input_border = tk.Frame(main_border, relief="sunken",bg="lightgreen")
    input_border.grid(row=0, column=0, padx=5, pady=10)
    #email
    E_mail = tk.Label(input_border,text = "Email ID ",bg="lightgreen", font=("Roboto Bold", 11))
    E_mail.grid(row = 0, column = 0, padx=7, pady=7)
    email_tex = tk.Entry(input_border)
    email_tex.grid(row = 0, column = 2, padx=7, pady=7)

    #password
    Pass_word = tk.Label(input_border, text = "Password",bg="lightgreen",font=("Roboto Bold", 11))
    Pass_word.grid(row=2, column = 0, padx=7, pady=7)
    pass_wrd = tk.Entry(input_border, show = '*')
    pass_wrd.grid(row=2, column = 2, padx=7, pady=7)

    submit_border = tk.Frame(main_border, relief="sunken", bg="lightgreen")
    submit_border.grid(row=3, column=0, padx=5, pady=10)
    
    tk.Button(submit_border, text = "Login", width=26,
              font=("Roboto Bold", 12),
              command = lambda:check_details(email_tex.get(),pass_wrd.get())
              ).grid(row=0, column = 0, padx=10, pady=10)
    tk.Button(submit_border, text = "Sign Up", width=26,
              font=("Roboto Bold", 12),
              command = lambda:sign_up_widget()
              ).grid(row=0, column = 1, padx=10, pady=10)

##OTP widget
def show_otp_widget(email, paswrd, One_tp, otp, submit_otp):
    if validate(email,paswrd):
        #OTP generation
        global OTP
        dig = "0123456789"
        for i in range(6):
            OTP += dig[math.floor(random.random()*10)]
            
        gen_OTP = "Welcome to \"Disease Detection System\" \nPlease verify your,\nEmail Id : " + email + "\nPassword : " + paswrd + " \nwith this OTP : " + OTP + "."

##        smtp = smtplib.SMTP('smtp.gmail.com',587)
##        smtp.starttls()
##        user_email = email
##        smtp.login("aadarshprem82@gmail.com","okmmhluijiaaoaqe")
##        smtp.sendmail('Aadarsh',user_email,gen_OTP)
        print(gen_OTP)
        #OTP Widget
        One_tp.grid(row=0, column=0)
        otp.grid(row=0, column = 1)
        submit_otp.grid(row=1, column=1)

def verification(temp, email, passwrd):
    global OTP
    if temp.get() == OTP:
        go_ahead(email,passwrd)
    else:
        msg.showwarning("Wrong!!","Entered Wrong OTP")

def validate_login(email, pswrd):
    em_txt = email
    if em_txt == "":
        msg.showwarning("Empty!!","Email ID cannot be empty.")
    elif em_txt[len(em_txt)-10:len(em_txt)] != '@gmail.com':
        msg.showwarning("Invalid!!","Please Enter a valid Email ID.\nEmail must include \"@gmail.com\"")       
    elif pswrd == "":
        msg.showwarning("Empty!!","Password cannot be empty.")
    else:
        return True

def validate(email, pswrd):
    em_txt = email
    flag = 0
    connection = sql.connect(host = 'localhost', user = 'root', password = 'Dongle@123', database="dds_user")
    point = connection.cursor()
    point.execute("select * from users")
    for i in point:
        if i[0] == email:
            msg.showwarning("Duplicate","Email already exists!!")
            flag = 1
            break
    if flag == 1:
        sign_up_widget()
    else:
        if em_txt == "":
            msg.showwarning("Empty!!","Email ID cannot be empty.")
        elif em_txt[len(em_txt)-10:len(em_txt)] != '@gmail.com':
            msg.showwarning("Invalid!!","Please Enter a valid Email ID.\nEmail must include \"@gmail.com\"")       
        elif pswrd == "":
            msg.showwarning("Empty!!","Password cannot be empty.")
        else:
            return True

def go_ahead(email, passwrd):
    connection = sql.connect(host = 'localhost', user = 'root', password = 'Dongle@123', database="dds_user")
    point = connection.cursor()
    
    sql_query = "insert into users (email, password) values(%s,%s)"
    point.execute(sql_query,(email, passwrd))
    connection.commit()
    if point.rowcount != 0:
        clear_everything()
        login_widget()
    else:
        msg.showwarning("Error!","Something wrong with the insertion.")
    

#MainWin(Login or SignUp Page)
MainWin = tk.Tk()
MainWin.geometry("562x420+150+150")
MainWin.configure(bg="lightgreen")
MainWin.resizable(False,False)
MainWin.iconbitmap("doc.ico")
#properly centers the window
'''MainWin.eval('tk::PlaceWindow . center')'''
def sign_up_widget():
    clear_everything()
    MainWin.title("Sign Up..")
    #Labels and Textboxes
    tk.Label(MainWin, text = "Disease Detection System", width=29,
             bg="light green", font=("Arial Bold", 24)
             ).grid(row = 0, column = 0, pady=7)
    tk.Label(MainWin, text = "Sign Up Page",
             bg="light green", font=("Roboto Bold", 12)).grid(row = 1, column = 0)

    main_border = tk.Frame(MainWin, bd=2, relief="sunken",bg="lightgreen")
    main_border.grid(row=2, column=0, padx=5, pady=10)

    input_border = tk.Frame(main_border, relief="sunken",bg="lightgreen")
    input_border.grid(row=0, column=0, padx=5, pady=10)
    #email
    E_mail = tk.Label(input_border,text = "Email ID ", bg="lightgreen",
                      font=("Roboto bold",11))
    E_mail.grid(row = 0, column = 0, padx=7, pady=7)
    email_tex = tk.Entry(input_border)
    email_tex.grid(row = 0, column = 2, padx=7, pady=7)

    #password
    Pass_word = tk.Label(input_border, text = "Password", bg="lightgreen"
                         ,font=("Roboto Bold", 11))
    Pass_word.grid(row=2, column = 0, padx=7, pady=7)
    pass_wrd = tk.Entry(input_border, show = '*')
    pass_wrd.grid(row=2, column = 2, padx=7, pady=7)


    #OTP_Widget
    otp_border = tk.Frame(main_border, relief="sunken", bg="lightgreen")
    otp_border.grid(row=3, column=0, padx=5, pady=10)
    
    One_tp = tk.Label(otp_border, text = "OTP ",font=("Roboto Bold", 11), bg="lightgreen")
    otp = tk.Entry(otp_border)
    submit_otp = tk.Button(otp_border, text = "Submit",
                           font=("Roboto Bold", 11),
                           command = lambda:verification(otp, email_tex.get(),
                                                         pass_wrd.get())
                           )

    submit_border = tk.Frame(main_border, relief="sunken",bg="lightgreen")
    submit_border.grid(row=2, column=0, padx=5, pady=10)
    #lambda is important here.
    tk.Button(submit_border, text = "Sign Up", width=30,
              font=("Roboto Bold", 12),
              command = lambda:show_otp_widget(email_tex.get(),pass_wrd.get(),
                                             One_tp, otp, submit_otp)
            ).grid(row=0, column = 0, padx=10, pady=10)

login_widget()
MainWin.mainloop()
##main_page()
