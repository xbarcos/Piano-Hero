from PPlay.window import *
from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.sound import *
from PPlay.mouse import *
import time
import globals

def notasMusica():
    notas = []
    f = open('music.txt', 'r')
    lines = f.readlines()
    for line in lines:
        x, y = line.strip().split(',')
        x = int(x)
        y = int(y)
        notas.append(criar_nota((x,y)))
    return notas

def totalNotas():
    count = 0
    f = open('music.txt', 'r')
    lines = f.readlines()
    for line in lines:
        count += 1
    return count

def criar_nota(posicao):
    nota = Sprite("nota2.png")
    nota.set_position(posicao[0] - nota.width / 2, posicao[1])
    nota.set_total_duration(1000)
    return nota

largura_janela = 1280
altura_janela = 720
janela = Window(largura_janela, altura_janela)
janela.set_title("Piano Hero")
background = Sprite("background2.jpg")
fundo = Sprite("fundo.png")
musica = Sound("zelda-lullaby.ogg")
finale = Sound("applause-4.ogg")
pad = Sprite("pad.png", 2)
pad_animado = Sprite("pad_animado.png", 2)
play = Sprite("menu_play.png", 1)
play.x = janela.width/2 - play.width/2
play.y = janela.height/2 - play.height/2 + 250
play_hover = Sprite("menu_play_hover.png", 1)
play_hover.x = play.x
play_hover.y = play.y
menu_bg = Sprite("menu-bg.png",1)


pad.set_total_duration(1000)

pos_padX = 500
pos_padY = 600
linha = Sprite("linha.png")
linha.set_position(498, 0)
linha2 = Sprite("linha.png")
linha2.set_position(498+70, 0)
linha3 = Sprite("linha.png")
linha3.set_position(498+140, 0)
linha4 = Sprite("linha.png")
linha4.set_position(498+210, 0)
linha5 = Sprite("linha.png")
linha5.set_position(498+280, 0)
posicoes_pads = [(pos_padX, pos_padY), (pos_padX+70, pos_padY), (pos_padX+140, pos_padY), (pos_padX+210, pos_padY), (pos_padX+280, pos_padY)]
tempo_inicial = time.time()
count = 0
teclado = Keyboard()
mouse = Mouse()
teclada = False
pontuacao = 0
total_notas = totalNotas()
inicio_musica = False
notas = notasMusica()
inicio = True
count_tecla = 0
pontos = 0
while True:
    if globals.GAME_STATE == 0:
        menu_bg.draw()
        play.draw()
        if globals.HELPER:
            janela.draw_text("Pad 1 - Botão 1", 10, 10, size=20, color=(255, 255, 255))
            janela.draw_text("Pad 2 - Botão 2", 10, 40, size=20, color=(255, 255, 255))
            janela.draw_text("Pad 3 - Botão 3", 10, 70, size=20, color=(255, 255, 255))
            janela.draw_text("Pad 4 - Botão 4", 10, 100, size=20, color=(255, 255, 255))
            janela.draw_text("Pad 5 - Botão 5", 10, 130, size=20, color=(255, 255, 255))
    if mouse.is_over_object(play):
        play_hover.draw()
        if mouse.is_button_pressed(1):
            globals.GAME_STATE = 1
    if globals.GAME_STATE == 1:
        if inicio_musica == False:
            if notas[0].y > janela.height - notas[0].height - 80:
                musica.play()
                inicio_musica = True
        for i in range(5):
            if teclado.key_pressed(str(i+1)):
                for nota in notas:
                    if nota.y > janela.height - nota.height - 80 and abs(nota.x - posicoes_pads[i][0])+30:
                        pontuacao += 1
                        pontos += 1332
                        notas.remove(nota)

        for nota in notas:
            nota.move_y(200 * janela.delta_time())
            if nota.y > janela.height:
                notas.remove(nota)

        background.draw()
        fundo.draw()
        linha.draw()
        linha2.draw()
        linha3.draw()
        linha4.draw()
        linha5.draw()

        for i in range(5):
            pad.set_position(posicoes_pads[i][0] - pad.width / 2, posicoes_pads[i][1])
            pad_animado.set_position(posicoes_pads[i][0] - pad.width / 2, posicoes_pads[i][1])
            pad.update()
            pad.draw()
            if teclado.key_pressed(str(i+1)):
                pad_animado.draw()

        for nota in notas:
            nota.update()
            nota.draw()

        janela.draw_text("Pontuação: {}".format(pontos), 1070, 10, size=30, color=(255, 255, 255))
        janela.draw_text(globals.MUSIC_NAME, 10, 10, size=30, color=(255, 255, 255))
        janela.draw_text("{}%".format(round(pontuacao / total_notas*100)), 10, 40, size=30, color=(255, 255, 255))

        count += 1
        if count == 70:
            teclada = False
            count = 0
        if notas == [] and not musica.is_playing():
            globals.GAME_STATE = 2
            inicio = True
    if globals.GAME_STATE == 2:
        if inicio == True:
            musica.stop()
            finale.play()
            janela = Window(1280,720)
            janela.set_title("Piano Hero")
            janela.draw_text(globals.MUSIC_NAME, (janela.width/2) - 150, janela.height/2 - 300, size=60, color=(255, 255, 255))
            janela.draw_text("{} Pontos".format(pontos), (janela.width/2)-80, janela.height/2 , size=40, color=(255, 255, 255))
            janela.draw_text("{}%".format(round(pontuacao / total_notas*100),1), (janela.width/2)-25, janela.height/2 + 100, size=40, color=(255, 255, 255))
            inicio = False
    if globals.DEBUG:
        janela.draw_text("DEBUG MODE", 1150, 690, size=20, color=(255, 0, 0))

    if teclado.key_pressed('V'):
        if count_tecla >= 100:
            teclada = True
        if globals.DEBUG:
            if teclada:
                globals.DEBUG = False
                teclada = False
                count_tecla = 0
        else:
            if teclada:
                globals.DEBUG = True
                teclada = False
                count_tecla = 0
    if teclado.key_pressed('H'):
        if count_tecla >= 100:
            teclada = True
        if globals.HELPER:
            if teclada:
                globals.HELPER = False
                teclada = False
                count_tecla = 0
        else:
            if teclada:
                globals.HELPER = True
                teclada = False
                count_tecla = 0
    janela.update()
    count_tecla += 1


