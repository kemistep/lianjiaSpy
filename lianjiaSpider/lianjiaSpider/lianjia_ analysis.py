import numpy as np
import re
import pymongo
from matplotlib import pyplot as plt
from lianjiaSpider.settings import MONGODB_DBNAME, MONGODB_DOCNAME


def OpenMongodb(title):
    client = pymongo.MongoClient()
    db = client['%s' % MONGODB_DBNAME]
    collection = db['%s' % MONGODB_DOCNAME]
    # db = client.lianjia
    # collection = db.lianjiaBjZufang1
    data_list = []
    for book in collection.find():
        use_re_clean = useReClean(book['%s' % title])
        data_list.append(use_re_clean)
    return data_list


def useReClean(string):
    pat = re.compile('\d+')
    res = re.search(pat, string).group()
    return res


def listToArray(list_):
    array = np.zeros((len(list_)))
    for i in range(len(list_)):
        array[i] = list_[i]
    return array


h_price_list = OpenMongodb('house_price')
h_area_list = OpenMongodb('house_area')
h_price_array = listToArray(h_price_list)
h_area_array = listToArray(h_area_list)

print(h_area_array)
print(h_price_array)

max_area = int(np.max(h_area_array))
max_price = int(np.max(h_price_array))
min_area = int(np.min(h_area_array))
min_price = int(np.min(h_price_array))
print(max_price, max_area, min_price, min_area)

plt.subplot(1, 2, 1)
plt.plot(h_area_array, h_price_array, 'ro')
plt.axis([6, 900, 100, 150000])

plt.subplot(1, 2, 2)
plt.plot(h_area_array, h_price_array, 'ro')
plt.axis([0, 100, 100, 10000])
plt.show()

