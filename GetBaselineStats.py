import DailyQA
import os
import Helper
import sys
import numpy as np

def GetBaselineSmooth(path,SaveName):
	ROI_Results = {} #ROI_Results[seq][sample][ROI][slice]
	SNR_Results={}
	files =  (next(os.walk(path))[1])

	count=0
	for file in files:
		print ("working on " + file)
		count+=1
		Results = DailyQA.RunDailyQA(os.path.join(path,file))
		#Results = Helper.ProduceTestData(count)
		for seqNum in range(len(Results)):
			if Results[seqNum][-1] not in ROI_Results:
				ROI_Results[Results[seqNum][-1]] = []
				SNR_Results[Results[seqNum][-1]] = []
			SNR_Results[Results[seqNum][-1]].append(Results[seqNum][0])
			ROI_Results[Results[seqNum][-1]].append(Results[seqNum][1])
		

	#Get ROI baselines
	#Results[Seq][ROI][Slice] = [Mean,STD]
	Results = {}
	Sequences = list(ROI_Results.keys())
	ROIS = list(ROI_Results[Sequences[0]][0].keys())

	for seq in Sequences:
		NumberOfSlicesInSeq = len(ROI_Results[seq][0]["M1"])
		Results[seq] = {}
		for ROI in ROIS:
			Results[seq][ROI]=[]
			for slice in range(NumberOfSlicesInSeq):
				Results[seq][ROI].append( [])
				templist=[]
				for sample in range(len(files)):
					templist.append(ROI_Results[seq][sample][ROI][slice])
				Results[seq][ROI][slice].append(np.mean(templist))
				Results[seq][ROI][slice].append(np.std(templist))



	#Get global SNR Results
	GlobalResults = {}
	for seq in Sequences:
		GlobalResults[seq] = [np.mean(SNR_Results[seq]), np.std(SNR_Results[seq])]

	if True:
		#For Testing
		for seq in Sequences:
			for ROI in ROIS:
				NumberOfSlicesInSeq = len(ROI_Results[seq][0]["M1"])
				for slice in range(NumberOfSlicesInSeq):
					print("Seq;" + str(seq)+ "    Slice: " +str(slice) + "    ROI: " + str(ROI)  + "	Mean:" +str(Results[seq][ROI][slice][0]) + "	STD:" + str(Results[seq][ROI][slice][1]))
			print(GlobalResults[seq])

	np.save(os.path.join(path,"ROI_"+SaveName), Results)
	np.save(os.path.join(path,"Global_"+SaveName), GlobalResults)
	print("Baseline saved: " + SaveName)
	

path = "BaselineData/Head"
GetBaselineSmooth(path,"Head_Baseline.npy")

#path = "BaselineData/Body"
#GetBaselineSmooth(path,"Body_Baseline.npy")

path = "BaselineData/Spine"
GetBaselineSmooth(path,"Spine_Baseline.npy")