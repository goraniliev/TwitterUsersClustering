# -*- coding: utf-8 -*-
from math import sqrt

__author__ = 'goran'


def jaccard_sim(set1, set2):
    return 1.0 * len(set1 & set2) / len(set1 | set2)


def paper_sim(set1, set2):
    return 1.0 * len(set1 & set2) / (sqrt(len(set1)) * sqrt(len(set2)))