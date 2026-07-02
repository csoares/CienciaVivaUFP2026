# Dia 1 - Movimento, Camara e Cores com o JetRacer

Neste primeiro dia os alunos vao conhecer o JetRacer AI Kit, aprender regras de
seguranca, programar movimentos simples e usar a camara para detetar cores.

O objetivo e' comecar de forma pratica: escrever pequenas instrucoes em Python,
ver o robot executar essas instrucoes e perceber que sensores e atuadores podem
ser combinados para criar comportamentos mais interessantes.

## Objetivos do Dia

No final do dia, os alunos devem conseguir:

- executar notebooks no JupyterLab do Jetson Nano;
- importar e usar o ficheiro `robot_kit.py`;
- mandar o robot andar para a frente, para tras, virar e parar;
- ajustar tempos de movimento para criar trajetorias simples;
- ligar a camara e tirar fotografias;
- medir valores medios de vermelho, verde e azul numa imagem;
- criar regras simples para o robot reagir a cores.

## Material Necessario

- JetRacer AI Kit com Jetson Nano;
- camara CSI ligada ao Jetson Nano;
- computador com acesso ao JupyterLab do Jetson;
- bateria carregada;
- espaco livre e seguro para testar movimentos;
- fita adesiva, cones ou pequenos obstaculos;
- cartoes ou objetos vermelhos, verdes e azuis.

## Ficheiros deste Dia

```text
day1/
  README_day1.md
  01_movimento.ipynb
  02_cores.ipynb
  robot_kit.py
  solucoes_professor.md
```

- `01_movimento.ipynb`: notebook da manha, dedicado ao movimento.
- `02_cores.ipynb`: notebook da tarde, dedicado a camara e cores.
- `robot_kit.py`: modulo de apoio com funcoes simples para os alunos.
- `solucoes_professor.md`: notas, calibracao e solucoes de referencia para o
  professor.

## Antes de Comecar

Confirmar em cada robot:

- a bateria esta' carregada;
- o robot esta' em modo autonomo, nao em controlo manual;
- o `robot_kit.py` esta' na mesma pasta que os notebooks;
- o robot para quando se executa `robot.parar()`;
- ha' espaco suficiente a frente do robot antes de testar movimento;
- a camara nao esta' aberta noutro notebook.

O professor deve calibrar cada robot antes da atividade. Ver detalhes em
`solucoes_professor.md`.

## Plano do Dia

| Bloco | Duracao | Atividade |
|---|---:|---|
| 1 | 20 min | Apresentacao do robot, seguranca e JupyterLab |
| 2 | 35 min | Primeiros movimentos: frente, tras e parar |
| 3 | 35 min | Virar, ajustar tempo e velocidade |
| 4 | 45 min | Desafio: desenhar um quadrado |
| 5 | 45 min | Desafio: contornar obstaculo |
| 6 | 30 min | Introducao a camara |
| 7 | 45 min | Medir cores nas imagens |
| 8 | 60 min | Desafio final: reagir a cores |

Os tempos sao indicativos. Se a turma precisar de mais tempo na parte de
movimento, reduzir a parte final de desafios.

## Parte 1 - Movimento

Notebook principal:

```text
01_movimento.ipynb
```

Os alunos comecam por executar:

```python
import robot_kit as robot
```

Funcoes principais:

```python
robot.andar_frente(1)
robot.andar_tras(1)
robot.virar_esquerda(1)
robot.virar_direita(1)
robot.parar()
```

Ideias importantes:

- o numero dentro da funcao e' o tempo em segundos;
- pequenas mudancas no tempo mudam bastante a distancia percorrida;
- robots reais nao sao perfeitamente precisos;
- testar, observar e ajustar faz parte da programacao robotica.

## Exercicios de Movimento

### Exercicio 1 - Primeiro Movimento

Fazer o robot andar para a frente durante pouco tempo e parar.

### Exercicio 2 - Andar para Tras

Testar movimento para tras e discutir porque e' preciso mais cuidado.

### Exercicio 3 - Virar

Comparar virar a esquerda e virar a direita. Ajustar o tempo para fazer curvas
mais pequenas ou maiores.

### Desafio 1 - Quadrado

Criar uma sequencia de quatro lados e quatro curvas.

Ideia:

```python
for _ in range(4):
    robot.andar_frente(1)
    robot.virar_direita(0.5)
```

Os valores devem ser ajustados por cada grupo.

### Desafio 2 - Contornar Obstaculo

Criar uma sequencia de movimentos para evitar um obstaculo simples.

Nao ha' uma solucao unica. O objetivo e' planear, testar e melhorar.

## Parte 2 - Camara e Cores

Notebook principal:

```text
02_cores.ipynb
```

Funcoes principais:

```python
robot.ligar_camera()
foto = robot.tirar_foto()
robot.mostrar_foto(foto)
robot.quanto_vermelho(foto)
robot.quanto_verde(foto)
robot.quanto_azul(foto)
robot.cor_dominante(foto)
```

Ideias importantes:

- a camara devolve uma imagem como numeros;
- cada pixel tem informacao de cor;
- a luz da sala muda os resultados;
- uma regra simples pode funcionar bem num caso e falhar noutro.

## Exercicios de Camara

### Exercicio 1 - Tirar Foto

Ligar a camara, tirar uma fotografia e mostrar no notebook.

### Exercicio 2 - Quanto de Cada Cor?

Medir quanto vermelho, verde e azul existe numa imagem.

### Exercicio 3 - Cor Dominante

Usar `robot.cor_dominante(foto)` para descobrir a cor mais forte.

### Exercicio 4 - Misturas de Cor

Testar objetos como amarelo, roxo ou branco e discutir porque a regra simples
pode dar respostas inesperadas.

### Desafio Final - Reagir a Cor

Criar uma funcao de decisao:

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

## Perguntas para Discussao

- Porque dois robots podem precisar de valores diferentes para virar?
- O robot esta' a perceber o mundo ou apenas a executar instrucoes?
- Porque a luz altera os valores da camara?
- Que limitacoes tem uma regra baseada so na cor dominante?
- Como poderiamos usar estes conhecimentos no Dia 2 para treinar um modelo?

## Resultado Esperado

No final do Dia 1, cada grupo deve ter:

- executado movimentos simples com seguranca;
- criado pelo menos uma trajetoria com varios passos;
- usado a camara para tirar e mostrar fotografias;
- medido cores em imagens;
- criado uma regra simples para reagir a cores.

## Seguranca

- Testar sempre movimentos curtos primeiro.
- Manter maos, cabos e objetos soltos afastados das rodas.
- Usar velocidades baixas.
- Garantir que existe espaco livre antes de executar uma celula de movimento.
- Usar `robot.parar()` sempre que o comportamento for inesperado.
- Nao deixar o robot autonomo sem supervisao.

