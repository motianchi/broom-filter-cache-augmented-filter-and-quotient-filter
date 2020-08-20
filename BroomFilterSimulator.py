# Copyright 2020 Tianchi (Maverick) Mo
# Department of Computer Science
# Stony Brook University
# Email: timo@cs.stonybrook.edu

# Code is based on paper
# "Bloom Filters, Adaptivity, and the Dictionary Problem"
# by Michael Bender, Martin Farach-Colton et al.
# This is a simulator of the broom filter.

# You can use BroomFilterSimulator(positives, epsilon)
# to create a broom filter storing all positive items.
# positives: a list of all positive items, cannot be changed after the filter is created.
# epsilon: a float between 0 and 1 (both excluded). The false positive probability.

# You can use query(item) to query any item in the universe set

# If you get a false positive,
# you can use adapt(fpTrigger) to
# make sure the fpTrigger will not cause more false positives before the filter rehashes


import mmh3
import math
import random


class BroomFilterSimulator(object):

    def __init__(self, positives, epsilon):
        self.positives = positives
        self.epsilon = epsilon
        self.n = len(positives)
        self.adaBitsNum = 0
        self.quotientLen = math.ceil(math.log2(self.n))
        self.remainderLen = math.ceil(-math.log2(epsilon))
        self.seed = random.randint(0, 10000000000000000000)
        self.filter = {}
        self.fingerprintLib = []
        while True:
            if self.insertAll():
                break

    def getFingerprint(self, item):
        fingerprint = str(bin(mmh3.hash128(str(item), self.seed, signed=False)))[2:]
        while len(fingerprint) != 128:
            fingerprint = '0' + fingerprint
        return fingerprint

    def insertAll(self):
        success = True
        for item in self.positives:
            fingerprint = self.getFingerprint(item)

            # Hard collision test
            if fingerprint in self.fingerprintLib:
                success = False
                self.filter = {}
                self.fingerprintLib = []
                self.seed = random.randint(0, 10000000000000000000)  # rehash
                break
            else:
                self.fingerprintLib.append(fingerprint)

            key = fingerprint[0:self.quotientLen]
            value = fingerprint[self.quotientLen:self.quotientLen + self.remainderLen]
            if key in self.filter:
                for (rmdr, x) in self.filter[key]:
                    if rmdr.startswith(value):  # Soft collision
                        # ###################extension#######################
                        xfgp = self.getFingerprint(x)
                        for j in range(128 - self.quotientLen):
                            xnew = xfgp[self.quotientLen:self.quotientLen + j]
                            value = fingerprint[self.quotientLen:self.quotientLen + j]
                            if xnew != value:
                                self.filter[key].append((xnew, x))
                                self.filter[key].remove((rmdr, x))
                                break
                        # ####################################################
                self.filter[key].append((value, item))
            else:
                self.filter[key] = [(value, item)]
        return success

    def query(self, item):
        output = False
        fingerprint = self.getFingerprint(item)
        key = fingerprint[0:self.quotientLen]
        value = fingerprint[self.quotientLen:]
        if key in self.filter:
            for (rmdr, x) in self.filter[key]:
                output = value.startswith(rmdr)
                if output:
                    break
        return output

    def adapt(self, fpTrigger):
        fpFingerprint = self.getFingerprint(fpTrigger)
        if self.adaBitsNum > 3 * self.n or fpFingerprint in self.fingerprintLib:
            print('REHASH')
            self.adaBitsNum = 0
            self.seed = random.randint(0, 10000000000000000000)
            self.filter = {}
            self.fingerprintLib = []
            while True:
                if self.insertAll():
                    break
        else:
            key = fpFingerprint[0:self.quotientLen]
            value = fpFingerprint[self.quotientLen:]
            if key in self.filter:
                for (rmdr, x) in self.filter[key]:
                    if value.startswith(rmdr):  # Soft collision
                        # ###################extension#######################
                        xfgp = self.getFingerprint(x)
                        for j in range(128 - self.quotientLen):
                            xnew = xfgp[self.quotientLen:self.quotientLen + j]
                            if not (value.startswith(xnew)):
                                self.adaBitsNum = self.adaBitsNum + (len(xnew) - len(rmdr))
                                # print('add ada bits: {}'.format(len(xnew) - len(rmdr)))
                                self.filter[key].append((xnew, x))
                                self.filter[key].remove((rmdr, x))
                                break
                        #####################################################
