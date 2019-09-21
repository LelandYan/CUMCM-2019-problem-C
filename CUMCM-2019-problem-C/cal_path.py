import numpy as np
import pandas as pd
import os
from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000


path_total = {}
path_path = r"path_taxi"
out_path = r"cal_path"
all_data = os.listdir(path_path)
label = ["Vehicle_SimID", "GPS_Time", "GPS_Longitude", "GPS_Latitude", "GPS_Speed", "GPS_Direction",
         "Passenger_State"]

for file in all_data:
    df = pd.read_excel(os.path.join(path_path, file))
    tot = 0
    for i in range(1, len(df)):
        l = haversine(float(df["GPS_Longitude"][i]), float(df["GPS_Latitude"][i]), float(df["GPS_Longitude"][i - 1]),
                      float(df["GPS_Latitude"][i - 1]))
        tot += l
    print(str(file.split("_")[1].split(".")[0]), tot)
    path_total[file.split("_")[1].split(".")[0]] = tot

data = pd.read_excel("last_one_data.xlsx")
data_new = data.copy()
data["Total_Path"] = 0.0
for i in range(len(data)):
    if str(data.loc[i, :].Vehicle_SimID) in path_total.keys():
        data["Total_Path"][i] = path_total.get(str(data.loc[i, :].Vehicle_SimID))
# print(data)
data.to_excel("last_one_data_path.xlsx", index=None)
# 11 2.1