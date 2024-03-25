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
    ImageIds={}

    if len(DICOMFiles) == 0:
        raise NameError("No DICOMS found!")

    SkipSeqTerms = ["Cal", "ORIG", "Loc"]
    #AcceptedProts = ["RH - DailyQA Head","RH - DailyQA Body","RH - DailyQA Spine"]
    ScannerName = "Unknown"

    for file in DICOMFiles:
        Accept=True
        LoadedDICOM = pydicom.read_file( file )
        ScannerName = LoadedDICOM[0x08,0x80].value

        #TODOD add this back in when im sure what the prots are called on the scanner
        #if (LoadedDICOM[0x18,0x1030].value not in AcceptedProts):
        #    raise ValueError("Unknown protocol selected: " + LoadedDICOM[0x18,0x1030].value)

        for term in SkipSeqTerms:
            if term in LoadedDICOM.SeriesDescription:
                Accept=False
        if Accept==False:
            continue

        if LoadedDICOM.SeriesDescription not in DICOMS:
            DICOMS[LoadedDICOM.SeriesDescription] = []
            PixelData[LoadedDICOM.SeriesDescription] = []
            ImageIds[LoadedDICOM.SeriesDescription] = []

        #Sometimes the images are pushed more than once, this only adds each image once...
        ID = LoadedDICOM[0x20,0x13].value
        if ID in ImageIds[LoadedDICOM.SeriesDescription]:
            continue
        else:
            ImageIds[LoadedDICOM.SeriesDescription].append(ID)

        DICOMS[LoadedDICOM.SeriesDescription].append(LoadedDICOM) 

    Results = []
    #ReceiveCoilName
    count=0
    NumberOfFilesToProcess=0
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

        if (CoilUsed == "Head 24" or CoilUsed == "19HN"): 
            QAType="Head"
            KernalSize = 2
            Thresh= 0.2
            
            if Seq == "Ax T2 FSE head":
                ErorsionSteps=10
                #ROIarg=35
            elif Seq == "Ax EPI-GRE head":
                ErorsionSteps=5
                #ROIarg=10
            else:
                raise ValueError("Unknown sequence selected: " + Seq)

        elif (CoilUsed == "Body 48 1"  or CoilUsed == "16AA+40PA"):
            QAType="Body"
            KernalSize = 1

            if Seq == "Ax T2 SSFSE TE 90 Bot" or Seq == "Ax T2 SSFSE TE 90 Top":
                Thresh=0.2
                ErorsionSteps=5
            elif Seq == "Ax EPI-GRE body Bot" or Seq == "Ax EPI-GRE body Top":
                Thresh=0.2
                ErorsionSteps=5
            else:
                raise ValueError("Unknown sequence selected: " + Seq)


        elif (CoilUsed == "Spine 48 1" or CoilUsed == "Spine 48 2" or CoilUsed == "40PA"):
            QAType="Spine"
            KernalSize = 1
            if Seq == "Ax T2 SSFSE TE 90 Bot" or Seq == "Ax T2 SSFSE TE 90 Top":
                Thresh=0.1
                ErorsionSteps=5
            elif Seq == "Ax EPI-GRE body Bot" or Seq == "Ax EPI-GRE body Top":
                Thresh=0.1
                ErorsionSteps=5
            else:
                raise ValueError("Unknown sequence selected: " + Seq)

        else:
            raise ValueError("Unknown coil selected: " + CoilUsed)
        
        #moved this to here so the sequences are checked prior to getting loaded (if any issues this may need to be moved back)
        DICOMS[Seq].sort(key=lambda x: x.SliceLocation, reverse=False) 
        img_shape = list(DICOMS[Seq][0].pixel_array.shape) 
        img_shape.append(len(DICOMS[Seq]))
        PixelData[Seq] = np.zeros(img_shape)
        for i, s in enumerate(DICOMS[Seq]):
            img2d = s.pixel_array
            PixelData[Seq][:, :, i] = img2d
    
        if OverrideThreshBinaryMap!=None:
            Thresh=OverrideThreshBinaryMap
        
        if (AddInSlices!=None):
            for Slice in AddInSlices:
                RejectedSlices.remove(Slice)

        if NoiseAmount != None:
            PixelData[Seq] = Helper.AddNoise(PixelData[Seq],NoiseAmount)
        SNRSmooth,ROIResults = SmoothingMethod.SmoothedImageSubtraction(PixelData[Seq],KernalSize,Thresh=Thresh,ROISizeArg=ROIarg,Cent=Cent,width=width,seq=Seq,RejectedSlices=RejectedSlices,ScannerName=ScannerName,type=QAType)
        #SNRNessAiver = NessAiverMethod.NessAiver(PixelData[Seq],ErorsionSteps=ErorsionSteps,Thresh=Thresh, Seq=Seq,RejectedSlices=RejectedSlices)
        #Results.append( [SNRSmooth,SNRNessAiver,Seq])
        Results.append( [SNRSmooth,ROIResults,QAType,Seq])
        count+=1

        SlicesToBeRejected=[]
        if Seq in Helper.GetExcludedSlices(QAType).keys():
            SlicesToBeRejected=Helper.GetExcludedSlices(QAType)[Seq]

        NumberOfFilesToProcess+=((PixelData[Seq].shape[2]) - len(SlicesToBeRejected))
    np.save("temp.npy", NumberOfFilesToProcess)

    return Results

def GetManHoursSaved():
    TimePerImage = 0.028
    NumberOfFilesLastRun = int(np.load("temp.npy"))
    #os.remove("temp.npy") TODO: Fix this bit it seems to be funny on Mac...

    if os.path.isfile("TotalTime.npy") == False:
        TimeSaved = 0.0
        np.save("TotalTime.npy",TimeSaved)

    TotalTimeSaved = float(np.load("TotalTime.npy"))
    TotalTimeSaved+=(NumberOfFilesLastRun*TimePerImage)
    np.save("TotalTime.npy",TotalTimeSaved)
    return TotalTimeSaved
    
