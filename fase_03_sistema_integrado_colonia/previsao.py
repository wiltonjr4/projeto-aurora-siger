"""Regressão linear simples pelo método dos mínimos quadrados."""


def ajustar_reta(entradas, saidas):
    """Ajusta y = a*x + b a partir de duas listas do mesmo tamanho.

    Não exige numpy, pandas ou bibliotecas de machine learning.
    """
    if len(entradas) != len(saidas) or len(entradas) < 2:
        raise ValueError("São necessárias ao menos duas observações pareadas.")

    media_x = sum(entradas) / len(entradas)
    media_y = sum(saidas) / len(saidas)
    numerador = 0.0
    denominador = 0.0

    for indice in range(len(entradas)):
        dx = entradas[indice] - media_x
        dy = saidas[indice] - media_y
        numerador += dx * dy
        denominador += dx * dx

    if denominador == 0:
        raise ValueError("Não há variação de vento suficiente para ajustar a reta.")

    a = numerador / denominador
    b = media_y - a * media_x
    return a, b


def prever_energia_eolica(historico, vento_ms):
    """Estima a geração em kWh/h e marca extrapolações do histórico."""
    if vento_ms < 0:
        raise ValueError("Velocidade do vento não pode ser negativa.")

    x = historico["vento_ms"]
    y = historico["geracao_kwh"]
    if any(valor < 0 for valor in x + y):
        raise ValueError("Histórico de vento e geração não admite negativos.")

    coeficiente, intercepto = ajustar_reta(x, y)
    estimativa = max(0.0, coeficiente * vento_ms + intercepto)
    return {
        "vento_ms": vento_ms,
        "geracao_prevista_kwh": round(estimativa, 2),
        "coeficiente_a": round(coeficiente, 4),
        "intercepto_b": round(intercepto, 4),
        "faixa_historica_ms": (min(x), max(x)),
        "extrapolacao": not (min(x) <= vento_ms <= max(x)),
    }

