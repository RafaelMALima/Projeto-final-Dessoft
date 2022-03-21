import pygame

clock = pygame.time.Clock()
fps = 60

# resolução do jogo
largura = 1500
altura = 1000

tela = pygame.display.set_mode((largura, altura))

# fonte de texto
fonte_grande = pygame.font.SysFont('Bauhaus 93', 70)
fonte_pequena = pygame.font.SysFont('Bauhaus 93', 30)
fonte_enorme = pygame.font.SysFont("Bauhaus 93", 97)
# define o tamanho das casas
tamanho_casa = 50
fim_de_jogo = 0
menu_principal = True
fase = 1
maximo_de_fases = 3

# cores
branco = (255, 255, 255)
azul = (0, 0, 255)
vermelho = (0, 255, 0)

# declara os grupos pros sprites
grupo_espinho = pygame.sprite.Group()
grupo_inimigo = pygame.sprite.Group()
grupo_saida = pygame.sprite.Group()
grupo_gato = pygame.sprite.Group()

# carrega as imagens
fundo = pygame.image.load("Assets/Fundos/castle.jpg")
fundo = pygame.transform.scale(fundo, (largura, altura))
imagem_restart = pygame.image.load("Assets/morte.png")
imagem_start = pygame.image.load('Assets/comece.png')
imagem_exit = pygame.image.load('Assets/sair.png')
imagem_do_botao = imagem_restart

jogador = Jogador(100, altura - 130)

# carrega uma fase e cria o mundo
mapa = []

mundo = Mundo(mapa)

# cria botões
botao_reinicia = botao(largura / 2 - 200, altura / 2 - 50, imagem_restart)
imagem_do_botao = imagem_start
botao_inicia = botao(largura // 2 - 350, altura // 2, imagem_start)
imagem_do_botao = imagem_exit
botao_saida = botao(largura // 2 + 150, altura // 2, imagem_exit)

jogo = True
