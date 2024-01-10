import sys
import os 
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'DQA_Scripts'))
import DailyQA
import Helper
import numpy as np
#os.chdir('..')

def GetBaselineSmooth(files,SaveName,path):

	ROI_Results = {} #ROI_Results[seq][sample][ROI][slice]
	SNR_Results={}

	#files =  (next(os.walk(path))[1])
	count=0
	for file in files:
		print ("working on " + file)
		count+=1
		Results = DailyQA.RunDailyQA(file)
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

				Mean = np.mean(templist)
				Bounds = np.std(templist)

				Results[seq][ROI][slice].append(Mean)
				Results[seq][ROI][slice].append(Bounds)
				
	#Get global SNR Results
	GlobalResults = {}
	for seq in Sequences:
		GlobalResults[seq] = [np.mean(SNR_Results[seq]), np.std(SNR_Results[seq])]

	#Get Average Per Slice
	PerSliceResults = {}
	for seq in Sequences:
		PerSliceResults[seq] = []
		NumberOfSlicesInSeq = len(ROI_Results[seq][0]["M1"])
		for slice in range(NumberOfSlicesInSeq):
			SampleValue=[]
			for sample in range(len(files)):
				TempData = []
				for ROI in ROIS:
					TempData.append(ROI_Results[seq][sample][ROI][slice])
				SampleValue.append(np.mean(TempData))

			PerSliceResults[seq].append( [np.mean(SampleValue),np.std(SampleValue)] )

		print(PerSliceResults[seq])				
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
	np.save(os.path.join(path,"Slice_"+SaveName), PerSliceResults)
	print("Baseline saved: " + SaveName)
	


files = [x[0] for x in os.walk("BaselineData/Head/")][1:]
Archives = [x[0] for x in os.walk("Archive")][1:]
for folder in Archives:
    if "Head" in folder:
        files.append(folder)
#GetBaselineSmooth(files,"Head_Baseline.npy","BaselineData/Head/")

files = [x[0] for x in os.walk("BaselineData/Body/")][1:]
Archives = [x[0] for x in os.walk("Archive")][1:]
for folder in Archives:
    if "Body" in folder:
        files.append(folder)
#GetBaselineSmooth(files,"Body_Baseline.npy","BaselineData/Body/")

files = [x[0] for x in os.walk("BaselineData/Spine/")][1:]
Archives = [x[0] for x in os.walk("Archive")][1:]
for folder in Archives:
    if "Spine" in folder:
        files.append(folder)
#GetBaselineSmooth(files,"Spine_Baseline.npy","BaselineData/Spine/")