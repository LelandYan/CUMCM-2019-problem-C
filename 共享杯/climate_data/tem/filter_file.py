import numpy as np
import pandas as pd
import os

filename_list = os.listdir(os.getcwd())
filename_list = [file for file in filename_list if file.startswith("max_min")]
base_dir = os.getcwd()
position_n = pd.read_excel("气象站.xlsx")

for filename in filename_list:
    data = pd.read_csv(os.path.join(base_dir, filename), encoding="gbk")
    filter_data = pd.merge(data, position_n, how="inner", on="区站号")
    filter_data.drop("经度_y", axis=1, inplace=True)
    filter_data.drop("纬度_y", axis=1, inplace=True)
    filter_data.rename({"纬度_x": "纬度"})
    filter_data.rename({"经度_x": "经度"})
    print(filter_data)
    filter_data.to_csv("filter_max_min_" + filename, header=True, index=None, encoding="gbk")
