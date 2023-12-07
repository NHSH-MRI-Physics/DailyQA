import sys
import os 
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'DQA_Scripts'))
import DailyQA
import numpy as np
import Helper
os.chdir('..')
#Files = "Data/DQA_Head_20230914_214806084" # Head Coil 
#Files = "Data/DQA_Body_20230914_214817785" # Body Coil 
#Files = "Data/DQA_Spine_20230914_214814825" # Spine Coil 


#Files = "BaselineData/Head/DQA_Head_10_20231004_213318720"  
#Files = "BaselineData/Spine/DQA_Spine_10"  

#Files = "/Users/mri/Desktop/DailyQA/Archive/DQA_Head_2023-11-08 09-46-19"
Files = "Data/DQA_Head_1"
Results = DailyQA.RunDailyQA(Files)
for result in Results:
	print (result)
	QAResult = Helper.DidQAPass(result)
#DailyQA.Helper.SaveHistoricData(Results,"HeadQA.txt")
#DailyQA.Helper.PlotCSV("HeadQA.txt")


'''
data = []
for i in range (1,11):
	Files = "BaselineData/Head/DQA_Head_" + str(i)
	Results = DailyQA.RunDailyQA(Files)
	print( Results[0][-1] + " " + str(Results[0][1]['M4'][4]) + "         " + Results[1][-1] + " " +str(Results[1][1]['M4'][4]))

	if (Results[0][-1] == "Ax T2 FSE head"):
		data.append(Results[0][1]['M4'][4])

	if (Results[1][-1] == "Ax T2 FSE head"):
		data.append(Results[1][1]['M4'][4])

print(data)
print(np.mean(data))
print(np.std(data))
'''