from umatier_card_stats import *
from umatier_output import *
from umatier_files import *
import copy

oguri = Uma([20, 0, 10, 0, 0, 0], [112, 74, 118, 94, 102, 120])
finem = Uma([0, 0, 15, 0, 0, 15], [112, 74, 118, 94, 102, 120])
brian = Uma([10, 20, 0, 0, 0, 0], [112, 74, 118, 94, 102, 120])
urara = Uma([0, 0, 20, 10, 0, 0], [112, 74, 118, 94, 102, 120])

statweigh = [1.7, 3, 1.3, 0.9, 1, 0.6, 1.7]
statweigh_eval = [0, 1.4, 0, 1.3, 0, 0.7]

# teio.toreb = 20
# tachy.friendb = 44
print("creek, biko: ", give_training_values(1, [screek,biko], 100, training_stats_GL, 4, oguri, 0.2))
print("satono, biko: ", give_training_values(1, [satono,biko], 100, training_stats_GL, 4, oguri, 0.2))
biwa.toreb = 10
print("biwa, biko: ", give_training_values(1, [biwa,biko], 100, training_stats_GL, 4, oguri, 0.2))
# mrcb.statb = [1,0,0,0,2,1]
# print("test: ", give_training_values(4, [mrcb,tach,pasa], 100, training_stats_GL, 4, urara, 0.2))
# print("****")
# print("test: ", give_training_values(0, [biko], 100, training_stats_GL, 4, urara, 0.2))

trainingnum = 500
URA1 = Training_Environment("GL", Deck([biko, kita, baku, teio, biwa, screek]), oguri, [0, 6, 12, 0, 0], "GL", statweigh, statweigh_eval, training_stats_GL)
URA1.currency_val = 0.6
URA1.bond_scale = 55
# URA1 = Training_Environment("URA1", Deck([biko, pasa, fine, kita, vega, maru]), oguri, [0, 0, 3, 0, 15], "MANT", statweigh, statweigh_eval, training_stats_MANT)
myoutput = Output_wrap("GL_results", Deck([URA1.deck.cards[i] for i in range(5)]), URA1.scenario, trainingnum)
# URA1.statbonus_global = 1
URA1.statcap = [1600,1300,1300,1500,1300]
# URA1 = Training_Environment("URA1", Deck([kita,siriSR,oguSR,natu,fine,ayabe]),oguri,[3,6,9,0,0],"MANT",statweigh,statweigh_eval,training_stats_MANT)
# myoutput = Output_wrap("URA_intresults", Deck([URA1.deck.cards[i] for i in range(5)]), URA1.scenario, trainingnum)

# URA1.do_batch_GL(1,1)

# URA1.documentation_true = 0

# manum = 500
# URA1.calc_avg_vals = 1
# URA1.do_batch_GL(1,manum)
# URA1.calc_avg_vals = 2
# URA1.avg_train_val = [math.floor(val/manum) for val in URA1.avg_train_val]
# URA1.do_batch_GL(1,manum)

# URA1.do_batch_GL(1,2500)

# URA1.event_turns.sort()
# print(URA1.event_turns, URA1.total_turns)


# for i in range(10):
#     URA1.statweights[6] = 1.6 + 0.05*i
#     URA1.do_batch_GL(0,400)
#     print(URA1.statweights[6], math.floor(URA1.totalstats/400), [math.floor(stat / URA1.cutoff_trainings_done) for stat in URA1.avgstats])

# print(give_training_values(0,[baku,biko,kita],100,training_stats,2,oguri,0.2))
# print(give_training_values(4,[fine,baku],100,training_stats,4,oguri,0.2))
# print(give_training_values(2,[baku,pasa],100,training_stats,2,oguri,0.2))
# print(give_failrate(4,2,22))

# URA1.do_batch(1,1)
# testcards = [fine,copy.copy(mrcb)]

dotest = 1

if dotest:
    # testcards = [rudoGrp,copy.copy(fine),copy.copy(mrcb),copy.copy(tach),mati,natu,copy.copy(marv),copy.copy(yuki),festa,teio]
    # testcards = [copy.copy(fine),copy.copy(mrcb),copy.copy(tach),mati,copy.copy(marv),copy.copy(teio),fine3LB,cb3LB]
    testcards = [screek, suzus, satono, festaS, brianS, copy.copy(biwa), cafeSR, seiunS]

    # testcards = [copy.copy(fine),mrcb,tach]
    # testcards = [copy.copy(fine), mati, mrcb, natu, copy.copy(marv), copy.copy(tach), curr, siri, yuki, nishino, dober, taishin, seiun, sweepint, festa]
    # testcards = [copy.copy(pasa),groove,amaz,vega,rice,tama,siriGrp,riko]
    # testcards = [copy.copy(biko),copy.copy(baku),copy.copy(kita),maya,windy,sweep,suzu,tachy,pasta,maru]
    # testcards = [copy.copy(siriSR),copy.copy(oguSR),copy.copy(ayabe),urar,ines,grooveSR,bijin,palmer,grass]
    # targetstats = [1500, 0, 900, 0, 0, 0]
    for card in testcards:
        URA1.deck.cards[5] = card
        # statweigh = [1.2, 1, 1.4, 1, 1, 0.5, 0.8]
        # URA1.statweights = statweigh
        # conditions_met = 0
        # while conditions_met == 0:
        #    URA1.do_batch_GL(0,100)
        #    conditions_met = 1
        #    print(URA1.avgstats)
        #    for i in range(6):
        #        if URA1.avgstats[i] < 100*targetstats[i]:
        #            statweigh[i] += 0.1
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
        myoutput.add_result(Result_wrap(card, math.floor(URA1.totalstats / trainingnum*10)/10,0,URA1.total_racestats / URA1.cutoff_trainings_done))
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

