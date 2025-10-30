#!/usr/bin/env python3
# graph_swot.py
# Python 3.12
# Janela 640x640. Apenas UMA linha horizontal vermelha para S/W e UMA vertical para O/T.
# Um par (S/W ou O/T) muda por vez. Transição suave entre valores múltiplos de 25.

import tkinter as tk
import random
import time
import sys

WIDTH = 640
HEIGHT = 640

GRID_STEP = 32
AXIS_COLOR = "#00FF00"
GRID_COLOR = "#004400"
LINE_COLOR = "#FF0000"
TITLE_FONT = ("Helvetica", 28, "bold")
LABEL_FONT = ("Helvetica", 14, "normal")

# Valores atuais (0..100). S/W são complementares, O/T também.
S = 50
O = 50
# W = 100 - S
# T = 100 - O

# Animação
STEP_MS = 25           # ms entre frames de animação
TRANSITION_STEPS = 20  # quantos frames a transição levará
UPDATE_INTERVAL = 800  # ms entre escolhas de novo movimento

def value_to_y(v: int) -> int:
    """Converte valor 0..100 para coordenada Y (0 topo, HEIGHT base)"""
    # NOTE: v=0 -> topo (0), v=100 -> base (HEIGHT)
    return int((v / 100) * HEIGHT)

def value_to_x(v: int) -> int:
    """Converte valor 0..100 para coordenada X (0 esquerda, WIDTH direita)"""
    return int((v / 100) * WIDTH)

class SWOTApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Matriz SWOT")
        self.master.geometry(f"{WIDTH}x{HEIGHT}")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # estado atual (inteiros 0..100, múltiplos de 25)
        self.s = S
        self.o = O

        # elementos desenhados (vamos atualizar coords)
        self._draw_static()  # eixos, título, etc.
        self.hline = self.canvas.create_line(0, value_to_y(self.s), WIDTH, value_to_y(self.s), fill=LINE_COLOR, width=3)
        self.vline = self.canvas.create_line(value_to_x(self.o), 0, value_to_x(self.o), HEIGHT, fill=LINE_COLOR, width=3)

        # labels para mostrar valores atuais (opcional, na tela)
        self.label_s = self.canvas.create_text(10, 10, anchor="nw", text=f"S={self.s}  W={100-self.s}", fill="white", font=("Helvetica", 12))
        self.label_o = self.canvas.create_text(10, 30, anchor="nw", text=f"O={self.o}  T={100-self.o}", fill="white", font=("Helvetica", 12))

        # Iniciar ciclo de atualizações (agenda primeira escolha após um curto delay)
        self.master.after(400, self.schedule_next_move)

        # Permite fechar com ESC também
        self.master.bind("<Escape>", lambda e: self.master.destroy())

    def _draw_static(self):
        """Desenha eixos, grade, título e rótulos fixas."""
        # grade
        for x in range(0, WIDTH, GRID_STEP):
            self.canvas.create_line(x, 0, x, HEIGHT, fill=GRID_COLOR)
        for y in range(0, HEIGHT, GRID_STEP):
            self.canvas.create_line(0, y, WIDTH, y, fill=GRID_COLOR)

        # eixos principais (centro)
        cx = WIDTH // 2
        cy = HEIGHT // 2
        self.canvas.create_line(0, cy, WIDTH, cy, fill=AXIS_COLOR, width=2)
        self.canvas.create_line(cx, 0, cx, HEIGHT, fill=AXIS_COLOR, width=2)

        # título
        self.canvas.create_text(WIDTH // 2, int(HEIGHT * 0.05),
                                text="SWOT", fill="white",
                                font=TITLE_FONT, anchor="n")

        margin_x = 40

        # rótulos centralizados verticalmente nos quadrantes
        self.canvas.create_text(margin_x, cy / 2,
                                text="Força", fill=AXIS_COLOR,
                                font=LABEL_FONT, anchor="w")

        self.canvas.create_text(WIDTH - margin_x, cy / 2,
                                text="Oportunidade", fill=AXIS_COLOR,
                                font=LABEL_FONT, anchor="e")

        self.canvas.create_text(margin_x, cy + cy / 2,
                                text="Fraqueza", fill=AXIS_COLOR,
                                font=LABEL_FONT, anchor="w")

        self.canvas.create_text(WIDTH - margin_x, cy + cy / 2,
                                text="Ameaça", fill=AXIS_COLOR,
                                font=LABEL_FONT, anchor="e")

    def schedule_next_move(self):
        """Escolhe aleatoriamente mover o par horizontal (S/W) ou vertical (O/T) e inicia transição suave."""
        # Escolhe se vamos mover horizontais (S/W) ou verticais (O/T)
        move_type = random.choice(["horizontal", "vertical"])

        # Escolhe novo valor múltiplo de 25 diferente do atual (0..100)
        choices = [0, 25, 50, 75, 100]
        if move_type == "horizontal":
            cur = self.s
            # garantimos uma escolha diferente para ver movimento (se possível)
            possible = [v for v in choices if v != cur]
            new_val = random.choice(possible) if possible else cur
            self.animate_horizontal(cur, new_val)
        else:
            cur = self.o
            possible = [v for v in choices if v != cur]
            new_val = random.choice(possible) if possible else cur
            self.animate_vertical(cur, new_val)

        # agenda a próxima escolha depois do intervalo (após uma margem)
        self.master.after(UPDATE_INTERVAL, self.schedule_next_move)

    def animate_horizontal(self, start_val, end_val):
        """Transição suave da linha horizontal S (W é complementar)."""
        # calcula passos
        delta = (end_val - start_val) / TRANSITION_STEPS
        step = 0

        def step_func():
            nonlocal step
            if step < TRANSITION_STEPS:
                step += 1
                current = start_val + delta * step
                self.s = int(round(current))
                # atualiza linha (convertendo para pixel Y)
                y = value_to_y(self.s)
                self.canvas.coords(self.hline, 0, y, WIDTH, y)
                # atualiza label textual na tela
                self.canvas.itemconfigure(self.label_s, text=f"S={self.s:3d}  W={100-self.s:3d}")
                # força redraw
                # schedule next frame
                self.master.after(STEP_MS, step_func)
            else:
                # garantir valor final exato inteiro multiplo de 25
                self.s = int(end_val)
                y = value_to_y(self.s)
                self.canvas.coords(self.hline, 0, y, WIDTH, y)
                self.canvas.itemconfigure(self.label_s, text=f"S={self.s:3d}  W={100-self.s:3d}")
                # print no console para debug
                print(f"[H] S={self.s} W={100-self.s}")
        step_func()

    def animate_vertical(self, start_val, end_val):
        """Transição suave da linha vertical O (T é complementar)."""
        delta = (end_val - start_val) / TRANSITION_STEPS
        step = 0

        def step_func():
            nonlocal step
            if step < TRANSITION_STEPS:
                step += 1
                current = start_val + delta * step
                self.o = int(round(current))
                x = value_to_x(self.o)
                self.canvas.coords(self.vline, x, 0, x, HEIGHT)
                self.canvas.itemconfigure(self.label_o, text=f"O={self.o:3d}  T={100-self.o:3d}")
                self.master.after(STEP_MS, step_func)
            else:
                self.o = int(end_val)
                x = value_to_x(self.o)
                self.canvas.coords(self.vline, x, 0, x, HEIGHT)
                self.canvas.itemconfigure(self.label_o, text=f"O={self.o:3d}  T={100-self.o:3d}")
                print(f"[V] O={self.o} T={100-self.o}")
        step_func()

def main():
    root = tk.Tk()
    app = SWOTApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        # Em alguns consoles isso será chamado; em outros, feche a janela
        print("Programa interrompido (KeyboardInterrupt).")
        try:
            root.destroy()
        except Exception:
            pass
        sys.exit(0)

if __name__ == "__main__":
    main()
