import sys
import os 
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'DQA_Scripts'))
import DailyQA
import numpy as np
import Helper
#os.chdir('..')


#Files = "/Users/john/Documents/DailyQA/baselineData/Head/DQA_Head_1"
Files = "C:\\Users\\Johnt\\Desktop\\OneDrive_2024-01-16\\DQA_Body_2024-01-16 08-30-58"
Results = DailyQA.RunDailyQA(Files)
for result in Results:
	#print (result)
	QAResult = Helper.DidQAPassV2(result)
	print(QAResult)
	