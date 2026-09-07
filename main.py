import random


# Configuració de la simulació

JUGADORS_PER_ESTRATEGIA = 10
RONDES_PER_PARTIDA = 20
GENERACIONS = 3
JUGADORS_ELIMINATS = 2


# Funció de pagament

def pagament(jugada_a, jugada_b):

    if jugada_a == "C" and jugada_b == "C":
        return (3, 3)

    elif jugada_a == "C" and jugada_b == "T":
        return (0, 5)

    elif jugada_a == "T" and jugada_b == "C":
        return (5, 0)

    else:
        return (1, 1)


# Estratègies

def sempre_cooperar(historial_propi, historial_oponent):
    return "C"

sempre_cooperar.nom = "Sempre Cooperar"


def sempre_trair(historial_propi, historial_oponent):
    return "T"

sempre_trair.nom = "Sempre Trair"


def tit_for_tat(historial_propi, historial_oponent):

    if len(historial_oponent) == 0:
        return "C"

    return historial_oponent[-1]

tit_for_tat.nom = "Tit for Tat"


def tit_for_two_tats(historial_propi, historial_oponent):

    if len(historial_oponent) < 2:
        return "C"

    if historial_oponent[-1] == "T" and historial_oponent[-2] == "T":
        return "T"

    return "C"

tit_for_two_tats.nom = "Tit for Two Tats"


def atzar(historial_propi, historial_oponent):

    return random.choice(["C", "T"])

atzar.nom = "Atzar"


def atzar_cooperatiu(historial_propi, historial_oponent):

    if random.random() < 0.7:
        return "C"

    return "T"

atzar_cooperatiu.nom = "Atzar Cooperatiu"


def atzar_traidor(historial_propi, historial_oponent):

    if random.random() < 0.3:
        return "C"

    return "T"

atzar_traidor.nom = "Atzar Traïdor"


def venjanca(historial_propi, historial_oponent):

    if "T" in historial_oponent:
        return "T"

    return "C"

venjanca.nom = "Venjança"


def majoria_rival_bona(historial_propi, historial_oponent):

    if len(historial_oponent) == 0:
        return "C"

    cooperacions = historial_oponent.count("C")
    traicions = historial_oponent.count("T")

    if cooperacions > traicions:
        return "C"

    return "T"

majoria_rival_bona.nom = "Majoria Rival Bona"


def majoria_rival_dolenta(historial_propi, historial_oponent):

    if len(historial_oponent) == 0:
        return "T"

    cooperacions = historial_oponent.count("C")
    traicions = historial_oponent.count("T")

    if cooperacions > traicions:
        return "C"

    return "T"

majoria_rival_dolenta.nom = "Majoria Rival Dolenta"


def detectiu(historial_propi, historial_oponent):

    primeres_jugades = ["C", "T", "C", "C"]

    if len(historial_propi) < 4:
        return primeres_jugades[len(historial_propi)]

    if "T" not in historial_oponent:
        return "T"

    return historial_oponent[-1]

detectiu.nom = "Detectiu"


def contrari(historial_propi, historial_oponent):

    if len(historial_oponent) == 0:
        return "C"

    if historial_oponent[-1] == "C":
        return "T"

    return "C"

contrari.nom = "Contrari"


# Classe Jugador

class Jugador:

    def __init__(self, estrategia):

        self.estrategia = estrategia
        self.nom_estrategia = estrategia.nom

        self.historial_propi = []
        self.historial_oponent = []

        self.puntuacio = 0

    def jugar(self, oponent):

        jugada_propia = self.estrategia(
            self.historial_propi,
            self.historial_oponent
        )

        jugada_oponent = oponent.estrategia(
            oponent.historial_propi,
            oponent.historial_oponent
        )

        self.historial_propi.append(jugada_propia)
        self.historial_oponent.append(jugada_oponent)

        oponent.historial_propi.append(jugada_oponent)
        oponent.historial_oponent.append(jugada_propia)

        punts_propis, punts_oponent = pagament(
            jugada_propia,
            jugada_oponent
        )

        self.puntuacio += punts_propis
        oponent.puntuacio += punts_oponent


# Funcions de gestió dels jugadors

def reiniciar_jugadors(jugadors):

    for jugador in jugadors:

        jugador.historial_propi = []
        jugador.historial_oponent = []
        jugador.puntuacio = 0


def ordenar_jugadors(jugadors):

    return sorted(
        jugadors,
        key=lambda jugador: jugador.puntuacio,
        reverse=True
    )


def eliminar_jugadors(jugadors, quantitat):

    return jugadors[:-quantitat]


def reproduir_jugadors(jugadors, quantitat):

    nous_jugadors = []

    for i in range(quantitat):

        jugador_pare = jugadors[i]

        nou_jugador = Jugador(jugador_pare.estrategia)

        nous_jugadors.append(nou_jugador)

    return nous_jugadors


def comptar_estrategies(jugadors):

    comptador = {}

    for jugador in jugadors:

        nom = jugador.nom_estrategia

        if nom not in comptador:
            comptador[nom] = 0

        comptador[nom] += 1

    return comptador


# Funcions de joc

def jugar_partida(jugador1, jugador2, rondes):

    for _ in range(rondes):

        jugador1.jugar(jugador2)


def jugar_torneig(jugadors, rondes):

    for i in range(len(jugadors)):

        for j in range(i + 1, len(jugadors)):

            jugar_partida(
                jugadors[i],
                jugadors[j],
                rondes
            )


# Estratègies disponibles

estrategies = [
    sempre_cooperar,
    sempre_trair,
    tit_for_tat,
    tit_for_two_tats,
    atzar,
    atzar_cooperatiu,
    atzar_traidor,
    venjanca,
    majoria_rival_bona,
    majoria_rival_dolenta,
    detectiu,
    contrari
]


# Executar simulació

def executar_simulacio(
    jugadors_per_estrategia,
    rondes_per_partida,
    generacions,
    jugadors_eliminats
):

    jugadors = []

    for estrategia in estrategies:

        for _ in range(jugadors_per_estrategia):

            jugador = Jugador(estrategia)

            jugadors.append(jugador)

    evolucio = []

    for generacio in range(generacions):

        jugar_torneig(
            jugadors,
            rondes_per_partida
        )

        jugadors_ordenats = ordenar_jugadors(jugadors)

        jugadors = eliminar_jugadors(
            jugadors_ordenats,
            jugadors_eliminats
        )

        nous_jugadors = reproduir_jugadors(
            jugadors_ordenats,
            jugadors_eliminats
        )

        jugadors.extend(nous_jugadors)

        poblacio = comptar_estrategies(jugadors)

        evolucio.append(poblacio)

        reiniciar_jugadors(jugadors)

    return evolucio
