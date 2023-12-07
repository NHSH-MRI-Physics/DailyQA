import sys
import os 
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'DQA_Scripts'))
import DailyQA
import Helper
import shutil
import os
import requests
os.chdir('..')

Emails = {}
Emails["John"] = "Johnt717@gmail.com"
#Emails["John T"] = "John.tracey@NHS.scot"
EmailResultLines = []

#Results = Helper.ProduceTestData(1)
Images = []

Files = "Data/DQA_Head_1"
DataFolder = "/Users/mri/Desktop/DailyQA/Data/DQA_Head_1"
DataFolder = "Data/DQA_Head_1"
Results = DailyQA.RunDailyQA(Files)
QAResultTracker=[]
for result in Results:
	QAResult = Helper.DidQAPass(result)

	if QAResult[0] == False:
		EmailResultLines.append(QAResult[1])
	QAResultTracker.append(QAResult[0])
	print (QAResult[0])

	shutil.copyfile("Results/"+result[-1]+"_SmoothMethod.png", os.path.join(DataFolder,result[-1]+"_SmoothMethod.png"))
	print(os.path.join(DataFolder,result[-1]+"_SmoothMethod.png"))
	Images.append(os.path.join(DataFolder,result[-1]+"_SmoothMethod.png"))


for name in Emails.keys():
	Helper.SendEmailV2(name,Emails[name],EmailResultLines,Results[0][2],QAResultTracker,Archive=DataFolder,images=Images)
