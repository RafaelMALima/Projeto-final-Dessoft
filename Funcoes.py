import pygame

# funcoes para reiniciar fases
def reinicia_fase(fase):
    jogador = Jogador(100, altura - 130)
    grupo_inimigo.empty()
    grupo_espinho.empty()
    grupo_saida.empty()
    # carrega uma fase e cria o mundo
    mapa = []
    if path.exists(f'fase{fase}'):
        with open(f'fase{fase}', 'rb') as json_in:
            mapa = json.load(json_in)
    mundo = Mundo(mapa)

    return mundo


# funcao colocar texto
def desenha_texto(texto, fonte, cor_texto, x, y):
    img = fonte.render(texto, True, cor_texto)
    tela.blit(img, (x, y))


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
        tela.blit(fundo, (0, 0))
        desenha_texto('Pausado', fonte_grande, azul, (largura / 2) - 100, altura / 4)
        desenha_texto("Aperte c para continuar, ou q para sair", fonte_pequena, azul, (largura / 2) - 200, altura * 0.8)
        pygame.display.update()

def desenha_grade():
    for linha in range(0, 30):
        pygame.draw.line(tela, (255, 255, 255), (0, linha * tamanho_casa), (largura, linha * tamanho_casa))
        pygame.draw.line(tela, (255, 255, 255), (linha * tamanho_casa, 0), (linha * tamanho_casa, altura))
