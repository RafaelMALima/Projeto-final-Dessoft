import pygame
import Constantes
import Classes
import json
from os import path
pygame.init()

# funcoes para reiniciar fases
def reinicia_fase(fase):
    Constantes.jogador = Classes.Jogador(100, Constantes.altura - 130)
    Constantes.grupo_inimigo.empty()
    Constantes.grupo_espinho.empty()
    Constantes.grupo_saida.empty()
    # carrega uma fase e cria o mundo
    mapa = []
    if path.exists(f'fase{fase}'):
        with open(f'fase{fase}', 'rb') as json_in:
            mapa = json.load(json_in)
    mundo = Classes.Mundo(mapa)

    return mundo


# funcao colocar texto
def desenha_texto(texto, fonte, cor_texto, x, y):
    img = fonte.render(texto, True, cor_texto)
    Constantes.tela.blit(img, (x, y))


# A funcao serve para pausar o jogo. Caso o jogo seja pausado, a função checa por botões para que ou o jogador saia
# do jogo, ou para que o jogador retorne a jogar
def pause():
    pausado = True
    while pausado:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pausado = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit
        Constantes.tela.blit(Constantes.fundo, (0, 0))
        desenha_texto('Pausado', Constantes.fonte_grande, Constantes.azul, (Constantes.largura / 2) - 100, Constantes.altura / 4)
        desenha_texto("Aperte c para continuar, ou q para sair", Constantes.fonte_pequena, Constantes.azul, (Constantes.largura / 2) - 200, Constantes.altura * 0.8)
        pygame.display.update()

def desenha_grade():
    for linha in range(0, 30):
        pygame.draw.line(Constantes.tela, (255, 255, 255), (0, linha * Constantes.tamanho_casa), (Constantes.largura, linha * Constantes.tamanho_casa))
        pygame.draw.line(Constantes.tela, (255, 255, 255), (linha * Constantes.tamanho_casa, 0), (linha * Constantes.tamanho_casa, Constantes.altura))
