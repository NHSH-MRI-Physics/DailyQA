import sys
import os 
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'DQA_Scripts'))
import DailyQA
import numpy as np
import Helper

if( os.path.basename(os.path.normpath(os.getcwd())) ) == "UnitTesting": 
    os.chdir('..')
    
def GetBase(Files,savefile):
    Results = DailyQA.RunDailyQA(Files)
    np.save(savefile, Results) 

def GetFailResult(Files,savefile):
    Results = DailyQA.RunDailyQA(Files)

    baseline = []
    for result in Results:
        baseline.append(Helper.DidQAPassV2(result))
    np.save(savefile, baseline) 

#Passes
GetBase("UnitTesting/UnitTestData/PassData/DQA_Head_1","UnitTesting/UnitTestBaselines/HeadBaseline.npy")
GetBase("UnitTesting/UnitTestData/PassData/DQA_Body_1","UnitTesting/UnitTestBaselines/BodyBaseline.npy")
GetBase("UnitTesting/UnitTestData/PassData/DQA_Spine_1","UnitTesting/UnitTestBaselines/SpineBaseline.npy")

#Fails
GetFailResult("UnitTesting/UnitTestData/FailData/DQA_Head_Fail","UnitTesting/UnitTestBaselines/HeadFailBaseline.npy")