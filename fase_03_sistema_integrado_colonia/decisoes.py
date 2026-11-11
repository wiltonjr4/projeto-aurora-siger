"""Regras automáticas e priorização de cargas da colônia."""

from energia import calcular_consumo


def decidir_operacao(consumidores, geracao_kwh, reserva_kwh, capacidade_kwh):
    """Escolhe ações sem modificar a lista original de consumidores.

    Prioridades (ficcionais):
      1) Preservar cargas críticas (suporte à vida, comunicação, saúde).
      2) Desligar não essenciais em economia/contingência.
      3) Reduzir cargas ajustáveis em 50%.
      4) Em contingência, suspender cargas ajustáveis se necessário.
      5) Informar risco crítico caso nem a reserva sustente os críticos.

    A energia da bateria é considerada no balanço posterior.
    """
    if capacidade_kwh <= 0 or reserva_kwh < 0 or reserva_kwh > capacidade_kwh:
        raise ValueError("Reserva/capacidade da bateria inválida.")
    if geracao_kwh < 0:
        raise ValueError("Geração inválida.")

    operacionais = [item.copy() for item in consumidores]
    consumo_original = calcular_consumo(operacionais)
    deficit_inicial = max(0.0, consumo_original - geracao_kwh)
    reserva_percentual = 100 * reserva_kwh / capacidade_kwh

    if deficit_inicial > 0 and (deficit_inicial > reserva_kwh or reserva_percentual < 25):
        modo = "contingencia"
    elif deficit_inicial > 0 and reserva_percentual < 50:
        modo = "economia"
    elif deficit_inicial > 0:
        modo = "atencao"
    else:
        modo = "normal"

    acoes = []
    if modo in ("economia", "contingencia"):
        for item in operacionais:
            if item["ligado"] and item["categoria"] == "nao_essencial":
                poupado = item["consumo_kwh"]
                item["ligado"] = False
                item["consumo_kwh"] = 0.0
                acoes.append(f"Desligar {item['nome']} (-{poupado:.1f} kWh).")

        for item in operacionais:
            if item["ligado"] and item["categoria"] == "ajustavel":
                original = item["consumo_kwh"]
                item["consumo_kwh"] = round(original * 0.5, 2)
                acoes.append(f"Reduzir {item['nome']} em 50% (-{original - item['consumo_kwh']:.1f} kWh).")

    consumo_apos_economia = calcular_consumo(operacionais)
    if modo == "contingencia" and consumo_apos_economia - geracao_kwh > reserva_kwh:
        for item in operacionais:
            if item["ligado"] and item["categoria"] == "ajustavel":
                poupado = item["consumo_kwh"]
                item["ligado"] = False
                item["consumo_kwh"] = 0.0
                acoes.append(f"Suspender temporariamente {item['nome']} (-{poupado:.1f} kWh).")

    consumo_final = calcular_consumo(operacionais)
    criticos = [item for item in operacionais if item["categoria"] == "critico"]
    criticos_preservados_no_plano = all(item["ligado"] for item in criticos)
    risco_critico = consumo_final > geracao_kwh + reserva_kwh + 0.0001

    if risco_critico:
        modo = "alerta_critico"
        acoes.append("ALERTA: geração e reserva insuficientes para a demanda crítica; suporte à vida em risco.")
    elif consumo_final > geracao_kwh:
        acoes.append("ATENÇÃO: usar parte da bateria para completar o atendimento.")
    else:
        acoes.append("Manter cargas prioritárias e direcionar eventual excedente à bateria.")

    return {
        "modo": modo,
        "reserva_percentual": round(reserva_percentual, 1),
        "consumo_original_kwh": consumo_original,
        "consumo_final_kwh": consumo_final,
        "economia_kwh": round(consumo_original - consumo_final, 2),
        "sistemas_apos_decisao": operacionais,
        "criticos_preservados_no_plano": criticos_preservados_no_plano,
        "risco_critico": risco_critico,
        "acoes": acoes,
    }

