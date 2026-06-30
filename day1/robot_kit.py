"""
robot_kit.py
============
Modulo de apoio para a formacao JetRacer - Dia 1.

Este ficheiro esconde a complexidade da API do JetRacer (classe NvidiaRacecar,
valores de steering/throttle entre -1 e 1) e da camara (jetcam.CSICamera,
imagens em BGR) atras de funcoes simples em portugues.

OS ALUNOS NAO PRECISAM DE PERCEBER ESTE FICHEIRO.
Usam apenas as funcoes na seccao "FUNCOES PARA OS ALUNOS" mais abaixo,
chamando-as como, por exemplo: robot.andar_frente(1)

PROFESSOR: ajusta a seccao de CONFIGURACAO consoante a calibracao de cada robot.
"""

import time
import numpy as np

# =================================================================
# CONFIGURACAO - ajustar por robot, se necessario
# =================================================================
VELOCIDADE_PADRAO = 0.25      # throttle por omissao, entre 0 e 1 (cuidado: o carro e' rapido!)
ANGULO_PADRAO = 0.5           # steering por omissao ao virar, entre 0 e 1

INVERTER_THROTTLE = False     # mudar para True se "andar_frente" andar para tras
INVERTER_STEERING = False     # mudar para True se "virar_esquerda" virar para a direita

LARGURA_CAMARA = 224
ALTURA_CAMARA = 224

# =================================================================
# LIGACAO AO CARRO (NvidiaRacecar) - feita uma unica vez ao importar
# =================================================================
from jetracer.nvidia_racecar import NvidiaRacecar

_car = NvidiaRacecar()
_car.throttle = 0.0
_car.steering = 0.0


def _val_throttle(v):
    return -v if INVERTER_THROTTLE else v


def _val_steering(v):
    return -v if INVERTER_STEERING else v


# =================================================================
# FUNCOES PARA OS ALUNOS - MOVIMENTO
# =================================================================

def parar():
    """Para o robot imediatamente."""
    _car.throttle = 0.0
    _car.steering = 0.0


def andar_frente(segundos, velocidade=VELOCIDADE_PADRAO):
    """
    Anda em frente, em linha reta, durante 'segundos'.
    Exemplo: robot.andar_frente(1.5)
    """
    _car.steering = _val_steering(0.0)
    _car.throttle = _val_throttle(velocidade)
    time.sleep(segundos)
    parar()


def andar_tras(segundos, velocidade=VELOCIDADE_PADRAO):
    """
    Anda para tras, em linha reta, durante 'segundos'.
    Exemplo: robot.andar_tras(1)
    """
    _car.steering = _val_steering(0.0)
    _car.throttle = _val_throttle(-velocidade)
    time.sleep(segundos)
    parar()


def virar_esquerda(segundos, velocidade=VELOCIDADE_PADRAO, angulo=ANGULO_PADRAO):
    """
    Anda para a frente a virar para a esquerda, durante 'segundos'.
    Exemplo: robot.virar_esquerda(1)
    """
    _car.steering = _val_steering(-angulo)
    _car.throttle = _val_throttle(velocidade)
    time.sleep(segundos)
    parar()


def virar_direita(segundos, velocidade=VELOCIDADE_PADRAO, angulo=ANGULO_PADRAO):
    """
    Anda para a frente a virar para a direita, durante 'segundos'.
    Exemplo: robot.virar_direita(1)
    """
    _car.steering = _val_steering(angulo)
    _car.throttle = _val_throttle(velocidade)
    time.sleep(segundos)
    parar()


# =================================================================
# FUNCOES PARA OS ALUNOS - CAMARA E COR
# =================================================================

from jetcam.csi_camera import CSICamera
import ipywidgets
from IPython.display import display
from jetcam.utils import bgr8_to_jpeg

_camera = None


def ligar_camera():
    """
    Liga a camara do robot. So precisa de ser chamada uma vez no inicio.
    Exemplo: robot.ligar_camera()
    """
    global _camera
    if _camera is None:
        _camera = CSICamera(width=LARGURA_CAMARA, height=ALTURA_CAMARA)
        # Em vez de pedir um frame "avulso" de cada vez (o que pode devolver
        # um frame antigo que ficou em buffer no pipeline GStreamer/V4L2),
        # mantemos a camara a capturar continuamente em segundo plano.
        # Isto garante que o frame mais recente esta' sempre disponivel,
        # evitando o efeito de "imagens atrasadas/antigas".
        _camera.running = True
        time.sleep(1.0)  # esperar que o pipeline estabilize
    return _camera


def tirar_foto():
    """
    Tira uma foto com a camara e devolve a imagem.
    Tens de guardar o resultado numa variavel para a poderes usar.
    Exemplo: foto = robot.tirar_foto()
    """
    cam = ligar_camera()
    return cam.value


def mostrar_foto(imagem):
    """
    Mostra, no notebook, uma imagem tirada com tirar_foto().
    Exemplo: robot.mostrar_foto(foto)
    """
    widget = ipywidgets.Image(format="jpeg")
    widget.value = bgr8_to_jpeg(imagem)
    display(widget)


def quanto_vermelho(imagem):
    """Devolve um numero entre 0 e 255: quanto vermelho ha' na imagem."""
    return float(np.mean(imagem[:, :, 2]))


def quanto_verde(imagem):
    """Devolve um numero entre 0 e 255: quanto verde ha' na imagem."""
    return float(np.mean(imagem[:, :, 1]))


def quanto_azul(imagem):
    """Devolve um numero entre 0 e 255: quanto azul ha' na imagem."""
    return float(np.mean(imagem[:, :, 0]))


def cor_dominante(imagem):
    """
    Devolve qual e' a cor mais forte na imagem: 'vermelho', 'verde' ou 'azul'.
    Exemplo: cor = robot.cor_dominante(foto)
    """
    valores = {
        "vermelho": quanto_vermelho(imagem),
        "verde": quanto_verde(imagem),
        "azul": quanto_azul(imagem),
    }
    return max(valores, key=valores.get)


def reagir_as_cores(funcao_decisao, duracao_segundos=15):
    """
    Corre em ciclo durante 'duracao_segundos':
      1. tira uma foto
      2. descobre a cor dominante
      3. chama a tua funcao funcao_decisao(cor) para decidir o que o robot faz
    No final, o robot para sozinho.

    Exemplo:
        def decide(cor):
            if cor == "vermelho":
                robot.parar()
            else:
                robot.andar_frente(0.3)

        robot.reagir_as_cores(decide, 15)
    """
    inicio = time.time()
    try:
        while time.time() - inicio < duracao_segundos:
            imagem = tirar_foto()
            cor = cor_dominante(imagem)
            funcao_decisao(cor)
    finally:
        parar()