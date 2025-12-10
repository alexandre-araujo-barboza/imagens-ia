import tkinter as tk
import math
import time

# --- CONSTANTES DE CONFIGURAÇÃO ---
RETICLE_COLOR = '#00FF00' # Cor Neon Green
BACKGROUND_COLOR = '#1a1a1a' 
TARGET_COLOR = '#FF4500'   # Cor Orange-Red
WIDTH = 800
HEIGHT = 450
REFRESH_RATE_MS = 50 # 20 FPS

# Variáveis globais para rastrear o estado
current_distance = 75.0
start_time = time.time()
canvas = None
dot_item = None
label_distance = None
label_correction = None
# IDs para os elementos HUD (informações)
hud_info_ids = {}

def create_reticle_elements(canvas):
    """Cria todos os elementos estáticos do retículo e o ponto adaptativo."""
    
    # 1. Linhas Centrais (Crosshairs) - Replicação de .crosshair-h e .crosshair-v
    # Coordenadas relativas ao centro (50%, 50%)
    center_x = WIDTH / 2
    center_y = HEIGHT / 2
    
    # Linha Horizontal (60% de largura)
    canvas.create_line(WIDTH * 0.2, center_y, WIDTH * 0.8, center_y, 
                       fill=RETICLE_COLOR, width=2, tags="crosshair_h")
    
    # Linha Vertical (60% de altura)
    canvas.create_line(center_x, HEIGHT * 0.2, center_x, HEIGHT * 0.8, 
                       fill=RETICLE_COLOR, width=2, tags="crosshair_v")

    # 2. Ponto de Referência Central (Fixo)
    dot_radius = 4
    canvas.create_oval(center_x - dot_radius, center_y - dot_radius,
                       center_x + dot_radius, center_y + dot_radius,
                       fill=RETICLE_COLOR, tags="center_dot")

    # 3. Alvo Estático (Replicação do .target em 70%, 45%)
    target_x = WIDTH * 0.7
    target_y = HEIGHT * 0.45
    target_radius = 5
    canvas.create_oval(target_x - target_radius, target_y - target_radius,
                       target_x + target_radius, target_y + target_radius,
                       outline=TARGET_COLOR, fill=TARGET_COLOR, tags="target_dot")

    # 4. Ponto Adaptativo (O que se move) - Variável global para ser movida
    global dot_item
    dot_size = 20
    # Posição inicial arbitrária, será corrigida imediatamente no update_loop
    dot_item = canvas.create_oval(center_x - dot_size/2, center_y - dot_size/2,
                                  center_x + dot_size/2, center_y + dot_size/2,
                                  fill=RETICLE_COLOR, tags="adaptive_dot")


def create_hud_labels(root):
    """Cria os elementos HUD (Heads-Up Display) usando Labels."""
    global label_distance, label_correction
    
    # Estilo base para todos os textos do HUD
    hud_style = {'bg': BACKGROUND_COLOR, 'fg': RETICLE_COLOR, 'font': ('Helvetica', 10), 'bd': 0}

    # DISTÂNCIA (Topo Esquerda)
    label_distance = tk.Label(root, text="DISTÂNCIA: 75 M", **hud_style)
    label_distance.place(x=20, y=20)

    # CORREÇÃO (Baixo Direita)
    correction_text = "CORREÇÃO BALÍSTICA:\nELEV: +0.0 MOA\nVENTO: +0.0 MOA"
    label_correction = tk.Label(root, text=correction_text, **hud_style, justify=tk.RIGHT)
    label_correction.place(x=WIDTH - 20, y=HEIGHT - 70, anchor=tk.NE)

    # STATUS (Baixo Esquerda)
    label_status = tk.Label(root, text="STATUS: SISTEMA ÓPTICO [OK]", **hud_style)
    label_status.place(x=20, y=HEIGHT - 30)

    # TÍTULO (Topo Centro)
    tk.Label(root, text="OCULUS SYSTEM | P-87", bg='black', fg=RETICLE_COLOR, 
             font=('Helvetica', 12, 'bold'), padx=5, pady=2, bd=1, relief=tk.SOLID).place(x=WIDTH / 2, y=10, anchor=tk.N)

def update_loop(root):
    """
    Simula a lógica balística em Python e atualiza a posição do ponto adaptativo
    e o texto do HUD em tempo real.
    """
    global current_distance, start_time, canvas, dot_item
    
    elapsed = time.time() - start_time
    
    # 1. Simulação Balística (Lógica Pura em Python)
    
    # Simula a Distância (Mudança senoide entre 70m e 80m)
    current_distance = 75 + math.sin(elapsed / 3.0) * 5.0
    distance_rounded = round(current_distance)

    # Simula a Correção Vertical (Queda)
    # Quanto maior a distância, maior o ajuste para cima/baixo.
    # Ponto zero de referência (50% da altura)
    CENTER_Y_PIXELS = HEIGHT / 2 
    
    # A diferença de 75m é usada para calcular a queda. Ex: Se 76m, diff=1.
    distance_offset = current_distance - 75.0 
    
    # O fator 4.0 é um multiplicador arbitrário para simular o movimento (em pixels)
    vertical_correction_pixels = distance_offset * 4.0 
    
    # No HTML, 40% é a posição inicial. Aqui, é o centro (CENTER_Y_PIXELS)
    # Se a distância > 75m, o ponto adaptativo *cai* (aumenta o Y, sobe o Top em % do HTML)
    # Se a distância < 75m, o ponto adaptativo *sobe* (diminui o Y, desce o Top em % do HTML)
    final_y_pixels = CENTER_Y_PIXELS + vertical_correction_pixels 

    # Simula a Correção Horizontal (Vento)
    CENTER_X_PIXELS = WIDTH / 2
    # Vento oscilando lateralmente
    wind_correction_pixels = math.cos(elapsed / 1.5) * 5.0 
    final_x_pixels = CENTER_X_PIXELS + wind_correction_pixels

    # 2. Atualização dos Elementos Gráficos (Tkinter)

    # Move o ponto adaptativo para a nova posição (centro do dot)
    dot_size = 20
    x1 = final_x_pixels - dot_size/2
    y1 = final_y_pixels - dot_size/2
    x2 = final_x_pixels + dot_size/2
    y2 = final_y_pixels + dot_size/2
    
    canvas.coords(dot_item, x1, y1, x2, y2)
    
    # 3. Atualização do HUD (Texto)
    
    # Cálculo da correção em unidades MOA (simulação)
    elev_moa = -round(vertical_correction_pixels / 5.0, 1) # Negativo, pois a queda real é corrigida para cima
    wind_moa = round(wind_correction_pixels / 5.0, 1)
    
    label_distance.config(text=f"DISTÂNCIA: {distance_rounded} M")
    
    correction_text = (f"CORREÇÃO BALÍSTICA:\n"
                       f"ELEV: {elev_moa:+.1f} MOA\n"
                       f"VENTO: {wind_moa:+.1f} MOA")
    label_correction.config(text=correction_text)

    # Chama o loop novamente após um pequeno atraso
    root.after(REFRESH_RATE_MS, lambda: update_loop(root))

def main():
    """Configuração principal da janela Tkinter."""
    global canvas
    
    root = tk.Tk()
    root.title("Retículo Holográfico P-87 (Python Puro)")
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.configure(bg=BACKGROUND_COLOR)
    root.resizable(False, False)

    # 1. Canvas para Desenho
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # 2. Desenha o Retículo
    create_reticle_elements(canvas)

    # 3. Cria as Labels do HUD (elas flutuam sobre o Canvas)
    create_hud_labels(root)
    
    # 4. Inicia o loop de animação/cálculo
    update_loop(root)

    root.mainloop()

if __name__ == "__main__":
    main()