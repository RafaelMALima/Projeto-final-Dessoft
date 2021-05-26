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
    def __init__ (self, x, y):
        self.imagens_direita = []
        self.imagens_esquerda = []
        self.index = 0
        self.counter = 0
        for num in range(1, 18):
            lugar = "Assets/w{0}.png".format(num)
            print (lugar)
            img_direita = pygame.image.load(lugar)
            img_direita = pygame.transform.scale(img_direita, (40,80))
            img_esquerda = pygame.transform.flip(img_direita, True, False)
            self.imagens_direita.append(img_direita)
            self.imagens_esquerda.append(img_esquerda)
        self.image = self.imagens_direita[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.altura = self.image.get_height()
        self.largura = self.image.get_width()
        self.vel_y = 0
        self.pula = True
        self.direcao = 0
        
    def update(self):
    
        dx = 0
        dy = 0
        cooldown_andar = 5

      # teclas pressionadas
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.pula == False:
            self.vel_y = -15
            self.pula = True
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direcao = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direcao = 1
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.counter = 0
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

        #checa colisões
        for casa in mundo.lista_casas:
            #na direcao x
            if casa[1].colliderect(self.rect.x +dx ,self.rect.y ,self.largura,self.altura):
                dx = 0
            #na direção y
            if casa[1].colliderect(self.rect.x,self.rect.y + dy,self.largura,self.altura):
                #se bate a cabeca
                if self.vel_y < 0:
                    dy = casa[1].bottom - self.rect.top
                    self.vel_y = 0
                #se cai no chao
                elif self.vel_y >= 0:
                    dy = casa[1].top - self.rect.bottom
                    self.pula = False
        

        # atualiza a posicao do jogador
        self.rect.x += dx
        self.rect.y += dy

        # controla animação
        if self.counter > cooldown_andar:
            self.counter = 0        
            self.index += 1
            if self.index >= len(self.imagens_direita):
                self.index = 0
            if self.direcao == 1:
                self.image = self.imagens_direita[self.index] 
            if self.direcao == -1:
                self.image = self.imagens_esquerda[self.index] 


        #desenha o personagem na tela
        tela.blit(self.image, self.rect)
        
    
    
bruxo_group = pygame.sprite.Group()             
        
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
                if casa == 3:
                    bruxo = Inimigo(conta_colunas * tamanho_casa, conta_linhas * tamanho_casa-50)
                    bruxo_group.add(bruxo)
                conta_colunas += 1
            conta_linhas += 1
    def desenha(self):
        for casa in self.lista_casas:
            tela.blit(casa[0],casa[1])
# carrega um inimigo, com movimentações e o gera na tela, apenas adicionar a imagem do inimigo(bruxo)
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        for i in range(1,6):
            imagem_mago = pygame.image.load("Assets/mago{0}.png".format(i))
            self.image = pygame.transform.scale(imagem_mago,(60,100))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.muda_direcao = 1
            self.contador_muda_direcao = 0
    
    def update(self):
        self.rect.x += self.muda_direcao
        self.contador_muda_direcao += 1
        if abs(self.contador_muda_direcao) > 50:
            self.muda_direcao *= -1
            self.contador_muda_direcao *= -1




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
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]
mundo = Mundo(mapa)
jogador= Jogador(100,altura - 130)



jogo = True
while jogo == True:
    
    clock.tick(fps)
    tela.blit(fundo,(0,0))
    
    
    #desenha_grade()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo = False
    mundo.desenha()
    bruxo_group.draw(tela)
    bruxo_group.update()
    jogador.update()
    pygame.display.update()

pygame.quit()