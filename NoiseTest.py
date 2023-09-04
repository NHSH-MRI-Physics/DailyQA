import DailyQA
import numpy as np
import matplotlib.pyplot as plt




def GetNoisePlot(Files,Coil):
    NoiseSTD = np.arange(25, 100, 25, dtype=int)
    Seq1Smooth = []
    Seq2Smooth = []
    Seq1Ness = []
    Seq2Ness = []

    Results = DailyQA.RunDailyQA(Files)

    Seq1Smooth.append(Results[0][0])
    Seq1Ness.append(Results[0][1]) 
    Seq2Smooth.append(Results[1][0])
    Seq2Ness.append(Results[1][1])
    
    for Noise in NoiseSTD:
        Results = DailyQA.RunDailyQA(Files,NoiseAmount=Noise)
        Seq1Smooth.append(Results[0][0])
        Seq1Ness.append(Results[0][1]) 
        Seq2Smooth.append(Results[1][0])
        Seq2Ness.append(Results[1][1])
        
    for i in range(len(Seq1Smooth)-1,-1,-1):
        Seq1Smooth[i] = Seq1Smooth[i]/Seq1Smooth[0]
        Seq1Ness[i] = Seq1Ness[i]/Seq1Ness[0]
        Seq2Smooth[i] = Seq2Smooth[i]/Seq2Smooth[0]
        Seq2Ness[i] = Seq2Ness[i]/Seq2Ness[0]

    NoiseSTD = np.concatenate(([0], NoiseSTD))
    plt.figure(figsize=(10,6))
    plt.title(Coil+" Noise Response Test")
    plt.plot(NoiseSTD,Seq1Smooth,label="Seq1 Smooth Method",marker="x")
    plt.plot(NoiseSTD,Seq1Ness,label="Seq1 Ness Avir Method",marker="x")
    plt.plot(NoiseSTD,Seq2Smooth,label="Seq2 Smooth Method",marker="x")
    plt.plot(NoiseSTD,Seq2Ness,label="Seq2 Ness Avir Method",marker="x")
    plt.grid()
    plt.legend()
    plt.savefig(Coil+"_NoiseTest.png")
    plt.close()

def GetNoiseStabilityPlot(file,Coil):
    Seq1Smooth = []
    Seq2Smooth = []
    Seq1Ness = []
    Seq2Ness = []
    NoiseSTD= [100]*5
    for Noise in NoiseSTD:
        Results = DailyQA.RunDailyQA(Files,NoiseAmount=Noise)
        Seq1Smooth.append(Results[0][0])
        Seq1Ness.append(Results[0][1]) 
        Seq2Smooth.append(Results[1][0])
        Seq2Ness.append(Results[1][1])
        
    for i in range(len(Seq1Smooth)-1,-1,-1):
        Seq1Smooth[i] = Seq1Smooth[i]/Seq1Smooth[0]
        Seq1Ness[i] = Seq1Ness[i]/Seq1Ness[0]
        Seq2Smooth[i] = Seq2Smooth[i]/Seq2Smooth[0]
        Seq2Ness[i] = Seq2Ness[i]/Seq2Ness[0]

    plt.figure(figsize=(10,6))
    plt.title(Coil+" Noise Stability Test")
    plt.plot(Seq1Smooth,label="Seq1 Smooth Method",marker="x")
    plt.plot(Seq1Ness,label="Seq1 Ness Avir Method",marker="x")
    plt.plot(Seq2Smooth,label="Seq2 Smooth Method",marker="x")
    plt.plot(Seq2Ness,label="Seq2 Ness Avir Method",marker="x")
    plt.grid()
    plt.legend()
    plt.savefig(Coil+"_NoiseStabilityTest.png")
    plt.close()

Files = "Data/DailyQA_Test_20230824_201946068" # Head Coil 
GetNoisePlot(Files,"Head Coil")
GetNoiseStabilityPlot(Files,"Head Coil")

Files = "Data/Daily_QA_Test_Body_20230824_211440042"
GetNoisePlot(Files,"Body Coil")
GetNoiseStabilityPlot(Files,"Body Coil")

Files = "Data/SpineFiltered" # Head Coil 
GetNoisePlot(Files,"Spine Coil")
GetNoiseStabilityPlot(Files,"Spine Coil")