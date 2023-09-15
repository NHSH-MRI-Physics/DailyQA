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
    TEXT = "Hi " + name + "\n\n\n"
    TEXT+="Daily QA Results run on " + str(datetime.date.today()) + "\n\n"
    for line in results:
        TEXT+=line +  "\n"
    TEXT+="\n\n\n\n"
    TEXT+= "Random Fact: " + randfacts.get_fact()    
    
    if False in QAResult:
        message = 'Subject: {}\n\n{}'.format(QAName +" FAIL", TEXT)
    else:
        message = 'Subject: {}\n\n{}'.format(QAName +" PASS", TEXT)
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




@dataclass
class ROIResults:
    M1: float #center
    M2: float #top right
    M3: float #bottom left
    M4: float #bottom right
    M5: float #top left

@dataclass
class ROIBaseline:
    #list goes lower bounds, upper bounds and mean
    M1: list #center
    M2: list #top right
    M3: list #bottom left
    M4: list #bottom right
    M5: list #top left