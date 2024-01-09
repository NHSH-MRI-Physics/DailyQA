import sys
import os 
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'DQA_Scripts'))
import DailyQA
import Helper
import sys
#os.chdir('..')


NumberOfBaselines=11

def GetThresh(Coil,Thresh):
    #Thresh=[1.0,1.0]
    Step=0.05
    
    ThreshFound = False
    while (ThreshFound==False):
        Passes = 0
        IncreaseThresh=[False,False]
        for i in range (1,NumberOfBaselines+1):
            Files = "BaselineData/"+Coil+"/DQA_"+Coil+"_" + str(i)
            Results = DailyQA.RunDailyQA(Files)
            QAResultTracker=[]
            
            PassTracker=[]
            for result in Results:
                QAResult = Helper.DidQAPass(result,Thresh)
                print(QAResult[0],Files)
                PassTracker.append(QAResult[0])
                if (QAResult[0]==False):
                    #print(QAResult[1])
                    if "ROI" in QAResult[1]:
                        IncreaseThresh[1]=True
                    if "Overall" in QAResult[1]:
                        IncreaseThresh[0]=True
            
            if (False not in PassTracker):
                Passes+=1

        if IncreaseThresh[0]==False and IncreaseThresh[1]==False:
            print("Threshold found for " + Coil)
            print(Thresh)
            ThreshFound=True
            

        if IncreaseThresh[0] == True:
            Thresh[0]+=Step
            Thresh[0] = round(Thresh[0],4)
        if IncreaseThresh[1] == True:
            Thresh[1]+=Step
            Thresh[1] = round(Thresh[1],4)
        IncreaseThresh=[False,False]
        print("New Tresh " + str(Thresh[0]) + " " + str(Thresh[1]) + "  Passes at previous thresh " +str(Passes) + " out of " + str(NumberOfBaselines) )


def FinalTest(Coil):
    for i in range (1,NumberOfBaselines+1):
        Files = "BaselineData/"+Coil+"/DQA_"+Coil+"_" + str(i)
        Results = DailyQA.RunDailyQA(Files)
        for result in Results:
            QAResult = Helper.DidQAPassV2(result)
            print(QAResult[0],Files)

#GetThresh("Head",[3.3,3.7])
#GetThresh("Spine",[1.8,4.45])
#GetThresh("Body",[2.95,3.0])


#FinalTest("Head")
FinalTest("Spine")
#FinalTest("Body")