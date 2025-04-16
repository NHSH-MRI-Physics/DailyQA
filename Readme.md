DailyQA system for Raigmore Hospitals MRI unit which computed smoothed signal to noise ratio. 

# Data Acqusition
The phantom should be set up as shown in the below flowchart, refering to the phantom setup as required. 

FlowChart             |  Phantom setup
:-------------------------:|:-------------------------:
![image](https://github.com/user-attachments/assets/65ee924c-adca-45cb-90a3-8aade1e5fb91)  |  ![image](https://github.com/user-attachments/assets/1ff87615-4890-4893-a556-e3ce5501a8d4)

# Software Use 
Import the library 
```python
from DQA_Scripts import DailyQA
```

Pass the path where the DICOMS are stored to the RunDailyQA fucntion. The TestingSettings optional argument is not intended to be used for day to day use, it is for unit testing purposes.
```python
Files = "/Head/DQA_Head_1"
Results = DailyQA.RunDailyQA(Files)
```

The returned results has one entry per sequence. In each entry you get the following data 
- index 1: average SNR over all slices
- index 2: a dictonary of the ROI results, where the key is the ROI and each key contains a list of the that ROIs SNR for each slice.
- index 3: Type of QA, head, body etc
- index 4: the sequence being run.

The ROIs are numbered as following:
![image](https://github.com/user-attachments/assets/0ff4f5c0-21a8-403d-a797-232922f681dd)

You can pass the results into the DidQAPass functuion to determine if it is within thresholds.
```python
import Helper
QAResult = Helper.DidQAPassV2(Result)
```
The QAResult will give out a true or false based on if it passsed and a message explaining why it is outwith the threshold. 
