#mvp model (blueprint), real prediction done in mvp_predict
import numpy as np
import csv

np.random.seed(1)

from scraper import statRetrieval #realtime stats of player

#past mvp winners, team records, etc?

mvps = []
mvps_teams = []
players = []
mvp_bp = []

#ALL PLAYERS
playerReader = csv.reader(open('data/players.csv', newline=''), delimiter=',', quotechar='|')
for row in playerReader:
	players.append(''.join(row))

#MVPs
mvpReader = csv.reader(open('data/mvps.csv', newline=''), delimiter=',', quotechar='|')
for row in mvpReader:
	article = []
	article.append(''.join(row[0]))
	article.append(''.join(row[1]))
	mvps.append(article)

#MVP BLUEPRINT GENERATION

CSV_START_COLUMN = 7
CSV_END_COLUMN = 54

mvp_stats = np.genfromtxt('data/mvps.csv', delimiter=',', skip_header=1,
    usecols=np.arange(CSV_START_COLUMN,CSV_END_COLUMN), invalid_raise=False)

#mvp era weightage (/1)
dfp_weight = 0.20
lbj_weight = 0.30
tpr_weight = 0.50

def blueprint():
	mvp_amt = len(mvp_stats)

	# "The Days of Future Past"
	bloop_one = mvp_stats[0]
	for i in range(7):
		bloop_one = np.add(bloop_one, mvp_stats[i+1])

	bloop_one = dfp_weight*(np.divide(bloop_one, 8))

	# "The Lebron James Era"
	j = 8
	bloop_two = mvp_stats[8]
	while j < 12:
		bloop_two = np.add(bloop_two, mvp_stats[j+1])
		j += 1
	bloop_two = lbj_weight*(np.divide(bloop_two, 5))

	# "The Three Point Revolution"
	k = 13
	bloop_three = mvp_stats[13]
	while k < 16:
		bloop_three = np.add(bloop_three, mvp_stats[k+1])
		k += 1
	bloop_three = tpr_weight*(np.divide(bloop_three, 4))

	mvp_bloop = np.add(bloop_one, bloop_two)
	mvp_bloop = np.add(mvp_bloop, bloop_three)
	return mvp_bloop

def similarity(player_stat, stat_r, stat_c, bp_ind):
	#0 - 47
	return player_stat[stat_r][stat_c] - mvp_bp[bp_ind]


if __name__ == "__main__":
	mvp_bp = blueprint()



