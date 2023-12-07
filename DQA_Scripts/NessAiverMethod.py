#From Comparison of SNR Assessment Techniques for Routine Multi-Element RF Coil QC Testing
import pydicom
import glob
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import cv2 as cv
import matplotlib.patches as patches
from scipy import ndimage
import math
import Helper

def NessAiver(ImageData,ErorsionSteps = 10,Thresh=None,Seq = None,RejectedSlices=[]):
    SNRAvg=[]

    fig,axs,Cols = Helper.Setupplots(ImageData,Seq)

    if ImageData.shape[2] == len(RejectedSlices):
        raise ValueError ("all sices rejected, reduce rejecton threshold!")
    
    for i in range(ImageData.shape[2]):
        
        Image = ImageData[:,:,i]
        if i not in RejectedSlices:
            if Thresh==None:
                hist, bin_edges = np.histogram(Image,bins=200)
                peaks, _ = find_peaks(hist, height=1000,distance=100)
                Thresh = np.average(bin_edges[peaks])


            BinaryMapSignal = np.copy(Image)
            BinaryMapAir = np.copy(Image)
            High = np.where(BinaryMapSignal>=Thresh)
            Low = np.where(BinaryMapSignal<Thresh)
            BinaryMapSignal[High]=1
            BinaryMapSignal[Low]=0
            BinaryMapSignal = ndimage.binary_fill_holes(BinaryMapSignal)

            BinaryMapAir[:,:]=1
            BinaryMapAir=BinaryMapAir-ndimage.binary_dilation(BinaryMapSignal,iterations=ErorsionSteps)
            BinaryMapSignal=ndimage.binary_erosion(BinaryMapSignal,iterations=ErorsionSteps)*1.0

            

            AirIdx = np.where(BinaryMapAir==1)
            SignalIDx = np.where(BinaryMapSignal==1)
            MeanAirSignal = np.mean(Image[AirIdx])
            MeanSignal = np.mean(Image[SignalIDx])
            SNRAvg.append(MeanSignal/MeanAirSignal)

        row = math.floor(i/Cols)
        col = i%Cols

        axs[row,col].set_axis_on()
        axs[row,col].axis('off')
        axs[row,col].imshow(Image,cmap="Greys_r")
        axs[row,col].set_title("Slice Num: " + str(i+1), fontsize=20)
        SegImage = np.copy(Image)
        SegImage*=0
        if i not in RejectedSlices:
            SegImage[AirIdx]=-1
            SegImage[SignalIDx]=1
            axs[row,col].imshow(SegImage,alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(Seq+"_NessAiverMethod.png")
    plt.close()

    return sum(SNRAvg)/len(SNRAvg)
    