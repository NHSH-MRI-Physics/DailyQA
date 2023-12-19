import sys
import os 
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'DQA_Scripts'))
import DailyQA
import numpy as np
import Helper
#os.chdir('..')


Files = "/Users/john/Documents/DailyQA/baselineData/Head/DQA_Head_1"
#Files = "Archive/DQA_Head_2023-12-01 10-28-18" #High SNR One
#Files = "Archive/DQA_Body_2023-12-18 08-28-14" #Another one
Results = DailyQA.RunDailyQA(Files)
for result in Results:
	print (result)
	QAResult = Helper.DidQAPass(result)
	