import pygame
import sys
import random
from pathlib import Path

LARGURA = 1000
ALTURA = 500
FPS = 60
CHAO_Y = 400

FASES = {
    1: {"quantidade": 10, "velocidade": 7, "intervalo_min": 1.5, "intervalo_max": 3.0},
    2: {"quantidade": 15, "velocidade": 9, "intervalo_min": 1.2, "intervalo_max": 2.2},
    3: {"quantidade": 20, "velocidade": 9, "intervalo_min": 0.8, "intervalo_max": 1.5},
    4: {"quantidade": 25, "velocidade": 11, "intervalo_min": 0.6, "intervalo_max": 1.2},
    5: {"quantidade": 30, "velocidade": 13, "intervalo_min": 0.4, "intervalo_max": 0.9}
}
TOTAL_FASES = 5

VELOCIDADE_INICIAL = 5
VELOCIDADE_NUVENS_INICIAL = 3
FORCA_PULO = -16
GRAVIDADE = 0.8
CORACOES_INICIAIS = 3

pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Aventura Pygame")
relogio = pygame.time.Clock()

CEU = (235, 245, 255)
VERDE = (80, 180, 80)
BRANCO = (255, 255, 255)
PRETO = (30, 30, 30)

PASTA_PROJETO = Path(__file__).parent
PASTA_IMAGENS = PASTA_PROJETO / "img"
PASTA_SONS = PASTA_PROJETO / "som"

# Sons
som_start = pygame.mixer.Sound(str(PASTA_SONS / "start.mp3"))
som_jump = pygame.mixer.Sound(str(PASTA_SONS / "jump.mp3"))
som_dano = pygame.mixer.Sound(str(PASTA_SONS / "damage.mp3"))
som_gameover = pygame.mixer.Sound(str(PASTA_SONS / "gameover.mp3"))
som_endgame = pygame.mixer.Sound(str(PASTA_SONS / "end.mp3"))

# Personagem
imagem_run = pygame.image.load(str(PASTA_IMAGENS / "run.png")).convert_alpha()
imagem_jump = pygame.image.load(str(PASTA_IMAGENS / "jump.png")).convert_alpha()
imagem_down = pygame.image.load(str(PASTA_IMAGENS / "down.png")).convert_alpha()

TAMANHO_PERSONAGEM = (80, 100)
TAMANHO_DOWN = (80, 56)

imagem_run = pygame.transform.scale(imagem_run, TAMANHO_PERSONAGEM)
imagem_jump = pygame.transform.scale(imagem_jump, TAMANHO_PERSONAGEM)
imagem_down = pygame.transform.scale(imagem_down, TAMANHO_DOWN)

# Inimigos
imagem_arvore = pygame.image.load(str(PASTA_IMAGENS / "tree.png")).convert_alpha()
imagem_cueca = pygame.image.load(str(PASTA_IMAGENS / "underpants.png")).convert_alpha()
imagem_ladrao = pygame.image.load(str(PASTA_IMAGENS / "burglar.png")).convert_alpha()
imagem_careca = pygame.image.load(str(PASTA_IMAGENS / "bald.png")).convert_alpha()
imagem_aviao = pygame.image.load(str(PASTA_IMAGENS / "plane.png")).convert_alpha()

TAMANHO_INIMIGO_CHAO = (70, 80)
TAMANHO_AVIAO = (100, 60)

imagem_arvore = pygame.transform.scale(imagem_arvore, TAMANHO_INIMIGO_CHAO)
imagem_cueca = pygame.transform.scale(imagem_cueca, TAMANHO_INIMIGO_CHAO)
imagem_ladrao = pygame.transform.scale(imagem_ladrao, TAMANHO_INIMIGO_CHAO)
imagem_careca = pygame.transform.scale(imagem_careca, TAMANHO_INIMIGO_CHAO)
imagem_aviao = pygame.transform.scale(imagem_aviao, TAMANHO_AVIAO)

inimigos_chao = [imagem_arvore, imagem_cueca, imagem_ladrao, imagem_careca]

# Corações
TAMANHO_CORACAO = (40, 40)
imagem_coracao1 = pygame.transform.scale(
    pygame.image.load(str(PASTA_IMAGENS / "heart1.png")).convert_alpha(),
    TAMANHO_CORACAO
)
imagem_coracao2 = pygame.transform.scale(
    pygame.image.load(str(PASTA_IMAGENS / "heart2.png")).convert_alpha(),
    TAMANHO_CORACAO
)
imagem_coracao3 = pygame.transform.scale(
    pygame.image.load(str(PASTA_IMAGENS / "heart3.png")).convert_alpha(),
    TAMANHO_CORACAO
)

# Estado do personagem
personagem_x = 150
personagem_y = CHAO_Y - TAMANHO_PERSONAGEM[1]
velocidade_y = 0
pulando = False
abaixado = False

# Estado do jogo
velocidade = VELOCIDADE_INICIAL
velocidade_nuvens = VELOCIDADE_NUVENS_INICIAL
velocidade_inimigo = FASES[1]["velocidade"]

jogo_iniciado = False
game_over = False
jogo_finalizado = False

fase_atual = 1
inimigos_desviados = 0
mostrar_fase = False
tempo_mensagem_fase = 0

coracoes = CORACOES_INICIAIS
tempo_inicio = 0
tempo_final = 0
tempo_proximo_inimigo = 0

linha1_x = 0
linha2_x = LARGURA
nuvem1_x = 150
nuvem2_x = 600

inimigos = []

def criar_inimigo():
    tipo = random.choice(["chao", "chao", "chao", "chao", "aviao"])

    if tipo == "chao":
        imagem = random.choice(inimigos_chao)
        largura, altura = TAMANHO_INIMIGO_CHAO
        x = LARGURA + 50
        y = CHAO_Y - altura
    else:
        imagem = imagem_aviao
        largura, altura = TAMANHO_AVIAO
        x = LARGURA + 50
        y = random.choice([170, 210, 250, 290])

    inimigos.append({
        "imagem": imagem,
        "x": x,
        "y": y,
        "largura": largura,
        "altura": altura
    })

def configurar_fase():
    global velocidade, velocidade_nuvens, velocidade_inimigo
    global tempo_proximo_inimigo, inimigos_desviados
    global mostrar_fase, tempo_mensagem_fase

    config = FASES[fase_atual]

    velocidade = VELOCIDADE_INICIAL + fase_atual - 1
    velocidade_nuvens = VELOCIDADE_NUVENS_INICIAL + fase_atual - 1
    velocidade_inimigo = config["velocidade"]
    inimigos_desviados = 0
    inimigos.clear()

    intervalo = random.uniform(
        config["intervalo_min"],
        config["intervalo_max"]
    )
    tempo_proximo_inimigo = pygame.time.get_ticks() + int(intervalo * 1000)

    mostrar_fase = True
    tempo_mensagem_fase = pygame.time.get_ticks() + 2000

def desenhar_cenario():
    tela.fill(CEU)

    pygame.draw.circle(tela, (255, 220, 80), (850, 90), 40)

    pygame.draw.ellipse(tela, BRANCO, (nuvem1_x, 80, 100, 35))
    pygame.draw.ellipse(tela, BRANCO, (nuvem1_x + 40, 65, 90, 50))

    pygame.draw.ellipse(tela, BRANCO, (nuvem2_x, 120, 120, 35))
    pygame.draw.ellipse(tela, BRANCO, (nuvem2_x + 50, 100, 90, 50))

    pygame.draw.rect(tela, VERDE, (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y))

    pygame.draw.rect(tela, (50, 130, 50), (linha1_x, CHAO_Y - 5, 150, 5))
    pygame.draw.rect(tela, (50, 130, 50), (linha2_x, CHAO_Y - 5, 150, 5))

def desenhar_texto_central(texto, tamanho):
    fonte = pygame.font.Font(None, tamanho)
    superficie = fonte.render(texto, True, PRETO)
    retangulo = superficie.get_rect(center=(LARGURA // 2, ALTURA // 2))
    tela.blit(superficie, retangulo)

def desenhar_coracoes():
    x_inicial = LARGURA - 145
    y = 15
    espacamento = 45

    if coracoes >= 1:
        tela.blit(imagem_coracao1, (x_inicial, y))
    if coracoes >= 2:
        tela.blit(imagem_coracao2, (x_inicial + espacamento, y))
    if coracoes >= 3:
        tela.blit(imagem_coracao3, (x_inicial + espacamento * 2, y))

def reiniciar_jogo():
    global personagem_y, velocidade_y, pulando, abaixado
    global jogo_iniciado, game_over, jogo_finalizado, coracoes
    global tempo_inicio, tempo_final, fase_atual
    global linha1_x, linha2_x, nuvem1_x, nuvem2_x

    personagem_y = CHAO_Y - TAMANHO_PERSONAGEM[1]
    velocidade_y = 0
    pulando = False
    abaixado = False

    jogo_iniciado = True
    game_over = False
    jogo_finalizado = False
    coracoes = CORACOES_INICIAIS

    fase_atual = 1
    tempo_inicio = pygame.time.get_ticks()
    tempo_final = 0

    linha1_x = 0
    linha2_x = LARGURA
    nuvem1_x = 150
    nuvem2_x = 600

    configurar_fase()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if not jogo_iniciado and not game_over and not jogo_finalizado:
                    jogo_iniciado = True
                    tempo_inicio = pygame.time.get_ticks()
                    tempo_final = 0
                    fase_atual = 1
                    som_start.play()
                    configurar_fase()

                elif game_over or jogo_finalizado:
                    reiniciar_jogo()

                elif not pulando and not abaixado:
                    velocidade_y = FORCA_PULO
                    pulando = True
                    som_jump.play()

            elif evento.key == pygame.K_DOWN:
                if (
                    jogo_iniciado
                    and not game_over
                    and not jogo_finalizado
                    and not pulando
                ):
                    abaixado = True

        if evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN:
            abaixado = False

    if jogo_iniciado and not game_over and not jogo_finalizado:
        tempo_decorrido = (pygame.time.get_ticks() - tempo_inicio) / 1000

        # Pulo
        if pulando:
            velocidade_y += GRAVIDADE
            personagem_y += velocidade_y

            if personagem_y >= CHAO_Y - TAMANHO_PERSONAGEM[1]:
                personagem_y = CHAO_Y - TAMANHO_PERSONAGEM[1]
                velocidade_y = 0
                pulando = False

        # Chão
        linha1_x -= velocidade
        linha2_x -= velocidade

        if linha1_x < -150:
            linha1_x = LARGURA
        if linha2_x < -150:
            linha2_x = LARGURA

        # Nuvens
        nuvem1_x -= velocidade_nuvens
        nuvem2_x -= velocidade_nuvens

        if nuvem1_x < -150:
            nuvem1_x = LARGURA + 100
        if nuvem2_x < -150:
            nuvem2_x = LARGURA + 100

        # Criar inimigos
        tempo_atual_ms = pygame.time.get_ticks()

        if tempo_atual_ms >= tempo_proximo_inimigo:
            if inimigos_desviados < FASES[fase_atual]["quantidade"]:
                criar_inimigo()

                intervalo = random.uniform(
                    FASES[fase_atual]["intervalo_min"],
                    FASES[fase_atual]["intervalo_max"]
                )
                tempo_proximo_inimigo = tempo_atual_ms + int(intervalo * 1000)

        # Movimento dos inimigos
        for inimigo in inimigos:
            inimigo["x"] -= velocidade_inimigo

        # Hitbox
        if abaixado:
            personagem_rect = pygame.Rect(
                personagem_x + 10, personagem_y + 45, 60, 55
            )
        else:
            personagem_rect = pygame.Rect(
                personagem_x + 15,
                personagem_y + 10,
                TAMANHO_PERSONAGEM[0] - 30,
                TAMANHO_PERSONAGEM[1] - 15
            )

        # Colisão
        inimigos_para_remover = []

        for inimigo in inimigos:
            inimigo_rect = pygame.Rect(
                inimigo["x"],
                inimigo["y"],
                inimigo["largura"],
                inimigo["altura"]
            )

            if personagem_rect.colliderect(inimigo_rect):
                coracoes -= 1
                inimigos_para_remover.append(inimigo)
                som_dano.play()

                if coracoes <= 0:
                    coracoes = 0
                    tempo_final = tempo_decorrido
                    game_over = True
                    abaixado = False
                    som_gameover.play()
                    break

        for inimigo in inimigos_para_remover:
            if inimigo in inimigos:
                inimigos.remove(inimigo)

        # Contar inimigos desviados
        inimigos_fora = []

        for inimigo in inimigos:
            if inimigo["x"] <= -inimigo["largura"]:
                inimigos_fora.append(inimigo)

        for inimigo in inimigos_fora:
            if inimigo in inimigos:
                inimigos.remove(inimigo)
                inimigos_desviados += 1

        # Verificar fase
        quantidade_fase = FASES[fase_atual]["quantidade"]

        if inimigos_desviados >= quantidade_fase and len(inimigos) == 0:
            if fase_atual >= TOTAL_FASES:
                jogo_finalizado = True
                jogo_iniciado = True
                tempo_final = tempo_decorrido
                som_endgame.play()
            else:
                fase_atual += 1
                configurar_fase()

    # Desenhar
    desenhar_cenario()

    for inimigo in inimigos:
        tela.blit(inimigo["imagem"], (inimigo["x"], inimigo["y"]))

    if pulando:
        imagem_atual = imagem_jump
        posicao_personagem_y = personagem_y
    elif abaixado:
        imagem_atual = imagem_down
        posicao_personagem_y = personagem_y + 44
    else:
        imagem_atual = imagem_run
        posicao_personagem_y = personagem_y

    tela.blit(imagem_atual, (personagem_x, posicao_personagem_y))

    # Tela inicial
    if not jogo_iniciado and not game_over and not jogo_finalizado:
        desenhar_texto_central("APERTE ESPAÇO PARA COMEÇAR", 40)

    # Fase
    if mostrar_fase:
        if pygame.time.get_ticks() >= tempo_mensagem_fase:
            mostrar_fase = False
        else:
            fonte_fase = pygame.font.Font(None, 60)
            texto_fase = fonte_fase.render(f"FASE {fase_atual}", True, PRETO)
            retangulo_fase = texto_fase.get_rect(
                center=(LARGURA // 2, ALTURA // 2)
            )
            tela.blit(texto_fase, retangulo_fase)

    # Game Over
    if game_over:
        desenhar_texto_central("GAME OVER", 60)

        fonte_game_over = pygame.font.Font(None, 30)
        texto_reiniciar = fonte_game_over.render(
            "APERTE ESPAÇO PARA JOGAR NOVAMENTE",
            True,
            PRETO
        )
        retangulo_reiniciar = texto_reiniciar.get_rect(
            center=(LARGURA // 2, ALTURA // 2 + 60)
        )
        tela.blit(texto_reiniciar, retangulo_reiniciar)

    # Vitória
    if jogo_finalizado:
        desenhar_texto_central("PARABÉNS!", 60)

        fonte_final = pygame.font.Font(None, 30)

        texto_final = fonte_final.render(
            "VOCÊ COMPLETOU TODAS AS 5 FASES!",
            True,
            PRETO
        )
        retangulo_final = texto_final.get_rect(
            center=(LARGURA // 2, ALTURA // 2 + 50)
        )
        tela.blit(texto_final, retangulo_final)

        texto_novo_jogo = fonte_final.render(
            "APERTE ESPAÇO PARA JOGAR NOVAMENTE",
            True,
            PRETO
        )
        retangulo_novo_jogo = texto_novo_jogo.get_rect(
            center=(LARGURA // 2, ALTURA // 2 + 90)
        )
        tela.blit(texto_novo_jogo, retangulo_novo_jogo)

    # Informações
    fonte = pygame.font.Font(None, 28)

    texto_velocidade = fonte.render(
        f"Velocidade: {velocidade_inimigo}",
        True,
        PRETO
    )
    tela.blit(texto_velocidade, (20, 20))

    if jogo_iniciado:
        if game_over or jogo_finalizado:
            tempo_atual = tempo_final
        else:
            tempo_atual = (pygame.time.get_ticks() - tempo_inicio) / 1000
    else:
        tempo_atual = 0

    texto_tempo = fonte.render(
        f"Tempo: {int(tempo_atual)}s",
        True,
        PRETO
    )
    tela.blit(texto_tempo, (20, 50))

    texto_fase_info = fonte.render(
        f"Fase: {fase_atual}",
        True,
        PRETO
    )
    tela.blit(texto_fase_info, (20, 80))

    quantidade_fase = FASES[fase_atual]["quantidade"]
    texto_inimigos = fonte.render(
        f"Inimigos: {inimigos_desviados}/{quantidade_fase}",
        True,
        PRETO
    )
    tela.blit(texto_inimigos, (20, 110))

    desenhar_coracoes()

    pygame.display.flip()
    relogio.tick(FPS)