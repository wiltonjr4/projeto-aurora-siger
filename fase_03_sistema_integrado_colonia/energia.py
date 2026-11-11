"""Análise de consumo e balanço energético da colônia."""


def calcular_consumo(consumidores):
    """Soma somente os subsistemas ligados."""
    return round(sum(item["consumo_kwh"] for item in consumidores if item["ligado"]), 2)


def calcular_geracao(geracao_solar_kwh, geracao_eolica_kwh):
    if geracao_solar_kwh < 0 or geracao_eolica_kwh < 0:
        raise ValueError("Geração de energia não pode ser negativa.")
    return round(geracao_solar_kwh + geracao_eolica_kwh, 2)


def calcular_balanco(geracao_kwh, consumo_kwh, reserva_kwh, capacidade_kwh):
    """Equilibra geração, consumo e bateria durante um intervalo.

    Excedente carrega até o limite; déficit usa a reserva disponível.
    Se a energia não basta, o balanço registra demanda não atendida.
    """
    if any(v < 0 for v in [geracao_kwh, consumo_kwh, reserva_kwh, capacidade_kwh]):
        raise ValueError("Os valores de energia não podem ser negativos.")
    if reserva_kwh > capacidade_kwh:
        raise ValueError("A reserva não pode superar a capacidade.")

    saldo = round(geracao_kwh - consumo_kwh, 2)
    armazenado = 0.0
    utilizado = 0.0
    excedente_nao_armazenado = 0.0
    demanda_nao_atendida = 0.0

    if saldo >= 0:
        armazenado = round(min(saldo, capacidade_kwh - reserva_kwh), 2)
        excedente_nao_armazenado = round(saldo - armazenado, 2)
    else:
        utilizado = round(min(-saldo, reserva_kwh), 2)
        demanda_nao_atendida = round(-saldo - utilizado, 2)

    reserva_final = round(reserva_kwh + armazenado - utilizado, 2)
    return {
        "geracao_kwh": geracao_kwh,
        "consumo_kwh": consumo_kwh,
        "saldo_inicial_kwh": saldo,
        "reserva_inicial_kwh": reserva_kwh,
        "reserva_final_kwh": reserva_final,
        "armazenado_kwh": armazenado,
        "utilizado_bateria_kwh": utilizado,
        "excedente_nao_armazenado_kwh": excedente_nao_armazenado,
        "demanda_nao_atendida_kwh": demanda_nao_atendida,
    }

