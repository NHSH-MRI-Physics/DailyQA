import DailyQA
import Helper
Emails = {}
Emails["John"] = "Johnt717@gmail.com"
EmailResultLines = []

#Results = Helper.ProduceTestData(1)

Files = "Data/DQA_Head_20230914_214806084"
Results = DailyQA.RunDailyQA(Files)
QAResultTracker=[]
for result in Results:
	QAResult = Helper.DidQAPass(result)

	if QAResult[0] == False:
		EmailResultLines.append(QAResult[1])
	QAResultTracker.append(QAResult[0])
		
for name in Emails.keys():
	Helper.SendEmail(name,Emails[name],EmailResultLines,Results[0][2],QAResultTracker)