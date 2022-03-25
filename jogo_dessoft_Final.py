import pygame
from pygame.locals import *
import Constantes
import Funcoes
import Classes



while jogo == True:

    Constantes.clock.tick(Constantes.fps)

    Constantes.tela.blit(Constantes.fundo, (0, 0))

    if menu_principal == True:
        if Constantes.botao_saida.desenha():
            jogo = False
        if Constantes.botao_inicia.desenha():
            menu_principal = False
        Funcoes.desenha_texto("Cat quest", Constantes.fonte_enorme, ((255, 255, 255)), Constantes.largura / 2 - 200, Constantes.altura / 2 - 250)
        Funcoes.desenha_texto("Seu gato foi raptado por um culto maligno de magos, e só você pode salvá-lo!", Constantes.fonte_pequena,
                      ((255, 255, 255)), (Constantes.largura // 2) - 700, 850)
        Funcoes.desenha_texto("Use suas setas para andar, e o espaço para pular!", Constantes.fonte_pequena, ((255, 255, 255)),
                      (Constantes.largura // 2) - 700, 900)
        Funcoes.desenha_texto("Aperte P para pausar o jogo", Constantes.fonte_pequena, ((255, 255, 255)), (Constantes.largura // 2) - 700, 950)
    else:
        mundo.desenha()

        if fim_de_jogo == 0:
            Constantes.grupo_inimigo.update()

        Constantes.grupo_inimigo.draw(Constantes.tela)
        Constantes.grupo_inimigo.update()
        Constantes.grupo_espinho.draw(Constantes.tela)
        Constantes.grupo_saida.draw(Constantes.tela)
        Constantes.grupo_gato.draw(Constantes.tela)

        fim_de_jogo = jogador.update(fim_de_jogo)
        # se o jogador morrerf
        if fim_de_jogo == -1:
            if Constantes.botao_reinicia.desenha():
                mapa = []
                mundo = Funcoes.reinicia_fase(fase)
                fim_de_jogo = 0
                jogador = Classes.Jogador(100, Constantes.altura - 130)

        # se o jogador completar a fase
        if fim_de_jogo == 1:
            # reinicia o jogo a avança para o próximo nível
            fase += 1
            if fase <= Constantes.maximo_de_fases:
                # reinicia fase
                mapa = []
                mundo = Funcoes.reinicia_fase(fase)
                fim_de_jogo = 0
                jogador = Classes.Jogador(100, Constantes.altura - 130)
            else:
                if Constantes.botao_reinicia.desenha():
                    fase = 1
                    # reinicia fase
                    mapa = []
                    mundo = Funcoes.reinicia_fase(fase)
                    fim_de_jogo = 0
        elif fim_de_jogo == 2:
            while jogo:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            quit
                Constantes.tela.blit(Constantes.fundo, (0, 0))
                Funcoes.desenha_texto("Parabéns! Você conseguiu salvar o seu gato!", Constantes.fonte_enorme, (0, 0, 1),
                              (Constantes.largura / 2) - 750, Constantes.altura / 2 - 100)
                Funcoes.desenha_texto("Pressione Q para fechar o jogo", Constantes.fonte_pequena, (0, 0, 1), (Constantes.largura / 2) - 500,
                              Constantes.altura / 2 + 300)
                pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo = False

    pygame.display.update()

pygame.quit()
