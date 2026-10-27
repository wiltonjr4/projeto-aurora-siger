# Missão Aurora Siger 🚀

**Projeto Integrador | Ciência da Computação | FIAP**

A **Missão Aurora Siger** é um projeto acadêmico desenvolvido em fases, com simulações computacionais relacionadas à exploração espacial e à preparação de uma base humana em Marte.

Seu objetivo é aplicar, em cenários de estudo, conceitos de programação, algoritmos, estruturas de dados e raciocínio lógico. **Não se trata de software aeroespacial real:** dados, parâmetros e condições operacionais são fictícios.

## Fases do projeto

### Fase 1 | Verificação pré-decolagem

**Status: concluída.**

Simulação de parâmetros de telemetria e de condições pré-decolagem, com regras para avaliação de segurança, identificação de falhas e estimativas energéticas.

- **Tecnologias:** Python; Google Colab/Jupyter Notebook.
- **Conceitos:** condicionais, funções, análise de parâmetros e organização de dados.
- **Acesse:** [Fase 1](fase_01_pre_decolagem/)

### Fase 2 | MGPEB: Gerenciamento de Pouso e Estabilização de Base

**Status: concluída, com casos de teste no repositório.**

Protótipo de uma rotina de análise de pouso de **sete módulos simulados** destinados à implantação de uma base em Marte. A aplicação organiza a fila operacional e classifica os módulos entre situações como pousado, em espera ou em alerta, com base em regras explícitas.

Implementações centrais:

- **Listas, dicionários e fila:** representação dos módulos e controle da sequência de análise.
- **Busca linear:** consulta por ID e identificação de informações como menor percentual de combustível.
- **Bubble Sort:** ordenação dos módulos conforme prioridade, sem modificar a lista de entrada.
- **Lógica booleana e transição de estados:** análise de sensores, combustível, chegada e condições de pouso.
- **Testes com `assert`:** cenários de busca, ordenação, filas e condições operacionais simuladas.

- **Tecnologias:** Python, biblioteca padrão.
- **Acesse:** [Documentação e código da Fase 2](fase_02_mgpeb/)

### Rodar a Fase 2

```bash
cd fase_02_mgpeb
python mgpeb.py
```

Para executar os testes disponibilizados:

```bash
python test_mgpeb.py
```

A Fase 2 não exige dependências de terceiros. Para informações completas sobre módulos, cenários, decisões e limites da simulação, consulte o [README da Fase 2](fase_02_mgpeb/README.md).

## Conhecimentos demonstrados

| Área | Aplicação no projeto |
| --- | --- |
| Programação | Funções, condições, laços e organização de módulos |
| Estruturas de dados | Listas, dicionários, filas e histórico de estados |
| Algoritmos | Busca linear e ordenação Bubble Sort |
| Modelagem | Regras para representar estados e prioridades da operação simulada |
| Verificação | Casos de teste e validação de cenários |

## Autor

**Wilton Junior**  
Ciência da Computação, FIAP  
[GitHub](https://github.com/wiltonjr4) · [LinkedIn](https://www.linkedin.com/in/wilton-bezerra-27452820a/)

---

> **Aviso:** este repositório tem finalidade educacional. Não representa uma implementação certificada para uso espacial ou crítico.
