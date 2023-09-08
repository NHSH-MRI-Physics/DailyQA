import datetime
import time
import os
import DailyQA
import smtplib
from email.mime.text import MIMEText
import Helper
import shutil

FileCount =  {}
FileCount["DailyQA_Test_Head"] = 152
FileCount["DailyQA_Test_Body"] = 110
FileCount["DailyQA_Test_Spine"] = 272

Tolerance = {}
Tolerance["DailyQA_Test_Head"] = [90,77]
Tolerance["DailyQA_Test_Body"] = [120,120,120]
Tolerance["DailyQA_Test_Spine"] = [120,120,120]

Emails = {}
Emails["John"] = "Johnt717@gmail.com"
Emails["Frank"] = "Johnt717@gmail.com"


WatchFolder = "WatchFolder"
while (True):
    print ("Still alive at " + str(datetime.datetime.now()))

    #Check the folder 
    SubFolders = [x[0] for x in os.walk(WatchFolder)]
    
    for folder in SubFolders:
        
        for QAName in FileCount.keys():
            if QAName in folder:
                FileCounter = len(os.listdir(folder))
                
                if (FileCounter == FileCount[QAName]):
                    #Run the QA
                    print("Found " + folder + " at " + str(datetime.datetime.now()))
                    time.sleep(30)#Wait 30s to make sure it really is downaloded...
                    Results = DailyQA.RunDailyQA(folder)

                    EmailResultLines = []
                    count = 0
                    for result in Results:
                        SNR =  result[0]
                        QAResult="Fail"
                        if (SNR >= Tolerance[QAName][count]):
                            QAResult="Pass"
                        EmailResultLines.append("Sequence: " + result[-1] + "       SNR: " + str(round(SNR,2)) + "       QA Result: " + QAResult)
                        count+=1

                    #for name in Emails.keys():
                    #    Helper.SendEmail(name,Emails[name],EmailResultLines,QAName)
                    

                    #Move to the archive 
                    NewFolder = os.path.join("Archive",folder.split(os.path.sep)[1])
                    os.rename(folder, NewFolder)
                    for result in Results:
                        shutil.copyfile(result[-1]+"_SmoothMethod.png", os.path.join(NewFolder,result[-1]+"_SmoothMethod.png"))

    time.sleep(10)