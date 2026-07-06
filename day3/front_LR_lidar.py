
from rplidar import RPLidar
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output

# Abre a comunicacao com o RPLIDAR.
# Em alguns JetRacer a porta pode ser diferente, por exemplo /dev/ttyACM0.
lidar = RPLidar('/dev/ttyACM1', baudrate=115200)

def setores(scan):
    # Cada scan contem muitas medicoes no formato:
    # (qualidade, angulo_em_graus, distancia_em_mm).
    # Vamos separar essas medicoes em tres zonas importantes para navegacao.
    esquerda = []
    frente = []
    direita = []

    for quality, angle, distance in scan:
        # Distancias invalidas ou sem leitura aparecem como 0.
        if distance <= 0:
            continue

        # Frente: pequena janela em torno dos 0 graus.
        # Como o angulo tambem pode aparecer perto de 360, usamos duas condicoes.
        if angle <= 20 or angle >= 340:
            frente.append(distance)
        # Esquerda: pontos entre a frente e o lado esquerdo.
        elif 20 < angle < 90:
            esquerda.append(distance)
        # Direita: pontos entre o lado direito e a frente.
        elif 270 < angle < 340:
            direita.append(distance)

    # Para cada setor usamos a menor distancia, porque o obstaculo mais perto
    # e o que mais interessa para decidir a manobra.
    return {
        "frente": min(frente) if frente else None,
        "esquerda": min(esquerda) if esquerda else None,
        "direita": min(direita) if direita else None
    }

def decidir_acao(s):
    # Recebe as distancias minimas por setor e transforma-as numa acao simples.
    frente = s["frente"]
    esquerda = s["esquerda"]
    direita = s["direita"]

    # Se ha algo a menos de 600 mm na frente, o robo deve evitar o obstaculo.
    if frente is not None and frente < 600:
        if esquerda is not None and direita is not None:
            # Escolhe o lado com mais espaco livre.
            if esquerda > direita:
                return "VIRAR ESQUERDA"
            else:
                return "VIRAR DIREITA"
        # Se nao ha informacao suficiente dos lados, a opcao segura e parar.
        return "PARAR"

    # Se a frente esta livre, o robo pode continuar.
    return "SEGUIR EM FRENTE"



for scan in lidar.iter_scans():
    # O ciclo corre continuamente: le um scan, calcula os setores e decide a acao.
    s = setores(scan)
    acao = decidir_acao(s)
    print(s, "=>", acao)
