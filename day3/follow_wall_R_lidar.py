from rplidar import RPLidar
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output

# Abre a comunicacao com o RPLIDAR.
# Em alguns JetRacer a porta pode ser diferente, por exemplo /dev/ttyACM0.
lidar = RPLidar('/dev/ttyACM1', baudrate=115200)

# Distancia que queremos manter entre o JetRacer e a parede direita.
DISTANCIA_DESEJADA = 500  # mm

# Ganho proporcional: transforma o erro de distancia num valor de direcao.
# Um KP maior reage mais depressa, mas pode tornar o movimento instavel.
KP = 0.002

def distancia_direita(scan):
    # Guarda apenas as leituras que pertencem ao setor lateral direito.
    leituras = []

    for quality, angle, distance in scan:
        # Ignora leituras invalidas.
        if distance <= 0:
            continue

        # Setor lateral direito: janela estreita em torno dos 270 graus.
        # Usar uma janela evita depender de uma unica medicao exata.
        if 260 <= angle <= 280:
            leituras.append(distance)

    if not leituras:
        # None significa que nao houve medicoes validas nesse setor.
        return None

    # A menor distancia representa o ponto mais proximo da parede/obstaculo.
    return min(leituras)

for scan in lidar.iter_scans():
    # Le continuamente scans completos do LIDAR e estima a distancia a direita.
    d = distancia_direita(scan)

    if d is None:
        print("Parede direita não encontrada")
        continue

    # Erro positivo: estamos mais perto da parede do que a distancia desejada.
    # Erro negativo: estamos mais longe da parede do que a distancia desejada.
    erro = DISTANCIA_DESEJADA - d

    # Controlo proporcional simples: steering cresce na proporcao do erro.
    steering = KP * erro

    # Limita o comando ao intervalo normalmente aceite pelo servo/direcao.
    steering = max(-1.0, min(1.0, steering))

    print(f"Distância direita: {d:.0f} mm | erro: {erro:.0f} | steering: {steering:.2f}")
