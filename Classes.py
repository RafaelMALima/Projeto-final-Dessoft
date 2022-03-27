import pygame
import Funcoes
import Constantes
pygame.init()


class Botao():
    def __init__(self, x, y, image):

        self.imagem = Constantes.imagem_do_botao
        self.imagem = pygame.transform.scale(self.imagem, (400, 100))
        self.rect = self.imagem.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicou = False

    def desenha(self):
        reinicia = False

        # calcula a posicao do mouse
        posicao = pygame.mouse.get_pos()

        # verifica se o mouse está na posição
        if self.rect.collidepoint(posicao):
            if pygame.mouse.get_pressed()[0] == 1:
                reinicia = True

                # desenha
        Constantes.tela.blit(self.imagem, self.rect)

        return reinicia

class Jogador():
    def __init__(self, x, y):
        self.imagens_direita = []
        self.imagens_esquerda = []
        self.index = 0
        self.counter = 0
        for num in range(1, 18):
            lugar = "Assets/w{0}.png".format(num)
            img_direita = pygame.image.load(lugar)
            img_direita = pygame.transform.scale(img_direita, (40, 80))
            img_esquerda = pygame.transform.flip(img_direita, True, False)
            self.imagens_direita.append(img_direita)
            self.imagens_esquerda.append(img_esquerda)
        self.morto = pygame.image.load('Assets/fantasma.png')
        self.morto = pygame.transform.scale(self.morto, (40, 80))
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
            if key[pygame.K_p] == True:
                Funcoes.pause()

            # adiciona gravidade
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # checa colisões
            for casa in Constantes.mundo.lista_casas:
                # na direcao x
                if casa[1].colliderect(self.rect.x + dx, self.rect.y, self.largura, self.altura):
                    dx = 0
                # na direção y
                if casa[1].colliderect(self.rect.x, self.rect.y + dy, self.largura, self.altura):
                    # se bate a cabeca
                    if self.vel_y < 0:
                        dy = casa[1].bottom - self.rect.top
                        self.vel_y = 0
                    # se cai no chao
                    elif self.vel_y >= 0:
                        dy = casa[1].top - self.rect.bottom
                        self.pula = False

            # checar para colisoes com inimigos
            if pygame.sprite.spritecollide(self,    Constantes.grupo_inimigo, False):
                fim_de_jogo = -1
            # checar para colisoes com inimigos
            if pygame.sprite.spritecollide(self, Constantes.grupo_espinho, False):
                fim_de_jogo = -1
                print(fim_de_jogo)
            # checar para colisoes com a saida
            if pygame.sprite.spritecollide(self, Constantes.grupo_saida, False):
                fim_de_jogo = 1
                self.rect.x = 100
                self.rect.y = 900
            if pygame.sprite.spritecollide(self, Constantes.grupo_gato, False):
                fim_de_jogo = 2

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
            Funcoes.desenha_texto('GAME OVER...', Constantes.fonte_grande, Constantes.azul, (Constantes.largura // 2) - 200, Constantes.altura // 3)
            if self.rect.y > 200:
                self.rect.y -= 5

        # desenha o personagem na tela
        Constantes.tela.blit(self.image, self.rect)

        return fim_de_jogo

# carrega um dado mapa, e coloca-o na tela. Para adicionar novas coisas ao mapa, basta carregar a imagem, copiar e colar o cófigo da linha 36 à 42, trocando o if por elif, trocar o nome da imagem transformada e adicionar um número correspondente.
class Mundo():
    def __init__(self, data):
        self.lista_casas = []
        # carrega os assets do mundo
        imagem_chao = pygame.image.load("Assets/bloco_chao.png")
        conta_linhas = 0
        for linha in data:
            conta_colunas = 0
            for casa in linha:
                if casa == 1:
                    img = pygame.transform.scale(imagem_chao, (Constantes.tamanho_casa, Constantes.tamanho_casa))
                    img_retangulo = img.get_rect()
                    img_retangulo.x = conta_colunas * Constantes.tamanho_casa
                    img_retangulo.y = conta_linhas * Constantes.tamanho_casa
                    casa = (img, img_retangulo)
                    self.lista_casas.append(casa)
                if casa == 3:
                    bruxo = Inimigo(conta_colunas * Constantes.tamanho_casa, conta_linhas * Constantes.tamanho_casa - 50)
                    Constantes.grupo_inimigo.add(bruxo)
                if casa == 6:
                    espinho = Espinhos(conta_colunas * Constantes.tamanho_casa, conta_linhas * Constantes.tamanho_casa + (Constantes.tamanho_casa // 2))
                    Constantes.grupo_espinho.add(espinho)
                if casa == 8:
                    saida = Saida(conta_colunas * Constantes.tamanho_casa, conta_linhas * Constantes.tamanho_casa - (Constantes.tamanho_casa // 2))
                    Constantes.grupo_saida.add(saida)
                conta_colunas += 1
                if casa == 9:
                    gato = Gato(conta_colunas * Constantes.tamanho_casa, conta_linhas * Constantes.tamanho_casa + 10)
                    Constantes.grupo_gato.add(gato)
            conta_linhas += 1

    def desenha(self):
        for casa in self.lista_casas:
            Constantes.tela.blit(casa[0], casa[1])


# carrega um inimigo, com movimentações e o gera na tela, apenas adicionar a imagem do inimigo(bruxo)
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.imagens = []
        self.imagens_invertidas = []
        for i in range(1, 6):
            imagens_mago = pygame.image.load("Assets/mago{0}.png".format(i))
            imagens_mago = pygame.transform.scale(imagens_mago, (70, 100))
            self.imagens.append(imagens_mago)
        for i in range(len(self.imagens)):
            self.imagens_invertidas.append(pygame.transform.flip(self.imagens[i], True, False))
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
                self.indice += 1
            else:
                self.indice = 0
            self.timer = 0
        self.timer += 1
        if abs(self.contador_muda_direcao) > 50:
            # após certo tempo se passar, representado pelo timer, o inimigo irá se virar, mudando a direção que ele anda
            self.muda_direcao *= -1
            self.contador_muda_direcao *= -1
            self.image = pygame.transform.flip(self.image, True, False)


# Essa classe representa os espinhos, que matam o jogador caso ele pise neles
class Espinhos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        imagem_espinho = pygame.image.load("Assets/espinhos.png")
        self.image = pygame.transform.scale(imagem_espinho, (Constantes.tamanho_casa, Constantes.tamanho_casa // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Essa classe representa a saída de cada nível, e é representada no jogo por uma porta
class Saida(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        imagem_saida = pygame.image.load("Assets/porta_castelo.png")
        self.image = pygame.transform.scale(imagem_saida, (Constantes.tamanho_casa, int(Constantes.tamanho_casa * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Gato(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        imagem_gato = pygame.image.load("Assets/gatinho.png")
        self.image = pygame.transform.scale(imagem_gato, (Constantes.tamanho_casa, int(Constantes.tamanho_casa * 0.8)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
