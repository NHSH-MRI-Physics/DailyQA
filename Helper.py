#Helperfunction to add rician noise to test if the stuff is working...
import numpy as np
import matplotlib.pyplot as plt
import math

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