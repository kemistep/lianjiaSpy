import numpy as np
import json
import re
from matplotlib import pyplot as plt


def jsonToList(doc_path, title):
    file = open(doc_path, 'r', encoding='utf-8')
    data_list = []
    for line in file.readlines():
        dic = json.loads(line)
        use_re_clean = useReClean(dic[title])
        data_list.append(use_re_clean)
    return data_list
    file.close()


def useReClean(string):
    pat = re.compile('\d+')
    res = re.search(pat, string).group()
    return res


def listToArray(list_):
    array = np.zeros((len(list_)))
    for i in range(len(list_)):
        array[i] = list_[i]
    return array


path = 'C:/Users\ASUS\Desktop\data_clean\lianjia.json'

h_price_list = jsonToList(path, 'house_price')
h_area_list = jsonToList(path, 'house_area')
h_price_array = listToArray(h_price_list)
h_area_array = listToArray(h_area_list)


max_area = int(np.max(h_area_array))
max_price = int(np.max(h_price_array))
min_area = int(np.min(h_area_array))
min_price = int(np.min(h_price_array))


plt.subplot(1, 2, 1)
plt.plot(h_area_array, h_price_array, 'ro')
plt.axis([6, 900, 100, 150000])

plt.subplot(1, 2, 2)
plt.plot(h_area_array, h_price_array, 'ro')
plt.axis([0, 100, 100, 10000])
plt.show()
