from umatier_classes import *


class Result_wrap:
    def __init__(self,card,totalscore,medianscore,avg_racestats):
        self.card = card
        self.totalscore = totalscore
        self.medianscore = medianscore
        self.avg_racestats = avg_racestats


def totalscore_func(result):
    return -1 * result.totalscore


class Output_wrap:
    def __init__(self,name,inideck,scenario,trainingnum):
        self.name = name
        self.inideck = inideck
        self.results = []
        self.scenario = scenario
        self.trainingnum = trainingnum

    def add_result(self,result):
        self.results.append(result)

    def order_results(self,style):
        self.results.sort(key=totalscore_func)


def umatier_write_output(output_wrap):
    f = open("output_" + output_wrap.name + ".html","w")
    f.write('<!DOCTYPE html> <html> <head> <style> .imgContainer{ float:left; padding:10px } </style> </head> <body> <h1>Uma Musume training simulator output</h1> <p>The following 5 cards were put in the deck:</p> <div class="image123">')
    for card in output_wrap.inideck.cards:
        f.write('<div class="imgContainer"> <img src="cardImages\support_card_s_')
        f.write(str(card.id))
        f.write('.png"/ height="100" width="100"/><figcaption>')
        f.write(card.name.replace('*',''))
        f.write('</figcaption> </div>')
    f.write('<div style="clear:both"/> </div> ')
    f.write('<p> The scenario used was: ' + output_wrap.scenario + '</p>')
    f.write('<p> Total trainings done per deck: ' + str(output_wrap.trainingnum) + '</p>')
    f.write('<p> The following cards were ranked based on how well they perform as the last card in the deck: <p>')
    f.write('<div class="image123">')

    output_wrap.order_results(1)

    for result in output_wrap.results:
        f.write('<div class="imgContainer"> <img src="cardImages\support_card_s_')
        f.write(str(result.card.id))
        f.write('.png"/ height="100" width="100"/><figcaption>')
        f.write(result.card.name.replace('*',''))
        f.write('<br>')
        f.write(str(result.totalscore))
        # f.write('<br> <p> Median score: </p>')
        # f.write('<p>' + str(result.medianscore) + '</p>')
        f.write('<br> <p> Avg statgain <br>from training: </p>')
        f.write('<p>' + str(math.floor(result.card.training_statgain / output_wrap.trainingnum * 10) / 10) + '</p>')
        f.write('<br> <p> Rainbow only: </p>')
        f.write('<p>' + str(math.floor(result.card.rainbow_statgain / output_wrap.trainingnum * 10) / 10) + '</p>')
        f.write('<br> <p> Rainbows done: </p>')
        f.write('<p>' + str(math.floor(result.card.rainbows_done_total / output_wrap.trainingnum * 10) / 10) + ' / ' + str(math.floor(result.card.rainbows_available_total / output_wrap.trainingnum * 10) / 10) + '</p>')
        f.write('<br> <p> Turns to bond: </p>')
        f.write('<p>' + str(math.floor(result.card.turns_to_bond / output_wrap.trainingnum * 10) / 10) + '</p>')
        f.write('<br> <p> Race stats: </p>')
        f.write('<p>' + str(math.floor(result.avg_racestats * 10) / 10) + '</p>')
        f.write('</figcaption> </div>')
    f.write('<div style="clear:both"/> </div> </body> </html>')
    f.close()


def umatier_write_output2(output_wrap):
    f = open("output_" + output_wrap.name + ".html","w")
    f.write('<!DOCTYPE html> <html> <head> <style> .imgContainer{ float:left; padding:10px } </style> </head> <body> <h1>Uma Musume training simulator output</h1> <p>The following 5 cards were put in the deck:</p> <div class="image123">')
    for card in output_wrap.inideck.cards:
        f.write('<div class="imgContainer"> <img src="cardImages\support_card_s_')
        f.write(str(card.id))
        f.write('.png"/ height="100" width="100"/><figcaption>')
        f.write(card.name.replace('*',''))
        f.write('</figcaption> </div>')
    f.write('<div style="clear:both"/> </div> ')
    f.write('<p> The scenario used was: ' + output_wrap.scenario + '</p>')
    f.write('<p> Total trainings done per deck: ' + str(output_wrap.trainingnum) + '</p>')
    f.write('<p> The following cards were ranked based on how well they perform as the last card in the deck: <p>')
    f.write('<div class="image123">')

    output_wrap.order_results(1)

    for result in output_wrap.results:
        f.write('<div class="imgContainer"> <img src="cardImages\support_card_s_')
        f.write(str(result.card.id))
        f.write('.png"/ height="100" width="100"/><figcaption>')
        f.write(result.card.name.replace('*',''))
        f.write('<br>')
        f.write(str(math.floor(10 * result.totalscore) / 10))
        f.write('<br> <p> Median score: </p>')
        f.write('<p>' + str(result.medianscore) + '</p>')
        f.write('<p> Avg statgain <br>from training: </p>')
        f.write('<p>' + str(math.floor(result.card.training_statgain / output_wrap.trainingnum * 10) / 10) + '</p>')
        f.write('<p> Rainbow only: </p>')
        f.write('<p>' + str(math.floor(result.card.rainbow_statgain / output_wrap.trainingnum * 10) / 10) + '</p>')
        f.write('<p> Rainbows done: </p>')
        f.write('<p>' + str(math.floor(result.card.rainbows_done_total / output_wrap.trainingnum * 10) / 10) + ' / ' + str(math.floor(result.card.rainbows_available_total / output_wrap.trainingnum * 10) / 10) + '</p>')
        f.write('<p> Turns to bond: </p>')
        f.write('<p>' + str(math.floor(result.card.turns_to_bond / output_wrap.trainingnum * 10) / 10) + '</p>')
        f.write('<p> Race stats: </p>')
        f.write('<p>' + str(math.floor(result.avg_racestats * 10) / 10) + '</p>')
        f.write('</figcaption> </div>')
    f.write('<div style="clear:both"/> </div> </body> </html>')
    f.close()
