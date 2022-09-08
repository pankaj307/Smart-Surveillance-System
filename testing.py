import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import datetime
import time

def SendMail():
    yourEmail = 'example@mail.com'
    yourPassword = '************'
    receiverEmail = 'example2@mail.com'


    msg = MIMEMultipart()
    msg['Subject'] = 'Smart Surveillance System'
    msg['From'] = yourEmail
    msg['To'] = receiverEmail

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

    text = MIMEText('Warning!\n\nUnknown person detected in your home.\n\nTime: '+str(timeStamp)+'\nDate: '+str(date))
    msg.attach(text)

    def attachImage(msg,imageNo):
        img_data = open('ImagesUnknown/Image'+str(imageNo)+'.jpg', 'rb').read()
        image = MIMEImage(img_data, name=os.path.basename('ImagesUnknown/Image'+str(imageNo)+'.jpg'))
        msg.attach(image)

    for i in range(1, 6):
        attachImage(msg, i)

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    s.login(yourEmail, yourPassword)

    try:
        s.sendmail(yourEmail, receiverEmail, msg.as_string())
        print('Sent')
    except Exception as e:
        print('Not')
    s.quit()

SendMail()
