import numpy as np
import pandas as pd
import os

go_path = r"go_taxi"
path_path = r"pre_taxi"
out_path = r"path_taxi"
all_data = os.listdir(go_path)
label = ["Vehicle_SimID", "GPS_Time", "GPS_Longitude", "GPS_Latitude", "GPS_Speed", "GPS_Direction",
         "Passenger_State"]
cnt = 0
line = 0
for file in all_data:
    go_data = pd.read_excel(os.path.join(go_path, file)).iloc[-1, :]
    data = pd.read_excel(os.path.join(path_path, file))
    data.columns = label
    flag = True
    left_data = []
    n_flag = True
    for i in range(len(data)):
        if (data.loc[i, :].GPS_Time != go_data["GPS_Time"]) and n_flag:
            pass
        else:
            n_flag = False
            if (data.loc[i, :].GPS_Time == go_data["GPS_Time"] and flag) or (
                    data.loc[i, :].Passenger_State == 1 and flag):
                left_data.append(data.loc[i, :])
                line += 1
            else:
                flag = False
    data = pd.DataFrame([i for i in left_data])
    data.to_excel(os.path.join(out_path, file),index=None)
    cnt += 1

print("处理文件数量为:", cnt)
print("行数,", line)
