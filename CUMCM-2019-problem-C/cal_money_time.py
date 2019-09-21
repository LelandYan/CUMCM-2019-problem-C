import numpy as np
import pandas as pd
import os


# 11 2.1
data = pd.read_excel("last_one_data_path_time.xlsx")
go_taxi = r"go_taxi"
back_taxi = r"back_taxi"

# 以路程作为比较的标准
data["Time_Cost"] = 0
data["Income"] = 0

# 计算出租车的时间损失
for i in range(len(data)):
    num_id = data["Vehicle_SimID"][i]
    if data["Passenger_State"][i] == 1:
        average_v = np.average(pd.read_excel(os.path.join(go_taxi, "Taxi_" + str(num_id)+".xlsx"))["GPS_Speed"])
        data["Time_Cost"] = data["Time_Long"] / 60 * average_v * 1000
    else:
        average_v = np.average(pd.read_excel(os.path.join(back_taxi, "Taxi_"+str(num_id)+".xlsx"))["GPS_Speed"])
        data["Time_Cost"] = data["Time_Long"] / 60 * average_v * 1000

# 计算出租车收益
for i in range(len(data)):
    if data["Total_Path"][i] > 0:
        if data["Total_Path"][i] / 1000 <= 3:
            data["Income"][i] = 11
        else:
            data["Income"][i] = 11 + (data["Total_Path"][i] / 1000 - 3) * 2.1

data.to_excel("last_result.xlsx",index=None)