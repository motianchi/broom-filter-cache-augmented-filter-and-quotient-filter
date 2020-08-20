# Copyright 2020 Tianchi (Maverick) Mo
# Department of Computer Science
# Stony Brook University
# Email: timo@cs.stonybrook.edu

# Code is based on paper
# "Don’t Thrash: How to Cache your Hash on Flash"
# by Michael Bender, Martin Farach-Colton et al.
# This is a simulator of the broom filter.

# You can use QuotientFilterSimulator(positives, epsilon)
# to create a broom filter storing all positive items.
# positives: a list of all positive items, cannot be changed after the filter is created.
# epsilon: a float between 0 and 1 (both excluded). The false positive probability.

# You can use query(item) to query any item in the universe set

import mmh3
import math
import random


class QuotientFilterSimulator(object):

    def __init__(self, positives, epsilon):
        self.positives = positives
        self.epsilon = epsilon
        self.n = len(positives)
        self.quotientLen = math.ceil(math.log2(self.n))
        self.remainderLen = math.ceil(-math.log2(epsilon))
        self.seed = random.randint(0, 10000000000000000000)
        self.filter = {}
        self.insertAll()

    def getFingerprint(self, item):
        fingerprint = str(bin(mmh3.hash128(str(item), self.seed, signed=False)))[2:]
        while len(fingerprint) != 128:
            fingerprint = '0' + fingerprint
        return fingerprint

    def insertAll(self):
        for item in self.positives:
            fingerprint = self.getFingerprint(item)
            key = fingerprint[0:self.quotientLen]
            value = fingerprint[self.quotientLen:self.quotientLen + self.remainderLen]
            if key in self.filter:
                self.filter[key].append(value)
            else:
                self.filter[key] = [value]

    def query(self, item):
        output = False
        fingerprint = self.getFingerprint(item)
        key = fingerprint[0:self.quotientLen]
        value = fingerprint[self.quotientLen:self.quotientLen + self.remainderLen]
        if key in self.filter:
            output = value in self.filter[key]
        return output
