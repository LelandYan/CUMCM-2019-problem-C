import requests

# content = requests.get("https://raw.githubusercontent.com/DOsinga/deep_learning_cookbook/master/data/countries.csv")
# print(content)


import urllib.request as request
import csv
r = request.urlopen("https://raw.githubusercontent.com/DOsinga/deep_learning_cookbook/master/data/countries.csv").read().decode('utf8').split("\n")
reader = csv.reader(r)
for line in reader:
    print(line)