#!/usr/bin/env python3
# graph_swot.py
# Integração com simula_swot.py — animação gradual das linhas SWOT (seguro no Windows)

import tkinter as tk
import threading
import queue

WIDTH = 640
HEIGHT = 640
AXIS_COLOR = "#00FF00"
LINE_COLOR = "#00FF00"
GRID_COLOR = "#004400"
TITLE_FONT = ("Helvetica", 28, "bold")
LABEL_FONT = ("Helvetica", 14, "normal")

# fila segura entre threads
_queue = queue.Queue()
_app = {"root": None, "canvas": None, "hline": None, "vline": None,
        "label_s": None, "label_o": None, "current_s": 50, "current_o": 50}

# parâmetros da animação
ANIMATION_SPEED = 4      # quanto maior, mais rápido
REFRESH_MS = 25          # tempo entre frames (ms)

def value_to_y(v): return int((v / 100) * HEIGHT)
def value_to_x(v): return int((v / 100) * WIDTH)

def _draw_static(canvas):
    cx, cy = WIDTH // 2, HEIGHT // 2
    # grade
    for x in range(0, WIDTH, 32):
        canvas.create_line(x, 0, x, HEIGHT, fill=GRID_COLOR)
    for y in range(0, HEIGHT, 32):
        canvas.create_line(0, y, WIDTH, y, fill=GRID_COLOR)

    # eixos pontilhados manuais
    dash_len, dash_gap = 10, 6
    x = 0
    while x < WIDTH:
        canvas.create_line(x, cy, min(x + dash_len, WIDTH), cy, fill=AXIS_COLOR, width=2)
        x += dash_len + dash_gap
    y = 0
    while y < HEIGHT:
        canvas.create_line(cx, y, cx, min(y + dash_len, HEIGHT), fill=AXIS_COLOR, width=2)
        y += dash_len + dash_gap

    # título e rótulos
    canvas.create_text(cx, 30, text="Matriz SWOT", fill="white", font=TITLE_FONT)
    margin_x = 40
    canvas.create_text(margin_x, cy / 2, text="Força", fill=AXIS_COLOR, font=LABEL_FONT, anchor="w")
    canvas.create_text(WIDTH - margin_x, cy / 2, text="Oportunidade", fill=AXIS_COLOR, font=LABEL_FONT, anchor="e")
    canvas.create_text(margin_x, cy + cy / 2, text="Fraqueza", fill=AXIS_COLOR, font=LABEL_FONT, anchor="w")
    canvas.create_text(WIDTH - margin_x, cy + cy / 2, text="Ameaça", fill=AXIS_COLOR, font=LABEL_FONT, anchor="e")

def iniciar_interface():
    """Cria a janela e roda o mainloop (deve ser chamada no thread principal)."""
    root = tk.Tk()
    root.title("Matriz SWOT (Simulação)")
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.resizable(False, False)
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
    canvas.pack(fill="both", expand=True)

    _draw_static(canvas)
    cy, cx = HEIGHT // 2, WIDTH // 2

    hline = canvas.create_line(0, cy, WIDTH, cy, fill=LINE_COLOR, width=3)
    vline = canvas.create_line(cx, 0, cx, HEIGHT, fill=LINE_COLOR, width=3)
    label_s = canvas.create_text(10, 10, anchor="nw", text="S=50 W=50", fill="white", font=("Helvetica", 12))
    label_o = canvas.create_text(10, 30, anchor="nw", text="O=50 T=50", fill="white", font=("Helvetica", 12))

    _app.update(root=root, canvas=canvas, hline=hline, vline=vline,
                label_s=label_s, label_o=label_o, current_s=50, current_o=50)

    def processar_fila():
        while not _queue.empty():
            S, W, O, T = _queue.get_nowait()
            _app["target_s"] = S
            _app["target_w"] = W
            _app["target_o"] = O
            _app["target_t"] = T
        root.after(REFRESH_MS, processar_fila)

    def animar():
        """Move gradualmente as linhas até os novos valores."""
        if "target_s" in _app and "target_o" in _app:
            cs = _app["current_s"]
            co = _app["current_o"]
            ts = _app["target_s"]
            to = _app["target_o"]

            # aproxima gradualmente
            if cs < ts: cs += ANIMATION_SPEED
            elif cs > ts: cs -= ANIMATION_SPEED
            if co < to: co += ANIMATION_SPEED
            elif co > to: co -= ANIMATION_SPEED

            # limita ao intervalo [0, 100]
            cs = max(0, min(100, cs))
            co = max(0, min(100, co))

            _app["current_s"], _app["current_o"] = cs, co

            y_s = value_to_y(cs)
            x_o = value_to_x(co)
            canvas.coords(hline, 0, y_s, WIDTH, y_s)
            canvas.coords(vline, x_o, 0, x_o, HEIGHT)
            canvas.itemconfigure(label_s, text=f"S={int(cs):3d} W={100-int(cs):3d}")
            canvas.itemconfigure(label_o, text=f"O={int(co):3d} T={100-int(co):3d}")

        root.after(REFRESH_MS, animar)

    processar_fila()
    animar()
    root.mainloop()

def iniciar_grafico_swot(S, W, O, T):
    """Atualiza os valores do gráfico (thread-safe)."""
    _queue.put((S, W, O, T))
