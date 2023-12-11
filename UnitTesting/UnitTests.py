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
    def setUp(self):
        files = glob.glob("Results/*.png")
        for file in files:
            os.remove(file)

    def tearDown(self):
        files = glob.glob("Results/*.png")
        for file in files:
            os.remove(file)

    def test_headSNR(self):
        Results = DailyQA.RunDailyQA("BaselineData/Head/DQA_Head_1")
        Baseline = np.load('UnitTesting/HeadBaseline.npy',allow_pickle=True) 
        np.testing.assert_array_equal(Results,Baseline)

        files = glob.glob("Results/*.png")
        self.assertEqual(files[0],'Results/Ax T2 FSE head_SmoothMethod.png')
        self.assertEqual(files[1],'Results/Ax EPI-GRE head_SmoothMethod.png')
        self.assertEqual(2,len(files))


    def test_BodySNR(self):
        Results = DailyQA.RunDailyQA("BaselineData/Body/DQA_Body_1")
        Baseline = np.load('UnitTesting/BodyBaseline.npy',allow_pickle=True) 
        np.testing.assert_array_equal(Results,Baseline)

        files = glob.glob("Results/*.png")
        self.assertEqual(files[0],'Results/Ax T2 SSFSE TE 90 Top_SmoothMethod.png')
        self.assertEqual(files[1],'Results/Ax EPI-GRE body Bot_SmoothMethod.png')
        self.assertEqual(files[2],'Results/Ax EPI-GRE body Top_SmoothMethod.png')
        self.assertEqual(files[3],'Results/Ax T2 SSFSE TE 90 Bot_SmoothMethod.png')

    def test_SpineSNR(self):
        Results = DailyQA.RunDailyQA("BaselineData/Spine/DQA_Spine_1")
        Baseline = np.load('UnitTesting/SpineBaseline.npy',allow_pickle=True) 
        np.testing.assert_array_equal(Results,Baseline)

        files = glob.glob("Results/*.png")
        self.assertEqual(files[0],'Results/Ax T2 SSFSE TE 90 Top_SmoothMethod.png')
        self.assertEqual(files[1],'Results/Ax EPI-GRE body Bot_SmoothMethod.png')
        self.assertEqual(files[2],'Results/Ax EPI-GRE body Top_SmoothMethod.png')
        self.assertEqual(files[3],'Results/Ax T2 SSFSE TE 90 Bot_SmoothMethod.png')    
        
unittest.main()