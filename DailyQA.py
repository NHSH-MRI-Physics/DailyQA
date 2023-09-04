import pydicom
import glob
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import cv2 as cv
import SmoothingMethod
import Helper 
import NessAiverMethod
import os

def RunDailyQA(Files,NoiseAmount=None,OverrideThreshBinaryMap=None,AddInSlices=None,RunSeq=None,ThreshRejectionOveride=None):
    DICOMFiles = glob.glob( os.path.join( Files+"/*"))
    DICOMS={}
    PixelData={}

    if len(DICOMFiles) == 0:
        raise NameError("No DICOMS found!")

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

    Results = []
    #ReceiveCoilName
    count=0
    SeqToRun = DICOMS.keys()
    if RunSeq != None:
        SeqToRun = [RunSeq]
    for Seq in SeqToRun:
        CoilUsed = DICOMS[Seq][0]["ReceiveCoilName"].value
        Cent= None
        width = None
        RejectedSlices=[]

        if (CoilUsed == "Head 24"): #Use all slices
            KernalSize = 2
            Thresh=500
            if Seq == "Ax T2 FSE head":
                ROISize=36
                ErorsionSteps=10
            if Seq == "Ax EPI-GRE head":
                ROISize=10
                ErorsionSteps=5
        elif (CoilUsed == "Body 48 1"):
            KernalSize = 1
            PixelData[Seq] = PixelData[Seq][:, :, 15:-15] # This will be done on the scanner
            
            '''
            if(ThreshRejectionOveride!=None):
                RejectedSlices = Helper.GetRejectedSlicesSplit(PixelData[Seq],Thresh=ThreshRejectionOveride[count])
            else:
                RejectedSlices = Helper.GetRejectedSlicesSplit(PixelData[Seq])
            '''
            RejectedSlices = Helper.GetRejectedSlicesEitherSide(PixelData[Seq])

            Thresh=500
            ROISize=20
            ErorsionSteps=5
        elif (CoilUsed == "Spine 48 1"):
            KernalSize = 1

            if (Seq == "Ax EPI-GRE body"):
                PixelData[Seq] = PixelData[Seq][:, :, 15:-15] # This will be done on the scanner
            if (Seq == "Ax T2 SSFSE TE 90 BH"):
                PixelData[Seq] = PixelData[Seq][:, :, 10:-10] # This will be done on the scanner
            
            '''
            if(ThreshRejectionOveride!=None):
                RejectedSlices = Helper.GetRejectedSlicesSplit(PixelData[Seq],Thresh=ThreshRejectionOveride[count])
            else:
                RejectedSlices = Helper.GetRejectedSlicesSplit(PixelData[Seq])
            '''
            RejectedSlices = Helper.GetRejectedSlicesEitherSide(PixelData[Seq])

            Thresh=250
            ROISize=20
            ErorsionSteps=5
        else:
            raise ValueError("Unknown coil selected: " + CoilUsed)
        
        if OverrideThreshBinaryMap!=None:
            Thresh=OverrideThreshBinaryMap
        
        if (AddInSlices!=None):
            for Slice in AddInSlices:
                RejectedSlices.remove(Slice)

        if NoiseAmount != None:
            PixelData[Seq] = Helper.AddNoise(PixelData[Seq],NoiseAmount)
        SNRSmooth = SmoothingMethod.SmoothedImageSubtraction(PixelData[Seq],KernalSize,Thresh=Thresh,ROISize=ROISize,Cent=Cent,width=width,seq=Seq,RejectedSlices=RejectedSlices)
        SNRNessAiver = NessAiverMethod.NessAiver(PixelData[Seq],ErorsionSteps=ErorsionSteps,Thresh=Thresh, Seq=Seq,RejectedSlices=RejectedSlices)
        Results.append( [SNRSmooth,SNRNessAiver,Seq])
        count+=1
    return Results