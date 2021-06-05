import pygame
from pygame.locals import *
import json
from pygame import mixer
from os import path


pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

#resolução do jogo
largura = 1500
altura = 1000

tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption("Projeto Dessoft")

#fonte de texto
fonte_grande= pygame.font.SysFont('Bauhaus 93', 70)
fonte_pequena= pygame.font.SysFont('Bauhaus 93', 30)

#define o tamanho das casas
tamanho_casa = 50
fim_de_jogo = 0
menu_principal = True
fase = 1
maximo_de_fases = 3

#cores
branco= (255, 255, 255)
azul =(0,0,255)

#carrega imagens
grupo_espinho = pygame.sprite.Group()
grupo_inimigo = pygame.sprite.Group()
grupo_saida = pygame.sprite.Group() 

fundo = pygame.image.load("Assets/Fundos/castle.jpg")
fundo = pygame.transform.scale(fundo,(largura,altura))
imagem_restart = pygame.image.load("Assets/morte.png")
imagem_start = pygame.image.load('Assets/comece.png')
imagem_exit = pygame.image.load('Assets/sair.png')
imagem_do_botao = imagem_restart

#musica tematica
pygame.mixer.music.load('Assets/Musica_jogo.mp3')
pygame.mixer.music.play (-1, 0.0, 5000)
mixer.music.set_volume(0.5)

# funcoes para reiniciar fases
def reinicia_fase(fase):
    jogador = Jogador(100, altura - 130)
    grupo_inimigo.empty()
    grupo_espinho.empty()
    grupo_saida.empty()
    #carrega uma fase e cria o mundo
    mapa = []
    if path.exists(f'fase{fase}'):
        with open(f'fase{fase}', 'rb') as json_in:
            mapa = json.load(json_in)
    mundo = Mundo(mapa)

    return mundo

#funcao colocar texto
def desenha_texto (texto, fonte, cor_texto, x, y):
    img = fonte.render(texto, True, cor_texto)
    tela.blit(img,(x, y))


class botao():
    def __init__(self,x,y,image):
        
        self.imagem = imagem_do_botao
        self.imagem = pygame.transform.scale(self.imagem,(400,100))
        self.rect = self.imagem.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicou = False

    def desenha(self):
        reinicia = False

        #calcula a posicao do mouse
        posicao = pygame.mouse.get_pos()

        #verifica se o mouse está na posição
        if self.rect.collidepoint(posicao):
            if pygame.mouse.get_pressed()[0] == 1:
                reinicia = True 

        #desenha
        tela.blit(self.imagem, self.rect)

        return reinicia

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
            img_direita = pygame.image.load(lugar)
            img_direita = pygame.transform.scale(img_direita, (40,80))
            img_esquerda = pygame.transform.flip(img_direita, True, False)
            self.imagens_direita.append(img_direita)
            self.imagens_esquerda.append(img_esquerda)
        self.morto = pygame.image.load ('Assets/fantasma.png')
        self.morto = pygame.transform.scale(self.morto,(40,80))
        self.image = self.imagens_direita[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.altura = self.image.get_height()
        self.largura = self.image.get_width()
        self.vel_y = 0
        self.pula = True
        self.direcao = 0

        
    def update(self, fim_de_jogo):
    
        dx = 0
        dy = 0
        cooldown_andar = 5

        if fim_de_jogo == 0:
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

            #checar para colisoes com inimigos
            if pygame.sprite.spritecollide(self, grupo_inimigo, False):
                fim_de_jogo = -1
            #checar para colisoes com inimigos
            if pygame.sprite.spritecollide(self, grupo_espinho, False):
                fim_de_jogo = -1
                print (fim_de_jogo)
            #checar para colisoes com a saida
            if pygame.sprite.spritecollide(self, grupo_saida, False):
                fim_de_jogo = 1
                self.rect.x = 100
                self.rect.y = 900

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


        elif fim_de_jogo == -1:
            self.image = self.morto
            desenha_texto('GAME OVER...', fonte_grande, azul, (largura//2)-200, altura//3)
            if self.rect.y > 200 :
                self.rect.y -= 5

        #desenha o personagem na tela
        tela.blit(self.image, self.rect)

        return fim_de_jogo


        
    
                
        
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
                    grupo_inimigo.add(bruxo)
                if casa == 6:
                    espinho =Espinhos(conta_colunas * tamanho_casa, conta_linhas * tamanho_casa + (tamanho_casa//2))
                    grupo_espinho.add (espinho)
                if casa == 8:
                    saida = Saida(conta_colunas * tamanho_casa, conta_linhas * tamanho_casa - (tamanho_casa // 2))
                    grupo_saida.add(saida)
                conta_colunas += 1
            conta_linhas += 1   

    def desenha(self):
        for casa in self.lista_casas:
            tela.blit(casa[0],casa[1])
# carrega um inimigo, com movimentações e o gera na tela, apenas adicionar a imagem do inimigo(bruxo)
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.imagens = []
        self.imagens_invertidas = []
        for i in range(1,6):
            imagens_mago = pygame.image.load("Assets/mago{0}.png".format(i))
            imagens_mago = pygame.transform.scale(imagens_mago,(70,100))
            self.imagens.append(imagens_mago)
        for i in range (len(self.imagens)):
            self.imagens_invertidas.append(pygame.transform.flip(self.imagens[i],True,False))
        self.indice = 0
        self.image = self.imagens[self.indice]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.muda_direcao = 1
        self.contador_muda_direcao = 0
        self.timer = 0

    def update(self):
        self.rect.x += self.muda_direcao
        self.contador_muda_direcao += 1
        if self.timer == 15:
            if self.muda_direcao > 0:
                self.image = self.imagens[self.indice]
            else:
                self.image = self.imagens_invertidas[self.indice]
            if self.indice < len(self.imagens) - 1:
                self.indice +=1
            else:
                self.indice = 0
            self.timer = 0
        self.timer += 1
        if abs(self.contador_muda_direcao) > 50:
            self.muda_direcao *= -1
            self.contador_muda_direcao *= -1
            self.image = pygame.transform.flip(self.image, True, False)

class Espinhos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        imagem_espinho = pygame.image.load("Assets/espinhos.png")
        self.image = pygame.transform.scale(imagem_espinho, (tamanho_casa, tamanho_casa //2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Saida(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        imagem_espinho = pygame.image.load("Assets/porta_castelo.png")
        self.image = pygame.transform.scale(imagem_espinho, (tamanho_casa, int(tamanho_casa * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

jogador= Jogador(100,altura - 130)

#carrega uma fase e cria o mundo
mapa = []
if path.exists(f'fase{fase}'):
    with open(f'fase{fase}', 'rb') as json_in:
        mapa = json.load(json_in)
mundo = Mundo(mapa)

# cria botões
botao_reinicia = botao(largura/ 2 - 200, altura/ 2 -50, imagem_restart)
imagem_do_botao = imagem_start
botao_inicia = botao(largura // 2 - 350, altura // 2, imagem_start)
imagem_do_botao = imagem_exit
botao_saida = botao(largura // 2 + 150, altura // 2, imagem_exit)


jogo = True
while jogo == True:
    
    clock.tick(fps)

    tela.blit(fundo,(0,0))

    if menu_principal == True:
        if botao_saida.desenha():
            jogo = False
        if botao_inicia.desenha():
            menu_principal = False
    else:
        mundo.desenha()

        if fim_de_jogo == 0:
            grupo_inimigo.update()

        grupo_inimigo.draw(tela)
        grupo_inimigo.update()
        grupo_espinho.draw(tela)
        grupo_saida.draw(tela)

        fim_de_jogo = jogador.update(fim_de_jogo)
        # se o jogador morrer
        if fim_de_jogo == -1:
            if botao_reinicia.desenha():
                mapa = []
                mundo = reinicia_fase(fase)
                fim_de_jogo = 0
                jogador= Jogador(100,altura - 130)

        # se o jogador completar a fase
        if fim_de_jogo == 1:
            # reinicia o jogo a avança para o próximo nível
            fase += 1
            if fase <= maximo_de_fases:
                # reinicia fase
                mapa = []
                mundo = reinicia_fase(fase)
                fim_de_jogo = 0
                jogador= Jogador(100,altura - 130)
            else:
                if botao_reinicia.desenha():
                    fase = 1
                    # reinicia fase
                    mapa = []
                    mundo = reinicia_fase(fase)
                    fim_de_jogo = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo = False



    pygame.display.update()

pygame.quit()
