"""Missão Aurora Siger | MGPEB (FIAP, Fase 2).

Simulador acadêmico de gerenciamento de pousos de cargas em Marte.
Usa apenas Python básico: listas, dicionários, filas, pilhas, buscas,
Bubble Sort e lógica booleana.

IMPORTANTE: dados e limites são hipotéticos, não parâmetros reais de voo.
"""


# ============================================================
# 01. CONFIGURAÇÃO E CADASTRO DA MISSÃO
# ============================================================

LIMITE_COMBUSTIVEL = 40  # Percentual mínimo fictício para autorização.


def criar_modulos():
    """Cria os sete módulos com seus dados operacionais iniciais.

    Prioridade 1 é a mais alta. Horários usam HH:MM no mesmo dia.
    Cada execução recebe dicionários novos, sem estado residual.
    """
    return [
        {
            "id": "AS-001",
            "nome": "Reconhecimento e Comunicacoes",
            "prioridade": 1,
            "combustivel_percentual": 78,
            "massa_kg": 4500,
            "criticidade": "alta",
            "chegada_prevista": "09:30",
            "sensores_integros": True,
            "status": "em_orbita",
        },
        {
            "id": "AS-002",
            "nome": "Energia",
            "prioridade": 2,
            "combustivel_percentual": 65,
            "massa_kg": 6000,
            "criticidade": "alta",
            "chegada_prevista": "10:15",
            "sensores_integros": True,
            "status": "em_orbita",
        },
        {
            "id": "AS-003",
            "nome": "Infraestrutura e Robotica",
            "prioridade": 3,
            "combustivel_percentual": 72,
            "massa_kg": 5500,
            "criticidade": "alta",
            "chegada_prevista": "10:50",
            "sensores_integros": True,
            "status": "em_orbita",
        },
        {
            "id": "AS-004",
            "nome": "Producao e Armazenamento de Recursos",
            "prioridade": 4,
            "combustivel_percentual": 68,
            "massa_kg": 4200,
            "criticidade": "alta",
            "chegada_prevista": "11:30",
            "sensores_integros": True,
            "status": "em_orbita",
        },
        {
            "id": "AS-005",
            "nome": "Habitacao",
            "prioridade": 5,
            "combustivel_percentual": 82,
            "massa_kg": 9000,
            "criticidade": "alta",
            "chegada_prevista": "12:10",
            "sensores_integros": True,
            "status": "em_orbita",
        },
        {
            "id": "AS-006",
            "nome": "Suprimentos e Suporte Medico",
            "prioridade": 6,
            "combustivel_percentual": 74,
            "massa_kg": 5000,
            "criticidade": "alta",
            "chegada_prevista": "11:05",
            "sensores_integros": True,
            "status": "em_orbita",
        },
        {
            "id": "AS-007",
            "nome": "Laboratorio Cientifico",
            "prioridade": 7,
            "combustivel_percentual": 88,
            "massa_kg": 3800,
            "criticidade": "media",
            "chegada_prevista": "10:40",
            "sensores_integros": True,
            "status": "em_orbita",
        },
    ]


# ============================================================
# 02. ESTRUTURAS DE DADOS E ALGORITMOS
# ============================================================


def retirar_proximo_modulo(fila):
    """Retira o primeiro módulo (FIFO) ou devolve None se a fila estiver vazia.

    Atenção: pop(0) altera a lista recebida; o custo é O(n).
    Para a pequena frota de sete módulos, isso é suficiente.
    """
    if fila:
        return fila.pop(0)
    return None


def buscar_modulo_por_id(cadastro, id_procurado):
    """Busca linear pelo identificador. Pior caso: O(n)."""
    for modulo in cadastro:
        if modulo["id"] == id_procurado:
            return modulo
    return None


def buscar_modulo_menor_combustivel(cadastro):
    """Encontra o menor combustível em O(n), sem alterar o cadastro."""
    menor = None
    for modulo in cadastro:
        if menor is None:
            menor = modulo
        elif modulo["combustivel_percentual"] < menor["combustivel_percentual"]:
            menor = modulo
    return menor


def buscar_modulos_por_criticidade(cadastro, criticidade):
    """Lista módulos com a criticidade informada (busca linear)."""
    encontrados = []
    for modulo in cadastro:
        if modulo["criticidade"] == criticidade:
            encontrados.append(modulo)
    return encontrados


def ordenar_por_prioridade(fila):
    """Bubble Sort crescente por prioridade, em nova lista. Pior caso: O(n²).

    A ordem da lista de entrada é preservada. Os dicionários, porém,
    continuam compartilhados (cópia superficial).
    """
    ordenada = fila.copy()
    for passagem in range(len(ordenada) - 1):
        # A cada passagem, a última posição pendente fica ordenada.
        for i in range(len(ordenada) - 1 - passagem):
            if ordenada[i]["prioridade"] > ordenada[i + 1]["prioridade"]:
                ordenada[i], ordenada[i + 1] = ordenada[i + 1], ordenada[i]
    return ordenada


# ============================================================
# 03. REGRAS BOOLEANAS E ESTADOS OPERACIONAIS
# ============================================================


def avaliar_pouso(modulo, atmosfera_segura, area_disponivel, hora_atual):
    """Retorna (status, motivo) conforme as condições simuladas.

    ALERTA = NOT combustivel_ok OR NOT sensores_ok
    POUSO = combustivel_ok AND sensores_ok AND atmosfera_segura
            AND area_disponivel AND horario_ok

    HH:MM deve conter zeros à esquerda e referir-se ao mesmo dia.
    Prioridade organiza a análise, mas não substitui segurança.
    """
    combustivel_ok = modulo["combustivel_percentual"] >= LIMITE_COMBUSTIVEL
    sensores_ok = modulo["sensores_integros"]
    horario_ok = modulo["chegada_prevista"] <= hora_atual

    alerta = not combustivel_ok or not sensores_ok
    autorizado = (
        combustivel_ok
        and sensores_ok
        and atmosfera_segura
        and area_disponivel
        and horario_ok
    )

    if alerta:
        if not combustivel_ok and not sensores_ok:
            return "em_alerta", "Combustivel insuficiente e sensores com falha"
        if not combustivel_ok:
            return "em_alerta", "Combustivel abaixo do limite simulado"
        return "em_alerta", "Sensores sem integridade"
    elif autorizado:
        return "pousado", "Todas as condicoes foram atendidas"
    else:
        if not horario_ok:
            return "em_espera", "Horario previsto de chegada ainda nao atingido"
        if not atmosfera_segura:
            return "em_espera", "Condicoes atmosfericas desfavoraveis"
        return "em_espera", "Area de pouso indisponivel"


def registrar_estado(modulo, novo_status, lista_destino):
    """Atualiza o módulo e o adiciona ao destino após a avaliação.

    Usada apenas durante uma rodada, com cada módulo processado uma vez.
    """
    modulo["status"] = novo_status
    lista_destino.append(modulo)


def processar_fila(fila, hora_atual, atmosfera_segura, area_disponivel):
    """Processa a fila inteira e devolve listas de destino e pilha de histórico.

    A fila recebida é esvaziada. Não há reprocessamento nesta rodada.
    Uma autorização é registrada como 'pousado' por simplificação.
    """
    pousados = []
    em_espera = []
    em_alerta = []
    historico = []  # Pilha: append() insere no topo; pop() remove do topo.

    while fila:
        modulo = retirar_proximo_modulo(fila)
        modulo["status"] = "em_analise"

        status, motivo = avaliar_pouso(
            modulo, atmosfera_segura, area_disponivel, hora_atual
        )

        if status == "pousado":
            registrar_estado(modulo, status, pousados)
        elif status == "em_alerta":
            registrar_estado(modulo, status, em_alerta)
        else:
            registrar_estado(modulo, status, em_espera)

        # Evento estruturado facilita consultas e auditoria.
        historico.append({"id": modulo["id"], "status": status, "motivo": motivo})

    return pousados, em_espera, em_alerta, historico


# ============================================================
# 04. EXECUÇÃO DA SIMULAÇÃO
# ============================================================


def executar_simulacao(
    hora_atual="11:00",
    atmosfera_segura=True,
    area_disponivel=True,
    simular_falha_energia=True,
):
    """Prepara cenário, ordena a fila e executa uma rodada da missão.

    Cada chamada cria um cadastro novo: os testes não alteram outros cenários.
    """
    cadastro = criar_modulos()

    # Falha proposital apenas para demonstrar o estado 'em_alerta'.
    if simular_falha_energia:
        energia = buscar_modulo_por_id(cadastro, "AS-002")
        energia["sensores_integros"] = False

    # Fotografias da programação antes das mudanças de estado.
    # Como os valores dos dicionários são simples, copy() basta para a foto.
    fila_inicial = [modulo.copy() for modulo in cadastro]
    fila_priorizada = ordenar_por_prioridade(fila_inicial)

    # A fila operacional compartilha os registros reais do cadastro.
    fila_pouso = ordenar_por_prioridade(cadastro)

    pousados, em_espera, em_alerta, historico = processar_fila(
        fila_pouso, hora_atual, atmosfera_segura, area_disponivel
    )

    return {
        "hora_atual": hora_atual,
        "cadastro": cadastro,
        "fila_inicial": fila_inicial,
        "fila_priorizada": fila_priorizada,
        "fila_pouso": fila_pouso,
        "pousados": pousados,
        "em_espera": em_espera,
        "em_alerta": em_alerta,
        "historico": historico,
    }


# ============================================================
# 05. APRESENTAÇÃO DOS RESULTADOS
# ============================================================


def mostrar_modulos(titulo, modulos):
    """Exibe uma lista de módulos com ID, prioridade e estado."""
    print(f"\n=== {titulo} ({len(modulos)}) ===")
    if not modulos:
        print("Nenhum modulo nesta lista.")
        return

    for modulo in modulos:
        print(
            f"{modulo['id']} | {modulo['nome']} | "
            f"Prioridade {modulo['prioridade']} | {modulo['status']}"
        )


def mostrar_resultados(resultado):
    """Imprime um relatório textual sem alterar os dados da simulação."""
    print("\nMISSÃO AURORA SIGER | MGPEB - FASE 2")
    print(f"Simulacao de pousos | Horario: {resultado['hora_atual']}")

    mostrar_modulos("FILA DE ENTRADA", resultado["fila_inicial"])
    mostrar_modulos("FILA ORDENADA POR PRIORIDADE", resultado["fila_priorizada"])

    print("\n=== DECISOES DE POUSO ===")
    for evento in resultado["historico"]:
        print(f"{evento['id']} | {evento['status']} | {evento['motivo']}")

    mostrar_modulos("POUSADOS", resultado["pousados"])
    mostrar_modulos("EM ESPERA", resultado["em_espera"])
    mostrar_modulos("EM ALERTA", resultado["em_alerta"])
    mostrar_modulos("FILA APOS A RODADA", resultado["fila_pouso"])
    mostrar_modulos("CADASTRO GERAL", resultado["cadastro"])

    print("\n=== HISTORICO LIFO (MAIS RECENTE PRIMEIRO) ===")
    pilha_consulta = resultado["historico"].copy()
    while pilha_consulta:
        evento = pilha_consulta.pop()
        print(f"{evento['id']} | {evento['status']} | {evento['motivo']}")

    print("\n=== CONSULTAS ===")
    encontrado = buscar_modulo_por_id(resultado["cadastro"], "AS-004")
    if encontrado is not None:
        print(f"Busca por ID AS-004: {encontrado['nome']}")

    menor = buscar_modulo_menor_combustivel(resultado["cadastro"])
    if menor is not None:
        print(
            f"Menor combustivel: {menor['id']} | {menor['nome']} | "
            f"{menor['combustivel_percentual']}%"
        )

    alta = buscar_modulos_por_criticidade(resultado["cadastro"], "alta")
    print(f"Modulos de criticidade alta: {len(alta)}")


def main():
    """Ponto de entrada do programa."""
    resultado = executar_simulacao()
    mostrar_resultados(resultado)


if __name__ == "__main__":
    main()
