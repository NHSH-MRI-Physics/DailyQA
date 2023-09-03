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
    for roi in ROIS:
        rect = patches.Rectangle((roi[0]-RoiSizeHalf, roi[1]-RoiSizeHalf), ROISize, ROISize, linewidth=1, edgecolor='r', facecolor='none')
        axs[row,col].add_patch(rect)

def SmoothedImageSubtraction(ImageData,KernalSize,ROISize= 36,Thresh=None, width = None, Cent = None,seq=None, RejectedSlices = []):

    fig,axs,Cols = Helper.Setupplots(ImageData,seq)

    if ImageData.shape[2] == len(RejectedSlices):
        raise ValueError ("all sices rejected, reduce rejecton threshold!")

    SNRAvg=[]
    for i in range(ImageData.shape[2]):
        Image = ImageData[:,:,i]
        ROIs = []
        RoiSizeHalf=None
        BinaryMapSignal=None
        if i not in RejectedSlices:
            RoiSizeHalf = int(round(ROISize/2.0,0))

            MatrixSize = (KernalSize*2+1)**2
            kernel = np.ones((MatrixSize,MatrixSize),np.float32)/(MatrixSize*MatrixSize)
            Smoothed = cv.filter2D(Image,-1,kernel)
            Difference = Image - Smoothed

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

            #print(cent_x,cent_y,widthX,widthY)

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

        
        CurrentRow = math.floor(i/Cols)
        CurrentCol = i%Cols
        PlotROIS(ROIs,ROISize,RoiSizeHalf,BinaryMapSignal,Image,CurrentCol,CurrentRow,axs,i+1)
        

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(seq+"_SmoothMethod.png")
    plt.close()



    return sum(SNRAvg)/len(SNRAvg)