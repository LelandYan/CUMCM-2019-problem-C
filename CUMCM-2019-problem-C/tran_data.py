import pandas as pd
import numpy as np
import os

# 依次导入数据集
data_path = r"pre_taxi"
out_path1 = r"go_taxi"
out_path2 = r"back_taxi"
all_data = os.listdir(data_path)
label = ["Vehicle_SimID", "GPS_Time", "GPS_Longitude", "GPS_Latitude", "GPS_Speed", "GPS_Direction",
         "Passenger_State"]

# 参数
# a_为在出租车在机场的时间中的最后的0.3时间中
a_ = 0.3
cnt1 = 0
cnt2 = 0
a = []
# data = pd.DataFrame(columns=label)
for file in all_data:
    num = file.split("_")[1]
    df = pd.read_excel(os.path.join(data_path, file))
    # 限定为在机场内的所有时刻
    GPS_Longitude_in = ((121.7725501 <= df["GPS_Longitude"]) & (df["GPS_Longitude"] <= 121.8475213))
    GPS_Latitude_in = ((31.10587667 <= df["GPS_Latitude"]) & (df["GPS_Latitude"] <= 31.17790889))
    GPS_in = GPS_Latitude_in & GPS_Longitude_in
    in_data = df[GPS_in]
    if 1 == ((in_data["Passenger_State"].values[::-1])[0]):
        # in_data.to_excel(os.path.join(out_path1, "Taxi_" + str(num)), index=None)
        # 提取所有文件的最后一行数据
        a.append(in_data.iloc[-1, :])
        cnt1 += 1
    else:
        # in_data.to_excel(os.path.join(out_path2, "Taxi_" + str(num)), index=None)
        # 提取所有文件的最后一行数据
        a.append(in_data.iloc[-1, :])
        cnt2 += 1
# 提取所有文件的最后一行数据
data = pd.DataFrame([i for i in a])
# 提取所有文件的最后一行数据
data.to_excel("last_one_data.xlsx",index=None)
print("go", cnt1)
print("back", cnt2)
