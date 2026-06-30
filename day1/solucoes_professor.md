# Guia do Professor - Dia 1 (Movimento + Cor)

Este ficheiro é só para ti. Não dês isto aos alunos antes dos desafios,
para não estragares a descoberta.

## Antes da formação: calibração (importante!)

A classe `NvidiaRacecar` usa `steering` e `throttle` entre -1 e 1.
Cada robot pode estar montado/cablado de forma ligeiramente diferente, por
isso, **antes da formação**, testa em cada robot:

```python
from jetracer.nvidia_racecar import NvidiaRacecar
import time

car = NvidiaRacecar()
car.steering = 0.0
car.throttle = 0.2   # deve andar para a frente
time.sleep(1)
car.throttle = 0.0
```

- Se o robot andar para **trás** em vez de para a frente: abre o `robot_kit.py`
  e muda `INVERTER_THROTTLE = True`.
- Testa depois `car.steering = -0.5` com throttle ligeiro: deve virar para a
  **esquerda**. Se virar para a direita, muda `INVERTER_STEERING = True`.
- Ajusta também `VELOCIDADE_PADRAO` (0.25 é conservador) e `ANGULO_PADRAO`
  conforme o espaço que tiveres disponível na sala - em espaço apertado,
  reduz para 0.15-0.2.

Se tiveres vários robots, é provável que cada um precise de uma pequena
afinação diferente — vale a pena ter um `robot_kit.py` ligeiramente
ajustado por máquina, ou documentar os valores por etiqueta/número de robot.

## Distribuir os ficheiros

1. Copia `robot_kit.py`, `01_movimento.ipynb` e `02_cores.ipynb` para a
   **mesma pasta** em cada Jetson (ex: `~/jetracer/notebooks/day1/`).
   O `robot_kit.py` tem de estar na mesma pasta que os notebooks, ou os
   alunos têm de ajustar o `import`.
2. Mais fácil: abre o JupyterLab no browser (`http://<ip_da_jetson>:8888`)
   e arrasta os 3 ficheiros para dentro da pasta `day1`.

## Timings sugeridos (manhã, ~3h)

| Bloco | Tempo |
|---|---|
| Intro + segurança + Exercício 1 e 2 | 20 min |
| Exercício 3 (virar) | 15 min |
| Desafio 1 - quadrado | 30 min |
| Pausa | 15 min |
| Desafio 2 - contornar obstáculo | 45 min |
| Desafio bónus - zigzag (quem terminar cedo) | resto do tempo |

## Timings sugeridos (tarde, ~3h)

| Bloco | Tempo |
|---|---|
| Intro câmara + Exercícios 1-3 | 30 min |
| Exercício 4 - misturas de cor | 30 min |
| Pausa | 15 min |
| Desafio final - reagir a cores | 60 min |
| Desafio bónus | resto do tempo |

## Soluções de referência

### Desafio 1 - Quadrado (manhã)

```python
for _ in range(4):
    robot.andar_frente(1)
    robot.virar_direita(0.5)
```

(Os valores `1` e `0.5` vão precisar de afinação experimental consoante a
velocidade/ângulo calibrados — incentiva os alunos a testar e ajustar, é
parte do exercício.)

### Desafio 2 - Contornar obstáculo (manhã)

Não há solução única; um exemplo razoável, assumindo o obstáculo a ~50cm
em linha reta à frente:

```python
robot.virar_direita(0.5)   # sai da trajetória
robot.andar_frente(1)      # avança ao lado do obstáculo
robot.virar_esquerda(0.5)  # volta a direção original
robot.andar_frente(0.5)    # passa o obstáculo
robot.virar_esquerda(0.5)  # aponta de volta para a linha original
robot.andar_frente(1)
robot.virar_direita(0.5)   # endireita
```

### Exercício 4 - Misturas de cor (tarde)

Ponto importante a discutir com a turma: como `cor_dominante()` só escolhe
entre vermelho/verde/azul, para um objeto **amarelo** (muito vermelho +
muito verde) a função vai responder "vermelho" ou "verde" — qualquer que
tiver o valor ligeiramente mais alto — nunca "amarelo". Isto é uma boa
oportunidade para discutir as limitações desta abordagem simples, e abre
a porta para falar (mesmo que só conceptualmente) de deteção de cor mais
avançada nos dias seguintes, se isso fizer parte do plano do curso.

### Desafio final - Reagir a cores (tarde)

```python
def decide(cor):
    if cor == "vermelho":
        robot.parar()
    elif cor == "verde":
        robot.andar_frente(0.3)
    elif cor == "azul":
        robot.virar_direita(0.3)

robot.reagir_as_cores(decide, 15)
```

## Problemas comuns que podem surgir

- **"O robot não anda"**: verificar o interrutor de override manual no
  emissor RC (mencionado no notebook de fábrica `basic_motion.ipynb`) —
  tem de estar em modo autónomo, não manual.
- **Câmara não liga / erro ao criar `CSICamera`**: normalmente porque já
  havia uma instância de câmara aberta noutro notebook/kernel a correr.
  Pede para os alunos irem ao menu Kernel → Shutdown All Kernels antes de
  abrir o notebook da tarde.
- **Cores sempre erradas (vermelho e azul trocados)**: a `CSICamera`
  devolve imagens em BGR, não RGB — isto já está tratado dentro do
  `robot_kit.py` (`quanto_vermelho` lê o canal 2, `quanto_azul` lê o canal
  0). Se ainda assim os alunos virem valores trocados, confirma que não
  estão a aceder aos canais diretamente em vez de usar as funções dadas.
