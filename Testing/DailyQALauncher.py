import sys
import os 
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'DQA_Scripts'))
import DailyQA
import numpy as np
import Helper
#os.chdir('..')


#Files = "/Users/john/Documents/DailyQA/baselineData/Head/DQA_Head_1"
Files = "/Users/john/Downloads/DQA_Head_2023-12-20 08-21-21"
Results = DailyQA.RunDailyQA(Files)
for result in Results:
	#print (result)
	QAResult = Helper.DidQAPassV2(result)
	print(QAResult)
	