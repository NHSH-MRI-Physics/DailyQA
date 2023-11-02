import datetime
import time
import os
import DailyQA
import smtplib
from email.mime.text import MIMEText
import Helper
import shutil
import sys 

FileCount =  {}
FileCount["DQA_Head"] = 19
FileCount["DQA_Body"] = 50
FileCount["DQA_Spine"] = 48

Emails = {}
Emails["John"] = "john.tracey@nhs.scot"
Emails["Jonathan"] = "Jonathan.ashmore@nhs.scot"
Emails["Adam"] = "adam.scotson@nhs.scot"



WatchFolder = "/Users/mri/Documents/QA/ClinicalQA/RawDICOM"
#WatchFolder = "/Users/john/Documents/DailyQA/WatchFolder"
while (True):
    print ("Still alive at " + str(datetime.datetime.now()))

    #Check the folder 
    SubFolders = [x[0] for x in os.walk(WatchFolder)]
    
    for folder in SubFolders:
        for QAName in FileCount.keys():
            if QAName.lower() in folder.lower():
                FileCounter = len(os.listdir(folder))
                
                if (FileCounter == FileCount[QAName]):
                    #Run the QA
                    print("Found " + folder + " at " + str(datetime.datetime.now()))
                    time.sleep(30)#Wait 30s to make sure it really is downaloded...
                    print("Running QA " + QAName)

                    ErrorMessage= ""
                    QASuccess=False
                    try:
                        Results = DailyQA.RunDailyQA(folder)
                        QASuccess=True 
                    except Exception as e:
                        print (e)
                        ErrorMessage=e
                        pass


                    try:
                        NewFolder = os.path.join("Archive",folder.split(os.path.sep)[1]+"_"+str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")))
                        NewFolder = NewFolder.replace("Users", QAName)

                        if (QASuccess==True):
                            EmailResultLines = []
                            count = 0

                            OverallPass=[]
                            for result in Results:
                                QAResult = Helper.DidQAPass(result)
                                if QAResult[0] == False:
                                    EmailResultLines.append(QAResult[1])
                                OverallPass.append(QAResult[0])

                                '''
                                SNR =  result[0]
                                QAResult="Fail"
                                OverallPass.append([False])
                                if (SNR >= Tolerance[QAName][count]):
                                    QAResult="Pass"
                                    OverallPass[-1]=True
                                EmailResultLines.append("Sequence: " + result[-1] + "       SNR: " + str(round(SNR,2)) + "       QA Result: " + QAResult)
                                '''
                                count+=1


                            for name in Emails.keys():
                                Helper.SendEmail(name,Emails[name],EmailResultLines,QAName,OverallPass,Archive=NewFolder)
                        else:
                            for name in Emails.keys():
                                Helper.SendErrorEmail(name,Emails[name],ErrorMessage,QAName,Archive=NewFolder)
                        
                        
                        #Move to the archive 
                        
                        os.system("echo ilovege | sudo -S chown mri "+folder)
                        os.rename(folder, NewFolder)
                        if (QASuccess==True):
                            for result in Results:
                                shutil.copyfile(result[-1]+"_SmoothMethod.png", os.path.join(NewFolder,result[-1]+"_SmoothMethod.png"))
                    except Exception as e:
                        print (e)
                        pass

    time.sleep(60)