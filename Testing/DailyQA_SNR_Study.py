import sys
import os
current_module_dir = os.path.dirname(os.path.abspath(__file__))
DQAScriptsFolder = os.path.join(current_module_dir,"..","DQA_Scripts")
DQAScriptsFolder = os.path.abspath(DQAScriptsFolder)
if DQAScriptsFolder not in sys.path:
    sys.path.append(DQAScriptsFolder)
import DailyQA
import numpy as np
import Helper   
import glob
import shutil
import pandas as pd
import pydicom
import matplotlib.pyplot as plt
import math
from matplotlib.offsetbox import (AnnotationBbox, DrawingArea, OffsetImage,TextArea)
#import matplotlib
#matplotlib.use("TkAgg")
 
def GetData(path):
    Files = glob.glob(os.path.join(path, "*"))
    Files.sort(key=os.path.getmtime, reverse=False)
    Results = {}
    BaseFreq = None
    for file in Files:
        if "Analysis_Results" in file:
            continue

        QAresults = DailyQA.RunDailyQA(file)
        for result in QAresults:
            result.append( Helper.DidQAPassV2(result))

        DcmFiles = glob.glob(os.path.join(file, "*.dcm"))
        LoadedDICOM = pydicom.read_file( DcmFiles[0] )
        ImagingFreq = LoadedDICOM[0x18,0x84].value  

        Images = {}
        for Dicom in DcmFiles:
            Dcm = pydicom.read_file( Dicom )
            if Dcm.SeriesDescription not in Images:
                Images[Dcm.SeriesDescription] = []
            Images[Dcm.SeriesDescription].append(Dcm)

        seqs = list(Images.keys())
        for seq in seqs:
            Images[seq].sort(key=lambda x: x.SliceLocation)

        if "base" in file.lower():
            Results[0] = [QAresults,Images]
            BaseFreq = ImagingFreq
        else:
            
            ImagineFreqDiff = abs(int(round((ImagingFreq - BaseFreq)*1e6,0)))
            Results[ImagineFreqDiff] = [QAresults, Images]


    Keys = list(Results.keys())
    Keys.sort()

    AvgSNR = {}
    for key in Keys:
        for i in range(2):
            SingleResult = Results[key][0][i]
            Images = Results[key][1]
            seq = SingleResult[3]
            if seq not in AvgSNR:
                AvgSNR[seq] = [[],[],[],[]]
            
            MidImage = math.ceil(len(Images[seq])/2.0)
            AvgSNR[seq][0].append(key)
            AvgSNR[seq][1].append(SingleResult[0])
            AvgSNR[seq][2].append(SingleResult[4][0])
            AvgSNR[seq][3].append(Images[seq][MidImage].pixel_array)
    
    return AvgSNR

def MakePlot(x,y,passed,Title, XLabel, YLabel,Path,Images):
    # Create figure and axes objects explicitly
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.subplots_adjust(left=0.2, right=0.78, top=0.7, bottom=0.3) 
    
    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)
    xrange = xmax - xmin
    yrange = ymax - ymin

    StepX = xrange / 4
    StepY = yrange /1.7
    for idx in range(len(x)):
        zoom = 0.2
        if "EPI" in Title:
            zoom = 0.8
        
        vmin = np.percentile(Images[idx], 60)
        vmax = np.percentile(Images[idx], 100)
        im = OffsetImage(Images[idx], zoom=zoom, cmap='gray', norm=plt.Normalize(vmin=vmin, vmax=vmax))
        im.image.axes = ax

        if passed[idx] == True:
            Color = 'green'
        else:
            Color = 'red'

        border_props = dict(
            boxstyle='round,pad=0.2',
            facecolor=Color,
            edgecolor=Color,
            linewidth=2
        )

        if idx < 6:
            BoxPos = (xmin+StepX*(idx-1),ymin+yrange*1.2)
        else:
            BoxPos = (xmin+StepX*(5),ymin+yrange*1.2-StepY*(idx-6))
        boxalign = (0.5, 0)
        ab = AnnotationBbox(im, (x[idx], y[idx]),
                            xybox=BoxPos,
                            xycoords='data',
                            boxcoords="data",
                            pad=0.,
                            box_alignment=boxalign,
                            bboxprops=border_props,
                            arrowprops=dict(
                                arrowstyle='->',
                                connectionstyle='arc3,rad=0.0',  # Straight line
                                patchA=None,  # Important for bottom connection
                                shrinkB=0,  # Reduce gap between arrow and point
                                color=Color,
                            )
        )
        ax.add_artist(ab)
    
    # Use ax instead of plt for plotting
    ax.plot(x,y,linewidth = 2)
    ax.scatter(x[passed], y[passed], c='green', marker='x', linestyle='-', label='Pass',s=100)
    ax.scatter(x[~passed], y[~passed], c='red', marker='x', linestyle='-', label='Fail',s=100)
    ax.set_xlabel(XLabel, fontsize=12)
    ax.set_ylabel(YLabel, fontsize=12)
    ax.set_title(Title, fontsize=14,y=-0.3)
    ax.legend()
    ax.grid(True)
    
    # Save figure
    fig.savefig(os.path.join(Path, Title + ".png"),        bbox_inches='tight',
        pad_inches=0.2,  # Reduced padding
        dpi=300 )
    plt.close(fig)  # Clean up

'''
AvgSNR = GetData("Testing/DQA_DeltaFreq_Testing/FSE Testing")
OutputPath = "Testing/DQA_DeltaFreq_Testing"
seq = "Ax T2 FSE head"

passed = np.array(AvgSNR[seq][2])
x = np.array(AvgSNR[seq][0])
y = np.array(AvgSNR[seq][1])
Images = np.array(AvgSNR[seq][3])
title = "Avg SNR " + seq
xlabel = "Imaging Frequency Difference (Hz)"
ylabel = "Avg SNR"    
MakePlot(x, y, passed, title, xlabel, ylabel, OutputPath, Images)
'''

'''
AvgSNR = GetData("Testing/DQA_DeltaFreq_Testing/EPI Testing")
OutputPath = "Testing/DQA_DeltaFreq_Testing"
seq = "Ax EPI-GRE head"

passed = np.array(AvgSNR[seq][2])
x = np.array(AvgSNR[seq][0])
y = np.array(AvgSNR[seq][1])
Images = np.array(AvgSNR[seq][3])
title = "Avg SNR " + seq
xlabel = "Imaging Frequency Difference (Hz)"
ylabel = "Avg SNR"    
MakePlot(x, y, passed, title, xlabel, ylabel, OutputPath, Images)
'''

def RFArtefactTest(path):
    QAresults = DailyQA.RunDailyQA(path)
    for result in QAresults:
        result.append( Helper.DidQAPassV2(result))

RFArtefactTest("Testing/DQA_DeltaFreq_Testing/RF Testing/Test2")