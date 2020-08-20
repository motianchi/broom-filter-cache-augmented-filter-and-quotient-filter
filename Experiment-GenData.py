# This script shows how to use all 3 kinds of filter simulators

import QuotientFilterSimulator
import CAFLRUSimulator
import BroomFilterSimulator
import math


def read_data(filename):
    nums = []
    with open(filename, "r") as file:
        for line in file.readlines():
            line = line.strip('\n')
            if len(line) == 0:
                continue
            nums.append(int(line))
    file.close()
    return nums


n = 80
s = input('ZIPF CONSTANT: ')
dup = 20  # number of filters
positives = [i for i in range(n)]
queries = read_data('test-' + s + '.txt')

epsilons = [2 ** i for i in range(-10, -5)]
broomThm = []
broomOFPR = []
quotientOFPR = []
caf9_OFPR = []
caf6_OFPR = []
caf3_OFPR = []

for eps in epsilons:
    broomThm.append(min(eps, eps ** float(s) / n ** (float(s) - 1)))
    broomfpNum = 0
    broomFilters = [BroomFilterSimulator.BroomFilterSimulator(positives, eps)
                    for i in range(dup)]
    qffpNum = 0
    quotientFilters = [QuotientFilterSimulator.QuotientFilterSimulator(positives, eps)
                       for i in range(dup)]
    caf3fpNum = 0
    caf3s = [CAFLRUSimulator.CAFLRU(positives, eps, k=3) for i in range(dup)]
    caf6fpNum = 0
    caf6s = [CAFLRUSimulator.CAFLRU(positives, eps, k=6) for i in range(dup)]
    caf9fpNum = 0
    caf9s = [CAFLRUSimulator.CAFLRU(positives, eps, k=9) for i in range(dup)]

    tick = 0

    for q in queries:
        q = q + n
        tick = tick + 1
        print('epsilon=2^-{}||{}/{}'.format(round(-math.log2(eps)), tick, len(queries)))

        for flt in quotientFilters:
            if flt.query(q):
                qffpNum = qffpNum + 1

        for flt in broomFilters:
            if flt.query(q):
                flt.adapt(q)
                broomfpNum = broomfpNum + 1

        for flt in caf3s:
            if flt.query(q):
                flt.adapt(q)
                caf3fpNum = caf3fpNum + 1

        for flt in caf6s:
            if flt.query(q):
                flt.adapt(q)
                caf6fpNum = caf6fpNum + 1

        for flt in caf9s:
            if flt.query(q):
                flt.adapt(q)
                caf9fpNum = caf9fpNum + 1

    broomOFPR.append(broomfpNum / len(queries) / dup)
    quotientOFPR.append(qffpNum / len(queries) / dup)
    caf3_OFPR.append(caf3fpNum / len(queries) / dup)
    caf6_OFPR.append(caf6fpNum / len(queries) / dup)
    caf9_OFPR.append(caf9fpNum / len(queries) / dup)

rf = '0818-s-' + str(s) + '.csv'
out = 'static FPR,'
for eps in epsilons:
    out = out + str(eps) + ','

out = out + '\nbroom,'
for fpr in broomOFPR:
    out = out + str(fpr) + ','

out = out + '\nbroom-Thm,'
for fpr in broomThm:
    out = out + str(fpr) + ','

out = out + '\nquotient,'
for fpr in quotientOFPR:
    out = out + str(fpr) + ','

out = out + '\nCAF-3,'
for fpr in caf3_OFPR:
    out = out + str(fpr) + ','

out = out + '\nCAF-6,'
for fpr in caf6_OFPR:
    out = out + str(fpr) + ','

out = out + '\nCAF-9,'
for fpr in caf9_OFPR:
    out = out + str(fpr) + ','

with open(rf, 'a+') as f:
    f.write(out + '\n')
f.close()
