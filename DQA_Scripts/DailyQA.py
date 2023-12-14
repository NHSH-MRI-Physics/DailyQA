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
    DICOMFiles = glob.glob( os.path.join( Files+"/*.dcm"))
    DICOMS={}
    PixelData={}

    if len(DICOMFiles) == 0:
        raise NameError("No DICOMS found!")

    SkipSeqTerms = ["Cal", "ORIG", "Loc"]
    ScannerName = "Unknown"
    for file in DICOMFiles:
        Accept=True
        LoadedDICOM = pydicom.read_file( file )
        ScannerName = LoadedDICOM[0x08,0x80].value

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
        ROIarg=None

        QAType = None

        if (CoilUsed == "Head 24"): 
            QAType="Head"
            KernalSize = 2
            Thresh= 500
            
            if Seq == "Ax T2 FSE head":
                ErorsionSteps=10
                #ROIarg=35
            if Seq == "Ax EPI-GRE head":
                ErorsionSteps=5
                #ROIarg=10

        elif (CoilUsed == "Body 48 1"):
            QAType="Body"
            KernalSize = 1

            if Seq == "Ax T2 SSFSE TE 90 Bot" or Seq == "Ax T2 SSFSE TE 90 Top":
                Thresh=500
                ErorsionSteps=5
            if Seq == "Ax EPI-GRE body Bot" or Seq == "Ax EPI-GRE body Top":
                Thresh=900
                ErorsionSteps=5



        elif (CoilUsed == "Spine 48 1" or CoilUsed == "Spine 48 2"):
            QAType="Spine"
            KernalSize = 1
            if Seq == "Ax T2 SSFSE TE 90 Bot" or Seq == "Ax T2 SSFSE TE 90 Top":
                Thresh=250
                ErorsionSteps=5
            if Seq == "Ax EPI-GRE body Bot" or Seq == "Ax EPI-GRE body Top":
                Thresh=900
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
        SNRSmooth,ROIResults = SmoothingMethod.SmoothedImageSubtraction(PixelData[Seq],KernalSize,Thresh=Thresh,ROISizeArg=ROIarg,Cent=Cent,width=width,seq=Seq,RejectedSlices=RejectedSlices,ScannerName=ScannerName)
        #SNRNessAiver = NessAiverMethod.NessAiver(PixelData[Seq],ErorsionSteps=ErorsionSteps,Thresh=Thresh, Seq=Seq,RejectedSlices=RejectedSlices)
        #Results.append( [SNRSmooth,SNRNessAiver,Seq])
        Results.append( [SNRSmooth,ROIResults,QAType,Seq])
        count+=1
    return Results