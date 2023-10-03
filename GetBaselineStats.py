import DailyQA
import os


ROIResults = []
def GetBaseline(path):
	files =  (next(os.walk(path))[1])
	for file in files:
		Results = DailyQA.RunDailyQA(os.path.join(path,file))
		ROIResults.append(Results[1])

	SNR_Results = []
	ROI_Results=[]
	for entry in ROIResults:
		SNR_Results.append(entry[0])
		ROI_Results.append(entry[1])

	#ROI_Results[sample][ROI][slice]

	#BaselineData[ROI Name][slice][sample number]
	BaselineData = {}
	BaselineResults = {}
	for key in ROI_Results[0].keys():
		BaselineData[key]=[]
		for i in range(len(ROI_Results[0][key])):
			BaselineData[key].append([])
		BaselineResults[key] = []

	for SampleNum in range(len(ROI_Results)):
		for key in ROI_Results[SampleNum].keys():
			for SliceNum in range(len(ROI_Results[SampleNum][key])):
				BaselineData[key][SliceNum].append(ROI_Results[SampleNum][key][SliceNum])
	print(BaselineData["M1"])

path = "/Users/mri/Desktop/DailyQA/BaselineData/Head"
GetBaseline(path)