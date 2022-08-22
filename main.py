from umatier_card_stats import *
from umatier_output import *
from umatier_files import *
import copy

oguri = Uma([20, 0, 10, 0, 0, 0], [112, 74, 118, 94, 102, 120])

statweigh = [1, 1, 1, 1, 1, 0.4, 0.8]
statweigh_eval = [1.2, 1, 1.2, 1, 1, 0.5]

trainingnum = 300
URA1 = Training_Environment("GL", Deck([biko, pasa, fine, kita, vega, maru]), oguri, [0, 18, 0, 0, 0], "URA", statweigh, statweigh_eval, training_stats_MANT)
# URA1 = Training_Environment("URA1", Deck([biko, pasa, fine, kita, vega, maru]), oguri, [0, 0, 3, 0, 15], "MANT", statweigh, statweigh_eval, training_stats_MANT)
myoutput = Output_wrap("URA_results", Deck([URA1.deck.cards[i] for i in range(5)]), URA1.scenario, trainingnum)
URA1.statbonus_global = 1
URA1.statcap = 1600
# URA1 = Training_Environment("URA1", Deck([kita,siriSR,oguSR,natu,fine,ayabe]),oguri,[3,6,9,0,0],"MANT",statweigh,statweigh_eval,training_stats_MANT)
# myoutput = Output_wrap("URA_intresults", Deck([URA1.deck.cards[i] for i in range(5)]), URA1.scenario, trainingnum)

# numma = 1000
# URA1.do_batch(1,numma)

# print(give_training_values(0,[baku,biko,kita],100,training_stats,2,oguri,0.2))
# print(give_training_values(4,[fine,baku],100,training_stats,4,oguri,0.2))
# print(give_training_values(2,[baku,pasa],100,training_stats,2,oguri,0.2))
# print(give_failrate(4,2,22))

# URA1.do_batch(1,1)

testcards = [copy.copy(fine),mati,natu,mrcb,copy.copy(marv),rudoGrp]
# testcards = [copy.copy(fine), mati, mrcb, natu, copy.copy(marv), copy.copy(tach), curr, siri, yuki, nishino, dober, taishin, seiun, sweepint, festa]
# testcards = [copy.copy(pasa),groove,amaz,vega,rice,tama,siriGrp,riko]
# testcards = [copy.copy(biko),copy.copy(baku),kita,maya,windy,fuku,sweep,ntr,pasta,maru]
# testcards = [copy.copy(siriSR),copy.copy(oguSR),copy.copy(ayabe),urar,ines,grooveSR,bijin,palmer,grass]
targetstats = [1140, 0, 950, 0, 0, 0]
for card in testcards:
    URA1.deck.cards[5] = card
    # statweigh = [1, 1, 1.4, 1, 1, 0.5, 0.8]
    # URA1.statweights = statweigh
    # conditions_met = 0
    # while conditions_met == 0:
    #    URA1.do_batch(0,100)
    #    conditions_met = 1
    #    for i in range(6):
    #        if URA1.avgstats[i] < 100*targetstats[i]:
    #            statweigh[i] += 0.02
    #            conditions_met = 0
    #    if not conditions_met:
    #        print("had to redo for: ", card.name, " statweights are: ", statweigh)

    # URA1.do_batch2(1,trainingnum,[1165,600,1000,300,800,1550],[1,0,1.5,0.2,1,0.5])
    # if len(URA1.score_list) > 0:
    #    median = URA1.score_list[math.floor(len(URA1.score_list)*(1-URA1.score_cutoff))]
    # else:
    #    median = 0
    # myoutput.add_result(Result_wrap(card,len(URA1.score_list),median,URA1.total_racestats/URA1.cutoff_trainings_done))

    URA1.do_batch_GL(1, trainingnum)
    # URA1.do_batch_MANT(1, trainingnum)
    myoutput.add_result(Result_wrap(card, URA1.totalstats / trainingnum,URA1.score_list[math.floor(len(URA1.score_list) * (1 - URA1.score_cutoff))],URA1.total_racestats / URA1.cutoff_trainings_done))
umatier_write_output(myoutput)

# maxstat = 0
# save_weigh = statweigh.copy()
# URA1.do_batch(1,200)
# for i in range(50):
#    for j in range(7):
#        URA1.statweights[j] = save_weigh[j] + 0.1 - 0.2*random.random()
#    URA1.do_batch(2,100)
#    if URA1.totalstats/URA1.cutoff_trainings_done > maxstat:
#        maxstat = URA1.totalstats/URA1.cutoff_trainings_done
#        save_weigh = URA1.statweights.copy()
# print(maxstat,[math.floor(100*num)/100 for num in save_weigh])
#
# print(URA1.senior_statgain)
# URA1.do_batch2(1,200,[1150,500,700,900,600,1600],[1,0.1,1,0.5,0.8,0.5])
#
# URA1.do_batch2(1,200,[1175,600,900,300,600,1600],[1,0.1,1,0.5,0.8,0.5])
#
# MANTR = Training_Environment("MANTR", Deck([kitaR, briaR, kawaR, teioR, maruR, fine]),oguri,[0,0,15,2,0],"MANT",statweigh,statweigh_eval,training_stats_MANT)
# MANTR.do_batch_MANT(1,100)
#
# URA1.do_batch2(1,1000,[1150,600,900,300,600,1200],[1,0.2,1.5,0.4,0.8,0.5])
#
# MANT1 = Training_Environment("MANT1", Deck([kita, biko, pasa, tach, marv, fine]),oguri,[0,9,6,0,3],"MANT",statweigh,statweigh_eval,training_stats_MANT)
# MANT1.bond_value = 14
# MANT1.do_batch_MANT(1,100)
#
# MANT2 = Training_Environment("MANT1", Deck([kita, biko, pasa, tach, marv, natu]),oguri,[0,9,6,0,3],"MANT",statweigh,statweigh_eval,training_stats_MANT)
# MANT2.bond_value = 14
# MANT2.do_batch_MANT(1,200)
#
# URA1.flat_cutoff = URA1.score_list[math.floor(URA1.totaltrains*(1-URA1.score_cutoff))]
#
# URA1.do_batch(1,600)
#
# URA2 = Training_Environment("URA2", Deck([kita, biko, pasa, baku, marv, natu]),oguri,[0,18,0,0,0],"URA",statweigh,statweigh_eval,training_stats)
#
# URA2.do_batch(1,500)
# URA2.do_batch2(1,1000,[1150,600,900,300,600,1200],[1,0.2,1.5,0.4,0.8,0.5])

