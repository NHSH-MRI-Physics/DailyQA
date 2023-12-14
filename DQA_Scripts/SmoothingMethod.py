import pydicom
import glob
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import cv2 as cv
import matplotlib.patches as patches
import math
import Helper

def PlotROIS(ROIS,ROISize,RoiSizeHalf,BinaryMap,Image,col,row,axs,sliceNum):
    axs[row,col].set_axis_on()
    axs[row,col].axis('off')
    axs[row,col].imshow(Image,cmap='Greys_r')
    axs[row,col].set_title("Slice Num: " + str(sliceNum), fontsize=20)
    count=1
    for roi in ROIS:
        rect = patches.Rectangle((roi[0]-RoiSizeHalf, roi[1]-RoiSizeHalf), ROISize, ROISize, linewidth=1, edgecolor='r', facecolor='none')
        axs[row,col].add_patch(rect)
        axs[row,col].text(roi[0], roi[1], str(count), style='italic', ha='center', va='center',fontsize=9,color='red')
        count+=1

def SmoothedImageSubtraction(ImageData,KernalSize,ROISizeArg=None,Thresh=None, width = None, Cent = None,seq=None, RejectedSlices = [],ScannerName = None):

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
        ROIs = []
        RoiSizeHalf=None
        BinaryMapSignal=None
        if i not in RejectedSlices:
            MatrixSize = (KernalSize*2+1)**2
            kernel = np.ones((MatrixSize,MatrixSize),np.float32)/(MatrixSize*MatrixSize)
            Smoothed = cv.filter2D(Image,-1,kernel)
            Difference = Image - Smoothed

            #plt.clf()
            #plt.imshow(Image)
            #plt.show()
            BinaryMapSignal = np.copy(Image)
            High = np.where(BinaryMapSignal>=Thresh)
            Low = np.where(BinaryMapSignal<Thresh)
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
        PlotROIS(ROIs,ROISize,RoiSizeHalf,BinaryMapSignal,Image,CurrentCol,CurrentRow,axs,i+1)
        

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("Results/"+seq+"_SmoothMethod.png")
    plt.close()



    return [sum(SNRAvg)/len(SNRAvg), SNRROIResults]