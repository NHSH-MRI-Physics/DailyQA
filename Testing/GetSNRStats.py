import sys
import os 
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'DQA_Scripts'))
import DailyQA
import numpy as np
import Helper
import glob
import matplotlib.pyplot as plt
#os.chdir('..')


def SortData(Datas):
    DataToPlot ={}
    OverallDataToPlot = {}
    FileTracker=[]
    for data in Datas:
        FileTracker.append(data)
        #print(data)
        Results = DailyQA.RunDailyQA(data)          

        '''
        if (Results[0][-1] == "Ax T2 FSE head"):
            print(data+ " " + str(Results[0][1]["M5"][0]))
        if (Results[1][-1] == "Ax T2 FSE head"):
            print(data+ " " + str(Results[1][1]["M5"][0]))
        print("     ")
        '''

        for result in Results: #result[0] = OverallSNR      result[1] = ROI SNR         result[3] = Seq
            seq = result[-1]
            if seq not in DataToPlot:
                DataToPlot[seq] = result[1]
                OverallDataToPlot[seq]=[result[0]]
                ROIs = list(result[1].keys())
                for roi in ROIs:
                    for slice in range(len(result[1][roi])):
                        DataToPlot[seq][roi][slice] = [result[1][roi][slice]]
            else:
                OverallDataToPlot[seq].append(result[0])
                ROIs = list(result[1].keys())
                for roi in ROIs:
                    for slice in range(len(result[1][roi])):
                        DataToPlot[seq][roi][slice].append(result[1][roi][slice])
    return [DataToPlot,OverallDataToPlot],FileTracker

def AnalyseData(Data,FileTracker,type):
    ConfLevel = 1.96 #2.576

    DataToPlot = Data[0]
    OverallDataToPlot = Data[1]

    Sequences = DataToPlot.keys()
    for sequence in Sequences:
        Failures=[]
        fig, axs = plt.subplots(7)
        fig.set_size_inches(9, 21)
        fig.suptitle(type + " DQA Stats " + sequence,y=0.99)
        ROIs = list(DataToPlot[sequence].keys())

        #Per ROI Analysis
        for count, roi in enumerate(ROIs):
            NumberOfSlices = len(DataToPlot[sequence][roi])
            for slice in range(NumberOfSlices):
                Base,STD = Helper.GetBaselineROI(type,slice,roi,sequence)
                Lower = Base - STD*ConfLevel
                
                Base,STD = Helper.GetBaselineROI(type,slice,roi,sequence)
                for filecount, point in enumerate(DataToPlot[sequence][roi][slice]):
                    if point >= Lower:
                        axs[count].plot( [slice+1],[point],linestyle="",marker=".",color="blue")
                    else:
                        axs[count].plot( [slice+1],[point],linestyle="",marker=".",color="red")
                        Failures.append(FileTracker[filecount])
                #Base=1.0
                axs[count].plot([slice+1-0.1,slice+1,slice+1+0.1],[Base,Base,Base],color='green',marker='',linewidth=0.5)
                axs[count].plot([slice+1-0.1,slice+1,slice+1+0.1],[Lower,Lower,Lower],color='red',marker='',linewidth=0.5)
                #print("Slice: " +str(slice) + "     roi: " + str(roi) + "     sequence: " + sequence + "     Base: " + str(Base) +"     STD " +str(STD) )

            axs[count].set_xlabel("Slice Number")
            axs[count].set_ylabel("SNR")
            axs[count].set_title(roi)
            axs[count].grid()



        #Average Per Slice
        NumberOfSlices = len(DataToPlot[sequence]["M1"])
        xvalues = []
        count+=1
        for slice in range(NumberOfSlices):
            Base,STD = Helper.GetBaselineSlice(type,slice,sequence)
            Lower = Base - STD*ConfLevel

            Average = np.array([0]*len(DataToPlot[sequence]["M1"][0]))
            xvalues.append(slice+1)
            for roi in ROIs:
                Average = Average+np.array(DataToPlot[sequence][roi][slice])
            Average = Average/len(ROIs)

            for value in Average:
                if value >=Lower:
                    axs[count].plot( [slice+1],[value],linestyle="",marker=".",color="blue")
                else:
                    axs[count].plot( [slice+1],[value],linestyle="",marker=".",color="red")
            axs[count].plot([slice+1-0.1,slice+1,slice+1+0.1],[Base,Base,Base],color='green',marker='',linewidth=0.5)
            axs[count].plot([slice+1-0.1,slice+1,slice+1+0.1],[Lower,Lower,Lower],color='red',marker='',linewidth=0.5)
            
        axs[count].set_xlabel("Slice Number")
        axs[count].set_ylabel("Average SNR")
        axs[count].set_title("Average Per Slice")
        axs[count].grid()
        #print( type + " Seq: " + sequence + " False Neg Rate: " + str(round(float(len(set(Failures))/float(len(DataToPlot[sequence][roi][slice]))*100.0),1)) + "%" )



        count+=1
        #Average over all slices
        Base,STD = Helper.GetBaselineOverall(type,sequence)
        Lower = Base - STD*ConfLevel

        for value in OverallDataToPlot[sequence]:
                if value >=Lower:
                    axs[count].plot( [0],[value],linestyle="",marker=".",color="blue")
                else:
                    axs[count].plot( [slice+1],[value],linestyle="",marker=".",color="red")
        axs[count].plot([-0.1,0,0.1],[Base,Base,Base],color='green',marker='',linewidth=0.5)
        axs[count].plot([-0.1,0,0.1],[Lower,Lower,Lower],color='red',marker='',linewidth=0.5)
        axs[count].set_xlim(-2.5,2.5)
        axs[count].set_ylabel("Average SNR")
        axs[count].set_title("Average SNR over all slices")
        axs[count].grid()
        axs[count].set_xticks([])
        

        plt.tight_layout()
        plt.savefig("Testing/SNRStats/"+type + "_"+sequence+"_AnalysisResults.png")

HeadSNRFilesSources=[]
HeadSNRFilesSources = [x[0] for x in os.walk("BaselineData/Head/")][1:]
HeadArchives = [x[0] for x in os.walk("Archive")][1:]
for folder in HeadArchives:
    if "Head" in folder:
        HeadSNRFilesSources.append(folder)

#Data,FileTracker = SortData(HeadSNRFilesSources)
#np.save("Testing/SNRStats/HeadDataFile.npy", Data)
#np.save("Testing/SNRStats/FileTracker.npy", FileTracker)
Data = np.load("Testing/SNRStats/HeadDataFile.npy",allow_pickle=True)
FileTracker = np.load("Testing/SNRStats/FileTracker.npy",allow_pickle=True)
AnalyseData(Data,FileTracker,"Head")