import tkinter as tk
import cv2
import os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

window = tk.Tk()
window.title("Smart Surveillance System")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'

window.geometry('1280x720')
backgroundColor = '#9999ff'
window.configure(background=backgroundColor)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

line1 = tk.Label(window, text="Samrat Ashok Technological Institute, Vidisha", fg="black", bg=backgroundColor, font=('times', 40, 'bold'))
line1.place(x=250, y=10)

line2 = tk.Label(window, text="Major Project", fg="black", bg=backgroundColor, font=('times', 25, 'bold'))
line2.place(x=640, y=90)

line3 = tk.Label(window, text="on", fg="black", bg=backgroundColor, font=('times', 20, 'bold'))
line3.place(x=720, y=130)

line4 = tk.Label(window, text="Smart Surveillance System", fg="black", bg=backgroundColor, font=('times', 35, 'italic bold underline'))
line4.place(x=480, y=170)

lbl = tk.Label(window, text="Enter ID :", width=20, height=2, bg=backgroundColor, font=('times', 15, ' bold '))
lbl.place(x=400, y=260)

txt = tk.Entry(window, width=20, bg="white", font=('times', 15, ' bold '))
txt.place(x=700, y=275)

lbl2 = tk.Label(window, text="Enter Name :", width=20, bg=backgroundColor, height=2, font=('times', 15, ' bold '))
lbl2.place(x=400, y=340)

txt2 = tk.Entry(window, width=20, bg="white", font=('times', 15, ' bold '))
txt2.place(x=700, y=355)

lbl3 = tk.Label(window, text="Notification : ", width=20, bg=backgroundColor, height=2, font=('times', 15, ' bold '))
lbl3.place(x=400, y=440)

message = tk.Label(window, text="", bg=backgroundColor, width=30, height=2, activebackground="yellow", font=('times', 15, 'bold'))
message.place(x=700, y=440)
 
def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text=res)

def clear2():
    txt2.delete(0, 'end')
    res = ""
    message.configure(text=res)
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def generateEmail(date, time, imageCount):
    def sendImages(server, imageFiles, yourEmail, receiverEmail, imageCount):

        def attachImages(imageFiles, imageNo):
            img_data = open('ImagesUnknown/Image' + str(imageNo) + '.jpg', 'rb').read()
            image = MIMEImage(img_data, name=os.path.basename('ImagesUnknown/Image' + str(imageNo) + '.jpg'))
            imageFiles.attach(image)

        for i in range(imageCount - 4, imageCount + 1):
            attachImages(imageFiles, i)

        try:
            server.sendmail(yourEmail, receiverEmail, imageFiles.as_string())
            print('Images to {} successfully sent!\n\n'.format(receiverEmail))
        except Exception as e:
            print('Images to {} could not be sent :( because {}\n\n'.format(receiverEmail, str(e)))

    def sendNotification(server, yourEmail, receiverEmail, notification):
        try:
            server.sendmail(yourEmail, [receiverEmail], notification)
            print('Notification to {} successfully sent!\n\n'.format(receiverEmail))
        except Exception as e:
            print('Notification to {} could not be sent :( because {}\n\n'.format(receiverEmail, str(e)))

    yourName = 'Smart Surveillance System'
    yourEmail = 'example@mail.com'
    yourPassword = '************'
    subject = 'Security Problem'
    receiverName = 'Admin'
    receiverEmail = 'example2@mail.com'

    notification = ("From: {0} <{1}>\nTo: {2} <{3}>\nSubject: {4}\n\n"
                     "Warning!\nThere is a unknown person detected in your home.\n\nDate: {5}\nTime: {6}")\
                    .format(yourName, yourEmail, receiverName, receiverEmail, subject, date, time)


    imageFiles = MIMEMultipart()
    imageFiles['Subject'] = 'Smart Surveillance System - Detected Images'
    imageFiles['From'] = yourEmail
    imageFiles['To'] = receiverEmail
    text = MIMEText('Images captured\n\nTime: {}\nDate: {}'.format(time, date))
    imageFiles.attach(text)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(yourEmail, yourPassword)

    sendNotification(server, yourEmail, receiverEmail, notification)
    sendImages(server, imageFiles, yourEmail, receiverEmail,imageCount)

    server.close()
 
def TakeImages():        
    Id = (txt.get())
    name = (txt2.get())

    if (is_number(Id)) and name.isalpha() and (name != "") and (name.lower() != 'unknown'):
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img,(x, y), (x+w, y+h), (255, 0, 0), 2)
                #incrementing sample number 
                sampleNum += 1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('Taking 100 images...', img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 99:
                break
        cam.release()
        cv2.destroyAllWindows()

        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id, name]
        with open('FamilyMemberDetails\FamilyMemberDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if (name == '' or Id == ''):
            res = 'Invalid Details'
        elif name.lower() == 'unknown':
            res = 'Invalid Name'
        else:
            if is_number(Id) == False:
                res = "Enter Numeric Id"
            elif name.isalpha() == False:
                res = "Enter Alphabetical Name"
        message.configure(text=res)
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    #recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"
    #+",".join(str(f) for f in Id)
    message.configure(text=res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    #print(imagePaths)

    #create empth face list
    faces = []
    #create empty ID list
    Ids = []
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        #getting the Id from the image
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces, Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("FamilyMemberDetails\FamilyMemberDetails.csv")
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names = ['Id', 'Name', 'Date', 'Time']
    detail = pd.DataFrame(columns=col_names)

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    fileName = 'VideoData\VideoData_'+str(date)+'.avi'
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    videoOut = cv2.VideoWriter(fileName, fourcc, 20.0, (640, 480))

    prevEmail = None
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2,5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf < 40:
                aa = df.loc[df['Id'] == Id]['Name'].values
                tt = str(Id)+"-"+aa
            else:
                Id = 'Unknown'
                tt = str(Id)
                aa = 'Admin'
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                noOfFile = len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])
                detail.loc[len(detail)] = [Id, aa, date, timeStamp]

                if noOfFile%5 == 0:
                    if (prevEmail == None) or (int(prevEmail[3:5]) != int(timeStamp[3:5])):
                        generateEmail(date, timeStamp, noOfFile)
                        # print('Sent', noOfFile)
                        prevEmail = timeStamp

            cv2.putText(im, str(tt),(x, y+h), font, 1, (255, 255, 255), 2)
        detail = detail.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('Tracking for unknown preson...', im)
        videoOut.write(im)
        if cv2.waitKey(1) == ord('q'):
            break

    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = "Records\Records_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    detail.to_csv(fileName, index=False)

    cam.release()
    videoOut.release()
    cv2.destroyAllWindows()
  
clearButton = tk.Button(window, text="Clear", command=clear, width=5, height=1, activebackground="Red", font=('times', 15, ' bold '))
clearButton.place(x=950, y=270)

clearButton2 = tk.Button(window, text="Clear", command=clear2, width=5, height=1, activebackground="Red", font=('times', 15, ' bold '))
clearButton2.place(x=950, y=350)

takeImg = tk.Button(window, text="Take Images", command=TakeImages, width=10, height=1, activebackground="Red", font=('times', 15, ' bold '))
takeImg.place(x=200, y=560)

trainImg = tk.Button(window, text="Train Images", command=TrainImages, width=10, height=1, activebackground="Red", font=('times', 15, ' bold '))
trainImg.place(x=500, y=560)

trackImg = tk.Button(window, text="Track Images", command=TrackImages, width=10, height=1, activebackground="Red", font=('times', 15, ' bold '))
trackImg.place(x=800, y=560)

quitWindow = tk.Button(window, text="Quit", command=window.destroy, width=10, height=1, activebackground ="Red", font=('times', 15, ' bold '))
quitWindow.place(x=1100, y=560)

window.mainloop()
