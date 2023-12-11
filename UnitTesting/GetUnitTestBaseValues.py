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

GetBase("BaselineData/Head/DQA_Head_1","UnitTesting/HeadBaseline.npy")
GetBase("BaselineData/Body/DQA_Body_1","UnitTesting/BodyBaseline.npy")
GetBase("BaselineData/Spine/DQA_Spine_1","UnitTesting/SpineBaseline.npy")