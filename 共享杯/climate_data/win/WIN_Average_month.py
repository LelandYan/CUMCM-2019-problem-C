import os
import pandas as pd
import numpy as np

columns_TEM_name = ["区站号", "纬度", "经度", "观测场拔海高度", "年", "月", "日", "平均风速", "最大风速", "最大风速的风向", "极大风速", "极大风速的风向",
                    "平均风速质量控制码", "最大风速质量控制码", "最大风速的风向质量控制码", "最大风速的风向质量控制码", "极大风速的风向质量控制码"]


def data_process(group_line):
    bool_index = (group_line["平均风速"] != 32766)
    line_index = np.where(bool_index)[0]
    group_line["平均风速"] = group_line["平均风速"].iloc[line_index].mean() * 0.1
    group_line.rename({"平均风速": "月平均风速"})

    return pd.DataFrame([group_line.iloc[0, :]], columns=group_line.columns)


filename_list = os.listdir(os.getcwd())
filename_list.remove("WIN_Average_month.py")
base_dir = os.getcwd()

for filename in filename_list:
    data_txt = np.loadtxt(os.path.join(base_dir, filename))
    raw_data = pd.DataFrame(data_txt)
    raw_data.columns = columns_TEM_name
    raw_data["纬度"] = raw_data["纬度"] / 100
    raw_data["经度"] = raw_data["经度"] / 100
    raw_data["观测场拔海高度"] = raw_data["观测场拔海高度"] * 0.1
    data = raw_data[["区站号", "纬度", "经度", "观测场拔海高度", "年", "月", "平均风速"]]
    data_n = data.groupby(["区站号"]).apply(data_process)
    data_n.to_csv("average_" + filename, header=True, index=None, encoding="gbk")
