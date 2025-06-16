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


Files = "Testing/DQA_DeltaFreq_Testing/EPI Testing/Delta50"
Results = DailyQA.RunDailyQA(Files)
for result in Results:
    print(Helper.DidQAPassV2(result))