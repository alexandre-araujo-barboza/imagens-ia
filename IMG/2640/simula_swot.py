# simula_swot.py
# Python 3.12
from __future__ import annotations
from typing import Dict

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
        # atributos públicos (python: por padrão são públicos)
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
    (incluí variantes sem acento quando houve ambiguidade para manter compatibilidade).
    """
    
    def __init__(self, nome: str = "Oponente") -> None:
        super().__init__()
        self.nome = nome

    def __repr__(self) -> str:
        return f"Oponente(nome={self.nome})"

    def Reagir(self) -> None:
        print("[Oponente] Reagir: comportamento reativo executado.")

    def Retirar(self) -> None:
        print("[Oponente] Retirar: oponente recua estrategicamente.")

    def Evadir(self) -> None:
        print("[Oponente] Evadir: oponente tenta evitar confronto.")

    def Render(self) -> None:
        print("[Oponente] Render: rendição do oponente.")

    def Avancar(self) -> None:
        print("[Oponente] Avancar: oponente avança (sem acento).")

    def Espalhar(self) -> None:
        print("[Oponente] Espalhar: oponente dispersa suas unidades.")

    def Abrigar(self) -> None:
        print("[Oponente] Abrigar: oponente busca abrigo/tomar posição defensiva.")

    def Proteger(self) -> None:
        print("[Oponente] Proteger: oponente protege unidade/posição.")


# ---------- Classe Humanoide e filhas -------------------------------------
class Humanoide:
    """Classe base Humanoide."""
    def __init__(self, nome: str = "Humanoide") -> None:
        self.nome = nome

    def estado(self) -> str:
        return f"Humanoide '{self.nome}' pronto."


class M3(Humanoide):
    """Herda Humanoide. Métodos pedidos: Render, Protejer, Prender, Abrigar.
       Também implementei variantes e métodos adicionais usados nas transições (Prover, Auxiliar, Evadir, Retirar)."""
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
        print("[M8] Espalhar: M8 dispersa fogo/unidades.")

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


# ---------- Estrutura SWOT -------------------------------------------------
# "matriz de 4 dimensões chamada SWOT, cada dimensão da matriz é um par nome-valor"
# Implementamos como um dicionário com as 4 chaves solicitadas.
SWOT: Dict[str, int] = {
    "Forca": 50,
    "Fraqueza": 50,
    "Oportunidade": 50,
    "Ameaca": 50,
}


# ---------- Funções de decisão (SO, WO, ST, WT) -----------------------------
# Precisam existir com exatamente estes nomes e chamar os métodos conforme o DOC.

# As funções recebem instâncias de M3 e M8 para operar sobre elas.
def SO(m3: M3, m8: M8) -> None:
    """Cenário SO: chama M3.Render(), M3.Prender() e M8.Espalhar(), M8.Avancar()."""
    print("\n[SO] Cenário SO acionado (Eficiência).")
    m3.Render()
    m3.Prender()
    m8.Espalhar()
    m8.Avancar()

def WO(m3: M3, m8: M8) -> None:
    """Cenário WO: chama M3.Proteger(), M3.Abrigar() e M8.Reagrupar(), M8.Manter()."""
    print("\n[WO] Cenário WO acionado (Manutenção).")
    m3.Proteger()
    m3.Abrigar()
    m8.Reagrupar()
    m8.Manter()

def ST(m3: M3, m8: M8) -> None:
    """Cenário ST: chama M3.Prover(), M3.Auxiliar() e M8.Reagrupar(), M8.Manter()."""
    print("\n[ST] Cenário ST acionado (Resiliência sob ameaça).")
    m3.Prover()
    m3.Auxiliar()
    m8.Reagrupar()
    m8.Manter()

def WT(m3: M3, m8: M8) -> None:
    """Cenário WT: chama M3.Evadir(), M3.Retirar() e M8.Evadir(), M8.Retirar()."""
    print("\n[WT] Cenário WT acionado (Vulnerabilidade).")
    m3.Evadir()
    m3.Retirar()
    m8.Evadir()
    m8.Retirar()

# ---------- Função principal ------------------------------------------------
def main() -> None:
    print("Iniciando simulação SWOT...\n")
    print("SWOT inicial:", SWOT)

    # instâncias
    m3 = M3()
    m8 = M8()
    ambiente = Ambiente(temperatura=22.0, pressao=0.98, relevo="montanhoso", vegetacao="densa", fauna="diversa")
    oponente = Oponente("insurgente")

    print("\nInstâncias criadas:")
    print(" -", m3.estado())
    print(" -", m8.estado())
    print(" -", repr(ambiente))
    print(" -", repr(oponente))

    Forca = SWOT["Forca"]
    Fraqueza = SWOT["Fraqueza"]
    Oportunidade = SWOT["Oportunidade"]
    Ameaca = SWOT["Ameaca"]

    # Apresentando as variáveis para clareza
    print(f"\nAvaliação: Forca={Forca}, Fraqueza={Fraqueza}, Oportunidade={Oportunidade}, Ameaca={Ameaca}")

    # If Forca >= Fraqueza && Oportunidade >= Ameaca GOTO SO()
    if Forca >= Fraqueza and Oportunidade >= Ameaca:
        SO(m3, m8)

    # Else If Fraqueza > Forca && Oportunidade >= Ameaca GOTO WO()
    elif Fraqueza > Forca and Oportunidade >= Ameaca:
        WO(m3, m8)

    # Else If Forca >= Fraqueza && Ameaca > Oportunidade GOTO ST()
    elif Forca >= Fraqueza and Ameaca > Oportunidade:
        ST(m3, m8)

    # Else If Fraqueza > Forca && Ameaca > Oportunidade GOTO WT()
    elif Fraqueza > Forca and Ameaca > Oportunidade:
        WT(m3, m8)

    else:
        # /* nothing todo */
        print("\nNenhuma condição combinada satisfeita. Nothing to do.")

    print("\nSimulação finalizada.")


if __name__ == "__main__":
    main()


### Como testar / executar
### Salve o arquivo como: `simula_swot.py`
### Execute no terminal: `python simula_swot.py` (certifique-se de usar Python 3.12).
