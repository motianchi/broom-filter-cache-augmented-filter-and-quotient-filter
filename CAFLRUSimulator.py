# Copyright 2020 Tianchi (Maverick) Mo
# Department of Computer Science
# Stony Brook University
# Email: timo@cs.stonybrook.edu

# This is a simulator of the cache augmented filter (CAF).

# You can use CAFLRU(positives, epsilon, k)
# to create a broom filter storing all positive items.
# positives: a list of all positive items, cannot be changed after the filter is created.
# epsilon: a float between 0 and 1 (both excluded). The false positive probability.
# k: integer > 0. The cache size (How many items can be cached)

# You can use query(item) to query any item in the universe set.

# If you get a false positive,
# you can use adapt(fpTrigger) to cache it with LRU eviction cache policy


import QuotientFilterSimulator


class CAFLRU(object):

    def __init__(self, positives, epsilon, k):
        self.qf = QuotientFilterSimulator.QuotientFilterSimulator(positives, epsilon)
        self.k = k
        self.cache = []

    def query(self, item):
        if item in self.cache:
            self.cache.pop(self.cache.index(item))
            self.cache.append(item)
        return self.qf.query(item) and (item not in self.cache)

    def adapt(self, item):
        if len(self.cache) == self.k:
            self.cache.pop(0)
            self.cache.append(item)
        else:
            self.cache.append(item)
