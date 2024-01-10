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
        print(data)
        Results = DailyQA.RunDailyQA(data) #Just dont reject slices here this is done below

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

def AnalyseData(Data,FileTracker,type,Normalise=False,ExcludeSlicesOption=True):

    files = glob.glob("Testing/SNRStats/*.png")
    for file in files:
        os.remove(file)

    files = glob.glob("Testing/SNRStats/*.txt")
    for file in files:
        os.remove(file)

    DataToPlot = Data[0]
    OverallDataToPlot = Data[1]
    Sequences = DataToPlot.keys()

    SNRThreshold = Helper.GetThresholds(type)
    ExcludedSlices = Helper.GetExcludedSlices(type)

    for sequence in Sequences:        
        fig, axs = plt.subplots(7)
        fig.set_size_inches(9, 21)
        fig.suptitle(type + " DQA Stats " + sequence,y=0.99)
        ROIs = list(DataToPlot[sequence].keys())
        f=open("Testing/SNRStats/"+sequence+"_Failures.txt",'w')
        #Per ROI Analysis
        f.write("\n\n\n\nSequence : " + str(sequence)+"\n")
        f.write("####  Per ROI Failures ####\n")
        f.write("File     Metric     Slice     ROI\n")
        Failures=[]
        for count, roi in enumerate(ROIs):
            NumberOfSlices = len(DataToPlot[sequence][roi])
            for slice in range(NumberOfSlices):
                if ExcludeSlicesOption:
                    if slice in ExcludedSlices[sequence]:
                        continue

                Base,STD = Helper.GetBaselineROI(type,slice,roi,sequence)
                Lower = SNRThreshold[sequence]
                if Normalise==False:
                    Lower = Base*SNRThreshold[sequence]
                Base,STD = Helper.GetBaselineROI(type,slice,roi,sequence)
                for filecount, value in enumerate(DataToPlot[sequence][roi][slice]):
                    if Normalise:
                        value /=Base
                    if value >= Lower:
                        axs[count].plot( [slice+1],[value],linestyle="",marker=".",color="blue")
                    else:
                        axs[count].plot( [slice+1],[value],linestyle="",marker=".",color="red")
                        f.write(FileTracker[filecount]+"     " + str(value) + "     "+str(slice+1)+"     "+ roi+"\n")
                        Failures.append(FileTracker[filecount])
                
                if Normalise==False:
                    axs[count].plot([slice+1-0.1,slice+1,slice+1+0.1],[Base,Base,Base],color='green',marker='',linewidth=0.5)
                axs[count].plot([slice+1-0.1,slice+1,slice+1+0.1],[Lower,Lower,Lower],color='red',marker='',linewidth=0.5)
                #print("Slice: " +str(slice) + "     roi: " + str(roi) + "     sequence: " + sequence + "     Base: " + str(Base) +"     STD " +str(STD) )

            axs[count].set_xlabel("Slice Number")
            if (Normalise):
                axs[count].set_ylabel("Realtive SNR")
            else:
                axs[count].set_ylabel("SNR")
            axs[count].set_title(roi)
            axs[count].grid()
        f.write("\nUnique Fails\n")
        for fail in set(Failures):
            f.write(fail + "\n")
        f.write(str(len(set(Failures)))+"/"+str(len(DataToPlot[sequence][roi][slice]))+"   "+ str(round( (len(set(Failures))/len(DataToPlot[sequence][roi][slice]))*100.0,1)) +"%\n\n")
        Failures=[]
        

        #Average Per Slice
        f.write("\n####  Per Slice Failures ####\n")
        f.write("File     Metric     Slice\n")
        NumberOfSlices = len(DataToPlot[sequence]["M1"])
        xvalues = []
        count+=1
        for slice in range(NumberOfSlices):
            if ExcludeSlicesOption:
                if slice in ExcludedSlices[sequence]:
                    continue

            Base,STD = Helper.GetBaselineSlice(type,slice,sequence)
            Lower = SNRThreshold[sequence]
            if Normalise==False:
                Lower = Base*SNRThreshold[sequence]
            Average = np.array([0]*len(DataToPlot[sequence]["M1"][0]))
            xvalues.append(slice+1)
            for roi in ROIs:
                Average = Average+np.array(DataToPlot[sequence][roi][slice])
            Average = Average/len(ROIs)
            
            for filecount,value in enumerate(Average):
                if Normalise:
                    value/=Base
                if value >=Lower:
                    axs[count].plot( [slice+1],[value],linestyle="",marker=".",color="blue")
                else:
                    axs[count].plot( [slice+1],[value],linestyle="",marker=".",color="red")
                    f.write(FileTracker[filecount]+"     " + str(value) + "     "+str(slice+1)+"\n")
                    Failures.append(FileTracker[filecount])
            if Normalise==False:
                axs[count].plot([slice+1-0.1,slice+1,slice+1+0.1],[Base,Base,Base],color='green',marker='',linewidth=0.5)
            axs[count].plot([slice+1-0.1,slice+1,slice+1+0.1],[Lower,Lower,Lower],color='red',marker='',linewidth=0.5)
            
        axs[count].set_xlabel("Slice Number")
        if (Normalise):
            axs[count].set_ylabel("Average Realtive SNR")
        else:
            axs[count].set_ylabel("Average SNR")
        axs[count].set_title("Average Per Slice")
        axs[count].grid()
        #print( type + " Seq: " + sequence + " False Neg Rate: " + str(round(float(len(set(Failures))/float(len(DataToPlot[sequence][roi][slice]))*100.0),1)) + "%" )
        f.write("\nUnique Fails\n")
        for fail in set(Failures):
            f.write(fail + "\n")
        f.write(str(len(set(Failures)))+"/"+str(len(Average))+"   "+ str(round( (len(set(Failures))/len(Average))*100.0,1)) +"%\n\n")
        Failures=[]


        count+=1
        #Average over all slices
        f.write("\n####  Average over all slices Failures ####\n")
        f.write("File     Metric     Slice\n")
        Base,STD = Helper.GetBaselineOverall(type,sequence)
        Lower = SNRThreshold[sequence]
        if Normalise==False:
            Lower = Base*SNRThreshold[sequence]

        for value in OverallDataToPlot[sequence]:
                if Normalise:
                    value/=Base
                if value >=Lower:
                    axs[count].plot( [0],[value],linestyle="",marker=".",color="blue")
                else:
                    axs[count].plot( [0],[value],linestyle="",marker=".",color="red")
                    f.write(FileTracker[filecount]+"     " + str(value) + "     "+str(slice+1)+"\n")
                    Failures.append(FileTracker[filecount])
        if Normalise==False:
            axs[count].plot([-0.1,0,0.1],[Base,Base,Base],color='green',marker='',linewidth=0.5)
        axs[count].plot([-0.1,0,0.1],[Lower,Lower,Lower],color='red',marker='',linewidth=0.5)
        axs[count].set_xlim(-2.5,2.5)
        if (Normalise):
            axs[count].set_ylabel("Average Realtive SNR")
        else:
            axs[count].set_ylabel("Average SNR")
        axs[count].set_title("Average SNR over all slices (no exclusions)")
        axs[count].grid()
        axs[count].set_xticks([])
        

        plt.tight_layout()
        plt.savefig("Testing/SNRStats/"+type + "_"+sequence+"_AnalysisResults.png")
        f.write("\nUnique Fails\n")
        for fail in set(Failures):
            f.write(fail + "\n")
        f.write(str(len(set(Failures)))+"/"+str(len(OverallDataToPlot[sequence]))+"   "+ str(round( (len(set(Failures))/len(OverallDataToPlot[sequence]))*100.0,1)) +"%")
        Failures=[]
    f.close()

'''
HeadSNRFilesSources=[]
HeadSNRFilesSources = [x[0] for x in os.walk("BaselineData/Head/")][1:]
HeadArchives = [x[0] for x in os.walk("Archive")][1:]
for folder in HeadArchives:
    if "Head" in folder:
        HeadSNRFilesSources.append(folder)
Data,FileTracker = SortData(HeadSNRFilesSources)
np.save("Testing/SNRStats/HeadDataFile.npy", Data)
np.save("Testing/SNRStats/HeadFileTracker.npy", FileTracker)

Data = np.load("Testing/SNRStats/HeadDataFile.npy",allow_pickle=True)
FileTracker = np.load("Testing/SNRStats/HeadFileTracker.npy",allow_pickle=True)
AnalyseData(Data,FileTracker,"head",Normalise=True,ExcludeSlicesOption=False)
'''

'''
BodySNRFilesSources=[]
BodySNRFilesSources = [x[0] for x in os.walk("BaselineData/Body/")][1:]
BodyArchives = [x[0] for x in os.walk("Archive")][1:]
for folder in BodyArchives:
    if "Body" in folder:
        BodySNRFilesSources.append(folder)
Data,FileTracker = SortData(BodySNRFilesSources)
np.save("Testing/SNRStats/BodyDataFile.npy", Data)
np.save("Testing/SNRStats/BodyFileTracker.npy", FileTracker)

Data = np.load("Testing/SNRStats/BodyDataFile.npy",allow_pickle=True)
FileTracker = np.load("Testing/SNRStats/BodyFileTracker.npy",allow_pickle=True)
AnalyseData(Data,FileTracker,"body",Normalise=True,ExcludeSlicesOption=True)
'''


SpineSNRFilesSources=[]
SpineSNRFilesSources = [x[0] for x in os.walk("BaselineData/Spine/")][1:]
SpineArchives = [x[0] for x in os.walk("Archive")][1:]
for folder in SpineArchives:
    if "Spine" in folder:
        SpineSNRFilesSources.append(folder)
Data,FileTracker = SortData(SpineSNRFilesSources)
np.save("Testing/SNRStats/SpineDataFile.npy", Data)
np.save("Testing/SNRStats/SpineFileTracker.npy", FileTracker)

Data = np.load("Testing/SNRStats/SpineDataFile.npy",allow_pickle=True)
FileTracker = np.load("Testing/SNRStats/SpineFileTracker.npy",allow_pickle=True)
AnalyseData(Data,FileTracker,"spine",Normalise=True,ExcludeSlicesOption=False)