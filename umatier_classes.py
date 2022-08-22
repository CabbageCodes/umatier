import random
import math
from umatier_lin_programming import find_num_of_trainings, find_num_of_trainings_fast


class Uma:
    def __init__(self, bonuses, inistats):
        self.bonuses = bonuses
        self.inistats = inistats


class Card:
    def __init__(self, name, stype, yaruki, tokui, raceb, toreb, inibond, inistats, statb, friendb, hintrate):
        self.name = name
        self.stype = stype
        self.yaruki = yaruki
        self.tokui = tokui
        self.raceb = raceb
        self.toreb = toreb
        self.inibond = inibond
        self.bond = inibond
        self.inistats = inistats
        self.statb = statb
        self.friendb = friendb
        self.hintrate = hintrate
        self.has_hint = 0
        self.has_rainbow = 0

        self.chain = 0


        self.rainbows_done_total = 0
        self.rainbows_available_total = 0
        self.rainbows_done = 0
        self.training_statgain = 0
        self.rainbow_statgain = 0
        self.turns_to_bond = 0
        self.id = 10001
        self.where = -1
        self.failrate_decrease = 0
        self.energy_discount = 0
        self.rating = 0 + 1 * ("*" in name) + 1 * ("**" in name)
        self.bond_value = 9

        self.chain_events = [['r', 13], ['r', 13], ['r', 13]]
        if stype == 4:
            self.energyb = 5
            if self.rating == 1:
                # SR wis cards have 4 energy bonus only
                self.energyb = 4
        else:
            self.energyb = 0

    def reset(self):
        self.has_hint = 0
        self.chain = 0
        self.bond = self.inibond
        self.rainbows_done = 0
        self.where = -1

    def reset_full(self):
        self.reset()
        self.rainbows_done_total = 0
        self.rainbows_available_total = 0
        self.training_statgain = 0
        self.rainbow_statgain = 0
        self.turns_to_bond = 0


class Deck:
    def __init__(self, cards):
        self.cards = cards
        self.total_racebonus = 0
        self.decksize = len(cards)
        self.event_total = 15

    def init_values(self):
        self.total_racebonus = 0
        self.event_total = 15
        for card in self.cards:
            card.reset()
            self.total_racebonus += card.raceb


def is_acceptable_stats(stats, mandatory_stats, weights):
    score = sum([weights[i] * (stats[i] - mandatory_stats[i]) for i in range(6)])
    for i in range(6):
        if stats[i] < mandatory_stats[i]:
            score = 0
    return score


def give_failrate(training, level, energy):
    failrate = 0
    if training < 4:
        failrate = (48 - 0) / (25 - 52) * (energy - 52) - 1
        if training == 1:
            failrate -= 0.8
        if training == 0:
            failrate += 1
        if training == 3:
            failrate += 2
        failrate += 0.5 * level
    if training == 4:
        failrate = (12 - 0) / (25 - 30) * (energy - 30)
    failrate = max(failrate, 0)
    return failrate


def give_training_values(training, cards, bondstat, training_stats, level, uma, motivation):
    total_motiv = 0
    total_toreb = 0
    total_friendb = 1
    total_energyb = 0
    total_hintsp = 0
    did_hint = 0
    hint_nums = 0
    hint_unbonded = 0
    for mycard in cards:
        total_motiv += mycard.yaruki
        total_toreb += mycard.toreb
        if bondstat > 80 and mycard.stype == training:
            total_friendb = total_friendb * (1 + mycard.friendb / 100)
    result_stats = training_stats[training][level].copy()
    for k in range(6):
        for mycard in cards:
            if result_stats[k] > 0:
                result_stats[k] += mycard.statb[k]
    for k in range(6):
        result_stats[k] = result_stats[k] * (1 + 0.05 * len(cards)) * total_friendb * (1 + total_toreb / 100) * (1 + motivation * (1 + total_motiv / 100)) * (1 + uma.bonuses[k] / 100)
        result_stats[k] = math.floor(result_stats[k])
    return result_stats


class Training_Environment:
    def __init__(self, name, deck, uma, inheritance, scenario, statweights, statweights_eval, scenario_training_stats_list):
        self.name = name
        self.deck = deck
        self.uma = uma
        self.scenario = scenario
        self.total_turns = 65
        self.temp_trainstats = [[12, 0, 5, 0, 0, 2, -22], [0, 11, 0, 4, 0, 2, -20], [0, 5, 10, 0, 0, 2, -21], [4, 0, 4, 10, 0, 2, -23], [2, 0, 0, 0, 11, 4, 5], [0, 0, 0, 0, 0, 0, 55], [1, 1, 1, 1, 1, 20, -15]]
        self.inheritance = inheritance
        self.training_names = ["speed", "stamina", "power", "guts", "int", "rest", "away"]
        self.training_names_report = ["speed", "stamina", "power", "guts", "int", "rest", "race"]
        self.scenario_training_stats_list = scenario_training_stats_list
        self.race_list = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 3, 3, 2, 1, 2, 1, 2, 2, 3, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 2, 3, 2, 2, 2, 2, 2, 3, 2, 3, 3, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 2, 3, 0, 0, 0, 0, 0, 0, 0]
        self.race_statvals = [0, 5, 8, 10]
        self.race_spvals = [0, 35, 35, 45]

        self.turn_num = 0
        self.training_num = 0
        self.training_batch_num = 0
        self.maxenergy = 100
        self.is_summer = 0
        self.did_rainbow = 0

        self.statweights = statweights

        self.statweights_eval = statweights_eval
        self.statbonus_global = 1
        self.statcap = 1200
        self.global_friendb = 1
        self.global_tokui = 0

        self.totaltrains = 1000

        self.totalstats = 0
        self.total_racestats = 0
        self.avgstats = [0, 0, 0, 0, 0, 0]
        self.avg_optional_races = 0
        self.average_trainings_done = [0, 0, 0, 0, 0, 0]
        self.beststats = [0, 0, 0, 0, 0, 0]
        self.beststatsval = 0
        self.score_list = []
        # self.avg_stat_per_turn = [0] * (self.total_turns + 1)
        self.calc_avg_stat = 0
        self.cutoff_trainings_done = 0
        self.score_cutoff = 0.5
        self.flat_cutoff = 0

        self.training_amounts = [0, 0, 0, 0, 0, 0]
        self.optional_races_done = 0
        self.stats = [0, 0, 0, 0, 0, 0]

        self.documentation_true = 0

        self.energy = 100
        self.motiv = 0.1
        self.consecutive_races = 0
        self.last_training = -1
        self.event_turns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        self.senior_turns = 30
        self.senior_avg_stat = [0, 0, 0, 0, 0, 0]
        self.senior_statgain = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]

    def umaevent(self, amount):
        randomstat1 = random.randint(0, 5)
        randomstat2 = random.randint(0, 5)
        if randomstat1 == 6:
            increase1 = math.floor(amount * 1.5)
            value1 = (min(100, self.energy + increase1) - self.energy) * self.statweights[randomstat1]
        else:
            increase1 = amount * (1 + (randomstat1 == 5))
            value1 = increase1 * self.statweights[randomstat1]
        if randomstat2 == 6:
            increase2 = math.floor(amount * 1.5)
            value2 = (min(100, self.energy + increase2) - self.energy) * self.statweights[randomstat2]
        else:
            increase2 = amount * (1 + (randomstat2 == 5))
            value2 = increase2 * self.statweights[randomstat2]
        if value1 > value2:
            if randomstat1 == 6:
                self.energy = min(100, self.energy + increase1)
            else:
                self.stats[randomstat1] += increase1
        else:
            if randomstat2 == 6:
                self.energy = min(100, self.energy + increase2)
            else:
                self.stats[randomstat2] += increase2

    def set_inheritance(self, inheritance):
        self.inheritance = inheritance

    def set_deck_special(self):
        for card in self.deck.cards:
            card.has_rainbow = 0
            if card.stype == card.where and card.bond > 79 and card.stype < 5:
                card.has_rainbow = 1

            if card.name == "mati":
                card.energyb = 5 + 5 * (card.bond > 99)
            if card.name == "nishino":
                card.statb[4] = 0 + 3 * (card.bond > 99)
            if card.name == "groove":
                card.statb[2] = 0 + 1 * (card.bond > 79)
                card.statb[5] = 1 * (card.bond > 79)
            if card.name == "mrcb":
                card.statb[5] = 1 * (card.bond > 79)
                card.statb[4] = 1 + 1 * (card.bond > 79)
            if card.name == "bamboo":
                card.friendb = 20 + (100 - self.energy) / 100 * 17.5
            if card.name == "siri":
                card.friendb = 20 + min(18, 3 * card.rainbows_done)
            if card.name == "ntr":
                card.toreb = min(math.floor(20 * (self.turn_num / (0.7 * self.total_turns)) ** 2), 20)

            if card.name == "siriGrp":
                card.toreb = 10*(card.bond > 79)
                if 15 < self.turn_num < 21 or 29 < self.turn_num < 34:
                    card.has_rainbow = 1
            if card.name == "rudoGrp":
                card.statb[5] = 2*(card.bond > 79)
                if 15 < self.turn_num < 21 or 29 < self.turn_num < 34:
                    card.has_rainbow = 1
            if card.name == "maru":
                if card.where >= 0:
                    training_level = min(math.floor(self.training_amounts[card.where] / 4),4)
                    if self.is_summer:
                        training_level = 4
                    card.toreb = training_level*5+5
                else:
                    card.toreb = 0
            if card.name == "festa":
                if random.random() < 0.2:
                    card.failrate_decrease = 100
                else:
                    card.failrate_decrease = 0


    def init_training(self):
        self.last_training = -1
        for i in range(6):
            self.stats[i] = self.uma.inistats[i]
        self.deck.init_values()
        for i in range(5):
            self.stats[i] += self.inheritance[i] * 19
        if self.scenario == "URA" or self.scenario == "GL":
            self.total_turns = 65
            for event in range(27):
                self.umaevent(10)
            for objective in range(9):
                for i in range(5):
                    self.stats[i] += math.floor(3 * (1 + self.deck.total_racebonus / 100))
                    self.total_racestats += math.floor(3 * (1 + self.deck.total_racebonus / 100))
                self.stats[5] += math.floor(45 * (1 + self.deck.total_racebonus / 100))
            for URAfinals in range(3):
                for i in range(5):
                    self.stats[i] += math.floor(10 * (1 + self.deck.total_racebonus / 100))
                    self.total_racestats += math.floor(10 * (1 + self.deck.total_racebonus / 100))
                self.stats[5] += math.floor(60 * (1 + self.deck.total_racebonus / 100))
                self.stats[5] += 30
        elif self.scenario == "MANT":
            self.total_turns = 36
            for umaevents in range(15):
                randomstat = random.randint(0, 4)
                self.stats[randomstat] += 10
            for objective in range(7):
                for i in range(5):
                    self.stats[i] += 5
                self.stats[5] += 30
            for G1race in range(17):
                randomstat = random.randint(0, 4)
                self.stats[randomstat] += 2 + math.floor(10 * (1 + self.deck.total_racebonus / 100))
                self.total_racestats += 2 + math.floor(10 * (1 + self.deck.total_racebonus / 100))
                self.stats[5] += math.floor(30 * (1 + self.deck.total_racebonus / 100))
            for G23race in range(21):
                randomstat = random.randint(0, 4)
                self.stats[randomstat] += 2 + math.floor(8 * (1 + self.deck.total_racebonus / 100))
                self.total_racestats += 2 + math.floor(8 * (1 + self.deck.total_racebonus / 100))
                self.stats[5] += math.floor(25 * (1 + self.deck.total_racebonus / 100))
            for books_scrolls in range(10):
                # average 10 scrolls 20 books
                randomstat = random.randint(0, 4)
                self.stats[randomstat] += 7
                randomstat = random.randint(0, 4)
                self.stats[randomstat] += 7
                randomstat = random.randint(0, 4)
                self.stats[randomstat] += 15
            for MANT_event in range(100):
                # counting average of 25 5+5 events from chairman and MANT scenario
                randomstat = random.randint(0, 4)
                self.stats[randomstat] += 5
            for MANTFINALS in range(3):
                for i in range(5):
                    self.stats[i] += math.floor(13.5 * (1 + self.deck.total_racebonus / 100))
                    self.total_racestats += math.floor(13.5 * (1 + self.deck.total_racebonus / 100))
                self.stats[5] += math.floor(20 * (1 + self.deck.total_racebonus / 100))
        # pick event turns
        self.event_turns = random.sample(range(1, 15), 6) + random.sample(range(16, self.total_turns - 8), self.deck.event_total - 6)
        for card in self.deck.cards:
            for j in range(6):
                self.stats[j] += card.inistats[j]
        self.maxenergy = 100
        self.energy = 100
        self.motiv = 0.1
        self.optional_races_done = 0
        self.consecutive_races = 0
        self.training_amounts = [0, 0, 0, 0, 0, 0]
        self.turn_num = 0
        self.is_summer = 0
        self.global_friendb = 1
        self.global_tokui = 0

    def init_batch(self):
        for card in self.deck.cards:
            card.reset_full()
        self.totalstats = 0
        self.total_racestats = 0
        self.avgstats = [0, 0, 0, 0, 0, 0]
        self.avg_optional_races = 0
        self.average_trainings_done = [0, 0, 0, 0, 0, 0]
        self.beststats = [0, 0, 0, 0, 0, 0]
        self.beststatsval = 0
        self.score_list = []
        # self.avg_stat_per_turn = [0] * (self.turn_num + 1)
        self.cutoff_trainings_done = 0
        self.training_num = 0

    def set_documentation(self, documentation_true):
        self.documentation_true = documentation_true

    def take_turn(self):
        did_hint = 0
        self.did_rainbow = 0
        # do chain events:
        if self.turn_num in self.event_turns:
            chain_cards = [card for card in self.deck.cards if card.chain < len(card.chain_events)]
            if len(chain_cards) > 0:
                event_card = random.choice(chain_cards)
                if event_card.chain_events[event_card.chain][0] == 's':
                    for i in range(6):
                        self.stats[i] += event_card.chain_events[event_card.chain][1][i]
                    self.energy = min(self.maxenergy, max(0, self.energy + event_card.chain_events[event_card.chain][1][6]))
                    bondgain = event_card.chain_events[event_card.chain][1][7]
                    event_card.bond += bondgain
                    if 79 < event_card.bond < 80 + bondgain:
                        event_card.turns_to_bond += self.turn_num + 1
                    self.motiv += 0.1 * event_card.chain_events[event_card.chain][1][8]
                    self.motiv = min(0.2, max(self.motiv, 0.1))
                    if self.documentation_true:
                        print("did chain event for ", event_card.name, ", got stats: ", [event_card.chain_events[event_card.chain][1][i] for i in range(6)])
                        if event_card.chain_events[event_card.chain][1][6] != 0:
                            print("also got energy: ", event_card.chain_events[event_card.chain][1][6], " energy now is: ", self.energy)
                        if bondgain != 0:
                            print("card got bond: ", bondgain, " for a total bond of ", event_card.bond)
                elif event_card.chain_events[event_card.chain][0] == 'r':
                    randomstat = random.randint(0, 4)
                    self.stats[randomstat] += event_card.chain_events[event_card.chain][1]
                event_card.chain += 1
            else:
                self.umaevent(10)
        if self.documentation_true:
            print("motivation is: ", self.motiv)
        if self.motiv == 0.2:
            if random.random() < 0.02:
                self.motiv = 0.1
                if self.documentation_true:
                    print("motivation went randomly down to: ", self.motiv)
        else:
            if random.random() < 1 / 13:
                self.motiv = 0.2
                if self.documentation_true:
                    print("motivation went randomly up to: ", self.motiv)

        if self.documentation_true:
            print("turn number: ", self.turn_num)
        # put cards in their trainings
        for mycard in self.deck.cards:
            if random.random() < 0.07 * (1 + mycard.hintrate / 100):
                mycard.has_hint = 1
            else:
                mycard.has_hint = 0
            randomtraining = random.random()
            if randomtraining < 0.05:
                mycard.where = -1
            elif randomtraining < 0.05 + 0.19 * (1 + (mycard.tokui+self.global_tokui) / 100) and mycard.stype < 5:
                mycard.where = mycard.stype
            else:
                noconflict = 0
                while noconflict == 0:
                    randomtraining = random.randint(0, 4)
                    if randomtraining != mycard.stype:
                        mycard.where = randomtraining
                        noconflict = 1
        if self.documentation_true:
            print("cards are in categories: ", [self.training_names[mycard.where] for mycard in self.deck.cards])
            print("which cards have hints: ", [mycard.has_hint for mycard in self.deck.cards])
            print("bonds are: ", [mycard.bond for mycard in self.deck.cards])
            print("energy is: ", self.energy)
            print("stats are: ", self.stats)
            print("trainings done so far: ", self.training_amounts)
            print(" ")
        # set training values to be used to choose the best training
        trainingvals = [0, 0, 0, 0, 0, 0]
        # first we check how much each training gives in base stats
        if self.documentation_true and self.is_summer:
            print("it is summer this turn my dudes")
        for i in range(6):
            training_level = min(math.floor(self.training_amounts[i] / 4), 4)
            if self.is_summer:
                training_level = 4
            for j in range(7):
                self.temp_trainstats[i][j] = self.scenario_training_stats_list[i][training_level][j]
        # calculate rest value
        trainingvals[5] += 0.125 * (min(self.maxenergy, self.energy + 30) - self.energy) * self.statweights[6]
        trainingvals[5] += 0.625 * (min(self.maxenergy, self.energy + 50) - self.energy) * self.statweights[6]
        trainingvals[5] += 0.25 * (min(self.maxenergy, self.energy + 70) - self.energy) * self.statweights[6]
        rest_random = random.random()
        if rest_random < 0.125:
            self.temp_trainstats[5][6] = 30
        elif rest_random < 0.125 + 0.625:
            self.temp_trainstats[5][6] = 50
        else:
            self.temp_trainstats[5][6] = 70

        if self.documentation_true:
            print(self.temp_trainstats[5][6])
        # give cards special effects
        self.set_deck_special()
        # adjust bond values
        for mycard in self.deck.cards:
            if mycard.stype < 5:
                mycard.bond_value = 7 * (1 + max(0,(80 - mycard.bond) / 320)) * (mycard.friendb / 30) * self.statweights[mycard.stype]
            else:
                mycard.bond_value = 6
        # calculate other values for all 5 trainings
        for i in range(5):
            temp_trainlist = []
            total_motiv = 0
            total_toreb = 0
            total_friendb = self.global_friendb
            total_energyb = 0
            total_hintsp = 0
            did_hint = 0
            hint_nums = 0
            for mycard in self.deck.cards:
                # check which cards are on the training and add their stats together, including rainbows
                if mycard.where == i:
                    if mycard.has_hint == 1:
                        hint_nums += 1
                        if did_hint == 0:
                            total_hintsp = 3
                            did_hint = 1
                    temp_trainlist.append(mycard)
                    total_motiv += mycard.yaruki
                    total_toreb += mycard.toreb
                    if mycard.has_rainbow:
                        total_friendb = total_friendb * (1 + mycard.friendb / 100)
                        mycard.rainbows_available_total += 1
                        if i == 4:
                            total_energyb += mycard.energyb
                    if mycard.bond < 80:
                        # give bonding some extra value
                        trainingvals[i] += mycard.bond_value
            if hint_nums > 0:
                trainingvals[i] += sum([card.bond_value * 5 / 7 * (card.bond < 73) * card.has_hint for card in temp_trainlist]) / hint_nums

            # add flat stat bonuses from cards on that training
            for k in range(6):
                for mycard in temp_trainlist:
                    if self.temp_trainstats[i][k] > 0:
                        self.temp_trainstats[i][k] += mycard.statb[k]
            for k in range(6):
                # calculate together training stat values and add them to the trainingvals list to evaluate which training is the best to do
                self.temp_trainstats[i][k] = self.temp_trainstats[i][k] * (1 + 0.05 * len(temp_trainlist)) * total_friendb * (1 + total_toreb / 100) * (1 + self.motiv * (1 + total_motiv / 100)) * (1 + self.uma.bonuses[k] / 100)
                self.temp_trainstats[i][k] = min(100, self.temp_trainstats[i][k]) * self.statbonus_global
                self.temp_trainstats[i][k] = math.floor(self.temp_trainstats[i][k])
                # give small sp bonus for hints
                if k == 5:
                    self.temp_trainstats[i][k] += total_hintsp
                # only give training stat a value if it is not capped
                if self.stats[k] < self.statcap and k < 5:
                    trainingvals[i] += min(self.temp_trainstats[i][k], self.statcap - self.stats[k]) * self.statweights[k]
            # energy cost must be factored too
            if i < 4:
                for mycard in temp_trainlist:
                    self.temp_trainstats[i][6] *= (100 - mycard.energy_discount) / 100
                self.temp_trainstats[i][6] = max(0, self.energy + self.temp_trainstats[i][6]) - self.energy
            else:
                self.temp_trainstats[i][6] += total_energyb
                self.temp_trainstats[i][6] = min(self.energy + self.temp_trainstats[i][6], self.maxenergy) - self.energy
            trainingvals[i] += self.statweights[6] * self.temp_trainstats[i][6]
            failrate = give_failrate(i, min(math.floor(self.training_amounts[i] / 4), 4), self.energy)
            for mycard in temp_trainlist:
                failrate *= (100 - mycard.failrate_decrease) / 100
            if failrate > 0:
                trainingvals[i] *= (100 - 1.4 * failrate) / 100
        # end turn by picking the best training and doing it
        maxval = max(trainingvals)
        maxindex = trainingvals.index(maxval)

        # check if we should do an optional race instead though
        random_racestat = random.randint(0, 4)
        racestat_increase = 2 * (self.race_list[self.turn_num + 6] == 3) + math.floor((1 + self.deck.total_racebonus / 100) * self.race_statvals[self.race_list[self.turn_num + 6]])
        racesp_increase = math.floor((1 + self.deck.total_racebonus / 100) * self.race_spvals[self.race_list[self.turn_num + 6]])
        current_race_value = racestat_increase + racesp_increase * self.statweights[5] - 15 * self.statweights[6]
        current_race_value *= 0.95
        for i in range(5):
            self.temp_trainstats[6][i] = racestat_increase / 5
        self.temp_trainstats[6][5] = racesp_increase
        self.temp_trainstats[6][6] = max(0, self.energy - 15) - self.energy

        #check what date could be done


        # document average stats from training per turn
        # if self.calc_avg_stat:
        #     self.avg_stat_per_turn[self.turn_num] += maxval

        if self.documentation_true:
            print("training options: ", self.temp_trainstats)
            print("stat weights: ", [math.floor(num * 100) / 100 for num in self.statweights])
            print("training values: ", [math.floor(num * 100) / 100 for num in trainingvals])
            print("which training is best: ", self.training_names[maxindex])
            print("race type on this turn: ", self.race_list[self.turn_num + 6])
            print("race values (stat, sp): ", racestat_increase, racesp_increase)
            print("race value: ", current_race_value)
            print("consecutive races done: ", self.consecutive_races)
        # if race is worse we train the best stat
        skipval = 0
        didskip = 0
        if maxval > skipval and (current_race_value < maxval or self.consecutive_races == 2):
            self.consecutive_races = 0
            failrate = give_failrate(maxindex, min(math.floor(self.training_amounts[maxindex] / 4), 4), self.energy) / 100
            for mycard in self.deck.cards:
                if mycard.where == maxindex:
                    failrate *= (100 - mycard.failrate_decrease) / 100
            if random.random() > failrate:
                for i in range(6):
                    self.stats[i] += self.temp_trainstats[maxindex][i]
            else:
                if self.motiv == 0.2:
                    self.motiv -= 0.1
                self.stats[maxindex] -= 5
                # if give_failrate(maxindex,min(math.floor(self.training_amounts[maxindex]/4),4),self.energy)/100 > 0:
                #     print(give_failrate(maxindex,min(math.floor(self.training_amounts[maxindex]/4),4),self.energy)/100, self.training_names[maxindex], self.energy, self.turn_num, self.temp_trainstats[maxindex][maxindex])
                # if self.turn_num == 64:
                #     print('')

            did_hint = 0
            for mycard in self.deck.cards:
                # give cards bond if they were on the training
                if mycard.where == maxindex:
                    if mycard.has_rainbow:
                        mycard.rainbow_statgain += sum([self.temp_trainstats[maxindex][i] for i in range(5)])
                        mycard.rainbows_done += 1
                        mycard.rainbows_done_total += 1
                        self.did_rainbow = 1
                    mycard.bond += 7
                    if 79 < mycard.bond < 87:
                        mycard.turns_to_bond += self.turn_num + 1
                    if mycard.has_hint == 1 and did_hint == 0:
                        mycard.bond += 5
                        if 79 < mycard.bond < 85:
                            mycard.turns_to_bond += self.turn_num + 1
                        did_hint = 1
                    mycard.training_statgain += sum([self.temp_trainstats[maxindex][i] for i in range(5)])
                # fix this please, extra stats for friend cards sometimes
                    if mycard.stype == 5 and random.random() < 0.3:
                        self.stats[4] += 4
                        mycard.training_statgain += 4
                        mycard.bond += 5
                        if 79 < mycard.bond < 85:
                            mycard.turns_to_bond += self.turn_num + 1

            # change energy based on which training we did
            self.energy += self.temp_trainstats[maxindex][6]
            self.energy = min(self.energy, self.maxenergy)
            self.energy = max(self.energy, 0)

            # documentation for what we have done so far
            self.training_amounts[maxindex] += 1
            self.average_trainings_done[maxindex] += 1
            self.last_training = maxindex
            if self.documentation_true:
                print("we did training: ", self.training_names[maxindex], " current stats: ", self.stats)
                print("current energy", self.energy)
            if maxindex < 5 and random.random() < 0.1:
                if self.energy < self.maxenergy:
                    self.energy = min(self.maxenergy, self.energy + 5)
                else:
                    self.energy = max(0, self.energy - 5)
                    self.stats[maxindex] += 5
                if self.documentation_true:
                    print("got extra training random event, energy is now: ", self.energy)
        elif current_race_value > maxval and current_race_value > skipval and self.consecutive_races < 2:
            # otherwise we do the race
            self.consecutive_races += 1
            self.energy += -15
            self.energy = max(self.energy, 0)
            self.stats[random_racestat] += racestat_increase
            self.total_racestats += racestat_increase
            self.stats[5] += racesp_increase
            self.optional_races_done += 1

            self.last_training = 6
            if self.documentation_true:
                print("we did race, current stats: ", self.stats)
                print("current energy", self.energy)
        else:
            if self.documentation_true:
                print("we skipped the turn since it was bad")
            didskip = 1
        if self.documentation_true:
            print("*****************")
            print(" ")
        if didskip == 0:
            self.turn_num += 1

    def do_training(self):
        self.init_training()
        total_max_motiv_turns = 0

        for i in range(self.total_turns):
            # print(self.stats,self.optional_races_done)
            # if self.turn_num > 55:
            #     self.documentation_true = 1
            # self.consecutive_races = 2
            if self.turn_num == 31 or self.turn_num == 52:
                self.is_summer = 1
            elif self.turn_num == 35 or self.turn_num == 56:
                self.is_summer = 0
            self.take_turn()
            # if self.turn_num == 20 and self.training_num == 1:
            #     print self.
            if self.turn_num > self.total_turns - self.senior_turns:
                for i in range(5):
                    for j in range(7):
                        self.senior_statgain[i][j] += self.temp_trainstats[i][j]
                for j in range(7):
                    self.senior_statgain[5][j] += self.temp_trainstats[6][j]
            if self.motiv == 0.2:
                total_max_motiv_turns += 1
        addstats = 0
        # print(self.stats)
        for i in range(6):
            if i < 5:
                self.stats[i] = min(self.statcap, self.stats[i])
            addstats += math.floor(self.stats[i] * self.statweights_eval[i])

        if addstats > self.flat_cutoff:
            self.cutoff_trainings_done += 1
            self.totalstats += addstats
            for i in range(6):
                self.avgstats[i] += self.stats[i]
            self.avg_optional_races += self.optional_races_done
            self.score_list.append(addstats)
        if addstats > self.beststatsval:
            for i in range(6):
                self.beststats[i] = self.stats[i]
            self.beststatsval = addstats
        self.training_num += 1
        if self.documentation_true:
            self.event_turns.sort()
            print("")
            print("finished training")
            print("chains were on turns: ", self.event_turns)
            print("motivation was max for this many turns: ", total_max_motiv_turns)
            print("")

    def do_training2(self, mandatory_stats, statweights_cutoff):
        self.init_training()
        save_weights = self.statweights.copy()
        for i in range(self.total_turns):
            # if self.turn_num == 45 and self.training_num == 1:
            #     self.documentation_true = 1
            # else:
            #     self.documentation_true = 0
            if self.turn_num == 31 or self.turn_num == 52:
                self.is_summer = 1
            elif self.turn_num == 35 or self.turn_num == 56:
                self.is_summer = 0

            turns_remaining = self.total_turns - self.turn_num
            if turns_remaining < 40:
                # self.documentation_true = 1
                trainings_needed = find_num_of_trainings_fast(self.senior_statgain, [max(0, mandatory_stats[k] - self.stats[k]) for k in range(6)])
                # if turns_remaining % 10 == 5:
                #     trainings_needed = find_num_of_trainings(self.senior_statgain,[max(0,mandatory_stats[k]-self.stats[k]) for k in range(6)])
                # print(find_num_of_trainings(self.senior_statgain,[max(0,mandatory_stats[k]-self.stats[k]) for k in range(6)]), find_num_of_trainings_fast(self.senior_statgain,[max(0,mandatory_stats[k]-self.stats[k]) for k in range(6)]))
                # print("")
                if sum(trainings_needed) > max(0, self.total_turns - self.turn_num - 6):
                    for j in range(5):
                        if trainings_needed[j] > 0:
                            self.statweights[j] = save_weights[j] + 3
                        else:
                            self.statweights[j] = save_weights[j]
                    if trainings_needed[6] > 0:
                        self.statweights[5] = save_weights[j] + 1.5
                    else:
                        self.statweights[5] = save_weights[5]
                # print(trainings_needed)
                # print(self.statweights)
            for j in range(6):
                if self.stats[j] > mandatory_stats[j]:
                    self.statweights[j] = 0
            self.take_turn()
            # if turns_remaining < 36:
            #     if self.last_training == 5:
            #         trainings_needed[self.last_training] += -1
            #     elif self.last_training < 5:
            #         trainings_needed[self.last_training] += -self.temp_trainstats[self.last_training][self.last_training]/self.senior_statgain[self.last_training][self.last_training]
            #         trainings_needed[self.last_training] = max(trainings_needed[self.last_training],0)
            #     elif self.last_training == 6:
            #         trainings_needed[6] += -self.temp_trainstats[6][5]/self.senior_statgain[5][5]
            #         trainings_needed[6] = max(trainings_needed[6],0)

        for j in range(6):
            self.statweights[j] = save_weights[j]
        addstats = 0
        for i in range(6):
            if i < 5:
                self.stats[i] = min(self.statcap, self.stats[i])
            addstats += math.floor(self.stats[i] * self.statweights_eval[i])

        if addstats > self.flat_cutoff:
            self.cutoff_trainings_done += 1
            self.totalstats += addstats
            for i in range(6):
                self.avgstats[i] += self.stats[i]
            self.avg_optional_races += self.optional_races_done
            if is_acceptable_stats(self.stats, [num - 25 for num in mandatory_stats], statweights_cutoff) > 0:
                self.score_list.append(addstats)
        if addstats > self.beststatsval:
            for i in range(6):
                self.beststats[i] = self.stats[i]
            self.beststatsval = addstats
        self.training_num += 1

    ##        print(self.stats, rainbows, self.optional_races_done)

    def do_training_MANT(self):
        self.init_training()
        for i in range(self.total_turns):
            ##            if self.turn_num > 30 and self.turn_num < 34 and self.training_num == 1:
            ##                self.documentation_true = 1
            ##            else:
            ##                self.documentation_true = 0
            ##            if self.training_num == 1:
            ##                print(self.stats)
            if self.turn_num == 22 or self.turn_num == 30:
                self.is_summer = 1
                self.energy = 100
                self.statbonus_global = 1.6
            elif self.turn_num == 26 or self.turn_num == 34:
                self.is_summer = 0
                self.statbonus_global = 1.4
            if self.turn_num == 13 or self.turn_num == 18:
                for mycard in self.deck.cards:
                    mycard.bond += 5
                    if 79 < mycard.bond < 85:
                        mycard.turns_to_bond += self.turn_num + 1
            # inelegant, may want to fix this:
            self.consecutive_races = 2
            if self.turn_num > 25:
                self.energy = 100
            self.take_turn()
        addstats = 0
        for i in range(6):
            if i < 5:
                self.stats[i] = min(self.statcap, self.stats[i])
            addstats += math.floor(self.stats[i] * self.statweights_eval[i])

        if addstats > self.flat_cutoff:
            self.cutoff_trainings_done += 1
            self.totalstats += addstats
            for i in range(6):
                self.avgstats[i] += self.stats[i]
            self.avg_optional_races += self.optional_races_done
            self.score_list.append(addstats)
        if addstats > self.beststatsval:
            for i in range(6):
                self.beststats[i] = self.stats[i]
            self.beststatsval = addstats
        self.training_num += 1

    def do_training_GL(self):
        self.init_training()
        total_max_motiv_turns = 0

        for i in range(self.total_turns):
            self.global_friendb = 1+self.turn_num*0.6/75
            self.global_tokui = self.turn_num*40/75
            if self.turn_num == 31 or self.turn_num == 52:
                self.is_summer = 1
            elif self.turn_num == 35 or self.turn_num == 56:
                self.is_summer = 0
            self.take_turn()
            if self.turn_num > self.total_turns - self.senior_turns:
                for i in range(5):
                    for j in range(7):
                        self.senior_statgain[i][j] += self.temp_trainstats[i][j]
                for j in range(7):
                    self.senior_statgain[5][j] += self.temp_trainstats[6][j]
            if self.motiv == 0.2:
                total_max_motiv_turns += 1
            vocalstats = 5 + 5*self.did_rainbow
            randomstat = random.randint(0,4)
            self.stats[randomstat] += vocalstats
        addstats = 0
        # print(self.stats)
        for i in range(6):
            if i < 5:
                self.stats[i] = min(self.statcap, self.stats[i])
            addstats += math.floor(self.stats[i] * self.statweights_eval[i])

        if addstats > self.flat_cutoff:
            self.cutoff_trainings_done += 1
            self.totalstats += addstats
            for i in range(6):
                self.avgstats[i] += self.stats[i]
            self.avg_optional_races += self.optional_races_done
            self.score_list.append(addstats)
        if addstats > self.beststatsval:
            for i in range(6):
                self.beststats[i] = self.stats[i]
            self.beststatsval = addstats
        self.training_num += 1
        if self.documentation_true:
            self.event_turns.sort()
            print("")
            print("finished training")
            print("chains were on turns: ", self.event_turns)
            print("motivation was max for this many turns: ", total_max_motiv_turns)
            print("")

    def do_batch(self, report, totaltrains):
        self.senior_statgain = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        self.totaltrains = totaltrains
        self.init_batch()
        for i in range(self.totaltrains):
            self.do_training()
        self.score_list.sort()
        for i in range(6):
            for j in range(7):
                self.senior_statgain[i][j] = math.floor(10 * self.senior_statgain[i][j] / self.senior_turns / self.totaltrains) / 10
        if report == 1:
            print("used deck: ", [mycard.name for mycard in self.deck.cards])
            if self.flat_cutoff == 0:
                print("did a total number of trainings equal to: ", self.cutoff_trainings_done)
            else:
                print("a total number of trainings equal to: ", self.cutoff_trainings_done, " out of ", self.totaltrains, " made the cutoff")
                print("we only accepted trainings in the top ", self.score_cutoff * 100, "% of all trainings, with a flat score cutoff equal to: ", self.flat_cutoff)
            print("average rainbows done with each card: ", [math.floor(100 * card.rainbows_done_total / self.totaltrains) / 100 for card in self.deck.cards])
            print("average trainings done per category: ", [math.floor(100 * num / self.totaltrains) / 100 for num in self.average_trainings_done])
            print("average stat distribution: ", [math.floor(stat / self.cutoff_trainings_done) for stat in self.avgstats])
            print("average optional races done: ", math.floor(100 * self.avg_optional_races / self.cutoff_trainings_done) / 100)
            print("average total stats (weighted): ", math.floor(self.totalstats / self.cutoff_trainings_done))
            print("stats from the best run: ", self.beststats)
            if self.flat_cutoff == 0:
                print("score of percentile ", self.score_cutoff, " is equal to: ", self.score_list[math.floor(self.totaltrains * (1 - self.score_cutoff))])
            print("***********************")
            print("")
        elif report == 2:
            print("average total stats (weighted): ", math.floor(self.totalstats / self.cutoff_trainings_done))
        self.training_batch_num += 1

    def do_batch2(self, report, totaltrains, mandatory_stats, statweights_cutoff):
        self.totaltrains = totaltrains
        self.init_batch()
        cutoff_avgscore = 0
        missed_stats = [0, 0, 0, 0, 0, 0]

        for i in range(self.totaltrains):
            self.do_training2(mandatory_stats, statweights_cutoff)
            a = is_acceptable_stats(self.stats, [num - 25 for num in mandatory_stats], statweights_cutoff)
            for j in range(6):
                if self.stats[j] < mandatory_stats[j] - 25:
                    missed_stats[j] += 1
            if a > 0:
                ##                made_cutoff += 1
                cutoff_avgscore += a

        self.score_list.sort()
        if report == 1:
            print("used deck: ", [mycard.name for mycard in self.deck.cards])
            print("we set the mandatory stats to be attained as: ", mandatory_stats)
            print("the following amount of trainings made the mandatory stats: ", len(self.score_list), " out of ", self.totaltrains)
            if len(self.score_list) > 0:
                print("average overflow score for those trainings: ", math.floor(cutoff_avgscore / len(self.score_list) * 100) / 100)
            print("average stat distribution: ", [math.floor(stat / self.cutoff_trainings_done) for stat in self.avgstats])
            print(missed_stats)
            print("")
        self.training_batch_num += 1

    def do_batch_MANT(self, report, totaltrains):
        self.totaltrains = totaltrains
        self.init_batch()
        for i in range(self.totaltrains):
            self.do_training_MANT()
        self.score_list.sort()
        if report == 1:
            print("used deck: ", [mycard.name for mycard in self.deck.cards])
            if self.flat_cutoff == 0:
                print("did a total number of trainings equal to: ", self.cutoff_trainings_done)
            else:
                print("a total number of trainings equal to: ", self.cutoff_trainings_done, " out of ", self.totaltrains, " made the cutoff")
                print("we only accepted trainings in the top ", self.score_cutoff * 100, "% of all trainings, with a flat score cutoff equal to: ", self.flat_cutoff)
            print("average rainbows done with each card: ", [math.floor(100 * card.rainbows_done_total / self.totaltrains) / 100 for card in self.deck.cards])
            print("average trainings done per category: ", [math.floor(100 * num / self.totaltrains) / 100 for num in self.average_trainings_done])
            print("average stat distribution: ", [math.floor(stat / self.cutoff_trainings_done) for stat in self.avgstats])
            print("average optional races done: ", math.floor(100 * self.avg_optional_races / self.cutoff_trainings_done) / 100)
            print("average total stats (weighted): ", math.floor(self.totalstats / self.cutoff_trainings_done))
            print("stats from the best run: ", self.beststats)
            if self.flat_cutoff == 0:
                print("score of percentile ", self.score_cutoff, " is equal to: ", self.score_list[math.floor(self.totaltrains * (1 - self.score_cutoff))])
            print("***********************")
            print("")
        elif report == 2:
            print("average total stats (weighted): ", math.floor(self.totalstats / self.cutoff_trainings_done))
        self.training_batch_num += 1


    def do_batch_GL(self, report, totaltrains):
        self.senior_statgain = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        self.totaltrains = totaltrains
        self.init_batch()
        for i in range(self.totaltrains):
            self.do_training_GL()
        self.score_list.sort()
        for i in range(6):
            for j in range(7):
                self.senior_statgain[i][j] = math.floor(10 * self.senior_statgain[i][j] / self.senior_turns / self.totaltrains) / 10
        if report == 1:
            print("used deck: ", [mycard.name for mycard in self.deck.cards])
            if self.flat_cutoff == 0:
                print("did a total number of trainings equal to: ", self.cutoff_trainings_done)
            else:
                print("a total number of trainings equal to: ", self.cutoff_trainings_done, " out of ", self.totaltrains, " made the cutoff")
                print("we only accepted trainings in the top ", self.score_cutoff * 100, "% of all trainings, with a flat score cutoff equal to: ", self.flat_cutoff)
            print("average rainbows done with each card: ", [math.floor(100 * card.rainbows_done_total / self.totaltrains) / 100 for card in self.deck.cards])
            print("average trainings done per category: ", [math.floor(100 * num / self.totaltrains) / 100 for num in self.average_trainings_done])
            print("average stat distribution: ", [math.floor(stat / self.cutoff_trainings_done) for stat in self.avgstats])
            print("average optional races done: ", math.floor(100 * self.avg_optional_races / self.cutoff_trainings_done) / 100)
            print("average total stats (weighted): ", math.floor(self.totalstats / self.cutoff_trainings_done))
            print("stats from the best run: ", self.beststats)
            if self.flat_cutoff == 0:
                print("score of percentile ", self.score_cutoff, " is equal to: ", self.score_list[math.floor(self.totaltrains * (1 - self.score_cutoff))])
            print("***********************")
            print("")
        elif report == 2:
            print("average total stats (weighted): ", math.floor(self.totalstats / self.cutoff_trainings_done))
        self.training_batch_num += 1



