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


Files = "C:\\Users\\Johnt\\Desktop\\DQA_body_20250306_082926361"
Results = DailyQA.RunDailyQA(Files)
Helper.DidQAPassV2(Results)
print(Results)