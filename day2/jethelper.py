# jethelper.py
import time
import cv2
import ipywidgets.widgets as widgets
from jetracer.nvidia_racecar import NvidiaRacecar

# Inicializa o carro globalmente para evitar conflitos de re-inicialização
try:
    car = NvidiaRacecar()
except Exception as e:
    print("Aviso: Não foi possível ligar ao hardware do carro. Modo simulação ativo.")
    car = None

def mover(velocidade, direcao):
    """Define a velocidade (-1.0 a 1.0) e a direção (-1.0 a 1.0)"""
    if car:
        car.throttle = velocidade
        car.steering = direcao

def parar():
    """Pára o carro imediatamente"""
    if car:
        car.throttle = 0.0
        car.steering = 0.0

def esperar(segundos):
    """Faz uma pausa no código por X segundos"""
    time.sleep(segundos)
