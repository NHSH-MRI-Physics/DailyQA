import DailyQA
import os


ROIResults = []
def GetBaseline(path):
	files =  (next(os.walk(path))[1])
	for file in files:
		Results = DailyQA.RunDailyQA(file)
		ROIResults.append(Results[1])




path = "/Users/mri/Desktop/DailyQA/BaselineData/Head"
GetBaseline(path)