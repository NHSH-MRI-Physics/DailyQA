import DailyQA
import Helper
import sys





def GetThresh(Coil,Thresh):
    #Thresh=[1.0,1.0]
    Step=0.05
    NumberOfBaselines=10

    
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

#GetThresh("Head",[2.25,2.9])


GetThresh("Spine",[2.1,2.75])