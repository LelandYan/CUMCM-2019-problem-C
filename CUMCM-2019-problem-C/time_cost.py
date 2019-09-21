import numpy as np
import pandas as pd
import os

go_path = r"go_taxi"
back_path = r"back_taxi"
all_go_data = os.listdir(go_path)
all_back_data = os.listdir(back_path)
label = ["Vehicle_SimID", "GPS_Time", "GPS_Longitude", "GPS_Latitude", "GPS_Speed", "GPS_Direction",
         "Passenger_State", "Total_Path"]
# 没拉客每个车在机场的花费的时间
time_in_place = {}
# 拉客每个车在机场的花费的时间
time_not_place = {}

for file_go in all_go_data:
    df = pd.read_excel(os.path.join(go_path, file_go))
    time = (pd.to_datetime(df["GPS_Time"].max()).minute - pd.to_datetime(df["GPS_Time"].min()).minute) + (
            pd.to_datetime(
                df["GPS_Time"].max()).hour - pd.to_datetime(df["GPS_Time"].min()).hour) * 60
    time_in_place[df["Vehicle_SimID"][0]] = time

for file_back in all_back_data:
    df = pd.read_excel(os.path.join(back_path, file_back))
    ime = (pd.to_datetime(df["GPS_Time"].max()).minute - pd.to_datetime(df["GPS_Time"].min()).minute) + (
            pd.to_datetime(
                df["GPS_Time"].max()).hour - pd.to_datetime(df["GPS_Time"].min()).hour) * 60
    time_not_place[df["Vehicle_SimID"][0]] = time

# 读入已知的数据集
data = pd.read_excel("last_one_data_path.xlsx")
data["Time_Long"] = -1
for i in range(len(data)):
    if not time_in_place.get(data["Vehicle_SimID"][i], None) is None:
        data["Time_Long"][i] = time_in_place.get(data["Vehicle_SimID"][i], None)
    if not time_not_place.get(data["Vehicle_SimID"][i], None) is None:
        data["Time_Long"][i] = time_not_place.get(data["Vehicle_SimID"][i], None)

data.to_excel("last_one_data_path_time.xlsx", index=None)
