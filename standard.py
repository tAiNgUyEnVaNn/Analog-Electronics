import numpy as np

res = np.array([10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91])

res = np.array([res, res*10, res*100, res*1000, res*10000, res*100000])
res = res.reshape((np.shape(res)[1]*np.shape(res)[0],))

RE1_standard = np.array([10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91])
RE2_standard = np.array([1000, 1100, 1200, 1300, 1500, 1600, 1800, 2000, 2200, 2400, 3000, 3300, 3600, 3900, 4700, 5100, 5600, 6200, 6800, 7500, 8200, 9100])

def stand(value):
    round = min(res, key=lambda x: abs(x-value))
    return round, value-round

def lower(value): #return 1 value less than value
    # if value < 10000:
    #     return 0, 0
    # new = np.array([v for v in res if (v<value and v>5000)])
    new = np.array([v for v in res if v<value])
    s = np.shape(new)[0]
    val = new[s-1]
    return val, value - val

def all_lower(val): #return all value that is less than val
    if val < 1000:
        return 0
    new = np.array([v for v in res if (v<val and v>1000)])
    return new


def standardize(arr, typ):
    if typ == 'approx':
        arr = np.array([stand(value) for value in arr])
    elif typ == 'lower':
        arr = np.array([lower(value) for value in arr])
    return arr[:, 0], arr[:, 1]
    # return arr


# test = np.array([99120, 8000, 5000, 1000])
# print(standardize(test, typ='lower'))
# print(all_lower(3120))