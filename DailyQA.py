import pydicom
import glob
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

Files = "Data\DailyQA_Test_20230824_201946068"

DICOMFiles = glob.glob(Files+"\*")
DICOMS={}
PixelData={}

SkipSeqTerms = ["Cal", "ORIG"]
for file in DICOMFiles:
    Accept=True
    LoadedDICOM = pydicom.read_file( file )
    for term in SkipSeqTerms:
        if term in LoadedDICOM.SeriesDescription:
            Accept=False
    if Accept==False:
        continue

    if LoadedDICOM.SeriesDescription not in DICOMS:
        DICOMS[LoadedDICOM.SeriesDescription] = []
        PixelData[LoadedDICOM.SeriesDescription] = []
    DICOMS[LoadedDICOM.SeriesDescription].append(LoadedDICOM) 

for Seq in DICOMS.keys():
    DICOMS[Seq].sort(key=lambda x: x.SliceLocation, reverse=False) # sort them by slice 
    img_shape = list(DICOMS[Seq][0].pixel_array.shape) 
    img_shape.append(len(DICOMS[Seq]))
    PixelData[Seq] = np.zeros(img_shape)
    for i, s in enumerate(DICOMS[Seq]):
        img2d = s.pixel_array
        PixelData[Seq][:, :, i] = img2d


#ReceiveCoilName
for seq in DICOMS:
    CoilUsed = DICOMS[seq][0]["ReceiveCoilName"].value


    if (CoilUsed == "Head 24"): #Use all slices
        hist, bin_edges = np.histogram(PixelData[Seq].flatten(),bins=200)
        peaks, _ = find_peaks(hist, height=1000,distance=100)
        Thresh = np.average(bin_edges[peaks])
        