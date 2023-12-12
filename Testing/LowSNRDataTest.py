import sys
import os 
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'DQA_Scripts'))
import DailyQA
import numpy as np
import Helper
if( os.path.basename(os.path.normpath(os.getcwd())) ) == "UnitTesting": 
    os.chdir('..')


Files = "Testing/LowSNR_Data/25%SNR_Head"
Results = DailyQA.RunDailyQA(Files)
for result in Results:
	#print (result)
	QAResult = Helper.DidQAPass(result)
	print(QAResult[0])
	print(QAResult[1])