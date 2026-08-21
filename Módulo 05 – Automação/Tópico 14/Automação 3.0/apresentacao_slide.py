import time
import pyautogui

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# ==========================================
# CONFIGURAÇÕES
# ==========================================

LINK_SLIDES = "https://docs.google.com/presentation/d/1BFVfXxrT-7zGtYcy17Da_J7nVtMSJjvi/edit?usp=sharing&ouid=116997068820365933677&rtpof=true&sd=true"

TEMPO_SLIDE = 3


# ==========================================
# ABRIR GOOGLE SLIDES
# ==========================================

print("[1/4] Abrindo Google Slides...")

options = Options()
options.add_argument("--start-maximized")

navegador = webdriver.Chrome(options=options)

navegador.get(LINK_SLIDES)

time.sleep(8)

print("[OK] Google Slides carregado.")


# ==========================================
# INICIAR APRESENTAÇÃO
# ==========================================

print("[2/4] Iniciando apresentação...")

pyautogui.press("f5")

time.sleep(6)


# ==========================================
# ATIVAR TELA CHEIA PELO MENU DO NAVEGADOR
# ==========================================

print("[3/4] Tentando ativar tela cheia...")

# Clica na área da apresentação para garantir que ela está em foco
pyautogui.click()

time.sleep(1)

# Atalho de tela cheia do Chrome/macOS
pyautogui.hotkey("shift", "command", "enter")

time.sleep(4)


# ==========================================
# PASSAR SLIDES
# ==========================================

print("[4/4] Apresentação automática iniciada.")
print(f"[INFO] Troca a cada {TEMPO_SLIDE} segundos.")
print("[INFO] CTRL + C no terminal encerra o programa.")

while True:

    time.sleep(TEMPO_SLIDE)

    pyautogui.press("right")

    print("[SLIDE] Próximo slide")