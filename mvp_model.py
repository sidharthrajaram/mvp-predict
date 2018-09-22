import numpy as np
import pandas as pd
from scipy import stats
import math

np.random.seed(1)
pd.options.display.max_rows = 10
pd.options.display.float_format = '{:.1f}'.format

# field_df = pd.read_csv('data/mvpfield.csv')
years = ['2016', '2017', '2018']
mvp_index = 0
stats_of_interest = ['VORP','PER','BPM','WS','USG%','TOV%','FTr']
zscore_list = []

def zscore_model():
    for stat in stats_of_interest:
        # print('Z-scores for {}'.format(stat))
        stat_zscores = np.array([0.0, 0.0, 0.0, 0.0, 0.0,
                                 0.0, 0.0, 0.0, 0.0, 0.0,
                                 0.0, 0.0, 0.0, 0.0, 0.0,
                                 0.0, 0.0, 0.0, 0.0, 0.0])

        for year in years:
            field_df = pd.read_csv('data/mvp'+year+'.csv')
            stat_for_t20 = field_df[stat].tolist()
            math_ready = np.array(stat_for_t20)
            yearly_zscores = np.array(stats.zscore(math_ready))
            # print(yearly_zscores)
            stat_zscores += yearly_zscores
            # print('mvp z-score for {} is {}'.format(stat, yearly_zscores[mvp_index]))

        # print()
        zscore_list.append((stat_zscores/(len(years)))[mvp_index])

    # print()
    # print()
    # print("MVP Z-Scores compared to top 20")
    # for ind in range(len(zscore_list)):
    #     print(interest[ind])
    #     print(zscore_list[ind])
    #     print()
    return zscore_list

# a = [1.0,2.0,3.0,4.0]
# b = [1.0,0.6,4.1,4.0]
# print(eucliddist(a,b))






