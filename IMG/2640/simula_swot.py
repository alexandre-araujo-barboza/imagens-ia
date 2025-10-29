# simula_swot.py
# Python 3.12
from __future__ import annotations
from typing import Dict, Any, Optional
import random
import time

# ---------- Classes base ---------------------------------------------------
class Desafio:
    """Classe base para desafios (contrato mínimo)."""
    def __init__(self) -> None:
        pass

    def descricao(self) -> str:
        return "Desafio genérico"


class Ambiente(Desafio):
    """
    Ambiente extende Desafio.
    Variáveis públicas: Temperatura, Pressao, Relevo, Vegetacao, Fauna
    """
    def __init__(
        self,
        temperatura: float = 25.0,
        pressao: float = 1.0,
        relevo: str = "plano",
        vegetacao: str = "escassa",
        fauna: str = "ausente",
    ) -> None:
        super().__init__()
        self.Temperatura: float = temperatura
        self.Pressao: float = pressao
        self.Relevo: str = relevo
        self.Vegetacao: str = vegetacao
        self.Fauna: str = fauna

    def __repr__(self) -> str:
        return (
            f"Ambiente(Temperatura={self.Temperatura}, Pressao={self.Pressao}, "
            f"Relevo={self.Relevo}, Vegetacao={self.Vegetacao}, Fauna={self.Fauna})"
        )


class Oponente(Desafio):
    """
    Oponente extende Desafio e aceita apenas o nome como parâmetro.
    Funções exigidas: Reagir, Retirar, Evadir, Render, Avançar, Espalhar, Abrigar, Proteger
    """
    
    def __init__(self, nome: str = "Oponente") -> None:
        super().__init__()
        self.nome = nome

    def __repr__(self) -> str:
        return f"Oponente(nome={self.nome})"

    def Reagir(self) -> None:
        print(f"[{self.nome}] Reagir: comportamento reativo executado.")

    def Retirar(self) -> None:
        print(f"[{self.nome}] Retirar: oponente recua estrategicamente.")

    def Evadir(self) -> None:
        print(f"[{self.nome}] Evadir: oponente tenta evitar confronto.")

    def Render(self) -> None:
        print(f"[{self.nome}] Render: rendição do oponente.")

    def Avancar(self) -> None:
        print(f"[{self.nome}] Avancar: oponente avança.")

    def Espalhar(self) -> None:
        print(f"[{self.nome}] Espalhar: oponente dispersa suas unidades.")

    def Abrigar(self) -> None:
        print(f"[{self.nome}] Abrigar: oponente busca abrigo/tomar posição defensiva.")

    def Proteger(self) -> None:
        print(f"[{self.nome}] Proteger: oponente protege unidade/posição.")


# ---------- Classe Humanoide e filhas -------------------------------------
class Humanoide:
    """Classe base Humanoide."""
    def __init__(self, nome: str = "Humanoide") -> None:
        self.nome = nome

    def estado(self) -> str:
        return f"Humanoide '{self.nome}' pronto."


class M3(Humanoide):
    """Herda Humanoide. Métodos pedidos: Render, Proteger, Prender, Abrigar."""
    def __init__(self, nome: str = "M3") -> None:
        super().__init__(nome)

    def Render(self) -> None:
        print("[M3] Render: M3 paralisa o alvo.")

    def Proteger(self) -> None:
        print("[M3] Proteger: M3 procura proteção.")

    def Prender(self) -> None:
        print("[M3] Prender: M3 imobiliza/alvo é detido.")

    def Abrigar(self) -> None:
        print("[M3] Abrigar: M3 procura abrigo/cover.")

    def Prover(self) -> None:
        print("[M3] Prover: M3 provê suporte/recursos.")

    def Auxiliar(self) -> None:
        print("[M3] Auxiliar: M3 auxilia unidades amigas.")

    def Evadir(self) -> None:
        print("[M3] Evadir: M3 executa manobra evasiva.")

    def Retirar(self) -> None:
        print("[M3] Retirar: M3 se retira do teatro de operações.")

class M8(Humanoide):
    """Herda Humanoide. Métodos pedidos: Espalhar, Avançar, Reagrupar, Manter, Evadir, Retirar."""
    def __init__(self, nome: str = "M8") -> None:
        super().__init__(nome)

    def Espalhar(self) -> None:
        print("[M8] Espalhar: M8 dispersa unidades.")

    def Avancar(self) -> None:
        print("[M8] Avancar: M8 avança.")

    def Reagrupar(self) -> None:
        print("[M8] Reagrupar: M8 reorganiza/une unidades.")

    def Manter(self) -> None:
        print("[M8] Manter: M8 mantém posição e condições.")

    def Evadir(self) -> None:
        print("[M8] Evadir: M8 tenta evadir sob ordem.")

    def Retirar(self) -> None:
        print("[M8] Retirar: M8 recua/retira fogo.")


# ---------- Estruturas Globais (Estado Central) ----------------------------
# Matriz SWOT é global para manter o estado da avaliação tática.
SWOT: Dict[str, int] = {
    "Forca": 50,
    "Fraqueza": 50,
    "Oportunidade": 50,
    "Ameaca": 50,
}

# Variáveis globais de instância m3 e m8 (agentes) e ambiente/oponente. 
# Estas serão inicializadas em main() e acessadas em Batalha().
m3: Optional[M3] = None
m8: Optional[M8] = None
ambiente: Optional[Ambiente] = None
oponente: Optional[Oponente] = None


# ---------- Funções de Resposta do Switch (Novas Funções) ---------------------------------------

def resposta_ambiente(cenario: int) -> None:
    """
    Simula a resposta do Ambiente (Desafio) ao cenário tático.
    Recebe o código do cenário (1=SO, 2=WO, 3=ST, 4=WT).
    Utiliza a variável global ambiente.
    """
    global ambiente
    if ambiente is None:
        print("[ERRO] Instância Ambiente não inicializada.")
        return

    print("\n--- Resposta do Ambiente (Desafio Externo) ---")
    
    # Simula o switch de 1 a 4 com if/elif
    if cenario == 1: # CENÁRIO SO: Max-Max (Ambiente Favorável)
        print(f"[Ambiente] Clima estável, Relevo {ambiente.Relevo} proporciona cobertura mínima.")
        Atualizar(5,0,5,0);
    elif cenario == 2: # CENÁRIO WO: Min-Max (Ambiente Favorável, mas exige cautela)
        print(f"[Ambiente] {ambiente.Temperatura}ºC e {ambiente.Vegetacao} densa facilitam o abrigo e ocultação.")
        Atualizar(5,0,-5,0);
    elif cenario == 3: # CENÁRIO ST: Max-Min (Ambiente Ameaçador)
        print(f"[Ambiente] Fauna {ambiente.Fauna} indica perigo biológico. Pressão de {ambiente.Pressao} hPa, dificuldade de locomoção.")
        Atualizar(-5,0,5,0);
    elif cenario == 4: # CENÁRIO WT: Min-Min (Ambiente Hostil)
        print(f"[Ambiente] Relevo {ambiente.Relevo} e clima instável (vento, chuva) dificultam a evasão.")
        Atualizar(-5,0,-5,0);
    else:
        print("[Ambiente] Sem resposta definida para o cenário.")

def resposta_oponente(cenario: int) -> None:
    """
    Simula a resposta do Oponente (Desafio) ao cenário tático,
    incluindo uma resposta randômica e Recalibragem da SWOT para o Cenário 1 (SO).
    """
    global oponente # CORRIGIDO: Referencia oponente
    if oponente is None:
        print("[ERRO] Instância Oponente não inicializada.")
        return

    print("\n--- Resposta do Oponente (Desafio Externo) ---")

    # Simula o switch de 1 a 4 com if/elif
    if cenario == 1: # CENÁRIO SO: Max-Max -> Lógica Randômica
        print(f"[{oponente.nome}] Oponente encontra-se desorganizado (CENÁRIO SO).")
        acoes = ["Reagir", "Evadir", "Render"]
        acao = random.choice(acoes)
        print(f"[{oponente.nome}] Ação escolhida: {acao}")
        
        if acao == "Reagir":
            oponente.Reagir()
            print("Recalibragem Tática: Oponente Reagiu, Força e Oportunidade Diminuem.")
            Recalibrar(S=35, W=75, O=35, T=75) 
            
        elif acao == "Evadir":
            oponente.Evadir()
            print("Recalibragem Tática: Oponente Evadiu, Retorno ao Ponto Neutro.")
            Recalibrar(S=50, W=50, O=50, T=50)

        elif acao == "Render":
            oponente.Render()
            print("Recalibragem Tática: Oponente se Rendeu, Força e Oportunidade Aumentam, Ameaça Diminui.")
            Recalibrar(S=75, W=35, O=75, T=35)
        
    elif cenario == 2: # CENÁRIO WO: Min-Max (Oponente Cauteloso)
        oponente.Abrigar()
        oponente.Proteger()

    elif cenario == 3: # CENÁRIO ST: Max-Min (Oponente Agressivo)
        oponente.Reagir()
        oponente.Avancar()

    elif cenario == 4: # CENÁRIO WT: Min-Min (Oponente Predatório)
        oponente.Espalhar()
        oponente.Retirar()
    
    else:
        print(f"[{oponente.nome}] Sem resposta definida para o cenário.")


# ---------- Funções de Controle ---------------------------------------

def Batalha() -> None:
    """
    Bloco principal de lógica de decisão. 
    Acessa os agentes m3 e m8 globalmente, mas SEM recebê-los como parâmetro.
    """
    # Declara acesso às variáveis globais m3 e m8
    global m3, m8

    # Garante que os agentes globais foram inicializados
    if m3 is None or m8 is None:
        print("[ERRO FATAL] Agentes m3 e m8 não inicializados. Chame main() primeiro.")
        return
    
    Forca = SWOT["Forca"]
    Fraqueza = SWOT["Fraqueza"]
    Oportunidade = SWOT["Oportunidade"]
    Ameaca = SWOT["Ameaca"]

    print(f"\nAvaliação: Forca={Forca}, Fraqueza={Fraqueza}, Oportunidade={Oportunidade}, Ameaca={Ameaca}")
    if Forca <= 0:
        print("\nHumanoide está morto!")
    elif Forca >= Fraqueza and Oportunidade >= Ameaca:
        print("\n[CENÁRIO SO] Tática: Eficiência (Max-Max) - Ações Humanoides:")
        m3.Render()
        m3.Prender()
        m8.Espalhar()
        m8.Avancar()
        print(f"[RESULTADO] Cenário Tático Acionado (Código): 1")
        resposta_oponente(1)
        resposta_ambiente(1)

    elif Fraqueza > Forca and Oportunidade >= Ameaca:
        print("\n[CENÁRIO WO] Tática: Manutenção (Min-Max) - Ações Humanoides:")
        m3.Proteger()
        m3.Abrigar()
        m8.Reagrupar()
        m8.Manter()
        print(f"[RESULTADO] Cenário Tático Acionado (Código): 2")
        resposta_oponente(2)
        resposta_ambiente(2)
    elif Forca >= Fraqueza and Ameaca > Oportunidade:
        print("\n[CENÁRIO ST] Tática: Resiliência (Max-Min) - Ações Humanoides:")
        m3.Prover()
        m3.Auxiliar()
        m8.Reagrupar()
        m8.Manter()
        print(f"[RESULTADO] Cenário Tático Acionado (Código): 3")
        resposta_oponente(3)
        resposta_ambiente(3)
    elif Fraqueza > Forca and Ameaca > Oportunidade:
        print("\n[CENÁRIO WT] Tática: Vulnerabilidade (Min-Min) - Ações Humanoides:")
        m3.Evadir()
        m3.Retirar()
        m8.Evadir()
        m8.Retirar()
        print(f"[RESULTADO] Cenário Tático Acionado (Código): 4")
        resposta_oponente(4)
        resposta_ambiente(4)
    else:
        print("\nNenhuma condição combinada satisfeita. Nothing to do.")

def Recalibrar(S: int, W: int, O: int, T: int) -> None:
    """
    Atualiza a matriz SWOT (global) e chama a função Batalha.
    """
    print("\n--- Recalibrando Matriz SWOT ---")
    global SWOT
    SWOT["Forca"] = S
    SWOT["Fraqueza"] = W
    SWOT["Oportunidade"] = O
    SWOT["Ameaca"] = T
    print("Novos valores SWOT:", SWOT)
    time.sleep(1)
    Batalha()

def Atualizar(S: int, W: int, O: int, T: int) -> None:
    """
    Atualiza a matriz SWOT (global) e chama a função Batalha.
    """
    print("\n--- Atualizando Matriz SWOT ---")
    global SWOT
    SWOT["Forca"] += S
    SWOT["Fraqueza"] += W
    SWOT["Oportunidade"] += O
    SWOT["Ameaca"] += T
    print("Novos valores SWOT:", SWOT)
    time.sleep(1)
    Batalha()

# ---------- Função principal ------------------------------------------------
def main() -> None:
    print("Iniciando simulação SWOT...\n")
    print("SWOT inicial:", SWOT)

    # Instâncias persistentes criadas uma única vez no início da execução
    # Acessa as variáveis globais para as instâncias
    global m3, m8, ambiente, oponente
    m3 = M3()
    m8 = M8()
    ambiente = Ambiente(temperatura=22.0, pressao=0.98, relevo="montanhoso", vegetacao="densa", fauna="diversa")
    oponente = Oponente("insurgente")

    print("\nInstâncias criadas:")
    # Usando as variáveis globais para a exibição de estado
    print(" -", m3.estado())
    print(" -", m8.estado())
    print(" -", repr(ambiente))
    print(" -", repr(oponente))
    
    Batalha()

    print(f"\nAvaliação: Forca={SWOT['Forca']}, Fraqueza={SWOT['Fraqueza']}, Oportunidade={SWOT['Oportunidade']}, Ameaca={SWOT['Ameaca']}")
    print("\nSimulação finalizada.")


if __name__ == "__main__":
    main()
