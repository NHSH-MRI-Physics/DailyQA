import unittest
import sys
import os 
#current_dir = os.path.dirname(os.path.abspath(__file__))
#parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
#sys.path.append(parent_dir)
from DQA_Scripts import DailyQA
import numpy as np
from DQA_Scripts import Helper   
import glob
import shutil
import pandas as pd


import matplotlib.pyplot as plt
#import matplotlib
#matplotlib.use('TkAgg')  # Use a GUI backend
from DQA_Scripts.SmoothingMethod import TestingSettings as testingsettings

#If the unit tests are run in the UnitTesting folder then move the working directory back to the DailyQA folder
if( os.path.basename(os.path.normpath(os.getcwd())) ) == "UnitTesting": 
    os.chdir('..')

def CompareToBaseline(Results,Baseline):
    for result in Results:
        for baseResult in Baseline:
            if baseResult[-1]==result[-1]:
                pd.testing.assert_series_equal(pd.Series(result),pd.Series(baseResult))

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
        Results = DailyQA.RunDailyQA("UnitTesting/UnitTestData/PassData/DQA_Head_1")
        Baseline = np.load('UnitTesting/UnitTestBaselines/HeadBaseline.npy',allow_pickle=True) 

        CompareToBaseline(Results,Baseline)

        files = glob.glob("Results/*.png")
        self.assertEqual(2,len(files))

        PredictedFiles =[]
        PredictedFiles.append(os.path.join('Results','Ax T2 FSE head_SmoothMethod.png'))
        PredictedFiles.append(os.path.join('Results','Ax EPI-GRE head_SmoothMethod.png'))
        unittest.TestCase().assertCountEqual(files, PredictedFiles)


    def test_BodySNR(self):
        Results = DailyQA.RunDailyQA("UnitTesting/UnitTestData/PassData/DQA_Body_1")
        Baseline = np.load('UnitTesting/UnitTestBaselines/BodyBaseline.npy',allow_pickle=True) 
        CompareToBaseline(Results,Baseline)

        files = glob.glob("Results/*.png")
        self.assertEqual(4,len(files))
        PredictedFiles =[]
        PredictedFiles.append(os.path.join('Results','Ax T2 SSFSE TE 90 Top_SmoothMethod.png'))
        PredictedFiles.append(os.path.join('Results','Ax EPI-GRE body Bot_SmoothMethod.png'))
        PredictedFiles.append(os.path.join('Results','Ax EPI-GRE body Top_SmoothMethod.png'))
        PredictedFiles.append(os.path.join('Results','Ax T2 SSFSE TE 90 Bot_SmoothMethod.png'))
        unittest.TestCase().assertCountEqual(files, PredictedFiles)
        

    def test_SpineSNR(self):
        Results = DailyQA.RunDailyQA("UnitTesting/UnitTestData/PassData/DQA_Spine_1")
        Baseline = np.load('UnitTesting/UnitTestBaselines/SpineBaseline.npy',allow_pickle=True) 
        CompareToBaseline(Results,Baseline)

        files = glob.glob("Results/*.png")
        self.assertEqual(4,len(files))
        PredictedFiles =[]
        PredictedFiles.append(os.path.join('Results','Ax T2 SSFSE TE 90 Top_SmoothMethod.png'))
        PredictedFiles.append(os.path.join('Results','Ax EPI-GRE body Bot_SmoothMethod.png'))
        PredictedFiles.append(os.path.join('Results','Ax EPI-GRE body Top_SmoothMethod.png'))
        PredictedFiles.append(os.path.join('Results','Ax T2 SSFSE TE 90 Bot_SmoothMethod.png'))
        unittest.TestCase().assertCountEqual(files, PredictedFiles)
        
class TestPass(unittest.TestCase):
    def setUp(self):
        files = glob.glob("Results/*.png")
        for file in files:
            os.remove(file)

    def tearDown(self):
        files = glob.glob("Results/*.png")
        for file in files:
            os.remove(file)

    def test_headPassAndEmail(self):
        Emails = {}
        Emails["John"] = "Johnt717@gmail.com"
        EmailResultLines = []
        Images = []

        Files = "UnitTesting/UnitTestData/PassData/DQA_Head_1"
        DataFolder = "UnitTesting/UnitTestData/PassData/DQA_Head_1"
        Results = DailyQA.RunDailyQA(Files)
        QAResultTracker=[]
        for result in Results:
            QAResult = Helper.DidQAPassV2(result)

            if QAResult[0] == False:
                EmailResultLines.append(QAResult[1])
            QAResultTracker.append(QAResult[0])
            
            self.assertEqual(True, QAResult[0])
            self.assertEqual(0, len(QAResult[1]))

            shutil.copyfile("Results/"+result[-1]+"_SmoothMethod.png", os.path.join(DataFolder,result[-1]+"_SmoothMethod.png"))
            Images.append(os.path.join(DataFolder,result[-1]+"_SmoothMethod.png"))

        #for name in Emails.keys():
        #    Helper.SendEmailV2(name,Emails[name],EmailResultLines,Results[0][2]+" (UNIT TEST RUN)",QAResultTracker,Archive=DataFolder,images=Images)

    
    def test_bodyPass(self):
        Emails = {}
        Emails["John"] = "Johnt717@gmail.com"
        EmailResultLines = []
        Images = []

        Files = "UnitTesting/UnitTestData/PassData/DQA_Body_1"
        DataFolder = "UnitTesting/UnitTestData/PassData/DQA_Body_1"
        Results = DailyQA.RunDailyQA(Files)
        QAResultTracker=[]
        for result in Results:
            QAResult = Helper.DidQAPassV2(result)

            if QAResult[0] == False:
                EmailResultLines.append(QAResult[1])
            QAResultTracker.append(QAResult[0])
            
            self.assertEqual(True, QAResult[0])
            self.assertEqual(0, len(QAResult[1]))

            shutil.copyfile("Results/"+result[-1]+"_SmoothMethod.png", os.path.join(DataFolder,result[-1]+"_SmoothMethod.png"))
            Images.append(os.path.join(DataFolder,result[-1]+"_SmoothMethod.png"))

        #for name in Emails.keys():
        #    Helper.SendEmailV2(name,Emails[name],EmailResultLines,Results[0][2]+" (UNIT TEST RUN)",QAResultTracker,Archive=DataFolder,images=Images)
    
    def test_spinePassAndEmail(self):
        Emails = {}
        Emails["John"] = "Johnt717@gmail.com"
        EmailResultLines = []
        Images = []

        Files = "UnitTesting/UnitTestData/PassData/DQA_Spine_1"
        DataFolder = "UnitTesting/UnitTestData/PassData/DQA_Spine_1"
        Results = DailyQA.RunDailyQA(Files)
        QAResultTracker=[]
        for result in Results:
            QAResult = Helper.DidQAPassV2(result)

            if QAResult[0] == False:
                EmailResultLines.append(QAResult[1])
            QAResultTracker.append(QAResult[0])
            
            self.assertEqual(True, QAResult[0])
            self.assertEqual(0, len(QAResult[1]))

            shutil.copyfile("Results/"+result[-1]+"_SmoothMethod.png", os.path.join(DataFolder,result[-1]+"_SmoothMethod.png"))
            Images.append(os.path.join(DataFolder,result[-1]+"_SmoothMethod.png"))

        #for name in Emails.keys():
        #    Helper.SendEmailV2(name,Emails[name],EmailResultLines,Results[0][2]+" (UNIT TEST RUN)",QAResultTracker,Archive=DataFolder,images=Images)
        

class TestFail(unittest.TestCase):
    def setUp(self):
        files = glob.glob("Results/*.png")
        for file in files:
            os.remove(file)

    def tearDown(self):
        files = glob.glob("Results/*.png")
        for file in files:
            os.remove(file)

    def test_headFailAndEmail(self):
        Emails = {}
        Emails["John"] = "Johnt717@gmail.com"
        EmailResultLines = []
        Images = []

        Files = "UnitTesting/UnitTestData/FailData/DQA_Head_Fail"
        DataFolder = "UnitTesting/UnitTestData/FailData/DQA_Head_Fail"
        Results = DailyQA.RunDailyQA(Files)
        QAResultTracker=[]
        AllResults = []
        for result in Results:
            QAResult = Helper.DidQAPassV2(result)
            AllResults.append(QAResult)
            if QAResult[0] == False:
                EmailResultLines.append(QAResult[1])
            QAResultTracker.append(QAResult[0])
            
            shutil.copyfile("Results/"+result[-1]+"_SmoothMethod.png", os.path.join(DataFolder,result[-1]+"_SmoothMethod.png"))
            Images.append(os.path.join(DataFolder,result[-1]+"_SmoothMethod.png"))

        BaselineFail = np.load('UnitTesting/UnitTestBaselines/HeadFailBaseline.npy',allow_pickle=True) 
        np.testing.assert_array_equal(AllResults,BaselineFail)

        #for name in Emails.keys():
        #    Helper.SendEmailV2(name,Emails[name],EmailResultLines,Results[0][2]+" (UNIT TEST RUN)",QAResultTracker,Archive=DataFolder,images=Images)

    def test_bodyFail(self):
        Emails = {}
        Emails["John"] = "Johnt717@gmail.com"
        EmailResultLines = []
        Images = []

        Files = "UnitTesting/UnitTestData/FailData/DQA_Body_Fail"
        DataFolder = "UnitTesting/UnitTestData/FailData/DQA_Body_Fail"
        Results = DailyQA.RunDailyQA(Files)
        QAResultTracker=[]
        for result in Results:
            QAResult = Helper.DidQAPassV2(result)

            if QAResult[0] == False:
                EmailResultLines.append(QAResult[1])
            QAResultTracker.append(QAResult[0])

            shutil.copyfile("Results/"+result[-1]+"_SmoothMethod.png", os.path.join(DataFolder,result[-1]+"_SmoothMethod.png"))
            Images.append(os.path.join(DataFolder,result[-1]+"_SmoothMethod.png"))

        #for name in Emails.keys():
        #    Helper.SendEmailV2(name,Emails[name],EmailResultLines,Results[0][2]+" (UNIT TEST RUN)",QAResultTracker,Archive=DataFolder,images=Images)

class TestFundementalFunctions(unittest.TestCase):
    def setUp(self):
        files = glob.glob("Results/*.png")
        for file in files:
            os.remove(file)

        self.UnitTestSettings = testingsettings()
        self.UnitTestSettings.imageindex = 2
        self.UnitTestSettings.ReturnImage = True
        self.UnitTestSettings.SeqToTest = "Ax T2 FSE head"

    def tearDown(self):
        files = glob.glob("Results/*.png")
        for file in files:
            os.remove(file)

    def test_Loading(self):
        matrix = np.loadtxt("UnitTesting/UnitTestData/ValidationTestData/LoadedData.txt", delimiter='\t')   
        results = DailyQA.RunDailyQA("UnitTesting/UnitTestData/PassData/DQA_Head_1",TestingSettings=self.UnitTestSettings)
        difference = (self.UnitTestSettings.ReturnImage-matrix)
        np.testing.assert_array_equal(np.max(difference),0)

    def test_smoothing(self):
        matrix = np.loadtxt("UnitTesting/UnitTestData/ValidationTestData/SmoothedImage.txt", delimiter='\t')   
        results = DailyQA.RunDailyQA("UnitTesting/UnitTestData/PassData/DQA_Head_1",TestingSettings=self.UnitTestSettings)

        '''
        plt.figure(figsize=(10, 6))
        plt.subplot(1, 3, 1)  # (rows, columns, index)
        plt.imshow(matrix)
        plt.colorbar()
        plt.subplot(1, 3, 2)
        plt.imshow(self.UnitTestSettings.ReturnSmoothedImage)
        plt.colorbar()
        plt.subplot(1, 3, 3)
        plt.imshow((matrix-self.UnitTestSettings.ReturnSmoothedImage))
        plt.colorbar()
        plt.tight_layout()
        plt.savefig("test.png")
        '''
        #This would be the maximum rounding difference
        np.testing.assert_array_less(np.max(np.abs(matrix-self.UnitTestSettings.ReturnSmoothedImage)),1)

    def test_difference(self):
        DifferenceData = np.loadtxt("UnitTesting/UnitTestData/ValidationTestData/Subtraction.txt", delimiter='\t')   
        results = DailyQA.RunDailyQA("UnitTesting/UnitTestData/PassData/DQA_Head_1",TestingSettings=self.UnitTestSettings)

        '''
        plt.figure(figsize=(10, 6))
        plt.subplot(1, 3, 1)  # (rows, columns, index)
        plt.imshow(DifferenceData)
        plt.colorbar()
        plt.subplot(1, 3, 2)
        plt.imshow(self.UnitTestSettings.ReturnDifferenceImage)
        plt.colorbar()
        plt.subplot(1, 3, 3)
        plt.imshow((DifferenceData-self.UnitTestSettings.ReturnDifferenceImage))
        plt.colorbar()
        plt.tight_layout()
        plt.savefig("test.png")
        '''

        np.testing.assert_array_less(np.max(np.abs(DifferenceData-self.UnitTestSettings.ReturnDifferenceImage)),1)

    def testSNR(self):
        Results = DailyQA.RunDailyQA("UnitTesting/UnitTestData/PassData/DQA_Head_1",TestingSettings=self.UnitTestSettings)

        M1SNR = Results[0][1]['M1'][2]
        M2SNR = Results[0][1]['M2'][2]
        M3SNR = Results[0][1]['M3'][2]
        M4SNR = Results[0][1]['M4'][2]
        M5SNR = Results[0][1]['M5'][2]


        M1ManualSNR = 2314.719/33.896
        M2ManualSNR = 2923.297/34.765
        M3ManualSNR = 2322.649/29.302
        M4ManualSNR = 2305.347/30.258
        M5ManualSNR = 3048.659/35.187
    
        i=0
        print(Results[i][-1])
        if (Results[i][-1]) != "Ax T2 FSE head":
            i=1
        
        print( abs(M1SNR-M1ManualSNR)/M1ManualSNR*100.0) 
        print( abs(M2SNR-M2ManualSNR)/M2ManualSNR*100.0) 
        print( abs(M3SNR-M3ManualSNR)/M3ManualSNR*100.0) 
        print( abs(M4SNR-M4ManualSNR)/M4ManualSNR*100.0) 
        print( abs(M5SNR-M5ManualSNR)/M5ManualSNR*100.0) 

        np.testing.assert_array_less(abs(M1SNR-M1ManualSNR)/M1ManualSNR*100.0,3)
        np.testing.assert_array_less(abs(M2SNR-M2ManualSNR)/M2ManualSNR*100.0,3)
        np.testing.assert_array_less(abs(M3SNR-M3ManualSNR)/M3ManualSNR*100.0,3)
        np.testing.assert_array_less(abs(M4SNR-M4ManualSNR)/M4ManualSNR*100.0,3)
        np.testing.assert_array_less(abs(M5SNR-M5ManualSNR)/M5ManualSNR*100.0,3)
        

#unittest.main()