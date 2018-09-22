import math
import numpy as np
import pandas as pd
from scipy import stats
from mvp_model import zscore_model, stats_of_interest


def eucliddist(a,b):
    sum = 0.0
    for i in range(len(a)):
        sum += (a[i]-b[i])**2
    return math.sqrt(sum)

print("mvp z-score compared to top 20 PER players")
print(stats_of_interest)
print(zscore_model())
