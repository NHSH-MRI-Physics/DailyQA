import pydicom
import glob
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import cv2 as cv
import os
import scipy.ndimage

def AddNoise(Image,sigma):
    NoiseImage = np.copy(Image)
    noiseReal = np.random.normal(0,sigma,[Image.shape[0],Image.shape[1]])
    noiseImag = np.random.normal(0,sigma,[Image.shape[0],Image.shape[1]])
    NoiseImage[:,:] = np.sqrt( (NoiseImage[:,:] + noiseReal)**2 + noiseImag*noiseImag)
    return np.abs(NoiseImage - Image)

def GetSNRHeadMask(img):
    t = 500
    binary_mask = img > t
    SignalMask = scipy.ndimage.binary_erosion(binary_mask,iterations=10)
 
    binary_mask = img < t
    NoiseMask = scipy.ndimage.binary_erosion(binary_mask,iterations=10)

    return SignalMask,NoiseMask
    

def MakeLowSNRData(DataPath,FilePath,type,signaldrop,noiseincrease):
    DICOMFiles = glob.glob( os.path.join( DataPath+"/*.dcm"))

    if not os.path.exists(FilePath):
        os.makedirs(FilePath)

    NewSNRAvg = []
    OldSNRAvg = []
    for file in DICOMFiles:
        LoadedDICOM = pydicom.read_file( file )
        img = LoadedDICOM.pixel_array

        if type=="head":
            SignalMask, NoiseMask = GetSNRHeadMask(img)
    
        SNRBefore = np.mean(img[SignalMask])/np.std(img[NoiseMask])
        OldSNRAvg.append(SNRBefore)

        fig, (ax1, ax2) = plt.subplots(1, 2)
        imgmax= np.max(img)
        ax1.imshow(img,cmap="Greys_r",vmin=0, vmax=imgmax)

        img = img.astype(float)
        NoiseImage = AddNoise(img,noiseincrease)
        img=img*signaldrop
        img += NoiseImage
        img = img.astype(int)

        ax2.imshow(img,cmap="Greys_r",vmin=0, vmax=imgmax)
        plt.show()

        NewSNR = np.mean(img[SignalMask])/np.std(img[NoiseMask])
        NewSNRAvg.append(NewSNR)

        LoadedDICOM.PixelData = img
        LoadedDICOM.save_as( os.path.join(FilePath, os.path.split(file)[-1]))
    
    print("SNR Change: " + str((sum(NewSNRAvg)/len(NewSNRAvg)) / (sum(OldSNRAvg)/len(OldSNRAvg))))


MakeLowSNRData("/Users/john/Documents/DailyQA/Data/DQA_Head_1","/Users/john/Documents/DailyQA/Testing/LowSNR_Data/25%SNR_Head","head",0.7,165)