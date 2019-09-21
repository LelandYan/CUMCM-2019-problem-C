import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression

labels = ["Vehicle_SimID", "GPS_Longitude", "GPS_Latitude", "GPS_Speed", "GPS_Direction",
          "Total_Path", "Time_Long", "Time_Cost", "Income"]
data = pd.read_excel("last_result.xlsx")
x = data[labels]
label = data["Passenger_State"]
data = pd.concat([x, label], axis=1)
train_data, test_data = train_test_split(data, train_size=0.8, random_state=42)
train_x = train_data.to_numpy()[:, 0:8]
train_y = train_data.to_numpy()[:, 9]
test_x = test_data.to_numpy()[:, 0:8]
test_y = test_data.to_numpy()[:, 9]
scale = StandardScaler().fit(train_x)
train_x = scale.transform(train_x)
test_x = scale.transform(test_x)

# turn_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]},
#                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
# # clf分离器
# # 使用网格搜索法调超参数
# # 训练集做5折交叉验证
# # clf = GridSearchCV(SVC(C=1), turn_parameters, cv=5)
# clf = SVC(C=1000, gamma=0.001, kernel="rbf")
# # 用前一半train数据再做5折交叉验证
# # 因为之前的train_test_split已经分割为2份了
# # fit-拟合
# clf.fit(train_x, train_y)
# # 超参数
# print(clf.best_params_)
# # 得分
# for scores in clf.cv_results_["mean_test_score"]:
#     print(scores)
# 分类报告
log = LogisticRegression()
log.fit(train_x, train_y)
print(log.coef_)
# clf = MLPClassifier(solver="adam", alpha=1e-5, hidden_layer_sizes=(6, 4, 2), random_state=1)
# clf.fit(train_x, train_y)
# print(clf.n_iter_)
# y_true, y_pred = test_y, clf.predict(test_x)
# print(y_true)
# print(y_pred)
# print(classification_report(y_true, y_pred))
