import os
import pandas as pd
import numpy as np

columns_TEM_name = ["区站号", "纬度", "经度", "观测场拔海高度", "年", "月", "日", "平均气温", "日最高气温", "日最低气温", "平均气温质量控制码", "日最高气温质量控制码",
                    "日最低气温质量控制码"]


def data_process(group_line):
    group_line["温差"] = group_line["温差"].max()
    group_line = group_line.drop_duplicates().reset_index(drop=True)
    # bool_index = (group_line["平均气温"] != 32766)
    # line_index = np.where(bool_index)[0]
    # group_line["天最高气温"] = group_line["平均气温"].iloc[line_index].max() * 0.1
    # group_line["天最低气温"] = group_line["平均气温"].iloc[line_index].min() * 0.1
    # group_line.rename({"平均气温": "月平均气温"})
    return pd.DataFrame([group_line.iloc[0, :]], columns=group_line.columns)


filename_list = os.listdir(os.getcwd())
filename_list.remove("TEM_Average_month.py")
filename_list.remove("Max_Min.py")
filename_list.remove("气象站.xlsx")
base_dir = os.getcwd()
# position_n = pd.read_excel("气象站.xlsx")
for filename in filename_list:
    data_txt = np.loadtxt(os.path.join(base_dir, filename))
    raw_data = pd.DataFrame(data_txt)
    raw_data.columns = columns_TEM_name
    raw_data["纬度"] = raw_data["纬度"] / 100
    raw_data["经度"] = raw_data["经度"] / 100
    raw_data["观测场拔海高度"] = raw_data["观测场拔海高度"] * 0.1
    new_data = raw_data[["区站号", "纬度", "经度", "观测场拔海高度", "年", "月", "平均气温", "日最高气温", "日最低气温"]]
    bool_index = (new_data["平均气温"] != 32766)
    line_index = np.where(bool_index)[0]
    data = new_data.iloc[line_index]
    data.drop("平均气温", inplace=True, axis=1)
    data["温差"] = data["日最高气温"] - data["日最低气温"]
    data_n = data.groupby(["区站号", "月"]).apply(data_process)
    data_n.to_csv("max_min_" + filename, header=True, index=None, encoding="gbk")
# print(position_n["气象站代码"])
