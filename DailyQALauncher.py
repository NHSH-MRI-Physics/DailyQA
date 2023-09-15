import DailyQA

Files = "Data/DQA_Head_20230914_214806084" # Head Coil 
#Files = "Data/DQA_Body_20230914_214817785" # Body Coil 
#Files = "Data/DQA_Spine_20230914_214814825" # Spine Coil 

Results = DailyQA.RunDailyQA(Files)
for result in Results:
	print (result)
#DailyQA.Helper.SaveHistoricData(Results,"HeadQA.txt")
#DailyQA.Helper.PlotCSV("HeadQA.txt")