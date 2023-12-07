import pydicom
import glob
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import cv2 as cv
import os

def MakeLowSNRData(DataPath,FilePath,signaldrop,noiseincrease):
    DICOMFiles = glob.glob( os.path.join( DataPath+"/*.dcm"))

    if not os.path.exists(FilePath):
        os.makedirs(FilePath)

    for file in DICOMFiles:
        LoadedDICOM = pydicom.read_file( file )
        img = LoadedDICOM.pixel_array
        LoadedDICOM.PixelData = img
        LoadedDICOM.save_as( os.path.join(FilePath, os.path.split(file)[-1]))
    
MakeLowSNRData("/Users/john/Documents/DailyQA/Data/DQA_Head_1","/Users/john/Documents/DailyQA/Testing/LowSNR_Data/25%SNR_Head",0.5,2)