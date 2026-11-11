# Missão Aurora Siger | Fase 03

## Sistema Integrado de Gestão Inteligente da Colônia (SIGIC)

**Projeto Integrador | Ciência da Computação - FIAP | 2026**

Continuação da Missão Aurora Siger, após a Fase 01 (pré-decolagem) e a Fase 02 (gerenciamento de pousos). Nesta etapa, a colônia marciana fictícia monitora geração solar e eólica, consumo de sete cargas operacionais e reserva em bateria. O sistema transforma dados em decisões automáticas e faz uma estimativa de geração por regressão linear.

> **Finalidade acadêmica.** Todos os dados e limites são fictícios, inclusive a hipótese simplificada de geração eólica em Marte. Não é um sistema real de segurança aeroespacial.

### Como executar

Requisito: Python 3.8+ com biblioteca padrão. Abra um terminal nesta pasta.

| Comando | Finalidade |
| --- | --- |
| `python main.py` | Cenário nominal |
| `python main.py economia` | Economia de energia |
| `python main.py contingencia` | Suspensão de cargas ajustáveis |
| `python main.py alerta_critico` | Insuficiência para cargas vitais |
| `python main.py excedente` | Excesso de geração |
| `python main.py todos` | Executa os cinco cenários |
| `python -m unittest discover -s tests -v` | Executa 21 testes |

No Windows, pode-se usar o comando `py` em vez de `python`.

### Organização dos dados

- `dados.py`: dicionário hierárquico `colonia → sistemas → energetico → fontes/armazenamento` e `colonia → sistemas → operacional → consumidores`; registro dos módulos AS-001 a AS-007 da Fase 02, além de cinco cenários reproduzíveis.
- `previsao.py`: listas de vento e energia histórica simulada, regressão linear por mínimos quadrados, sem bibliotecas avançadas.
- `decisoes.py`: regras de economia e prioridade, sem modificar os dados de entrada.
- `energia.py`: balanço da geração, consumo, recarga, uso da reserva, excedente não armazenado e demanda não atendida.
- `main.py`: orquestração e apresentação legível das decisões.
- `tests/test_sistema.py`: 21 testes automatizados.

### Como funciona a previsão

Histórico hipotético:

- Vento (m/s): [8, 10, 12, 14, 16]
- Energia eólica (kWh por intervalo de uma hora): [20, 24, 30, 34, 41]

O ajuste por mínimos quadrados fornece a equação **energia ≈ 2,6 × vento − 1,4**. Para vento observado de 11 m/s, a previsão é **27,2 kWh**. A regressão estima a geração para o vento fornecido, e **não** prevê a velocidade futura do vento.

### Regras de decisão e prioridade

As cargas são classificadas em:

| Categoria | Exemplos | Demanda inicial |
| --- | --- | ---: |
| Crítico | Suporte à vida, comunicações e médico | 38 kWh |
| Ajustável | Produção de recursos, robótica | 22 kWh |
| Não essencial | Laboratório, conforto | 14 kWh |
| **Total** | 7 cargas | **74 kWh** |

Quando a geração cobre o consumo, a sobra vai para a bateria até a capacidade máxima de 100 kWh. Com déficit e reserva entre 50% e 100% suficiente para cobri-lo, o sistema pode usar a bateria sem cortes. Abaixo de 50%, entra em economia, desliga cargas não essenciais e reduz as ajustáveis pela metade. Se a reserva é insuficiente para o déficit inicial, ou está abaixo de 25% havendo déficit, entra em contingência e pode suspender as ajustáveis.

As cargas críticas permanecem no **plano** mesmo em contingência. Quando geração mais bateria não sustentam as cargas críticas, a saída sinaliza **ALERTA CRÍTICO** e registra a energia não atendida. O sistema não promete segurança onde há falta de energia.

### Exemplo de entrada e saída

Cenário nominal: geração solar = 50 kWh, vento = 11 m/s, reserva = 60 kWh, demanda = 74 kWh, intervalo = 1 hora.

```text
Cenário: NOMINAL
Geração eólica estimada: 27.20 kWh
Geração total estimada: 77.20 kWh
Consumo solicitado:     74.00 kWh
Modo: NORMAL | Bateria: 60.0%
Consumo após decisões:  74.00 kWh
Carregamento da bateria: 3.20 kWh
Reserva final:           63.20 kWh
RESULTADO: SUGESTÃO: armazenar energia excedente.
```

### Resultados simulados

| Cenário | Geração (kWh) | Consumo inicial → final (kWh) | Reserva final (kWh) | Situação |
| --- | ---: | ---: | ---: | --- |
| Nominal | 77,20 | 74 → 74 | 63,20 | Armazena 3,20 kWh |
| Economia | 49,60 | 74 → 49 | 45,60 | Redução de demanda |
| Contingência | 29,40 | 74 → 38 | 6,40 | Preserva cargas críticas |
| Alerta crítico | 19,40 | 74 → 38 | 0,00 | 13,60 kWh não atendidos |
| Excedente | 120,00 | 74 → 74 | 100,00 | 41 kWh não armazenados |

Cada cenário representa um único intervalo independente de uma hora. Não são simulados a física real marciana, eficiência de baterias, falhas físicas ou múltiplos ciclos.

### Documentação e testes

A Fase 03 contém código organizado em funções, entrada e saída demonstráveis, teste de conservação energética, testes de valores negativos, regressão, decisões e casos extremos. O **relatório em PDF** é entregue separadamente no ambiente da atividade.

**Repositório da missão:** https://github.com/wiltonjr4/projeto-aurora-siger

