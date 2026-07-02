# Ciencia Viva UFP 2026 - Robotica com JetRacer AI Kit

Este repositorio organiza uma atividade de 3 dias para alunos em ferias usando
um robot JetRacer AI Kit com Jetson Nano. A progressao vai de movimentos simples
e camara ate treino de modelos, LIDAR, ROS1, visualizacao e SLAM.

Cada dia tem uma pasta propria com o respetivo guiao e materiais de apoio.

## Indice

| Dia | Tema | README |
|---|---|---|
| Dia 1 | Movimento, camara e cores | [day1/README_day1.md](day1/README_day1.md) |
| Dia 2 | Camara, recolha de dados e treino de modelos | [day2/README_day2.md](day2/README_day2.md) |
| Dia 3 | LIDAR, ROS1, joystick, SLAM e modelos com sensores | [day3/README_day3.md](day3/README_day3.md) |

## Visao Geral

### Dia 1 - Movimento, Camara e Cores

Os alunos aprendem a controlar o JetRacer com Python, testam movimentos simples,
criam pequenos percursos e usam a camara para detetar cores. Este dia introduz
os conceitos basicos de atuadores, sensores e regras de decisao.

### Dia 2 - Camara, Dados e Treino

O foco passa a ser IA pratica: recolher imagens, organizar dados, treinar um
modelo simples e testar previsoes no robot. O objetivo e' perceber que a
qualidade dos dados influencia diretamente o comportamento do modelo.

### Dia 3 - LIDAR, ROS1 e SLAM

O robot passa a usar LIDAR para medir distancias, visualizar sensores em
Foxglove/RViz, experimentar controlo por joystick e observar uma demonstracao de
SLAM. Tambem se discute como combinar modelos treinados com regras de seguranca
baseadas em sensores.

## Estrutura do Repositorio

```text
.
  README.md
  day1/
    README_day1.md
    01_movimento.ipynb
    02_cores.ipynb
    robot_kit.py
    solucoes_professor.md
  day2/
    README_day2.md
  day3/
    README_day3.md
```

## Nota para o Professor

Antes da atividade, testar cada robot individualmente:

- movimento para a frente e para tras;
- direcao esquerda/direita;
- paragem;
- camara;
- bateria;
- ligacao ao JupyterLab;
- sensores adicionais, especialmente LIDAR no Dia 3.

Robots diferentes podem precisar de pequena calibracao. No Dia 1, o ficheiro
`day1/solucoes_professor.md` inclui notas especificas para calibrar
`robot_kit.py`.

