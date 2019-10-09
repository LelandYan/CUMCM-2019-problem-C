import pandas as pd
import numpy as np
import os

data_base_path = "site20170101-20171231"

months_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

data_path = "china_sites_2017"

data_list = []


def func(data=None):
    return data[data["type"] == "PM2.5"]


def run():
    for month_id in np.arange(12):
        for day_id in np.arange(months_days[month_id]):
            if month_id <= 8:
                if day_id <= 8:
                    data = pd.read_csv(
                        os.path.join(data_base_path,
                                     (data_path + "0" + str(month_id + 1) + "0" + str(day_id + 1) + ".csv")))
                    data_list.append(func(data))

                else:
                    data = pd.read_csv(
                        os.path.join(data_base_path, (data_path + "0" + str(month_id + 1) + str(day_id + 1) + ".csv")))
                    data_list.append(func(data))
            else:
                if day_id <= 8:
                    data = pd.read_csv(
                        os.path.join(data_base_path, (data_path + str(month_id + 1) + "0" + str(day_id + 1) + ".csv")))
                    data_list.append(func(data))
                else:
                    data = pd.read_csv(
                        os.path.join(data_base_path, (data_path + str(month_id + 1) + str(day_id + 1) + ".csv")))
                    data_list.append(func(data))

    data = pd.concat(data_list)
    data.to_csv("PM.5_get_together.csv", header=True, index=None)


if __name__ == '__main__':
    run()
