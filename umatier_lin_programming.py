# from pulp import LpMinimize,LpProblem,LpStatus,lpSum,LpVariable
import math


# def find_num_of_trainings(statmatrix,goalstats):
#     model = LpProblem(name="find_num_of_trainings",sense=LpMinimize)
#     spd_num = LpVariable(name="spd",lowBound=0,cat="Integer")
#     sta_num = LpVariable(name="stm",lowBound=0,cat="Integer")
#     pow_num = LpVariable(name="pow",lowBound=0,cat="Integer")
#     gut_num = LpVariable(name="gut",lowBound=0,cat="Integer")
#     int_num = LpVariable(name="int",lowBound=0,cat="Integer")
#     race_num = LpVariable(name="race",lowBound=0,cat="Integer")
#     rest_num = LpVariable(name="rest",lowBound=0,cat="Integer")
#     names = ["spd","stm","pow","gut","int","rest","race"]
#     training_nums = [0,0,0,0,0,0,0]
#
#     model += (statmatrix[0][0] * spd_num + statmatrix[3][0] * gut_num + statmatrix[4][0] * int_num + gut_num + statmatrix[5][0] * race_num >= goalstats[0])
#     model += (statmatrix[1][1] * sta_num + statmatrix[2][1] * pow_num + statmatrix[5][1] * race_num >= goalstats[1])
#     model += (statmatrix[0][2] * spd_num + statmatrix[2][2] * pow_num + statmatrix[3][2] * gut_num + statmatrix[5][2] * race_num >= goalstats[2])
#     model += (statmatrix[1][3] * sta_num + statmatrix[3][3] * gut_num + statmatrix[5][3] * race_num >= goalstats[3])
#     model += (statmatrix[4][4] * int_num + statmatrix[5][4] * race_num >= goalstats[4])
#     model += (statmatrix[0][5] * spd_num + statmatrix[1][5] * sta_num + statmatrix[2][5] * pow_num + statmatrix[3][5] * gut_num + statmatrix[4][5] * int_num + statmatrix[5][5] * race_num >= goalstats[5])
#     model += (statmatrix[0][6] * spd_num + statmatrix[1][6] * sta_num + statmatrix[2][6] * pow_num + statmatrix[3][6] * gut_num + statmatrix[4][6] * int_num + statmatrix[5][6] * race_num + 52.5 * rest_num >= 0)
#
#     obj_func = spd_num + pow_num + sta_num + gut_num + int_num + race_num
#     model += obj_func
#     if model.solve():
#         for var in model.variables():
#             i = names.index(var.name)
#             training_nums[i] = var.value()
#         #print("success", training_nums)
#     else:
#         print("fail")
#     return training_nums


def find_num_of_trainings_fast(statmatrix,goalstats):
    #names = ["spd","stm","pow","gut","int","rest","race"]
    training_nums = [0,0,0,0,0,0,0]
    leftstats = goalstats.copy()
    fullstat = sum(goalstats) - goalstats[5]
    avgstat = sum([sum(statmatrix[i]) - statmatrix[i][6] for i in range(5)]) / 5
    leftstats[5] -= 3 * fullstat / avgstat
    training_nums[6] = leftstats[5] / statmatrix[5][5]
    for i in range(5):
        leftstats[i] -= training_nums[6] * statmatrix[5][i]
        leftstats[i] = max(0,leftstats[i])
    training_nums[4] = leftstats[4] / statmatrix[4][4]
    leftstats[0] -= training_nums[4] * statmatrix[4][0]
    training_nums[3] = (leftstats[3] - leftstats[1] * 0.3) / statmatrix[3][3]
    leftstats[0] -= training_nums[3] * statmatrix[3][0]
    leftstats[2] -= training_nums[3] * statmatrix[3][2]
    leftstats[0] = max(0,leftstats[0])
    leftstats[2] = max(0,leftstats[2])
    training_nums[1] = (leftstats[1] - leftstats[2] * 0.3) / statmatrix[1][1]
    training_nums[2] = (leftstats[2] - leftstats[0] * 0.5) / statmatrix[2][2]
    training_nums[0] = leftstats[0] / statmatrix[0][0]

    energyuse = sum([statmatrix[i][6] * training_nums[i] for i in range(5)])
    energyuse = statmatrix[5][6] * training_nums[6]
    training_nums[5] = 1 + max(0,-1 * energyuse) / 50
    for i in range(7):
        training_nums[i] = max(0,math.floor(training_nums[i] + 0.5))
    return training_nums
