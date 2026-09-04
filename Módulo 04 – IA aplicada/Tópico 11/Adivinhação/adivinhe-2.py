import random
import subprocess
import platform
import time

# --- FUNÇÃO PRINCIPAL ---
def pedir_palpite():
    """
    Função que pede um número ao usuário, garantindo a validação
    (try-except forte) para não quebrar o programa.
    """
    while True:
        try:
            # Pede a entrada e tenta converter para inteiro
            entrada = input("\nDigite seu palpite (um número de 1 a 10): ")
            palpite = int(entrada)
            
            # Garante que o número está no intervalo correto
            if 1 <= palpite <= 10:
                return palpite
            else:
                print("❌ Número fora do intervalo. Digite entre 1 e 10.")
                
        except ValueError:
            # Captura o erro se o usuário digitar uma palavra (ex: "cinco")
            print(f"❌ '{entrada}' não é um número válido. Tente novamente.")

# --- PROGRAMA PRINCIPAL ---
def rodar_desafio_integrador():
    print("==================================================")
    print("🎮 DESAFIO INTEGRADOR (Missão Final) 🎮")
    print("==================================================")
    print("Objetivo: Adivinhe o número secreto.")

    # 1. Gera um número secreto de 1 a 10 no início
    numero_secreto = random.randint(1, 10)
    
    # 2. Loop para as tentativas (simplificado para focar na lógica)
    venceu = False
    tentativas = 0
    
    while not venceu:
        tentativas += 1
        
        # 3. Chama a função com try-except forte
        palpite_usuario = pedir_palpite()
        
        # 4. Valida se o jogador venceu
        if palpite_usuario == numero_secreto:
            venceu = True
            print(f"\n🎉 PARABÉNS! Você acertou ({numero_secreto}) em {tentativas} tentativa(s)!")
            
            # --- PARTE ALTERNATIVA ---
            print("\n⚠️ Preparando a recompensa: Reiniciando o computador em 60 segundos...")

            # Pequeno delay para aviso (opcional)
            time.sleep(5)

            print("Pressione Ctrl+C agora para cancelar se estiver testando!")
            
            # Pequeno delay para aviso (opcional)
            time.sleep(60)
            
            # Detecção de sistema operacional para o comando correto
            sistema_operacional = platform.system()
            print(f"\n[INFO] Detectado sistema: {sistema_operacional}")
            
            # Verifica o sistema operacional e executa o comando
            if sistema_operacional == "Windows":
                subprocess.run(["shutdown", "/r", "/t", "0"])

            elif sistema_operacional in ["Linux", "Darwin"]:  # Darwin é macOS
                subprocess.run(["sudo", "reboot"])

            else:
                print("[ERRO] Sistema operacional não suportado.")
            
        elif palpite_usuario < numero_secreto:
            print("💡 Dica: O número secreto é MAIOR.")
        else:
            print("💡 Dica: O número secreto é MENOR.")

# Inicia o programa
if __name__ == "__main__":
    rodar_desafio_integrador()