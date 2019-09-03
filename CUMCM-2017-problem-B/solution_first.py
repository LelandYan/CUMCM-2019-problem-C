import pandas as pd
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_excel(r"附件一：已结束项目任务数据.xls")

# 筛选数据
is_solve_data = data[data["任务执行情况"] == 1]
not_solve_data = data[data["任务执行情况"] == 0]

# 储存数据
# is_solve_data.to_excel("已完成任务数据.xls")
# not_solve_data.to_excel("未完成任务数据.xls")


print(is_solve_data.describe())
print(not_solve_data.describe())

# 绘图
# plt.scatter(data["任务标价"], data["任务执行情况"], c=data["任务执行情况"])

# price = data["任务标价"].values
# sorted_price = sorted(price)
# plt.scatter(np.arange(len(price)), sorted_price, c=data["任务执行情况"], s=4)
# plt.legend(["line 2", "line 1"], loc='upper left')
# 绘制3D图形
ax = plt.axes(projection="3d")
ax.scatter(data["任务gps 纬度"], data["任务gps经度"], data["任务标价"], c=data["任务执行情况"], alpha=0.5)
plt.legend()
plt.show()
