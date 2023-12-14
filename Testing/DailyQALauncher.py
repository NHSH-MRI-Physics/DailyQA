import sys
import os 
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'DQA_Scripts'))
import DailyQA
import numpy as np
import Helper
#os.chdir('..')


#Files = "/Users/john/Documents/DailyQA/Data/DQA_Head_1"
Files = "Archive/DQA_Head_2023-12-01 10-28-18" #High SNR One
#Files = "BaselineData/Head/DQA_Head_20" #Another one
Results = DailyQA.RunDailyQA(Files)
for result in Results:
	print (result)
	QAResult = Helper.DidQAPass(result)
	