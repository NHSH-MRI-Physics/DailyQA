import DailyQA

Files = "Data/DailyQA_Test_20230824_201946068" # Head Coil 
#Files = "Data/Daily_QA_Test_Body_20230824_211440042" # Body Coil 
#Files = "Data/SpineFiltered" # Spine Coil 

Results = DailyQA.RunDailyQA(Files)
print (Results[0])
print (Results[1])