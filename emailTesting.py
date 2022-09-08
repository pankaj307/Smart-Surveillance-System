import pandas as pd
import smtplib

yourName = 'Security Problem'

yourEmail = 'example@email.com'
yourPassword = '************'

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

server.ehlo()
server.login(yourEmail, yourPassword)

emailList = pd.read_csv('Records/Records_2021-02-26_11-28-20.csv')

allIds = emailList['Id']
allNames = emailList['Name']
allDates = emailList['Date']
allTimes = emailList['Time']
allEmails = emailList['Email']

for ids in range(len(allEmails)):
    name = allNames[ids]
    email = 'pankushwah123@gmail.com'
    date = allDates[ids]
    time = allTimes[ids]
    subject = 'Smart Surviellance System Testing'

    fullEmail = ("From: {0} <{1}>\nTo: {2} <{3}>\nSubject: {4}\n\nThere is a unknown person detected\n\nDate: {5}\nTime {6}").format(yourName, yourEmail, name, email, subject, date, time)

    try:
        server.sendmail(yourEmail, [email], fullEmail)
        print('Email to {} succesfully sent!\n\n'.format(email))
    except Exception as e:
        print('Email to {} could not be sent :( because {}\n\n'.format(email, str(e)))

server.close()
