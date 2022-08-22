training_stats = [[[0 for i in range(7)] for j in range(5)] for k in range(6)]

mystats = [10,0,5,0,0,2,-21]
for i in range(7):
    training_stats[0][0][i] = mystats[i]
mystats = [11,0,5,0,0,2,-22]
for i in range(7):
    training_stats[0][1][i] = mystats[i]
mystats = [12,0,5,0,0,2,-23]
for i in range(7):
    training_stats[0][2][i] = mystats[i]
mystats = [13,0,6,0,0,2,-25]
for i in range(7):
    training_stats[0][3][i] = mystats[i]
mystats = [14,0,7,0,0,2,-27]
for i in range(7):
    training_stats[0][4][i] = mystats[i]

mystats = [0,9,0,4,0,2,-19]
for i in range(7):
    training_stats[1][0][i] = mystats[i]
mystats = [0,10,0,4,0,2,-20]
for i in range(7):
    training_stats[1][1][i] = mystats[i]
mystats = [0,11,0,4,0,2,-21]
for i in range(7):
    training_stats[1][2][i] = mystats[i]
mystats = [0,12,0,5,0,2,-23]
for i in range(7):
    training_stats[1][3][i] = mystats[i]
mystats = [0,13,0,6,0,2,-25]
for i in range(7):
    training_stats[1][4][i] = mystats[i]

mystats = [0,5,8,0,0,2,-20]
for i in range(7):
    training_stats[2][0][i] = mystats[i]
mystats = [0,5,9,0,0,2,-21]
for i in range(7):
    training_stats[2][1][i] = mystats[i]
mystats = [0,5,10,0,0,2,-22]
for i in range(7):
    training_stats[2][2][i] = mystats[i]
mystats = [0,6,11,0,0,2,-24]
for i in range(7):
    training_stats[2][3][i] = mystats[i]
mystats = [0,7,12,0,0,2,-26]
for i in range(7):
    training_stats[2][4][i] = mystats[i]

mystats = [4,0,4,8,0,2,-22]
for i in range(7):
    training_stats[3][0][i] = mystats[i]
mystats = [4,0,4,9,0,2,-23]
for i in range(7):
    training_stats[3][1][i] = mystats[i]
mystats = [4,0,4,10,0,2,-24]
for i in range(7):
    training_stats[3][2][i] = mystats[i]
mystats = [5,0,4,11,0,2,-26]
for i in range(7):
    training_stats[3][3][i] = mystats[i]
mystats = [5,0,5,12,0,2,-28]
for i in range(7):
    training_stats[3][4][i] = mystats[i]

mystats = [2,0,0,0,9,4,5]
for i in range(7):
    training_stats[4][0][i] = mystats[i]
mystats = [2,0,0,0,10,4,5]
for i in range(7):
    training_stats[4][1][i] = mystats[i]
mystats = [2,0,0,0,11,4,5]
for i in range(7):
    training_stats[4][2][i] = mystats[i]
mystats = [3,0,0,0,12,4,5]
for i in range(7):
    training_stats[4][3][i] = mystats[i]
mystats = [4,0,0,0,13,4,5]
for i in range(7):
    training_stats[4][4][i] = mystats[i]

for j in range(5):
    training_stats[5][j][6] = 52.5

#print(training_stats)

race_list = [0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,2,2,1,2,2,2,2,3,3,2,1,2,1,2,2,3,2,3,3,3,3,2,2,2,2,2,2,2,3,3,3,2,3,2,2,2,2,2,3,2,3,3,2,3,3,2,2,2,2,2,2,2,3,3,3,2,3,0,0,0]
race_statvals = [0,5,8,10]
race_spvals = [0,35,35,45]

avg_stat_list_doc = [42,44,45,44,45,46,45,45,45,46,46,45,45,45,45,44,44,44,43,42,42,50,50,48,49,41,40,40,40,40,41,39,39,40,39,39,39,39,40,40,40,48,48,47,48,41,40,40,40,41,41,40,40,40,41,40,40,39,40,39,39,0,0,0,0,0]

training_stats_MANT = [[[0 for i in range(7)] for j in range(5)] for k in range(6)]

mystats = [8,0,4,0,0,2,-19]
for i in range(7):
    training_stats_MANT[0][0][i] = mystats[i]
mystats = [9,0,4,0,0,2,-20]
for i in range(7):
    training_stats_MANT[0][1][i] = mystats[i]
mystats = [10,0,4,0,0,2,-21]
for i in range(7):
    training_stats_MANT[0][2][i] = mystats[i]
mystats = [12,0,5,0,0,2,-23]
for i in range(7):
    training_stats_MANT[0][3][i] = mystats[i]
mystats = [13,0,6,0,0,2,-25]
for i in range(7):
    training_stats_MANT[0][4][i] = mystats[i]

mystats = [0,7,0,3,0,2,-17]
for i in range(7):
    training_stats_MANT[1][0][i] = mystats[i]
mystats = [0,8,0,3,0,2,-18]
for i in range(7):
    training_stats_MANT[1][1][i] = mystats[i]
mystats = [0,9,0,3,0,2,-19]
for i in range(7):
    training_stats_MANT[1][2][i] = mystats[i]
mystats = [0,10,0,4,0,2,-21]
for i in range(7):
    training_stats_MANT[1][3][i] = mystats[i]
mystats = [0,11,0,5,0,2,-23]
for i in range(7):
    training_stats_MANT[1][4][i] = mystats[i]

mystats = [0,5,8,0,0,2,-18]
for i in range(7):
    training_stats_MANT[2][0][i] = mystats[i]
mystats = [0,5,9,0,0,2,-19]
for i in range(7):
    training_stats_MANT[2][1][i] = mystats[i]
mystats = [0,5,10,0,0,2,-20]
for i in range(7):
    training_stats_MANT[2][2][i] = mystats[i]
mystats = [0,6,11,0,0,2,-22]
for i in range(7):
    training_stats_MANT[2][3][i] = mystats[i]
mystats = [0,7,12,0,0,2,-24]
for i in range(7):
    training_stats_MANT[2][4][i] = mystats[i]

mystats = [3,0,3,6,0,2,-20]
for i in range(7):
    training_stats_MANT[3][0][i] = mystats[i]
mystats = [3,0,3,7,0,2,-21]
for i in range(7):
    training_stats_MANT[3][1][i] = mystats[i]
mystats = [3,0,3,8,0,2,-22]
for i in range(7):
    training_stats_MANT[3][2][i] = mystats[i]
mystats = [4,0,3,9,0,2,-24]
for i in range(7):
    training_stats_MANT[3][3][i] = mystats[i]
mystats = [4,0,4,10,0,2,-26]
for i in range(7):
    training_stats_MANT[3][4][i] = mystats[i]

mystats = [2,0,0,0,6,4,5]
for i in range(7):
    training_stats_MANT[4][0][i] = mystats[i]
mystats = [2,0,0,0,7,4,5]
for i in range(7):
    training_stats_MANT[4][1][i] = mystats[i]
mystats = [2,0,0,0,8,4,5]
for i in range(7):
    training_stats_MANT[4][2][i] = mystats[i]
mystats = [3,0,0,0,9,4,5]
for i in range(7):
    training_stats_MANT[4][3][i] = mystats[i]
mystats = [4,0,0,0,10,4,5]
for i in range(7):
    training_stats_MANT[4][4][i] = mystats[i]

for j in range(5):
    training_stats_MANT[5][j][6] = 52.5
