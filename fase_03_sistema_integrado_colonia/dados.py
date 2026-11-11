"""Dados simulados da colônia Aurora Siger (Fase 03).

Valores em kWh referem-se a UM intervalo hipotético de 1 hora.
Os dados não são medições reais de Marte nem especificações de engenharia.
"""

CENARIOS = {
    "nominal": {"solar_kwh": 50.0, "vento_ms": 11.0, "reserva_kwh": 60.0},
    "economia": {"solar_kwh": 25.0, "vento_ms": 10.0, "reserva_kwh": 45.0},
    "contingencia": {"solar_kwh": 10.0, "vento_ms": 8.0, "reserva_kwh": 15.0},
    "alerta_critico": {"solar_kwh": 0.0, "vento_ms": 8.0, "reserva_kwh": 5.0},
    "excedente": {"solar_kwh": 85.0, "vento_ms": 14.0, "reserva_kwh": 95.0},
}


def criar_colonia(cenario="nominal"):
    """Retorna estruturas novas para que execuções não se contaminem."""
    if cenario not in CENARIOS:
        opcoes = ", ".join(CENARIOS)
        raise ValueError(f"Cenário desconhecido: {cenario}. Opções: {opcoes}")

    entradas = CENARIOS[cenario]
    return {
        "nome": "Missão Aurora Siger",
        "local": "Colônia marciana (simulação acadêmica)",
        "cenario": cenario,
        "intervalo_horas": 1,
        "modulos_origem_fase_02": {
            "AS-001": "Reconhecimento e Comunicações",
            "AS-002": "Energia",
            "AS-003": "Infraestrutura e Robótica",
            "AS-004": "Produção e Armazenamento de Recursos",
            "AS-005": "Habitação",
            "AS-006": "Suprimentos e Suporte Médico",
            "AS-007": "Laboratório Científico",
        },
        "historico_eolico": {
            "vento_ms": [8, 10, 12, 14, 16],
            "geracao_kwh": [20, 24, 30, 34, 41],
        },
        "sistemas": {
            "energetico": {
                "fontes": {
                    "solar": {"geracao_kwh": entradas["solar_kwh"]},
                    "eolico": {"vento_ms": entradas["vento_ms"]},
                },
                "armazenamento": {
                    "reserva_kwh": entradas["reserva_kwh"],
                    "capacidade_kwh": 100.0,
                },
            },
            "operacional": {
                "consumidores": [
                    {"id": "AS-005", "nome": "Suporte à vida", "categoria": "critico", "consumo_kwh": 24.0, "ligado": True},
                    {"id": "AS-001", "nome": "Comunicações", "categoria": "critico", "consumo_kwh": 8.0, "ligado": True},
                    {"id": "AS-006", "nome": "Suporte médico", "categoria": "critico", "consumo_kwh": 6.0, "ligado": True},
                    {"id": "AS-004", "nome": "Produção de recursos", "categoria": "ajustavel", "consumo_kwh": 10.0, "ligado": True},
                    {"id": "AS-003", "nome": "Robótica e manutenção", "categoria": "ajustavel", "consumo_kwh": 12.0, "ligado": True},
                    {"id": "AS-007", "nome": "Laboratório científico", "categoria": "nao_essencial", "consumo_kwh": 8.0, "ligado": True},
                    {"id": "AS-005", "nome": "Conforto e iluminação secundária", "categoria": "nao_essencial", "consumo_kwh": 6.0, "ligado": True},
                ]
            },
        },
    }

