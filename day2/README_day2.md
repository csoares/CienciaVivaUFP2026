# Dia 2 - Camara, Dados e Treino com o JetRacer AI Kit

Neste dia vamos deixar de programar apenas movimentos fixos e comecar a usar a
camara do JetRacer para recolher dados, treinar um pequeno modelo de IA e testar
o comportamento no robot.

O objetivo nao e' fazer um carro autonomo perfeito. O objetivo e' perceber o
ciclo completo:

1. Ver o mundo pela camara do robot.
2. Recolher exemplos.
3. Treinar um modelo com esses exemplos.
4. Testar o modelo no Jetson Nano.
5. Melhorar o resultado com mais dados ou dados melhores.

## Objetivos do Dia

No final do dia, os alunos devem conseguir:

- ligar e visualizar a camara do JetRacer;
- perceber que uma imagem e' uma matriz de numeros;
- recolher imagens para diferentes classes ou decisoes;
- treinar um modelo simples usando os dados recolhidos;
- testar o modelo no robot;
- discutir porque o modelo acerta em alguns casos e falha noutros.

## Material Necessario

- JetRacer AI Kit com Jetson Nano;
- camara CSI ligada ao Jetson Nano;
- computador com acesso ao JupyterLab do Jetson;
- pista simples, fita adesiva ou cartolina para marcar o percurso;
- objetos/cartoes para criar situacoes de treino;
- bateria carregada;
- espaco livre e seguro para testes.

## Antes de Comecar

Confirma em cada robot:

- a bateria esta' carregada;
- o robot esta' em modo autonomo, nao em controlo manual;
- a camara esta' bem ligada;
- nao ha' outro notebook/kernel a usar a camara;
- o robot consegue parar quando se executa `robot.parar()`.

Se a camara der erro no JupyterLab, faz `Kernel -> Shutdown All Kernels` e volta
a abrir apenas o notebook que esta' a ser usado.

## Estrutura Sugerida da Pasta `day2`

Sugestao de ficheiros para este dia:

```text
day2/
  README_day2.md
  01_camera.ipynb
  02_recolha_dados.ipynb
  03_treino_modelo.ipynb
  04_teste_no_robot.ipynb
  datasets/
  models/
```

Os notebooks ainda podem ser criados depois. Este README serve como guiao da
atividade.

## Plano do Dia

| Bloco | Duracao | Atividade |
|---|---:|---|
| 1 | 30 min | Rever seguranca e ligar a camara |
| 2 | 45 min | Explorar imagens: pixels, canais de cor e resolucao |
| 3 | 60 min | Recolher dados para treino |
| 4 | 45 min | Organizar e verificar os dados |
| 5 | 60 min | Treinar o modelo |
| 6 | 45 min | Testar no robot |
| 7 | 30 min | Melhorar o modelo e discutir resultados |

Adapta os tempos ao ritmo da turma. A parte mais importante e' a qualidade dos
dados, nao apenas carregar no botao "treinar".

## Parte 1 - Ligar e Ver a Camara

Exemplo base:

```python
from jetcam.csi_camera import CSICamera
from jetcam.utils import bgr8_to_jpeg
import ipywidgets
from IPython.display import display

camera = CSICamera(width=224, height=224)
camera.running = True

image_widget = ipywidgets.Image(format="jpeg")
image_widget.value = bgr8_to_jpeg(camera.value)
display(image_widget)
```

Pontos para explorar com os alunos:

- o robot nao "ve" como uma pessoa; recebe numeros;
- cada imagem tem largura, altura e canais de cor;
- a iluminacao muda muito o resultado;
- uma imagem tremida ou mal enquadrada pode prejudicar o treino.

## Parte 2 - Recolha de Dados

Escolhe uma tarefa simples para o treino. Exemplos:

- classificar se o robot deve virar `esquerda`, seguir `frente` ou virar
  `direita`;
- distinguir `pista_livre` de `obstaculo`;
- distinguir cores ou sinais simples;
- reconhecer posicoes na pista.

Para uma primeira atividade, recomenda-se usar poucas classes:

```text
datasets/
  frente/
  esquerda/
  direita/
```

Cada pasta deve ter imagens da respetiva decisao.

Regras importantes:

- recolher imagens variadas;
- evitar ter todas as imagens quase iguais;
- incluir exemplos com pequenas mudancas de luz;
- nao misturar classes;
- apagar imagens erradas antes de treinar;
- recolher dados com o robot na mesma altura e inclinacao em que vai ser usado.

## Parte 3 - Treino

O treino pode ser feito com um modelo simples de classificacao de imagem. A ideia
principal para os alunos:

```text
imagem da camara -> modelo -> decisao
```

Exemplo conceptual:

```python
imagem = camera.value
decisao = modelo(imagem)

if decisao == "frente":
    robot.andar_frente(0.2)
elif decisao == "esquerda":
    robot.virar_esquerda(0.2)
elif decisao == "direita":
    robot.virar_direita(0.2)
else:
    robot.parar()
```

Durante o treino, discutir:

- o que sao dados de treino;
- o que sao exemplos bons e exemplos maus;
- porque o modelo nao "percebe" a pista, apenas aprende padroes;
- porque testar em imagens novas e' diferente de testar nas imagens usadas no
  treino.

## Parte 4 - Teste no Robot

Antes de deixar o robot andar sozinho:

1. testar primeiro com as rodas levantadas;
2. imprimir no ecra a decisao prevista pelo modelo;
3. confirmar que as decisoes parecem razoaveis;
4. usar velocidades baixas;
5. manter uma pessoa pronta para parar o robot.

Exemplo de teste seguro:

```python
for i in range(20):
    imagem = camera.value
    decisao = prever_decisao(imagem)
    print(decisao)
```

So depois de confirmar as previsoes se deve ligar movimento.

## Desafios

### Desafio 1 - Melhorar a Recolha

Cada grupo deve recolher mais 20 imagens por classe e voltar a treinar. Depois
compara:

- o modelo ficou melhor?
- falha menos vezes?
- ficou pior em alguma situacao?

### Desafio 2 - Testar com Luz Diferente

Testar o modelo com mais luz, menos luz ou sombras. Discutir:

- o modelo continua a funcionar?
- que tipo de imagens faltaram no treino?

### Desafio 3 - Robot Mais Calmo

Mesmo que o modelo acerte, o robot pode mover-se demasiado depressa. Ajustar:

- velocidade;
- tempo de cada movimento;
- frequencia das previsoes;
- comportamento quando a previsao tem pouca confianca.

## Perguntas para Discussao

- Um modelo com muitos dados maus e' melhor do que um modelo com poucos dados
  bons?
- O que acontece se uma imagem estiver na pasta errada?
- O robot aprendeu a "pensar" ou aprendeu a imitar exemplos?
- Que situacoes reais seriam perigosas para este sistema?
- Como poderiamos melhorar o projeto no Dia 3?

## Resultado Esperado

No final do Dia 2, cada grupo deve ter:

- uma pequena colecao de imagens;
- um modelo treinado;
- um teste do modelo com imagens novas;
- uma demonstracao simples no robot ou no notebook;
- uma lista de problemas encontrados e ideias para melhorar.

## Seguranca

- Nunca testar o robot em cima de uma mesa sem bloquear as rodas ou levantar o
  chassis.
- Usar velocidades baixas.
- Manter maos, cabos e objetos soltos afastados das rodas.
- Parar o robot imediatamente se o comportamento for inesperado.
- Nao deixar o robot autonomo sem supervisao.

