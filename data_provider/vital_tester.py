from data_loader2 import Dataset_Vital

root_path = r"""D:\Sujays documents & files\MS\DePaulUniversity\Employment\OnCampus Job docs\GraduateResearchAssitant\Projects\DPU Project_Apr25_Jun25\vitalDB_v1\TestIn"""

data_path = '.'

vital_data = Dataset_Vital(root_path, 
                           flag='train', 
                           size=[672, 576, 96], 
                           data_path='.', 
                           scale=True, 
                           seasonal_patterns=None, 
                           drop_short=False)

index = 0

while index < vital_data.__len__():
    vital_data.__getitem__(index)
    print(index)
    index += 1

#print(vital_data.__getitem__(0))