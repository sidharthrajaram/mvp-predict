#sandbox, may make a streamlined version later
import csv
import numpy as np
from scraper import statRetrieval #realtime stats of player
from player import Player
from mvp import blueprint, similarity

raw_players = []
#ALL PLAYERS
playerReader = csv.reader(open('data/players.csv', newline=''), delimiter=',', quotechar='|')
for row in playerReader:
	raw_players.append(''.join(row))

#np.percentile
test_indices = [17, 225, 217, 157, 104, 125, 445, 474, 271, 451, 179, 106, 469, 367, 14, 54, 76, 89, 90, 73, 422, 312, 27, 
43, 44, 78, 99, 105, 189, 192, 33, 65, 67, 88, 80, 21, 18, 24, 362, 277, 234, 431, 321, 1, 3]

mvp_pool = [17, 18, 56, 72, 97, 104, 106, 109, 125, 157, 162, 171, 175, 179, 192, 217, 225, 271, 
276, 284, 367, 381, 451, 469, 474, 478, 421]
# test_indices = [17, 225, 217, 192, 189, 73, 104]

eligibility = 10
player_percentile = 50

players = []

ppgs = []
pers = []
ts = []
bpms = []

ppgs_final = []
pers_final = []
ts_final = []
bpms_final = []

filt_mp_players = []

filt_ppg_players = []
filt_per_players = []
filt_ts_players = []

filt_bpm_players = []

def doAllThings():
	#DATA COLLECTION
	for i in mvp_pool:
	# for i in range(len(raw_players)):
		try:
			player = raw_players[i]
			player_stats = statRetrieval(player)
			player = Player(player,player_stats)
			players.append(player)

		except:
			pass

	#players now has player objects with stats and names

	mpg = []

	#PLAYTIME ELIGIBILITY
	for player in players:
		try:
			mpg.append(player.getStats()[0][1])
		except:
			pass

	mpg = np.array(mpg)
	mpg_thresh = np.percentile(mpg, eligibility)
	print()
	print("minutes threshold")
	print(mpg_thresh)
	print()

	eligible_players = []

	for player in players:
		try:
			if(player.getStats()[0][1] >= mpg_thresh):
					eligible_players.append(player)
		except:
			pass

	# for i in test_indices:
	for i in range(len(eligible_players)):
		try:
			player = eligible_players[i]
			player_stats = player.getStats()
			ppgs.append(player_stats[0][23])

			pers.append(player_stats[1][2])
			ts.append(player_stats[1][3])

			bpms.append(player_stats[1][22])

		except:
			pass
	print()
	ppgs_final = np.array(ppgs)
	ppg_thresh = np.percentile(ppgs_final, player_percentile)
	print(ppg_thresh)

	pers_final = np.array(pers)
	per_thresh = np.percentile(pers_final, player_percentile)
	print(per_thresh)

	ts_final = np.array(ts)
	ts_thresh = np.percentile(ts_final, player_percentile)
	print(ts_thresh)

	bpms_final = np.array(bpms)
	bpm_thresh = np.percentile(bpms_final, player_percentile)
	print(bpm_thresh)
	print()


	# for i in test_indices:
	for i in range(len(eligible_players)):
		try:
			player = eligible_players[i]
			player_stats = player.getStats()

			if(player_stats[0][23] >= ppg_thresh):
				#print('{0} makes the cut with {1} ppg'.format(player, player_stats[0][23]))
				filt_ppg_players.append(player)

			if(player_stats[1][2] >= per_thresh):
				filt_per_players.append(player)

			if(player_stats[1][3] >= ts_thresh):
				filt_ts_players.append(player)

			if(player_stats[1][22] >= bpm_thresh):
				filt_bpm_players.append(player)
		except:
			pass
	#print()

def getEligibleBallers():
	eligible = []

	for player in filt_ppg_players:
		if(eligible.count(player) == 0):
			eligible.append(player)

	for player in filt_per_players:
		if(eligible.count(player) == 0):
			eligible.append(player)

	for player in filt_ts_players:
		if(eligible.count(player) == 0):
			eligible.append(player)

	for player in filt_bpm_players:
		if(eligible.count(player) == 0):
			eligible.append(player)

	return eligible

if __name__ == "__main__":

	doAllThings()

	print()

	print("The Candidates")
	elig = getEligibleBallers()
	for player in elig:
		print(player.getName())

	print()
	print("PPG TOP 10%")
	for player in filt_ppg_players:
		print(player.getName())

	print()
	print("PER TOP 10%")
	for player in filt_per_players:
		print(player.getName())

	print()
	print("TS% TOP 10%")
	for player in filt_ts_players:
		print(player.getName())

	print()
	print("+/- TOP 10%")
	for player in filt_bpm_players:
		print(player.getName())

	print()
	mvp_bloop = blueprint()
	print(mvp_bloop)

	# ELIG LIST is the REAL DEAL

	#PPG
	closest_val_ppg = 100000
	closest_pl_ppg = elig[0]
	greatest_val_ppg = -100000
	greatest_pl_ppg = elig[0]

	for player in elig:
		try:
			#PPG
			ppg_diff = player.getStats()[0][23] - mvp_bloop[45]
			if(ppg_diff > greatest_val_ppg):
				greatest_val_ppg = ppg_diff
				greatest_pl_ppg = player

			if(abs(ppg_diff) < closest_val_ppg):
				closest_val_ppg = abs(ppg_diff)
				closest_pl_ppg = player

		except(TypeError):
			pass

	#PER
	closest_val_per = 100000
	closest_pl_per = elig[0]
	greatest_val_per = -100000
	greatest_pl_per = elig[0]

	for player in elig:
		try:
			#PPG
			per_diff = player.getStats()[1][2] - mvp_bloop[2]
			if(per_diff > greatest_val_per):
				greatest_val_per = per_diff
				greatest_pl_per = player

			if(abs(per_diff) < closest_val_per):
				closest_val_per = abs(per_diff)
				closest_pl_per = player

		except(TypeError):
			pass

	#BPM
	closest_val_bpm = 100000
	closest_pl_bpm = elig[0]
	greatest_val_bpm = -100000
	greatest_pl_bpm = elig[0]

	for player in elig:
		try:
			#PPG
			bpm_diff = player.getStats()[1][22] - mvp_bloop[20]
			if(bpm_diff > greatest_val_bpm):
				greatest_val_bpm = bpm_diff
				greatest_pl_bpm = player

			if(abs(bpm_diff) < closest_val_bpm):
				closest_val_bpm = abs(bpm_diff)
				closest_pl_bpm = player

		except(TypeError):
			pass

	#VORP
	closest_val_vorp = 100000
	closest_pl_vorp = elig[0]
	greatest_val_vorp = -100000
	greatest_pl_vorp = elig[0]

	for player in elig:
		try:
			#PPG
			vorp_diff = player.getStats()[1][23] - mvp_bloop[21]
			if(vorp_diff > greatest_val_vorp):
				greatest_val_vorp = vorp_diff
				greatest_pl_vorp = player

			if(abs(vorp_diff) < closest_val_vorp):
				closest_val_vorp = abs(vorp_diff)
				closest_pl_vorp = player

		except(TypeError):
			pass

	#TS
	closest_val_ts = 100000
	closest_pl_ts = elig[0]
	greatest_val_ts = -100000
	greatest_pl_ts = elig[0]

	for player in elig:
		try:
			#PPG
			ts_diff = player.getStats()[1][3] - mvp_bloop[3]
			if(ts_diff > greatest_val_ts):
				greatest_val_ts = ts_diff
				greatest_pl_ts = player

			if(abs(ts_diff) < closest_val_ts):
				closest_val_ts = abs(ts_diff)
				closest_pl_ts = player

		except(TypeError):
			pass


	print()
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






















