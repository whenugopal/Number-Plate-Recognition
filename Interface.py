# Importing Modules and packages

from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter import filedialog
import os
import shutil
from tkinter import messagebox
from openpyxl import Workbook
import csv


import numberPlateRecognition
import trainRecognizeCharacters

#Excel Sheet
book = Workbook()
sheet = book.active
sheet.insert_cols(idx=100)

# Tkinter 
form = Tk()
form.title('Number Plate Recognition')
form.attributes("-fullscreen",True)

tab_parent = ttk.Notebook(form)

tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)
tab4 = ttk.Frame(tab_parent)

tab_parent.add(tab1, text="Image")
tab_parent.add(tab2, text="Video")
tab_parent.add(tab3, text="Train Model")
tab_parent.add(tab4, text="Group")

tab_parent.pack(expand=1, fill='both')

# ===================================== FUNCTIONS ==============================================

# To quit from app
def quit():
    global form
    form.quit()

# To open a Image File
def openfiler_image():

    # Set to Zero because it's an Image File
    detectVideo = 0

    form.filename = filedialog.askopenfilename(initialdir = '/', title='Select a File', filetypes = (("png files",'*.png'),("Jpeg files",'*.jpg')))
    file_name_label = Label(tab1, text="FileName:: "+form.filename, font=('times', 15, ' bold '))
    file_name_label.place(relx=0.0, rely=0.8,  )
    
    if(form.filename == ""):
        messagebox.showerror('ERROR', f'Please select an Image file')
    else:
        messagebox.showinfo("Processing.....", f"Please wait for a while, This might take a minute or two.")
    
    detected_plate_number = numberPlateRecognition.detectPlateNumber(form.filename, detectVideo)
   
    if(detected_plate_number == ""):
        messagebox.showerror('ERROR !!',"Couldn't find the Licence Plate/Plate Number, Please select a proper image")
    else:
        messagebox.showinfo("Plate Detected !", f'Predicted Plate Number :{detected_plate_number}')
        with open('recorded_plate.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([detected_plate_number])
        
        

# looper

def looper():
    form.foldername = filedialog.askdirectory(initialdir = '/', title='Select a File')
    file_name_label = Label(tab4, text="FileName:: "+form.foldername, font=('times', 15, ' bold '))
    file_name_label.place(relx=0.0, rely=0.8,  )
    if(form.foldername == ""):
        messagebox.showerror('ERROR', f'Please select a folder')
    else:
        messagebox.showinfo("Processing.....", f"Please wait for a while, This might take a minute or two.")
    
    with open('recorded_plates.csv', 'a', newline='') as file:
        # writer = csv.writer(file)
        # writer.writerow([detected_plate_number])
        for filename in os.listdir(form.foldername):
            if filename.endswith(".jpg") or filename.endswith(".png"): 
                # print(os.path.join(form.foldername, filename))
                detectVideo = 0
                detected_plate_number = numberPlateRecognition.detectPlateNumber(filename, detectVideo)
                if(detected_plate_number == ""):
                    messagebox.showerror('ERROR !!',"Couldn't find the Licence Plate/Plate Number, Please select a proper image")
                else:
                    messagebox.showinfo("Plate Detected !", f'Predicted Plate Number :{detected_plate_number}')
                    with open('recorded_plates.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([detected_plate_number])
                continue
            else:
                continue







# To open a Video file 
def openfiler_videos():

    # Set to One because it's a Video File
    detectVideo = 1

    form.filename = filedialog.askopenfilename(initialdir = '/', title='Select a File', filetypes = (("mp4 files",'*.mp4'),('All files','*.*')))
    file_name_label = Label(tab1, text="FileName:: "+form.filename, font=('times', 15, ' bold '))
    file_name_label.place(relx=0.0, rely=0.8,  )

    if(form.filename == ""):
        messagebox.showerror('ERROR !!',f'Please select a Video')
    else:
        messagebox.showinfo("Processing.....", f"Please wait for a while, This might take a minute or two.")
    
    detected_plate_number = numberPlateRecognition.detectPlateNumber(form.filename, detectVideo)
    


    if(detected_plate_number == ""):
        messagebox.showerror('ERROR',f"Could't find the Licence Plate/Plate number, Please select a proper video.")
    else:
        messagebox.showinfo("Plate Detected",f'Predicted Plate Number :{detected_plate_number}')
        with open('recorded_plates.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([detected_plate_number])
        
#Train Model
def getmodel():
    trainedmodel = trainRecognizeCharacters.trainedModel()
    
    if(trainedmodel == ""):
        messagebox.showerror('ERROR !!',f'Please Check the dataset characters and place accordingly.')
    else:
        messagebox.showinfo('SUCESS',f'Model Trained with new characters and saved as a file {trainedmodel}')

# ===================================== WIDGETS FOR TAB 1 ==============================================

#Title and Layout of the Tab1 Frame
label_title = Label(tab1, text="Number Plate Recognition",width=60  ,height=2 , bg='black', fg='white' ,font=('times', 30, ' bold ') ) 
label_title.place(x=0,y=0 )
label_title = Label(tab1, text="Using Image Files",width=60  ,font=('times', 30, ' bold ') ) 
label_title.place(relx=0.0, rely=0.1, x=0,y=10 )

#Select Button
select_image_btn = Button(tab1, text="Browse Image", bg="red", fg="white", command=openfiler_image, font=('times', 20, ' bold '))
select_image_btn.place(relx=0.45, rely=0.55)

#Selected File name and location
select_file_text = Label(tab1, text="Please Select an Image file", font=('times', 16)) 
select_file_text.place(relx=0.45, rely=0.45)



# ===================================== WIDGETS FOR TAB 2 ==============================================

label_title = Label(tab2, text="Number Plate Recognition",width=60  ,height=2 , bg='Blue', fg='white' ,font=('times', 30, ' bold ') ) 
label_title.place(x=0,y=0 )
label_title = Label(tab2, text="Using Video Files",width=60  ,font=('times', 30, ' bold ') ) 
label_title.place(relx=0.0, rely=0.1, x=0,y=10 )
select_image_btn = Button(tab2, text="Browse Videos", bg="red", fg="white", command=openfiler_videos, font=('times', 20, ' bold '))
select_image_btn.place(relx=0.45, rely=0.55)

select_file_text = Label(tab2, text="Please Select a Video file", font=('times', 16)) 
select_file_text.place(relx=0.45, rely=0.45)


# ===================================== WIDGETS FOR TAB 3 ==============================================

label_title = Label(tab3, text="Number Plate Recognition",width=60  ,height=2 , bg='Orange', fg='white' ,font=('times', 30, ' bold ') ) 
label_title.place(x=0,y=0 )
# label_title = Label(tab3, text="Train Model",width=60  ,font=('times', 30, ' bold ') ) 
label_title.place(relx=0.0, rely=0.1, x=0,y=10 )
select_image_btn = Button(tab3, text="Click To Train Model", bg="red", fg="white", command=getmodel, font=('times', 20, ' bold '))
select_image_btn.place(relx=0.40, rely=0.55)

select_file_text = Label(tab3, text="Train Model", font=('times', 16)) 
select_file_text.place(relx=0.45, rely=0.45)

# ===================================== WIDGETS FOR TAB 4 ==============================================

label_title = Label(tab4, text="Number Plate Recognition",width=60  ,height=2 , bg='Orange', fg='white' ,font=('times', 30, ' bold ') ) 
label_title.place(x=0,y=0 )
# label_title = Label(tab3, text="Train Model",width=60  ,font=('times', 30, ' bold ') ) 
label_title.place(relx=0.0, rely=0.1, x=0,y=10 )
select_image_btn = Button(tab4, text="Select the folder", bg="red", fg="white", command=looper, font=('times', 20, ' bold '))
select_image_btn.place(relx=0.40, rely=0.55)

# select_file_text = Label(tab3, text="Train Model", font=('times', 16)) 
# select_file_text.place(relx=0.45, rely=0.45)

# ===================================== Quit Button ==============================================

quit_btn = Button(form, text="Quit", bg="black", fg="white", command=quit, font=('times', 20, ' bold '))
quit_btn.place(relx=0.8, rely=0.8, x=0,y=30 )

form.mainloop()