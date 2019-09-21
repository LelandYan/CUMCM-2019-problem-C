import pandas as pd
import numpy as np
import os

# 依次导入数据集
data_path = r"taxi\Taxi_070220"
out_path = r"pre_taxi"
all_data = os.listdir(data_path)
label = ["Vehicle_SimID", "GPS_Time", "GPS_Longitude", "GPS_Latitude", "GPS_Speed", "GPS_Direction",
         "Passenger_State"]

"""
浦东机场 经度纬度范围
31.17790889	121.7725501		31.17790889	121.8475213
31.10587667	121.7725501		31.10587667	121.8475213
"""
# 经过机场的车辆数
cnt_in = 0
for i in all_data:
    num = i.split("_")[1]
    # 分别读入数据
    df = pd.read_csv(os.path.join(data_path, i))
    # 给数据添加标签
    df.columns = label
    # 数据预处理
    # 字段缺失数据处理
    df.dropna(subset=["Vehicle_SimID", "GPS_Time", "GPS_Longitude", "GPS_Latitude"], inplace=True)
    # 判断车辆是否经过浦东机场
    GPS_Longitude_in = ((121.7725501 <= df["GPS_Longitude"]) & (df["GPS_Longitude"] <= 121.8475213))
    GPS_Latitude_in = ((31.10587667 <= df["GPS_Latitude"]) & (df["GPS_Latitude"] <= 31.17790889))
    GPS_in = GPS_Latitude_in & GPS_Longitude_in
    # 经过机场的车辆 , 字段异常数据处理
    if np.sum(GPS_in.astype(int)) != 0 and df["GPS_Time"].is_monotonic_increasing and np.sum(
            (df["Passenger_State"]) == 2) != len(df["GPS_Latitude"]) and np.sum((df["Passenger_State"]) == 0) != len(
        df["GPS_Latitude"]):
        cnt_in += 1
        # print(df.describe())
        df.to_excel(os.path.join(out_path, "Taxi_" + str(num) + ".xlsx"), index=None)

print("数据预处理完成")
print("剩余可用文件数量为：", cnt_in)

