import pydicom
import glob
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import cv2 as cv
import matplotlib.patches as patches
import math
import Helper
from scipy import ndimage


#TestingSettings
class TestingSettings:
  def __init__(self):
    self.imageindex = None
    self.SeqToTest= None
    self.ReturnImage = None
    self.ReturnSmoothedImage = None
    self.ReturnDifferenceImage = None

def PlotROIS(ROIS,ROISize,RoiSizeHalf,BinaryMap,Image,col,row,axs,sliceNum,RejectedSlices):
    axs[row,col].set_axis_on()
    axs[row,col].axis('off')
    axs[row,col].imshow(Image,cmap='Greys_r')
    axs[row,col].set_title("Slice Num: " + str(sliceNum), fontsize=20)

    if sliceNum-1 not in RejectedSlices:
        count=1
        for roi in ROIS:
            rect = patches.Rectangle((roi[0]-RoiSizeHalf, roi[1]-RoiSizeHalf), ROISize, ROISize, linewidth=1, edgecolor='r', facecolor='none')
            axs[row,col].add_patch(rect)
            axs[row,col].text(roi[0], roi[1], str(count), style='italic', ha='center', va='center',fontsize=9,color='red')
            count+=1

def SmoothedImageSubtraction(ImageData,KernalSize,ROISizeArg=None,Thresh=None, width = None, Cent = None,seq=None, RejectedSlices = [],ScannerName = None,type=None, TestingSettings = None):

    fig,axs,Cols = Helper.Setupplots(ImageData,seq,ScannerName)
    

    if ImageData.shape[2] == len(RejectedSlices):
        raise ValueError ("all sices rejected, reduce rejecton threshold!")

    SNRAvg=[]
    SNRROIResults = {}
    SNRROIResults["M1"] = []
    SNRROIResults["M2"] = []
    SNRROIResults["M3"] = []
    SNRROIResults["M4"] = []
    SNRROIResults["M5"] = []

    for i in range(ImageData.shape[2]):
        Image = ImageData[:,:,i]
        #Image = Image.astype(int)
        ROIs = []
        RoiSizeHalf=None
        BinaryMapSignal=None

        if i not in RejectedSlices:
            #The paper says 9x9 is the best so lets go with that
            Smoothed = ndimage.uniform_filter(Image, 9, mode="constant")
            Difference = Image - Smoothed

            if TestingSettings != None:
                if i == TestingSettings.imageindex and seq== TestingSettings.SeqToTest:
                    TestingSettings.ReturnImage = Image
                    TestingSettings.ReturnSmoothedImage = Smoothed
                    TestingSettings.ReturnDifferenceImage = Difference

            
            
            ThreshRel = np.max(Image)*Thresh
            BinaryMapSignal = np.copy(Image)
            High = np.where(BinaryMapSignal>=ThreshRel)
            Low = np.where(BinaryMapSignal<ThreshRel)
            BinaryMapSignal[High]=1
            BinaryMapSignal[Low]=0


            mass_y, mass_x = np.where(BinaryMapSignal ==1)
            cent_y = int(round( np.average(mass_y),0 ))
            cent_x = int(round( np.average(mass_x),0 ))
            if Cent!=None:
                cent_x = Cent[0]
                cent_y = Cent[1]

            #Guess size of phantom
            LineProfile = BinaryMapSignal[cent_y,:]
            idx = np.where(LineProfile==1)
            widthX = int(round((idx[0][-1] - idx[0][0])/2.0,0))


            LineProfile = BinaryMapSignal[:,cent_x]
            idx = np.where(LineProfile==1)
            widthY = int(round((idx[0][-1] - idx[0][0])/2.0,0))

            if width!=None:
                widthX = width[0]
                widthY = width[1]

            #print(i,widthX)
            #print(ImageData.shape)

            if ROISizeArg==None:
                ROISize = widthX*0.3
            else:
                ROISize = ROISizeArg
            if ROISize<1:
                ROISize = 15
            RoiSizeHalf = int(round(ROISize/2.0,0))

            #Centre of each ROI
            M1 = [cent_x,cent_y]
            M2= [ int(round(cent_x+widthX*0.4,0)), int(round(cent_y+widthY*0.4,0)) ]
            M3= [ int(round(cent_x-widthX*0.4,0)), int(round(cent_y-widthY*0.4,0)) ]
            M4= [ int(round(cent_x+widthX*0.4,0)), int(round(cent_y-widthY*0.4,0)) ]
            M5= [ int(round(cent_x-widthX*0.4,0)), int(round(cent_y+widthY*0.4,0)) ]
            ROIs = [M1,M2,M3,M4,M5]

            SNRList=[]
            for roi in ROIs:                 
                Signal = np.mean(Image[roi[1]-RoiSizeHalf:roi[1]+RoiSizeHalf,roi[0]-RoiSizeHalf:roi[0]+RoiSizeHalf])
                Noise = np.std(Difference[roi[1]-RoiSizeHalf:roi[1]+RoiSizeHalf,roi[0]-RoiSizeHalf:roi[0]+RoiSizeHalf])
                SNR = Signal/Noise
                SNRList.append(SNR)
            SNRAvg.append(sum(SNRList)/len(SNRList))

            #ROIResults = Helper.ROIResults(SNRList[0],SNRList[1],SNRList[2],SNRList[3],SNRList[4])
            #SNRROIResults.append(ROIResults)
            SNRROIResults["M1"].append(SNRList[0])
            SNRROIResults["M2"].append(SNRList[1])
            SNRROIResults["M3"].append(SNRList[2])
            SNRROIResults["M4"].append(SNRList[3])
            SNRROIResults["M5"].append(SNRList[4])
        
        CurrentRow = math.floor(i/Cols)
        CurrentCol = i%Cols


        SlicesToBeRejected=[]
        if seq in Helper.GetExcludedSlices(type).keys():
            SlicesToBeRejected=Helper.GetExcludedSlices(type)[seq]
        PlotROIS(ROIs,ROISize,RoiSizeHalf,BinaryMapSignal,Image,CurrentCol,CurrentRow,axs,i+1,SlicesToBeRejected)
        

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path,"..","Results",seq+"_SmoothMethod.png")

    #plt.savefig("Results/"+seq+"_SmoothMethod.png")
    plt.savefig(path)
    plt.close()



    return [sum(SNRAvg)/len(SNRAvg), SNRROIResults]