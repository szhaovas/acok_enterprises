import csv
import numpy as np
import sys
import operator

def csv_as_dict(filename):
    result = {}
    with open(filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            dict_row = dict(row)
            result[dict_row.pop('')] = dict_row
        return result

def dict_as_nparr(dict):
    result = []
    for row in dict:
        result.append(list(dict[row].values()))
    return np.array(result)

if __name__ == '__main__':
    all_data = np.zeros((4,21,9))
    for i in range(4):
        filename = str(i) + '.csv'
        nparr = dict_as_nparr(csv_as_dict(filename))
        all_data[i] = nparr

    mean = np.mean(all_data, axis=0)
    var = np.var(all_data, axis=0)

    sorted_dict = {}
    for i in range(21):
        row = dict(enumerate(mean[i]))
        sorted_row = sorted(row.items(), key=lambda kv: kv[1])
        sorted_dict[i] = sorted_row

    result = {}
    counts = [0] * 9
    limits = [2] * 9
    limits[2] = 3
    limits[5] = 3
    limits[6] = 3
    for iter in range(21):
        all_diff = {}
        for town in sorted_dict:
            # FIXME
            try:
                best_income = sorted_dict[town][-1][1]
                second_best_income = sorted_dict[town][-2][1]
                all_diff[town] = best_income - second_best_income
            except IndexError:
                all_diff[town] = float('inf')
        best_town = max(all_diff.items(), key=operator.itemgetter(1))[0]
        best_enterprise = sorted_dict[best_town][-1][0]
        result[best_town] = best_enterprise
        sorted_dict.pop(best_town)
        counts[best_enterprise] += 1
        if counts[best_enterprise] >= limits[best_enterprise]:
            for t in sorted_dict:
                for enterprise_income in sorted_dict[t]:
                    if enterprise_income[0] == best_enterprise:
                        sorted_dict[t].remove(enterprise_income)
                        continue

    for pair in sorted(result.items(), key=lambda kv: kv[0]):
        print(mean[pair[0],pair[1]])
