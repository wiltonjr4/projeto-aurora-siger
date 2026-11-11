"""Aurora Siger | Fase 03: Sistema Integrado de Gestão da Colônia.

Execute: python main.py                (cenário nominal)
         python main.py economia
         python main.py contingencia
         python main.py alerta_critico
         python main.py excedente
         python main.py todos

Requer somente Python 3.8+ (biblioteca padrão).
"""

import sys

from dados import CENARIOS, criar_colonia
from decisoes import decidir_operacao
from energia import calcular_balanco, calcular_consumo, calcular_geracao
from previsao import prever_energia_eolica


def executar_simulacao(cenario="nominal"):
    """Orquestra dados -> previsão -> decisão -> balanço -> resultado."""
    colonia = criar_colonia(cenario)
    energetico = colonia["sistemas"]["energetico"]
    consumidores = colonia["sistemas"]["operacional"]["consumidores"]

    vento = energetico["fontes"]["eolico"]["vento_ms"]
    solar = energetico["fontes"]["solar"]["geracao_kwh"]
    armazenamento = energetico["armazenamento"]

    previsao = prever_energia_eolica(colonia["historico_eolico"], vento)
    geracao = calcular_geracao(solar, previsao["geracao_prevista_kwh"])
    consumo_inicial = calcular_consumo(consumidores)

    decisao = decidir_operacao(
        consumidores,
        geracao,
        armazenamento["reserva_kwh"],
        armazenamento["capacidade_kwh"],
    )
    balanco = calcular_balanco(
        geracao,
        decisao["consumo_final_kwh"],
        armazenamento["reserva_kwh"],
        armazenamento["capacidade_kwh"],
    )
    return {
        "colonia": colonia,
        "cenario": cenario,
        "previsao": previsao,
        "geracao_solar_kwh": solar,
        "geracao_total_kwh": geracao,
        "consumo_inicial_kwh": consumo_inicial,
        "decisao": decisao,
        "balanco": balanco,
    }


def apresentar_resultado(resultado):
    """Exibe um resumo auditável da operação do cenário."""
    p = resultado["previsao"]
    d = resultado["decisao"]
    b = resultado["balanco"]

    print("=" * 67)
    print("MISSÃO AURORA SIGER | FASE 03 | GESTÃO INTEGRADA DE ENERGIA")
    print("=" * 67)
    print(f"Cenário: {resultado['cenario'].upper()}")
    print("Intervalo simulado: 1 hora | Dados acadêmicos fictícios")
    print("\n[1] PREVISÃO POR REGRESSÃO LINEAR")
    print(f"Vento observado: {p['vento_ms']:.1f} m/s")
    print(f"Equação: energia = {p['coeficiente_a']:.2f} * vento + ({p['intercepto_b']:.2f})")
    print(f"Geração eólica estimada: {p['geracao_prevista_kwh']:.2f} kWh")
    if p["extrapolacao"]:
        print("AVISO: velocidade fora da faixa dos dados históricos.")

    print("\n[2] DADOS E ANÁLISE ENERGÉTICA")
    print(f"Geração solar:          {resultado['geracao_solar_kwh']:.2f} kWh")
    print(f"Geração total estimada: {resultado['geracao_total_kwh']:.2f} kWh")
    print(f"Consumo solicitado:     {resultado['consumo_inicial_kwh']:.2f} kWh")
    print(f"Reserva inicial:        {b['reserva_inicial_kwh']:.2f} kWh")

    print("\n[3] REGRAS E DECISÕES")
    print(f"Modo: {d['modo'].upper()} | Bateria: {d['reserva_percentual']:.1f}%")
    for acao in d["acoes"]:
        print(f" - {acao}")
    print(f"Consumo após decisões:  {d['consumo_final_kwh']:.2f} kWh")
    print(f"Redução de demanda:     {d['economia_kwh']:.2f} kWh")
    print(f"Cargas críticas no plano: {'MANTIDAS' if d['criticos_preservados_no_plano'] else 'NÃO MANTIDAS'}")

    print("\n[4] BALANÇO DA OPERAÇÃO")
    print(f"Carregamento da bateria: {b['armazenado_kwh']:.2f} kWh")
    print(f"Uso da bateria:          {b['utilizado_bateria_kwh']:.2f} kWh")
    print(f"Reserva final:           {b['reserva_final_kwh']:.2f} kWh")
    print(f"Excedente não armazenado:{b['excedente_nao_armazenado_kwh']:7.2f} kWh")
    print(f"Demanda não atendida:    {b['demanda_nao_atendida_kwh']:.2f} kWh")
    if d["risco_critico"]:
        print("RESULTADO: ALERTA CRÍTICO. O plano não garante o suprimento da colônia.")
    elif b["excedente_nao_armazenado_kwh"] > 0:
        print("RESULTADO: SUGESTÃO: reduzir geração ou ampliar armazenamento.")
    elif b["armazenado_kwh"] > 0:
        print("RESULTADO: SUGESTÃO: armazenar energia excedente.")
    elif b["utilizado_bateria_kwh"] > 0:
        print("RESULTADO: ATENÇÃO: geração abaixo do consumo; bateria utilizada.")
    else:
        print("RESULTADO: OPERAÇÃO EQUILIBRADA.")
    print()


def main():
    opcoes = ", ".join(CENARIOS)
    if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] not in CENARIOS and sys.argv[1] != "todos"):
        print(f"Uso: python main.py [nome_do_cenario|todos]\nCenários: {opcoes}")
        return 1

    escolhido = sys.argv[1] if len(sys.argv) == 2 else "nominal"
    cenarios = list(CENARIOS) if escolhido == "todos" else [escolhido]
    for cenario in cenarios:
        apresentar_resultado(executar_simulacao(cenario))
    return 0


if __name__ == "__main__":
    sys.exit(main())

