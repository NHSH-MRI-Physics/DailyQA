#Helperfunction to add rician noise to test if the stuff is working...
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import randfacts
import pandas as pd
import os
from dataclasses import dataclass
import random

def AddNoise(Image,sigma):
    NoiseImage = np.copy(Image)

    for i in range(Image.shape[2]):
        noiseReal = np.random.normal(0,sigma,[Image.shape[0],Image.shape[1]])
        noiseImag = np.random.normal(0,sigma,[Image.shape[0],Image.shape[1]])
        NoiseImage[:,:,i] = np.sqrt( (NoiseImage[:,:,i] + noiseReal)**2 + noiseImag*noiseImag)
    return NoiseImage

def GetRejectedSlicesAvgLine(Data):
    XShapeHalf = int(round(Data.shape[0]/2,0))
    YShapeHalf = int(round(Data.shape[1]/2,0))
    ROISize = 10
    Comp = []
    for i in range(Data.shape[2]):
        Comp.append(np.mean(Data[XShapeHalf-ROISize:XShapeHalf+ROISize:,YShapeHalf-ROISize:YShapeHalf+ROISize,i]))
    MeanVal = sum(Comp)/len(Comp)

    plt.plot(Comp,marker="x")
    plt.axhline(y=MeanVal, color='r', linestyle='-')
    plt.show()
    plt.close()

    RejectedSlices=[]
    for i in range(Data.shape[2]):
        if np.mean(Data[XShapeHalf-ROISize:XShapeHalf+ROISize:,YShapeHalf-ROISize:YShapeHalf+ROISize,i]) < MeanVal:
            RejectedSlices.append(i)
    return RejectedSlices

def GetRejectedSlicesSplit(Data,ThreshOption=None):
    XShapeHalf = int(round(Data.shape[0]/2,0))
    YShapeHalf = int(round(Data.shape[1]/2,0))
    ROISize = 10
    Comp = []
    for i in range(Data.shape[2]):
        Comp.append(np.mean(Data[XShapeHalf-ROISize:XShapeHalf+ROISize:,YShapeHalf-ROISize:YShapeHalf+ROISize,i]))

    Thresh=ThreshOption
    if Thresh==None:
        Thresh = (max(Comp) + min(Comp)) / 2.0
    
    if ThreshOption!=None:
        plt.plot(Comp,marker="x")
        plt.axhline(y=Thresh, color='r', linestyle='-')
        plt.show()
        plt.close()

    RejectedSlices=[]
    for i in range(Data.shape[2]):
        if np.mean(Data[XShapeHalf-ROISize:XShapeHalf+ROISize:,YShapeHalf-ROISize:YShapeHalf+ROISize,i]) < Thresh:
            RejectedSlices.append(i)
    return RejectedSlices

def GetRejectedSlicesEitherSide(Data,ThreshOption=None):
    XShapeHalf = int(round(Data.shape[0]/2,0))
    YShapeHalf = int(round(Data.shape[1]/2,0))
    ROISize = 10
    Comp = []
    for i in range(Data.shape[2]):
        Comp.append(np.mean(Data[XShapeHalf-ROISize:XShapeHalf+ROISize:,YShapeHalf-ROISize:YShapeHalf+ROISize,i]))
    Idx = Comp.index(min(Comp))
    return [Idx-1,Idx,Idx+1]

def Setupplots(ImageData,seq):
    if (ImageData.shape[2])>=10:
        Cols = 10 
        Rows = math.ceil( ImageData.shape[2]/Cols )
    else:
        Cols= ImageData.shape[2]
        Rows = 2

    fig, axs = plt.subplots(Rows, Cols)
    Size = 0.25*ImageData.shape[2]
    if Size < 7.5:
        Size = 7.5
    fig.set_size_inches(25, Size)
    fig.suptitle(seq, fontsize=35)
    for i in range(Cols):
        for j in range(Rows):
            axs[j,i].set_axis_off()
    return fig,axs,Cols

def SendEmail(name,email,results,QAName,QAResult):
    UserName = "raigmoremri@gmail.com"
    file = open('Password.txt',mode='r')
    Password = file.read()
    file.close()

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(UserName, Password)
    TEXT = "Hi " + name + "\n\n"

    if False in QAResult:
        TEXT+="Daily " + QAName + " QA Results run on " + str(datetime.date.today()) + "    Result: Fail\n\n"
    else:
        TEXT+="Daily " + QAName + " QA Results run on " + str(datetime.date.today()) + "    Result: Pass\n\n"

    for line in results:
        TEXT+=line +  "\n"
    TEXT+="\n"
    TEXT+= "Random Fact: " + randfacts.get_fact()    
    
    if False in QAResult:
        message = 'Subject: {}\n\n{}'.format("Daily " + QAName +" QA: FAIL", TEXT)
    else:
        message = 'Subject: {}\n\n{}'.format("Daily " + QAName +" QA: PASS", TEXT)
    s.sendmail(UserName, email, message)
    s.quit()

def SaveHistoricData(result,filename):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists(filename):
        f = open(filename, 'w')
        line = ""
        line = "date" + ","
        for OneSeq in result:
            line +=OneSeq[-1]+" Smooth SNR,"
            line +=OneSeq[-1]+" Ness-Anvier Method SNR,"
        line = line[:-1]
        line+="\n"
        f.write(line)
        f.close()
    f = open(filename,'a')

    f.write(str(date) + "," + str(result[0][0]) + "," + str(result[0][1]) + "," + str(result[1][0]) + "," + str(result[1][1]) + "\n")
    f.close()


def PlotCSV(file):
    data= pd.read_csv(file)
    

    #PlotNames = [file.split(".")[0]+"_SmoothSNR.png" , file.split(".")[0]+"_NessAvierSNR.png"]
    #labels = ["Smooth Method SNR" , "Ness-Avier Method SNR"]

    
    for i in range(4):
        plt.title(data.columns.values[i+1],fontsize=100)
        fig = plt.gcf()
        fig.set_size_inches(60, 30)
        x, y = zip(*sorted(zip(data["date"],data.iloc[:, 1+i]))) #This ensures the order of the data is in accending date
        plt.plot(x,y,linewidth=10,marker="o",markersize=60)
        plt.xlabel("Date",fontsize=60)
        plt.ylabel("SNR",fontsize=60)
        plt.xticks(rotation = 45,fontsize=50)
        plt.yticks(fontsize=50)
        plt.grid(linewidth = 5)
        plt.gca().spines['bottom'].set_linewidth(10) #These make the line bounds of the plot thicker or thinner
        plt.gca().spines['left'].set_linewidth(10)
        plt.gca().spines['top'].set_linewidth(0)
        plt.gca().spines['right'].set_linewidth(0)
        plt.tight_layout()
        plt.savefig(data.columns.values[i+1]+".png")
        plt.close()

def ProduceTestData(SampleReturn):
    if SampleReturn==1:
        DummyResult = [ ]
        SNRROIResults = {}
        SNRROIResults["M1"] = [8.8633576 , 8.22168769, 9.70128566, 9.63072772, 5.15352691]
        SNRROIResults["M2"] = [8.05761132, 7.61521955, 5.78417548, 7.44909098, 9.69474371]
        SNRROIResults["M3"] = [5.74136821, 6.0832267 , 8.86656073, 6.67228168, 8.70911806]
        SNRROIResults["M4"] = [6.48681254, 6.11240844, 9.22669321, 6.57971852, 9.19739686]
        SNRROIResults["M5"] = [7.52878316, 8.34842631, 9.19831386, 7.81120433, 7.75065708]
        FullData = SNRROIResults["M1"] + SNRROIResults["M2"] + SNRROIResults["M3"] + SNRROIResults["M4"] + SNRROIResults["M5"]
        DummyResult.append([sum(FullData)/len(FullData), SNRROIResults, "Head", "DummyDataSeq1"])
        #print(DummyResult[0][0]) 

        SNRROIResults = {}
        SNRROIResults["M1"] = [6.10592107, 5.70860682, 8.9985303 , 5.46031738, 5.8453783 , 6.82120479, 7.60462207, 7.39363334, 7.16485355, 6.23632868, 5.19630993, 6.43930318, 7.37078088, 6.34543183]
        SNRROIResults["M2"] = [6.49532712, 8.85460135, 6.52380466, 8.41295335, 6.90858613, 8.08454006, 7.12660041, 8.51265192, 5.50187123, 9.67796607, 5.03438364, 7.68562575, 9.55799361, 5.61545348]
        SNRROIResults["M3"] = [5.23101078, 9.03285251, 8.51082835, 7.38149451, 7.53306168, 5.99170431, 5.98593531, 6.98294862, 9.01660868, 6.02774162, 8.19801143, 7.09039863, 6.72578737, 8.80923194]
        SNRROIResults["M4"] = [7.38858228, 9.19754003, 6.90851995, 9.91347946, 5.23198985, 8.98052191, 6.33179861, 6.20522325, 6.7241958 , 8.78700436, 9.78874446, 6.64442793, 8.1707005 , 8.20452634]
        SNRROIResults["M5"] = [8.60137656, 5.44662036, 7.01971598, 6.37356807, 9.00218893, 6.34374114, 7.87412952, 7.53139485, 8.92522989, 6.16260427, 8.39409242, 8.65067258, 8.68045227, 9.15929925]
        FullData = SNRROIResults["M1"] + SNRROIResults["M2"] + SNRROIResults["M3"] + SNRROIResults["M4"] + SNRROIResults["M5"]
        DummyResult.append([sum(FullData)/len(FullData), SNRROIResults, "Head", "DummyDataSeq2"])
        #print(DummyResult[1][0])
        return DummyResult
    
    if SampleReturn==2:
        DummyResult = [ ]
        SNRROIResults = {}
        SNRROIResults["M1"] = [5.1303423 , 7.08845086, 6.10825289, 7.3677603 , 5.27348263]
        SNRROIResults["M2"] = [7.6412771 , 6.50168579, 9.0714044 , 8.47160101, 5.5773068 ]
        SNRROIResults["M3"] = [5.59902455, 6.61029038, 5.26679972, 6.50101474, 5.94810375]
        SNRROIResults["M4"] = [5.10401653, 5.37539124, 5.56939146, 7.66749155, 7.64221727]
        SNRROIResults["M5"] = [7.31773808, 6.27127583, 9.0495356 , 7.71829425, 7.93179535]
        FullData = SNRROIResults["M1"] + SNRROIResults["M2"] + SNRROIResults["M3"] + SNRROIResults["M4"] + SNRROIResults["M5"]
        DummyResult.append([sum(FullData)/len(FullData), SNRROIResults, "Head", "DummyDataSeq1"])
        #print(DummyResult[0][0])

        SNRROIResults = {}
        SNRROIResults["M1"] = [5.81791769, 9.64132247, 6.62280934, 8.89215173, 8.59738562, 6.59870594, 9.28905194, 8.21820272, 9.44359057, 5.91158876, 5.596963  , 8.0697869 , 5.29257149, 9.98202317]
        SNRROIResults["M2"] = [9.84010074, 8.54778004, 7.53903503, 9.20317236, 7.7687837 , 9.43192388, 9.058627  , 8.17161729, 9.78783377, 8.43168162, 7.99479224, 8.57493109, 5.83049242, 6.37558248]
        SNRROIResults["M3"] = [5.89491257, 5.34317036, 6.98666847, 9.55746271, 6.19284555, 8.01103426, 8.37040579, 9.95299212, 6.08283913, 9.48250833, 7.98443354, 6.45582275, 6.37040166, 5.15076491]
        SNRROIResults["M4"] = [5.9333325 , 6.17833572, 7.82834822, 5.98873262, 6.55829869, 8.64901984, 5.16696442, 7.35049073, 9.4659645 , 9.35787041, 5.19672763, 8.86219963, 6.57007379, 5.35801839]
        SNRROIResults["M5"] = [5.47749527, 6.19384568, 5.05280023, 5.75707747, 7.07266771, 7.15190459, 9.92190222, 8.67737402, 5.28049409, 6.42703496, 6.22748867, 7.29281415, 5.90094519, 5.04900084]
        FullData = SNRROIResults["M1"] + SNRROIResults["M2"] + SNRROIResults["M3"] + SNRROIResults["M4"] + SNRROIResults["M5"]
        DummyResult.append([sum(FullData)/len(FullData), SNRROIResults, "Head", "DummyDataSeq2"])
        #print(DummyResult[1][0])

        return DummyResult
    

def DidQAPass(Result):
    QAType = Result[2]
    SNR = Result[0]
    ROIResults = Result[1]
    Sequence = Result[3]

    #ROIBaseline[Seq][ROI][Slice] = [Mean,STD]
    if QAType=="Head":
        GlobalBaseline = np.load(os.path.join("BaselineData","Head","Global_Head_Baseline.npy"),allow_pickle=True).item()[Sequence]
        ROIBaseline = np.load(os.path.join("BaselineData","Head","ROI_Head_Baseline.npy"),allow_pickle=True).item()[Sequence]
        GlobalSTDModifier = 1.0
        ROISTDModifier = 1.0

    if QAType=="Body":
        GlobalBaseline = np.load(os.path.join("BaselineData","Body","Global_Body_Baseline.npy"),allow_pickle=True).item()[Sequence]
        ROIBaseline = np.load(os.path.join("BaselineData","Body","ROI_Body_Baseline.npy"),allow_pickle=True).item()[Sequence]
        GlobalSTDModifier = 1.0
        ROISTDModifier = 1.0

    if QAType=="Spine":
        GlobalBaseline = np.load(os.path.join("BaselineData","Spine","Global_Spine_Baseline.npy"),allow_pickle=True).item()[Sequence]
        ROIBaseline = np.load(os.path.join("BaselineData","Spine","ROI_Spine_Baseline.npy"),allow_pickle=True).item()[Sequence]
        GlobalSTDModifier = 1.0
        ROISTDModifier = 1.0

    #Global
    FailMessage=""
    Lower = GlobalBaseline[0] - GlobalBaseline[1]*GlobalSTDModifier
    Upper = GlobalBaseline[0] + GlobalBaseline[1]*GlobalSTDModifier
    if (Lower <= SNR <= Upper) == False:
        FailMessage+="Overall SNR Failed on "+ QAType +" QA Seq: " + Sequence + "  Result:" + str(round(SNR,4)) + "   Baseline Bounds:" + str(round(Lower,4)) + " to " + str(round(Upper,4)) +"\n"

    #ROI
    NumberOfSlicesInSeq = len(ROIResults["M1"])
    ROIS = list(ROIBaseline.keys())
    for ROI in ROIS:
        for Slice in range(NumberOfSlicesInSeq):
            Lower = ROIBaseline[ROI][Slice][0] - ROIBaseline[ROI][Slice][1]*ROISTDModifier
            Upper = ROIBaseline[ROI][Slice][0] + ROIBaseline[ROI][Slice][1]*ROISTDModifier
            if (Lower <= ROIResults[ROI][Slice] <= Upper) == False:
                FailMessage+="ROI " + ROI + " on slice " + str(Slice+1) + " SNR Failed on "+ QAType +" QA Seq: " + Sequence + "  Result:" + str(round(ROIResults[ROI][Slice],4)) + "   Baseline:" + str(round(Lower,4)) + " to " + str(round(Upper,4)) +"\n"


    if FailMessage=="":
        return True,FailMessage
    else:
        return False,FailMessage