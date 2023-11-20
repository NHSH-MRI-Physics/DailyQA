import DailyQA
import Helper
Emails = {}
Emails["John"] = "Johnt717@gmail.com"
Emails["John T"] = "John.tracey@NHS.scot"
EmailResultLines = []

#Results = Helper.ProduceTestData(1)

Files = "Data/DQA_Head_1"
Results = DailyQA.RunDailyQA(Files)
QAResultTracker=[]
for result in Results:
	QAResult = Helper.DidQAPass(result)

	if QAResult[0] == False:
		EmailResultLines.append(QAResult[1])
	QAResultTracker.append(QAResult[0])
	print (QAResult[0])
		
#for name in Emails.keys():
#	Helper.SendEmail(name,Emails[name],EmailResultLines,Results[0][2],QAResultTracker)