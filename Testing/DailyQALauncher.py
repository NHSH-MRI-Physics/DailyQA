import sys
import os 

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from DQA_Scripts import DailyQA
import numpy as np
from DQA_Scripts import Helper  
#os.chdir('..')

Files = "BaselineData\Head\DQA_Head_1"
#Files = "C:\\Users\John\Desktop\DailyQA_DQA_Body_2024-12-09 09-49-10"
Results = DailyQA.RunDailyQA(Files)

for result in Results:
	print (result)
	QAResult = Helper.DidQAPassV2(result)
	print(QAResult)
	