import numpy as np
import pandas as pd
from dateutil.parser import parse


def average_day_month(every_group, day=None):
    # 删除分组后的hour列，形成的结果数据是日平均，所以不在需要小时数据
    if day:
        every_group.drop("hour", axis=1, inplace=True)
        num = -3
    else:
        every_group.drop("date_day", axis=1, inplace=True)
        num = -2
    # 遍历每个站点，分别对每个站点进行求取平均值，这里不取列名为date_year,date_month,date_day三列
    for column in (every_group.columns[:num]):
        # 得到每个站点的非空的索引值
        bool_index = ~(pd.isna(every_group[column]) | pd.isnull(every_group[column]))
        # 如果该站点在一天都空，这日平均也为空
        if bool_index.sum() == 0:
            every_group[column] = np.nan
        # 如果该站点存在至少一个非空值，则计算其日平均的PM2.5的值
        else:
            line_index = np.where(bool_index)[0]
            every_group[column] = every_group[column].iloc[line_index].mean()
    # 返回的结果为对应的分组的每天的平均PM2.5的值
    return pd.DataFrame([every_group.iloc[0, :]], columns=every_group.columns)


# 读取数据
raw_data = pd.read_csv("PM.5_get_together.csv")
# 删除无用的列
raw_data.drop(["type"], axis=1, inplace=True)
# 将日期转化为datetime类型
raw_data["date"] = raw_data["date"].apply(lambda x: parse(str(x)))
# 将日期从的datetime类型转为str类型，并格式化输入 年-月-日
raw_data['date'] = raw_data['date'].apply(lambda x: x.strftime("%Y-%m-%d"))

# 分割日期数据列变成三列
data = raw_data.drop("date", axis=1).join(raw_data["date"].str.split("-", expand=True))
# 对数据中的year，month day的列进行重命名
data.rename(columns={0: "date_year", 1: "date_month", 2: "date_day"}, inplace=True)
# 对其按照月和日进行分组
group_by_month_and_day = data.groupby(["date_month", "date_day"])
# 进行分组处理,并得到日均的PM2.5的浓度值
group_by_month_and_day = group_by_month_and_day.apply(average_day_month, day=True)
# 对每日的PM2.5的浓度进行存储
group_by_month_and_day.to_csv("PM.5_per_day.csv", header=True, index=None)

group_by_month_and_day = pd.read_csv("PM.5_per_day.csv")
# 对其按照月进行分组
group_by_month = group_by_month_and_day.groupby("date_month")
# 进行分组处理,并得到月均的PM2.5的浓度值
group_by_month = group_by_month.apply(average_day_month, day=False)
# 对每月的PM2.5的浓度进行存储
group_by_month.to_csv("PM.5_per_month.csv", header=True, index=None)
