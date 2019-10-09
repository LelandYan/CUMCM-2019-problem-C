import os
import pandas as pd
import numpy as np

columns_TEM_name = ["区站号", "纬度", "经度", "观测场拔海高度", "年", "月", "日", "平均值", "日最高气温", "日最低气温", "平均气温质量控制码", "日最高气温质量控制码",
                    "日最低气温质量控制码"]
base_dir = r"C:\Users\27215\Desktop\数据\tem\SURF_CLI_CHN_MUL_DAY-TEM-12001-201701.TXT"
data_txt = np.loadtxt(base_dir)
data = pd.DataFrame(data_txt)
data.columns = columns_TEM_name
