import sys
import os 
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'DQA_Scripts'))
import DailyQA
import numpy as np
import Helper
#os.chdir('..')


#Files = "/Users/john/Documents/DailyQA/baselineData/Head/DQA_Head_1"
Files = "BaselineData\Body\DQA_Body_1"
Results = DailyQA.RunDailyQA(Files)
print(DailyQA.GetManHoursSaved())
sys.exit()


for result in Results:
	print (result)
	QAResult = Helper.DidQAPassV2(result)
	print(QAResult)
	