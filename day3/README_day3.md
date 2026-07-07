# Dia 3 - LIDAR, ROS1, SLAM e Modelos Mais Inteligentes

Neste dia vamos juntar uma nova forma de percecao ao JetRacer: o LIDAR. No Dia
2 o robot usou a camara para ver imagens. Agora vamos usar distancias medidas em
volta do robot, visualizar essas leituras, experimentar controlo por joystick e
discutir como um robot pode construir um mapa do espaco.

Tambem vamos continuar o trabalho de treino de modelos, comparando o que a
camara consegue perceber com o que o LIDAR mede diretamente.

O objetivo nao e' transformar o JetRacer num robot autonomo completo num so dia.
O objetivo e' perceber as pecas principais de um sistema robotico moderno:

1. Sensores: camara e LIDAR.
2. Software de comunicacao: ROS1.
3. Visualizacao: Foxglove ou ferramenta equivalente.
4. Controlo: joystick ou comandos de velocidade.
5. Mapeamento: SLAM.
6. Modelos treinados: decisoes aprendidas a partir de dados.

## Objetivos do Dia

No final do dia, os alunos devem conseguir:

- explicar a diferenca entre camara e LIDAR;
- visualizar leituras de distancia do LIDAR;
- perceber a ideia de topicos em ROS1;
- controlar o robot com joystick ou comandos simples;
- observar um mapa a ser construido com SLAM;
- perceber como os dados do LIDAR podem ajudar a treinar ou melhorar modelos;
- identificar limites e riscos de um robot autonomo.

## Material Necessario

- JetRacer AI Kit com Jetson Nano;
- LIDAR compativel com ROS1;
- camara CSI usada no Dia 2;
- computador ligado a mesma rede do Jetson;
- joystick ou comando USB/Bluetooth;
- pista ou espaco fechado com paredes/obstaculos seguros;
- bateria carregada;
- Foxglove Studio, RViz ou outra ferramenta de visualizacao ROS;
- imagem/software do Jetson com ROS1 e drivers do LIDAR preparados.

## Antes de Comecar

Confirma em cada robot:

- o LIDAR esta' bem fixo e ligado;
- o LIDAR consegue rodar ou medir sem tocar em cabos;
- o robot esta' em modo autonomo;
- o joystick foi detetado pelo sistema;
- o botao ou comando de paragem funciona;
- a rede entre computador e Jetson esta' estavel;
- as rodas foram testadas primeiro com o robot levantado.

Este dia tem mais componentes a correr ao mesmo tempo. Se algo falhar, testar uma
peca de cada vez: primeiro LIDAR, depois ROS, depois visualizacao, depois
controlo, e so no fim movimento autonomo.

## Estrutura da Pasta `day3`

Ficheiros usados neste dia:

```text
day3/
  README_day3.md
  test_LIDAR.ipynb
  front_LR_lidar.py
  follow_wall_R_lidar.py
  jetracer_follow_at_fixed_distance_4.ipynb
  jetracer_road_following_sinais.ipynb
  readme_foxglove.md
  readme_slam.md
```


## Plano do Dia

| Bloco | Duracao | Tema | Atividade pratica | Ficheiros/tecnologias |
|---|---:|---|---|---|
| 1 | 20 min | Arranque e seguranca | Rever o Dia 2, testar bateria, rodas levantadas, botao de paragem e ligacoes da camara/LIDAR. | JetRacer, camara CSI, RPLIDAR |
| 2 | 45 min | LIDAR basico | Confirmar a porta serie, ler informacao do sensor, recolher scans e observar distancias em texto/graficos. | `test_LIDAR.ipynb`, `front_LR_lidar.py` |
| 3 | 45 min | Decisoes com LIDAR | Dividir o scan em frente/esquerda/direita, detetar obstaculos e testar uma regra simples de decisao. | `front_LR_lidar.py`, `follow_wall_R_lidar.py` |
| 4 | 60 min | Road following com sinais | Reutilizar a camara para seguir a estrada e reconhecer sinais, discutindo como o LIDAR pode servir de seguranca. | `jetracer_road_following_sinais.ipynb`, modelo do Dia 2 |
| 5 | 45 min | ROS1 | Introduzir `roscore`, `rostopic list`, `/scan`, `/cmd_vel`, `/joy` e a ideia de varios nos a comunicar. | ROS Melodic, `rostopic`, drivers do robot |
| 6 | 45 min | Foxglove | Ligar o Foxglove ao robot por WebSocket e visualizar topicos em tempo real. | `readme_foxglove.md`, `foxglove_bridge`, `/scan`, `/cmd_vel` |
| 7 | 60 min | SLAM | Arrancar o LIDAR e o pacote de SLAM, conduzir devagar e observar o mapa a ser construido. | `readme_slam.md`, Hector SLAM/GMapping, `/map`, `/tf`, `/odom` |
| 8 | 30 min | Integracao final | Demonstrar road following com sinais e discutir como LIDAR, ROS, Foxglove e SLAM se complementam. | JetRacer completo, pista, mapa e visualizacao |

## Parte 1 - O que e' um LIDAR?

Uma camara devolve uma imagem. Um LIDAR devolve distancias.

Ideia simples:

```text
camara -> cores, formas, textura
LIDAR  -> distancias, paredes, obstaculos
```

Perguntas para os alunos:

- A camara consegue medir distancia diretamente?
- O LIDAR consegue saber a cor de um objeto?
- Que sensor e' melhor numa sala escura?
- Que sensor e' melhor para ler um sinal colorido?

O ponto importante: sensores diferentes dao informacao diferente. Robots reais
normalmente combinam varios sensores.

## Parte 2 - Primeiras Leituras do LIDAR

Antes de mexer em SLAM, confirmar que o LIDAR esta' a produzir dados.

Em ROS1, uma leitura de LIDAR costuma aparecer num topico semelhante a:

```text
/scan
```

Comandos uteis:

```bash
rostopic list
rostopic echo /scan
rostopic hz /scan
```

O que observar:

- `rostopic list` mostra os topicos ativos;
- `rostopic echo /scan` mostra os valores recebidos;
- `rostopic hz /scan` mostra a frequencia das leituras.

Se os valores nao aparecem, verificar:

- cabo USB;
- permissao da porta serie;
- driver correto do LIDAR;
- se o processo do driver esta' a correr;
- se outro programa ja esta' a usar o LIDAR.

## Parte 3 - Ideia Basica de ROS1

ROS1 ajuda os programas do robot a comunicarem entre si.

Explicacao simples:

```text
no do LIDAR       -> publica /scan
no do joystick    -> publica /joy
no de controlo    -> publica /cmd_vel
no de visualizacao -> le /scan, /map, /tf
```

Vocabulario minimo:

- `node`: um programa a correr;
- `topic`: um canal de mensagens;
- `publish`: enviar mensagens para um topico;
- `subscribe`: receber mensagens de um topico;
- `launch`: ficheiro para arrancar varios nos ao mesmo tempo.

Nao e' preciso decorar tudo. O importante e' perceber que o robot e' feito de
varios programas pequenos a trocar mensagens.

## Parte 4 - Visualizacao com Foxglove ou RViz

Para este dia, Foxglove e' uma boa opcao para mostrar aos alunos o que o robot
esta' a sentir. RViz tambem pode ser usado se ja estiver preparado na imagem.

Topicos interessantes para visualizar:

```text
/scan
/tf
/map
/odom
/cmd_vel
/joy
```

Atividade sugerida:

1. abrir a visualizacao;
2. ligar ao robot;
3. mostrar o LIDAR em tempo real;
4. aproximar uma parede ou caixa do robot;
5. observar as distancias a mudar;
6. rodar o robot devagar e ver como a leitura muda.

Ponto de discussao:

- o LIDAR nao "ve" uma parede como uma imagem;
- ele mede pontos ou distancias;
- o mapa e' construido a partir de muitas leituras ao longo do tempo.

## Parte 5 - Controlo por Joystick

Antes de autonomia, usar controlo manual ajuda a testar o robot com seguranca.

Topicos comuns:

```text
/joy
/cmd_vel
```

Fluxo esperado:

```text
joystick -> /joy -> no de teleop -> /cmd_vel -> robot
```

Sugestão: usar como alternativa a Foxglove Extensions "Teleop Twist Keyboard" para controlar com teclado

Teste seguro:

1. ligar o joystick;
2. confirmar que `/joy` recebe dados;
3. testar `/cmd_vel` com o robot levantado;
4. baixar o robot para o chao;
5. usar velocidade baixa;
6. manter uma pessoa pronta para parar o robot.

Comandos uteis:

```bash
rostopic echo /joy
rostopic echo /cmd_vel
```

Desafio: cada grupo deve conseguir conduzir o robot lentamente pela pista sem
tocar nos obstaculos.

## Parte 6 - SLAM: Construir um Mapa

SLAM significa localizacao e mapeamento simultaneos. Em linguagem simples:

```text
Onde estou?
Como e' o espaco a minha volta?
```

Para uma demonstracao, o professor pode preparar um pacote de SLAM compativel
com ROS1, por exemplo `gmapping`, `hector_slam` ou outro pacote ja testado com o
LIDAR disponivel.

Topicos normalmente envolvidos:

```text
/scan
/tf
/odom
/map
```

Atividade:

1. arrancar o driver do LIDAR;
2. arrancar odometria ou transformacoes necessarias;
3. arrancar o pacote de SLAM;
4. abrir Foxglove/RViz;
5. conduzir o robot devagar com joystick;
6. observar o mapa a aparecer.

Pontos importantes:

- movimentos bruscos pioram o mapa;
- rodas a derrapar confundem a odometria;
- paredes lisas e corredores muito iguais podem ser dificeis;
- SLAM nao e' magia: depende da qualidade dos sensores e do movimento.

## Parte 7 - Continuar o Treino de Modelos

No Dia 2 treinamos modelos com imagens. No Dia 3 podemos melhorar a ideia usando
LIDAR.

Possiveis tarefas:

- prever `livre` ou `obstaculo` usando distancias do LIDAR;
- combinar decisao da camara com distancia minima do LIDAR;
- usar LIDAR como seguranca: se ha' obstaculo perto, parar sempre;
- recolher exemplos com camara + LIDAR para comparar sensores.

Exemplo conceptual:

```python
decisao_camera = modelo_camera(imagem)
distancia_minima = ler_distancia_minima_lidar(scan)

if distancia_minima < 0.30:
    robot.parar()
elif decisao_camera == "frente":
    robot.andar_frente(0.2)
elif decisao_camera == "esquerda":
    robot.virar_esquerda(0.2)
elif decisao_camera == "direita":
    robot.virar_direita(0.2)
else:
    robot.parar()
```

Mensagem principal para os alunos: mesmo quando usamos IA, regras simples de
seguranca continuam a ser importantes.

## Desafios

### Desafio 1 - Distancia Minima

Usar as leituras do LIDAR para descobrir a distancia mais proxima ao robot.

Perguntas:

- onde esta' o obstaculo mais perto?
- a leitura muda quando alguem passa a frente?
- ha' leituras estranhas ou ruidosas?

### Desafio 2 - Travagem de Seguranca

Criar uma regra:

```text
se obstaculo estiver muito perto -> parar
caso contrario -> permitir movimento
```

Testar primeiro sem movimento e so depois com o robot muito lento.

### Desafio 3 - Mapa da Sala

Conduzir o robot com joystick e tentar criar um mapa simples da sala ou pista.

Comparar:

- mapa depois de conduzir devagar;
- mapa depois de conduzir com movimentos bruscos;
- zonas que ficaram bem representadas;
- zonas que ficaram confusas.

### Desafio 4 - Camara + LIDAR

Usar o modelo treinado no Dia 2, mas adicionar uma regra com LIDAR:

```text
modelo decide direcao
LIDAR decide se e' seguro mover
```

## Perguntas para Discussao

- Porque um robot pode precisar de mais do que um sensor?
- O LIDAR funciona melhor ou pior do que a camara?
- O que acontece se o LIDAR falhar?
- Um mapa gerado por SLAM e' sempre correto?
- A IA deve poder mandar o robot andar se o sensor de distancia diz que ha'
  obstaculo?
- Que partes deste sistema aparecem em carros autonomos reais?

## Resultado Esperado

No final do Dia 3, cada grupo deve ter:

- observado leituras reais do LIDAR;
- visualizado dados do robot em Foxglove, RViz ou ferramenta equivalente;
- controlado o robot com joystick ou comandos simples;
- visto uma demonstracao de SLAM;
- melhorado ou discutido um modelo usando dados do LIDAR;
- preparado uma pequena demonstracao final do projeto.

## Seguranca

- Testar motores sempre com o robot levantado antes de o colocar no chao.
- Usar velocidades baixas.
- Nao deixar o robot autonomo sem supervisao.
- Manter cabos afastados das rodas e do LIDAR.
- Nao olhar para o LIDAR a curta distancia se o fabricante indicar restricoes.
- Ter sempre uma forma rapida de parar o robot.
- Parar imediatamente se o mapa, o joystick ou o modelo tiverem comportamento
  inesperado.
