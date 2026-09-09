import pygame
import sys
import random
from pathlib import Path


# ============================================================
# CONFIGURAÇÕES
# ============================================================

W, H, FPS, CHAO = 1000, 500, 60, 400

BASE = Path(__file__).resolve().parent
IMG = BASE / "img"
SOM = BASE / "som"


# FASES
# quantidade, velocidade, intervalo mínimo, intervalo máximo
FASES = {
    1: (10, 7, 1.5, 3.0),
    2: (15, 9, 1.2, 2.2),
    3: (20, 9, 0.8, 1.5),
    4: (25, 11, 0.6, 1.2),
    5: (30, 13, 0.4, 0.9)
}


# ============================================================
# INICIALIZAÇÃO
# ============================================================

pygame.init()
pygame.mixer.init()

tela = pygame.display.set_mode((W, H))
pygame.display.set_caption("Aventura Pygame")

clock = pygame.time.Clock()


# ============================================================
# RECURSOS
# ============================================================

def imagem(nome, tamanho):
    return pygame.transform.scale(
        pygame.image.load(str(IMG / nome)).convert_alpha(),
        tamanho
    )


# Jogador
run = imagem("run.png", (80, 100))
jump = imagem("jump.png", (80, 100))
down = imagem("down.png", (80, 56))
eneas_img = imagem("eneas.png", (80, 100))

# Obstáculos
arvore = imagem("tree.png", (70, 80))
cueca = imagem("underpants.png", (70, 80))
maleta = imagem("briefcase.png", (70, 80))
ladrao = imagem("burglar.png", (70, 80))
careca = imagem("bald.png", (70, 80))


# Obstáculo aéreo
aviao = imagem("plane.png", (100, 60))


# Itens especiais
constitution = imagem("constitution.png", (55, 55))
microphone = imagem("microphone.png", (70, 70))


# Corações
coracoes_img = [
    imagem("heart1.png", (40, 40)),
    imagem("heart2.png", (40, 40)),
    imagem("heart3.png", (40, 40))
]


# ============================================================
# SONS
# ============================================================

som_start = pygame.mixer.Sound(str(SOM / "start.mp3"))
som_jump = pygame.mixer.Sound(str(SOM / "jump.mp3"))
som_dano = pygame.mixer.Sound(str(SOM / "damage.mp3"))
som_gameover = pygame.mixer.Sound(str(SOM / "gameover.mp3"))
som_end = pygame.mixer.Sound(str(SOM / "end.mp3"))
som_brasil = pygame.mixer.Sound(str(SOM / "brazil.mp3"))
eneas = pygame.mixer.Sound(str(SOM / "my-name-is-eneas.mp3"))


# ============================================================
# VARIÁVEIS
# ============================================================

fase = 1

vidas = 3

# Obstáculos desviados na fase atual
desviados = 0

# Obstáculos desviados durante todo o jogo
total_desviados = 0


# Próxima Constituição
proxima_constitution = 10


# Próximo microfone
proximo_microfone = 6


# Listas de objetos
inimigos = []
constitutions = []
microphones = []


# Jogador
px, py = 150, CHAO - 100

vel_y = 0

pulando = False
abaixado = False


# Estado do jogo
iniciado = False
game_over = False
venceu = False


# Controle do som do Brasil
brasil_tocou = False


# Cronômetro
tempo_inicio = 0
tempo_final = 0


# Próximo inimigo
proximo_inimigo = 0


# Mensagem do microfone
mensagem_microfone = False
tempo_microfone = 0
eneas_ativo = False
tempo_eneas = 0


# Elementos do cenário
linha1, linha2 = 0, W
nuvem1, nuvem2 = 150, 600


# ============================================================
# FUNÇÕES
# ============================================================

def configurar_fase():
    """
    Configura uma nova fase.
    """

    global desviados
    global proximo_inimigo

    desviados = 0

    inimigos.clear()
    constitutions.clear()
    microphones.clear()

    qtd, vel, mn, mx = FASES[fase]

    proximo_inimigo = pygame.time.get_ticks() + random.randint(
        int(mn * 1000),
        int(mx * 1000)
    )


# ------------------------------------------------------------

def criar_inimigo():
    """
    Cria um obstáculo aleatório.
    """

    # 20% de chance de avião
    if random.random() < 0.2:

        img = aviao

        w = 100
        h = 60

        y = random.choice([
            170,
            210,
            250,
            290
        ])

    else:

        img = random.choice([
            arvore,
            cueca,
            ladrao,
            careca,
            maleta
        ])

        w = 70
        h = 80

        y = CHAO - h

    inimigos.append([
        img,
        W + 50,
        y,
        w,
        h
    ])


# ------------------------------------------------------------

def criar_constitution():
    """
    Cria uma Constituição.
    """

    constitutions.append([
        constitution,
        W + 50,
        CHAO - 55,
        55,
        55
    ])


# ------------------------------------------------------------

def criar_microfone():
    """
    Cria o microfone especial.
    """

    microphones.append([
        microphone,
        W + 50,
        CHAO - 70,
        70,
        70
    ])


# ------------------------------------------------------------

def texto(msg, tamanho, y, cor=(30, 30, 30)):
    """
    Exibe um texto centralizado.
    """

    fonte = pygame.font.Font(None, tamanho)

    img = fonte.render(
        msg,
        True,
        cor
    )

    tela.blit(
        img,
        img.get_rect(
            center=(W // 2, y)
        )
    )


# ------------------------------------------------------------

def reiniciar():

    global fase
    global vidas
    global desviados
    global total_desviados

    global proxima_constitution
    global proximo_microfone

    global px
    global py
    global vel_y

    global pulando
    global abaixado

    global iniciado
    global game_over
    global venceu

    global brasil_tocou

    global tempo_inicio

    global mensagem_microfone
    global tempo_microfone
    
    global eneas_ativo
    global tempo_eneas


    # Reinicia fases
    fase = 1

    # Reinicia vidas
    vidas = 3

    # Reinicia contadores
    desviados = 0
    total_desviados = 0


    # Próximos itens
    proxima_constitution = 10
    proximo_microfone = 6


    # Jogador
    px = 150
    py = CHAO - 100

    vel_y = 0

    pulando = False
    abaixado = False


    # Estado
    iniciado = True
    game_over = False
    venceu = False


    # Som
    brasil_tocou = False


    # Cronômetro
    tempo_inicio = pygame.time.get_ticks()


    # Mensagem do microfone
    mensagem_microfone = False
    tempo_microfone = 0
    eneas_ativo = False
    tempo_eneas = 0


    # Limpa objetos
    inimigos.clear()
    constitutions.clear()
    microphones.clear()


    pygame.mixer.stop()

    configurar_fase()


# ============================================================
# CENÁRIO
# ============================================================

def desenhar_cenario():

    # Céu
    tela.fill(
        (235, 245, 255)
    )


    # Sol
    pygame.draw.circle(
        tela,
        (255, 220, 80),
        (850, 90),
        40
    )


    # Nuvens
    for x, y in [
        (nuvem1, 80),
        (nuvem2, 120)
    ]:

        pygame.draw.ellipse(
            tela,
            "white",
            (x, y, 100, 35)
        )

        pygame.draw.ellipse(
            tela,
            "white",
            (x + 40, y - 15, 90, 50)
        )


    # Chão
    pygame.draw.rect(
        tela,
        (80, 180, 80),
        (0, CHAO, W, H - CHAO)
    )


    # Marcas no chão
    for x in (
        linha1,
        linha2
    ):

        pygame.draw.rect(
            tela,
            (50, 130, 50),
            (x, CHAO - 5, 150, 5)
        )


# ============================================================
# VIDAS
# ============================================================

def desenhar_vidas():

    for i in range(vidas):

        tela.blit(
            coracoes_img[i],
            (W - 145 + i * 45, 15)
        )


# ============================================================
# TELA DE VITÓRIA
# ============================================================

def tela_vitoria():

    tela.fill("white")


    # Barras verdes
    pygame.draw.rect(
        tela,
        (80, 180, 80),
        (0, 0, W, 35)
    )

    pygame.draw.rect(
        tela,
        (80, 180, 80),
        (0, H - 35, W, 35)
    )


    texto(
        "VOCÊ VENCEU!",
        90,
        130,
        (30, 120, 50)
    )


    texto(
        "PARABÉNS!",
        42,
        205
    )


    texto(
        "Você completou todas as 5 fases!",
        30,
        260
    )


    texto(
        f"Obstáculos desviados: {total_desviados}",
        28,
        305
    )


    texto(
        f"Corações restantes: {vidas}",
        28,
        345
    )


    texto(
        "ESPAÇO - JOGAR NOVAMENTE    ESC - SAIR",
        27,
        425
    )


# ============================================================
# INÍCIO
# ============================================================

configurar_fase()


# ============================================================
# LOOP PRINCIPAL
# ============================================================

while True:

    # ========================================================
    # EVENTOS
    # ========================================================

    for e in pygame.event.get():

        # Fechar janela
        if e.type == pygame.QUIT:

            pygame.quit()
            sys.exit()


        # Teclado
        if e.type == pygame.KEYDOWN:

            # ESC
            if e.key == pygame.K_ESCAPE:

                pygame.quit()
                sys.exit()


            # ESPAÇO
            if e.key == pygame.K_SPACE:

                # Começar / reiniciar
                if (
                    not iniciado
                    or game_over
                    or venceu
                ):

                    reiniciar()

                    som_start.play()


                # Pular
                elif (
                    not pulando
                    and not abaixado
                ):

                    vel_y = -16

                    pulando = True

                    som_jump.play()


            # Abaixar
            if (
                e.key == pygame.K_DOWN
                and not pulando
            ):

                abaixado = True


        # Soltar tecla
        if (
            e.type == pygame.KEYUP
            and e.key == pygame.K_DOWN
        ):

            abaixado = False


    # ========================================================
    # JOGO
    # ========================================================

    if (
        iniciado
        and not game_over
        and not venceu
    ):

        agora = pygame.time.get_ticks()


        # ----------------------------------------------------
        # TEMPO
        # ----------------------------------------------------

        tempo = (
            agora - tempo_inicio
        ) / 1000


        # ----------------------------------------------------
        # PULO
        # ----------------------------------------------------

        if pulando:

            vel_y += 0.8

            py += vel_y


            if py >= CHAO - 100:

                py = CHAO - 100

                vel_y = 0

                pulando = False


        # ----------------------------------------------------
        # CENÁRIO
        # ----------------------------------------------------

        vel = FASES[fase][1]


        linha1 -= vel
        linha2 -= vel


        nuvem1 -= 3
        nuvem2 -= 3


        if linha1 < -150:
            linha1 = W


        if linha2 < -150:
            linha2 = W


        if nuvem1 < -150:
            nuvem1 = W + 100


        if nuvem2 < -150:
            nuvem2 = W + 100


        # ----------------------------------------------------
        # CRIAR INIMIGO
        # ----------------------------------------------------

        qtd, vel_inimigo, mn, mx = FASES[fase]


        if (
            agora >= proximo_inimigo
            and desviados < qtd
        ):

            criar_inimigo()


            proximo_inimigo = (
                agora
                + random.randint(
                    int(mn * 1000),
                    int(mx * 1000)
                )
            )


        # ----------------------------------------------------
        # MOVIMENTAR INIMIGOS
        # ----------------------------------------------------

        for i in inimigos:

            i[1] -= vel_inimigo


        # ----------------------------------------------------
        # MOVIMENTAR CONSTITUIÇÕES
        # ----------------------------------------------------

        for c in constitutions:

            c[1] -= vel_inimigo


        # ----------------------------------------------------
        # MOVIMENTAR MICROFONES
        # ----------------------------------------------------

        for m in microphones:

            m[1] -= vel_inimigo


        # ----------------------------------------------------
        # HITBOX DO JOGADOR
        # ----------------------------------------------------

        if abaixado:

            player = pygame.Rect(
                px + 10,
                py + 45,
                60,
                50
            )

        else:

            player = pygame.Rect(
                px + 15,
                py + 10,
                50,
                85
            )


        # ====================================================
        # COLISÃO COM INIMIGOS
        # ====================================================

        removidos = []


        for i in inimigos:

            rect = pygame.Rect(
                i[1],
                i[2],
                i[3],
                i[4]
            )


            if player.colliderect(rect):

                vidas -= 1

                removidos.append(i)

                som_dano.play()


                # GAME OVER
                if vidas <= 0:

                    vidas = 0

                    game_over = True

                    tempo_final = tempo

                    som_gameover.play()


        # Remove inimigos que bateram
        for i in removidos:

            if i in inimigos:

                inimigos.remove(i)


        # ====================================================
        # OBSTÁCULOS DESVIADOS
        # ====================================================

        for i in inimigos[:]:

            if i[1] < -i[3]:

                inimigos.remove(i)


                # Conta obstáculo
                desviados += 1

                total_desviados += 1


                # ------------------------------------------------
                # CONSTITUIÇÃO
                # ------------------------------------------------

                if (
                    total_desviados
                    >= proxima_constitution
                ):

                    criar_constitution()

                    proxima_constitution += 10


                # ------------------------------------------------
                # MICROFONE
                # ------------------------------------------------

                if (
                    total_desviados
                    >= proximo_microfone
                ):

                    criar_microfone()

                    proximo_microfone += 6


        # ====================================================
        # CONSTITUIÇÃO
        # ====================================================

        for c in constitutions[:]:

            rect = pygame.Rect(
                c[1],
                c[2],
                c[3],
                c[4]
            )


            # Pegou Constituição
            if player.colliderect(rect):

                if vidas < 3:

                    vidas += 1


                constitutions.remove(c)


            # Saiu da tela
            elif c[1] < -c[3]:

                constitutions.remove(c)


        # ====================================================
        # MICROFONE
        # ====================================================

        for m in microphones[:]:

            rect = pygame.Rect(
                m[1],
                m[2],
                m[3],
                m[4]
            )


            # Pegou o microfone
            if player.colliderect(rect):
                microphones.remove(m)

                # Ativa mensagem
                mensagem_microfone = True

                tempo_microfone = pygame.time.get_ticks()

                # Ativa sprite do Enéas
                eneas_ativo = True

                tempo_eneas = pygame.time.get_ticks()

                # Toca o áudio uma única vez
                eneas.play()

            # Saiu da tela
            elif m[1] < -m[3]:

                microphones.remove(m)


        # ====================================================
        # PRÓXIMA FASE
        # ====================================================

        if (
            desviados >= qtd
            and not inimigos
        ):

            # Última fase
            if fase == 5:

                venceu = True

                tempo_final = tempo

                som_end.play()


                # Toca Brasil apenas uma vez
                if not brasil_tocou:

                    som_brasil.play()

                    brasil_tocou = True


            # Próxima fase
            else:

                fase += 1

                configurar_fase()


    # ========================================================
    # DESENHO
    # ========================================================

    if venceu:

        tela_vitoria()


    else:

        # ----------------------------------------------------
        # CENÁRIO
        # ----------------------------------------------------

        desenhar_cenario()


        # ----------------------------------------------------
        # INIMIGOS
        # ----------------------------------------------------

        for i in inimigos:

            tela.blit(
                i[0],
                (i[1], i[2])
            )


        # ----------------------------------------------------
        # CONSTITUIÇÕES
        # ----------------------------------------------------

        for c in constitutions:

            tela.blit(
                c[0],
                (c[1], c[2])
            )


        # ----------------------------------------------------
        # MICROFONES
        # ----------------------------------------------------

        for m in microphones:

            tela.blit(
                m[0],
                (m[1], m[2])
            )


        # ----------------------------------------------------
        # JOGADOR
        # ----------------------------------------------------

        if eneas_ativo:
            # Sprite do Enéas durante o áudio
            img = eneas_img
            y = py

        elif pulando:
            img = jump
            y = py

        elif abaixado:
            img = down
            y = py + 44

        else:
            img = run
            y = py


        tela.blit(
            img,
            (px, y)
        )


        # ====================================================
        # HUD
        # ====================================================

        fonte = pygame.font.Font(
            None,
            28
        )


        # Fase
        tela.blit(
            fonte.render(
                f"Fase: {fase}",
                True,
                (30, 30, 30)
            ),
            (20, 20)
        )


        # Obstáculos da fase
        tela.blit(
            fonte.render(
                f"Obstáculos: {desviados}/{FASES[fase][0]}",
                True,
                (30, 30, 30)
            ),
            (20, 50)
        )


        # Total
        tela.blit(
            fonte.render(
                f"Total: {total_desviados}",
                True,
                (30, 30, 30)
            ),
            (20, 80)
        )


        # Constituição
        tela.blit(
            fonte.render(
                f"Constituição: {proxima_constitution - total_desviados}",
                True,
                (30, 30, 30)
            ),
            (20, 110)
        )


        # Vidas
        desenhar_vidas()


        # ====================================================
        # TELA INICIAL
        # ====================================================

        if not iniciado:

            texto(
                "A AVENTURA DO POLÍTICO HONESTO",
                48,
                90,
                (30, 100, 50)
            )


            texto(
                "Você é um político honesto tentando sobreviver à vida pública!",
                28,
                155
            )


            texto(
                "Desvie de ladrões, carecas e perigos da corrupção.",
                26,
                195
            )


            texto(
                "Cuidado também com aviões em pane!",
                26,
                230
            )


            texto(
                "Use a Constituição para recuperar seus corações.",
                26,
                265,
                (40, 80, 150)
            )


            texto(
                "Será que você consegue chegar ao final do mandato sem se corromper?",
                27,
                315,
                (30, 30, 30)
            )


            texto(
                "ESPAÇO - COMEÇAR",
                38,
                390,
                (200, 80, 40)
            )


        # ====================================================
        # GAME OVER
        # ====================================================

        if game_over:

            camada = pygame.Surface(
                (W, H),
                pygame.SRCALPHA
            )

            camada.fill(
                (255, 255, 255, 190)
            )

            tela.blit(
                camada,
                (0, 0)
            )


            texto(
                "GAME OVER",
                80,
                220,
                (200, 40, 40)
            )


            texto(
                "ESPAÇO - JOGAR NOVAMENTE",
                30,
                290
            )

        # ====================================================
        # TEMPO DO ENÉAS
        # ====================================================

        if eneas_ativo:

            if pygame.time.get_ticks() - tempo_eneas >= 3000:

                eneas_ativo = False

        # ====================================================
        # MENSAGEM DO MICROFONE
        # ====================================================

        if mensagem_microfone:

            tempo_mensagem = (
                pygame.time.get_ticks()
                - tempo_microfone
            )


            # Mensagem fica 1.5 segundos
            if tempo_mensagem < 1500:
                
                camada = pygame.Surface(
                    (W, H),
                    pygame.SRCALPHA
                )

                camada.fill(
                    (255, 255, 255, 210)
                )

                tela.blit(
                    camada,
                    (0, 0)
                )


                texto(
                    "MEU NOME É ENÉAS",
                    72,
                    210,
                    (30, 30, 30)
                )


                texto(
                    "🎤",
                    50,
                    280
                )


            else:

                mensagem_microfone = False


    # ========================================================
    # ATUALIZA TELA
    # ========================================================

    pygame.display.flip()

    clock.tick(FPS)