import unittest
import sys
import os 
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'DQA_Scripts'))
import DailyQA
import numpy as np
import Helper
import glob

#If the unit tests are run in the UnitTesting folder then move the working directory back to the DailyQA folder
if( os.path.basename(os.path.normpath(os.getcwd())) ) == "UnitTesting": 
    os.chdir('..')

class TestSNRNormal(unittest.TestCase):
    def test_headSNR(self):
        Results = DailyQA.RunDailyQA("BaselineData/Head/DQA_Head_1")
        Baseline = np.load('UnitTesting/HeadBaseline.npy',allow_pickle=True) 
        np.testing.assert_array_equal(Results,Baseline)

        files = glob.glob("Results/*.png")
        self.assertEqual(files[0],'Results/Ax T2 FSE head_SmoothMethod.png')
        self.assertEqual(files[1],'Results/Ax EPI-GRE head_SmoothMethod.png')
        
unittest.main()