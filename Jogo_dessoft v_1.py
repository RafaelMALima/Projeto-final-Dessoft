import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

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

class Jogador ():
    def__init__ (self, x, y):
        self.imagens_direita = []
        self.imagens_esquerda = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_direita = pygame.image.load(f'img/guy{num}.png')
            img_direita = pygame.tranform.scale(img_direita, (40,80))
            img_direita = pygame.transform.flip(img_direita, True, False)
            self.imagens_direita.append(img_direita)
            self.imagens_esquerda.append(img_esquerda)
        self.image = self.imagens_direita[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.pular = False
        self.direcao = 0
        
def atualiza(self):
    dx = 0
    dy = 0
    cooldown_andar = 5
    # teclas pressionadas
    key = pygame.key.get_pressed()
    if key[pygame.K_SAPCE] and self.pular == False:
        self.vel_y = -15
        self.pular = True
    if key[pygame.K_SPACE] == False:
        self.pular = False
    if key[pygame.K_ESQUERDA]:
        dx -= 5
        self.counter += 1
        self.direcao = -1
    if key[pygame.K_DIREITA]:
        dx += 5
        self.counter += 1
        self.direcao = 1
    if key[pygame.K_ESQUERDA] == False and key[pygame.K_DIREITA] == False:
        self.counter = 0
        self.index = 0
        if self.direcao == 1:
            self.image = self.imagens_direita[self.index] 
        if self.direcao == -1:
            self.image = self.imagens_esquerda[self.index] 
        
    # controla animação
    if self.counter > cooldown_andar:
        self.counter = 0        self.index += 1
        if self.index >= len(self.imagens_direita):
            self.index = 0
        if self.direcao == 1:
            self.image = self.imagens_direita[self.index] 
        if self.direcao == -1:
            self.image = self.imagens_esquerda[self.index] 
    # adiciona gravidade
    self.vel_y += 1
    if self.vel_y > 10:
        self.vel_y = 10
    dy += self.vel_y
        
    
    
             
        
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
jogador= Jogador(100,screen_height - 130)

jogo = True


while jogo == True:
    clock.tick(fps)
    tela.blit(fundo,(0,0))
    desenha_grade()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo = False
    mundo.draw()
    pygame.display.update()

pygame.quit()
