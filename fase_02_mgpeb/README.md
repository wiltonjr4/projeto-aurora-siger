# Missão Aurora Siger | MGPEB (Fase 2)

**Módulo de Gerenciamento de Pouso e Estabilização de Base**  
Projeto Integrador de Ciência da Computação | FIAP

## Visão geral

Protótipo acadêmico em Python que organiza e avalia operações simuladas de pouso de **sete módulos de carga** destinados à instalação inicial de uma base em Marte. Cada módulo possui ID, prioridade, combustível, massa, criticidade, horário estimado de chegada à órbita, integridade dos sensores e estado operacional.

O programa utiliza apenas a biblioteca padrão e recursos básicos da linguagem. **Não simula física orbital nem controla naves reais.** Todos os parâmetros são hipotéticos.

## Como executar

Abra o terminal na pasta `fase_02_mgpeb` e execute:

```bash
python mgpeb.py
```

Para executar os testes automatizados:

```bash
python test_mgpeb.py
```

Não há dependências externas.

## Estrutura de arquivos

```text
fase_02_mgpeb/
├── mgpeb.py          # Cadastro, algoritmos e simulação
├── test_mgpeb.py     # Testes com assert, sem bibliotecas externas
├── README.md         # Visão geral desta fase
└── documentacao/     # Relatório e diagramas da atividade
```

## Funcionalidades

- **Estruturas lineares:** cadastro com listas e dicionários; fila com `pop(0)`; listas auxiliares para módulos pousados, em espera e em alerta; histórico de eventos consultado como pilha LIFO.
- **Buscas lineares:** localização por identificador, menor percentual de combustível e criticidade.
- **Ordenação:** Bubble Sort por prioridade operacional, sem alterar a ordem da lista recebida.
- **Lógica booleana:** autorização por AND e alerta por OR/NOT; decisões com `if`, `elif` e `else`.
- **Estados:** `em_orbita` (registro inicial), `em_analise`, `pousado`, `em_espera` e `em_alerta`.
- **Testes:** fila vazia, buscas, lista invertida, condições seguras, falhas de sensor, baixo combustível, espera por horário/atmosfera/área e não duplicação de registros.

## Cenário padrão

A rodada ocorre às **11:00**; atmosfera e área de pouso estão disponíveis. Para testar o ramo de alerta, simulamos uma falha de sensores no módulo AS-002 (Energia).

| Resultado | Quantidade | Módulos |
|---|---:|---|
| Pousados | 3 | AS-001, AS-003, AS-007 |
| Em espera | 3 | AS-004, AS-005, AS-006 |
| Em alerta | 1 | AS-002 |

A prioridade numérica define a **ordem de análise**, nunca uma autorização automática. A hora no formato `HH:MM` é comparada como texto, supondo sempre o **mesmo dia** e dois dígitos em cada campo.

## Decisões de engenharia e limites do protótipo

- O limite de combustível de **40%** é fictício e pode ser alterado na constante `LIMITE_COMBUSTIVEL`.
- O pouso autorizado é registrado como `pousado` imediatamente, abstraindo tempo de descida, frenagem e estabilização física.
- A área é considerada novamente disponível a cada operação sequencial. Não são simulados pousos simultâneos.
- Os módulos são pré-cadastrados como `em_orbita` por simplificação. O horário de chegada determina quando podem ser autorizados, mesmo que o registro inicial já exista.
- A rodada processa todos os pedidos uma vez. Módulos adiados ou em alerta ficam em listas próprias; uma nova avaliação automática **não está implementada** nesta fase.
- `pop(0)` tem custo **O(n)**, aceitável para sete módulos. A ordenação Bubble Sort tem pior caso **O(n²)** e foi escolhida para demonstrar o algoritmo clássico solicitado.
- O código usa cópias de listas para organizar filas sem alterar a ordem original. A fila operacional compartilha os dicionários do cadastro para manter os estados atualizados.

## Entregáveis acadêmicos complementares

Além deste código, a atividade requer relatório técnico de **5 a 10 páginas**, com diagramas de portas lógicas, modelagem matemática e gráfico, contextualização histórica e arquitetural, reflexão ESG e explicação das estruturas lineares utilizadas.
