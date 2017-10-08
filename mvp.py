#mvp model (blueprint), real prediction done in mvp_predict
from sklearn import svm
import numpy as np
import csv
from player import Player

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
lbj_weight = 0.33
tpr_weight = 0.47

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

	print()
	print("Full MVP Statline for 2017-2018")
	print(mvp_bp)
	print()	

	#PLAYER MAPPING AND OUTCOMES

	#PER
	test_indices = [17, 225, 217, 157, 104, 125, 445, 474, 271, 451, 179, 106, 469, 367]
	closest_val_per = 100000
	closest_pl_per = ""
	greatest_val_per = -100000
	greatest_pl_per = ""

	#PPG
	closest_val_ppg = 100000
	closest_pl_ppg = ""
	greatest_val_ppg = -100000
	greatest_pl_ppg = ""

	#TS%
	closest_val_ts = 100000
	closest_pl_ts = ""
	greatest_val_ts = -100000
	greatest_pl_ts = ""

	#VORP
	closest_val_vorp = 100000
	closest_pl_vorp = ""
	greatest_val_vorp = -100000
	greatest_pl_vorp = ""

	#BPM
	closest_val_bpm = 100000
	closest_pl_bpm = ""
	greatest_val_bpm = -100000
	greatest_pl_bpm = ""

	# for i in range(len(players)):
	for i in test_indices:
		try:
			print(players[i])
			player_data = statRetrieval(players[i])
			#BPM
			bpm_diff = similarity(player_data, 1, 22, 20)
			if(bpm_diff > greatest_val_bpm):
				greatest_val_bpm = bpm_diff
				greatest_pl_bpm = players[i]

			if(abs(bpm_diff) < closest_val_bpm):
				closest_val_bpm = abs(bpm_diff)
				closest_pl_bpm = players[i]

			#VORP
			vorp_diff = similarity(player_data, 1, 23, 21)
			if(vorp_diff > greatest_val_vorp):
				greatest_val_vorp = vorp_diff
				greatest_pl_vorp = players[i]

			if(abs(vorp_diff) < closest_val_vorp):
				closest_val_vorp = abs(vorp_diff)
				closest_pl_vorp = players[i]

			#PER
			per_diff = similarity(player_data, 1, 2, 2)
			if(per_diff > greatest_val_per):
				greatest_val_per = per_diff
				greatest_pl_per = players[i]

			if(abs(per_diff) < closest_val_per):
				closest_val_per = abs(per_diff)
				closest_pl_per = players[i]

			#PPG
			ppg_diff = similarity(player_data, 0, 23, 45)
			if(ppg_diff > greatest_val_ppg):
				greatest_val_ppg = ppg_diff
				greatest_pl_ppg = players[i]

			if(abs(ppg_diff) < closest_val_ppg):
				closest_val_ppg = abs(ppg_diff)
				closest_pl_ppg = players[i]

			#TS%
			ts_diff = similarity(player_data, 1, 3, 3)
			if(ts_diff > greatest_val_ts):
				greatest_val_ts = ts_diff
				greatest_pl_ts = players[i]

			if(abs(ts_diff) < closest_val_ts):
				closest_val_ts = abs(ts_diff)
				closest_pl_ts = players[i]

			print()
		except(TypeError):
			pass

	print('{0} is closest to the MVP PER statline with a margin of {1}.'.format(closest_pl_per, closest_val_per))
	print('{0} is most above the MVP PER statline with a margin of {1}.'.format(greatest_pl_per, greatest_val_per))
	print()
	print('{0} is closest to the MVP PPG statline with a margin of {1} ppg.'.format(closest_pl_ppg, closest_val_ppg))
	print('{0} is most above the MVP PPG statline with a margin of {1} ppg.'.format(greatest_pl_ppg, greatest_val_ppg))
	print()
	print('{0} is closest to the MVP TS percentage statline with a margin of {1}%.'.format(closest_pl_ts, closest_val_ts))
	print('{0} is most above the MVP TS percentage statline with a margin of {1}%.'.format(greatest_pl_ts, greatest_val_ts))
	print()
	print('{0} is closest to the MVP VORP statline with a margin of {1}.'.format(closest_pl_vorp, closest_val_vorp))
	print('{0} is most above the MVP VORP statline with a margin of {1}.'.format(greatest_pl_vorp, greatest_val_vorp))
	print()
	print('{0} is closest to the MVP +/- statline with a margin of {1}.'.format(closest_pl_bpm, closest_val_bpm))
	print('{0} is most above the MVP +/- statline with a margin of {1}.'.format(greatest_pl_bpm, greatest_val_bpm))
	# boi = players[451]
	# player_data = statRetrieval(boi)

	# print(statRetrieval("Leonard Kawhi"))

	print()


