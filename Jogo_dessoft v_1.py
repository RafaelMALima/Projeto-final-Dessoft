import pygame
from pygame.locals import *

pygame.init()

#resolução do jogo
largura = 1500
altura = 1000

tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption("Projeto Dessoft")
#carrega imagens

fundo = pygame.image.load("Assets/fundo.png")
fundo = pygame.transform.scale(fundo,(largura,altura))

#define o tamanho das casas
tamanho_casa = 50

#desenha a grade com cada casa tendo o tamanho definidas. Usar para ver ser as dimensões da grade, não precisa rodar a função na hora
def desenha_grade():
    for linha in range(0,30):
        pygame.draw.line(tela, (255,255,255),(0,linha*tamanho_casa),(largura,linha*tamanho_casa))
        pygame.draw.line(tela, (255,255,255),(linha*tamanho_casa,0),(linha*tamanho_casa,altura))

#carrega um dado mapa, e coloca-o na tela. Para adicionar novas coisas ao mapa, basta carregar a imagem, copiar e colar o cófigo da linha 36 à 42, trocando o if por elif, trocar o nome da imagem transformada e adicionar um número correspondente. 
class Mundo():
    def __init__(self,data):
        self.lista_casas = []
        #carrega os assets do mundo
        imagem_chao = pygame.image.load("Assets/bloco_chao.png")
        conta_linhas = 0
        for linha in data:
            conta_colunas = 0
            for casa in linha:
                if casa == 1:
                    img = pygame.transform.scale(imagem_chao,(tamanho_casa,tamanho_casa))
                    img_retangulo = img.get_rect()
                    img_retangulo.x = conta_colunas*tamanho_casa
                    img_retangulo.y = conta_linhas*tamanho_casa
                    casa = (img,img_retangulo)
                    self.lista_casas.append(casa)
                conta_colunas += 1
            conta_linhas += 1
    def draw(self):
        for casa in self.lista_casas:
            tela.blit(casa[0],casa[1])

#Define um mapa para ser usado. Para mais mapas, basta criar novas listas disto, e modificálas de acordo.
mapa = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]
mundo = Mundo(mapa)


jogo = True

while jogo == True:
    tela.blit(fundo,(0,0))
    desenha_grade()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo = False
    mundo.draw()
    pygame.display.update()

pygame.quit()
