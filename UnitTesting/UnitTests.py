import unittest
import sys
import os 
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'DQA_Scripts'))
import DailyQA
import numpy as np
import Helper
import glob
import shutil

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
        Results = DailyQA.RunDailyQA("UnitTesting/UnitTestData/PassData/DQA_Head_1")
        Baseline = np.load('UnitTesting/UnitTestBaselines/HeadBaseline.npy',allow_pickle=True) 
        np.testing.assert_array_equal(Results,Baseline)

        files = glob.glob("Results/*.png")
        self.assertEqual(files[0],'Results/Ax T2 FSE head_SmoothMethod.png')
        self.assertEqual(files[1],'Results/Ax EPI-GRE head_SmoothMethod.png')
        self.assertEqual(2,len(files))


    def test_BodySNR(self):
        Results = DailyQA.RunDailyQA("UnitTesting/UnitTestData/PassData/DQA_Body_1")
        Baseline = np.load('UnitTesting/UnitTestBaselines/BodyBaseline.npy',allow_pickle=True) 
        np.testing.assert_array_equal(Results,Baseline)

        files = glob.glob("Results/*.png")
        self.assertEqual(files[0],'Results/Ax T2 SSFSE TE 90 Top_SmoothMethod.png')
        self.assertEqual(files[1],'Results/Ax EPI-GRE body Bot_SmoothMethod.png')
        self.assertEqual(files[2],'Results/Ax EPI-GRE body Top_SmoothMethod.png')
        self.assertEqual(files[3],'Results/Ax T2 SSFSE TE 90 Bot_SmoothMethod.png')
        self.assertEqual(4,len(files))

    def test_SpineSNR(self):
        Results = DailyQA.RunDailyQA("UnitTesting/UnitTestData/PassData/DQA_Spine_1")
        Baseline = np.load('UnitTesting/UnitTestBaselines/SpineBaseline.npy',allow_pickle=True) 
        np.testing.assert_array_equal(Results,Baseline)

        files = glob.glob("Results/*.png")
        self.assertEqual(files[0],'Results/Ax T2 SSFSE TE 90 Top_SmoothMethod.png')
        self.assertEqual(files[1],'Results/Ax EPI-GRE body Bot_SmoothMethod.png')
        self.assertEqual(files[2],'Results/Ax EPI-GRE body Top_SmoothMethod.png')
        self.assertEqual(files[3],'Results/Ax T2 SSFSE TE 90 Bot_SmoothMethod.png')    
        self.assertEqual(4,len(files))
        
class TestPassAndEmailFunction(unittest.TestCase):
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

        for name in Emails.keys():
            Helper.SendEmailV2(name,Emails[name],EmailResultLines,Results[0][2]+" (UNIT TEST RUN)",QAResultTracker,Archive=DataFolder,images=Images)

    '''
    def test_bodyPassAndEmail(self):
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

        for name in Emails.keys():
            Helper.SendEmailV2(name,Emails[name],EmailResultLines,Results[0][2]+" (UNIT TEST RUN)",QAResultTracker,Archive=DataFolder,images=Images)

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

        for name in Emails.keys():
            Helper.SendEmailV2(name,Emails[name],EmailResultLines,Results[0][2]+" (UNIT TEST RUN)",QAResultTracker,Archive=DataFolder,images=Images)
        '''

class TestFailAndEmailFunction(unittest.TestCase):
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

        for name in Emails.keys():
            Helper.SendEmailV2(name,Emails[name],EmailResultLines,Results[0][2]+" (UNIT TEST RUN)",QAResultTracker,Archive=DataFolder,images=Images)

unittest.main()