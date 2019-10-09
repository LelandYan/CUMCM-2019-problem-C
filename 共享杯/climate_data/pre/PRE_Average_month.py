import os
import pandas as pd
import numpy as np

columns_TEM_name = ["区站号", "纬度", "经度", "观测场拔海高度", "年", "月", "日", "20-8时降水量（夜晚）", "8-20时降水量(白天)", "20-20时累计降水量",
                    "20-8时降水量质量控制码", "20-8时降水量质量控制码", "20-20时降水量质量控制码"]


def data_process(group_line):
    small_rain_bool_index = (group_line["20-8时降水量（夜晚）"] != 32700)
    bool_index = (group_line["20-8时降水量（夜晚）"] != 32766)
    line_index = np.where(bool_index)[0]
    small_rain_index = np.where(small_rain_bool_index)[0]
    group_line["20-8时降水量（夜晚）"].iloc[small_rain_index] = 0.1
    group_line["20-8时降水量（夜晚）"] = group_line["20-8时降水量（夜晚）"].iloc[line_index].mean() * 0.1
    group_line.rename({"20-8时降水量（夜晚）": "月平均20-8时降水量（夜晚）"})

    ###
    small_rain_bool_index = (group_line["8-20时降水量(白天)"] != 32700)
    bool_index = (group_line["8-20时降水量(白天)"] != 32766)
    line_index = np.where(bool_index)[0]
    small_rain_index = np.where(small_rain_bool_index)[0]
    group_line["8-20时降水量(白天)"].iloc[small_rain_index] = 0.1
    group_line["8-20时降水量(白天)"] = group_line["8-20时降水量(白天)"].iloc[line_index].mean() * 0.1
    group_line.rename({"8-20时降水量(白天)": "月平均8-20时降水量(白天)"})

    return pd.DataFrame([group_line.iloc[0, :]], columns=group_line.columns)


filename_list = os.listdir(os.getcwd())
filename_list.remove("PRE_Average_month.py")
base_dir = os.getcwd()
for filename in filename_list:
    data_txt = np.loadtxt(os.path.join(base_dir, filename))
    raw_data = pd.DataFrame(data_txt)
    raw_data.columns = columns_TEM_name
    raw_data["纬度"] = raw_data["纬度"] / 100
    raw_data["经度"] = raw_data["经度"] / 100
    raw_data["观测场拔海高度"] = raw_data["观测场拔海高度"] * 0.1
    data = raw_data[["区站号", "纬度", "经度", "观测场拔海高度", "年", "月", "20-8时降水量（夜晚）", "8-20时降水量(白天)"]]
    data_n = data.groupby(["区站号"]).apply(data_process)
    data_n.to_csv("average_" + filename, header=True, index=None, encoding="gbk")
