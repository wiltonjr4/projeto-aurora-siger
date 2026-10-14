"""Testes do MGPEB, apenas com assert e Python padrão.

Execute: python test_mgpeb.py
"""

from mgpeb import (
    LIMITE_COMBUSTIVEL,
    avaliar_pouso,
    buscar_modulo_menor_combustivel,
    buscar_modulo_por_id,
    buscar_modulos_por_criticidade,
    criar_modulos,
    executar_simulacao,
    ordenar_por_prioridade,
    retirar_proximo_modulo,
)


def testar_cadastro_e_buscas():
    cadastro = criar_modulos()
    assert len(cadastro) == 7
    assert len({modulo["id"] for modulo in cadastro}) == 7
    assert buscar_modulo_por_id(cadastro, "AS-004")["nome"].startswith("Producao")
    assert buscar_modulo_por_id(cadastro, "AS-999") is None
    assert buscar_modulo_por_id([], "AS-001") is None
    assert buscar_modulo_menor_combustivel(cadastro)["id"] == "AS-002"
    assert buscar_modulo_menor_combustivel([]) is None

    cadastro[6]["combustivel_percentual"] = 30
    assert buscar_modulo_menor_combustivel(cadastro)["id"] == "AS-007"
    assert len(buscar_modulos_por_criticidade(cadastro, "alta")) == 6
    assert buscar_modulos_por_criticidade([], "alta") == []


def testar_fila_e_ordenacao():
    cadastro = criar_modulos()
    fila = [cadastro[6], cadastro[1], cadastro[0]]
    ordem_original = [modulo["id"] for modulo in fila]
    ordenada = ordenar_por_prioridade(fila)

    assert [modulo["prioridade"] for modulo in ordenada] == [1, 2, 7]
    assert [modulo["id"] for modulo in fila] == ordem_original
    assert ordenar_por_prioridade([]) == []

    proximo = retirar_proximo_modulo(ordenada)
    assert proximo["id"] == "AS-001"
    assert len(ordenada) == 2
    assert retirar_proximo_modulo([]) is None

    inversa = list(reversed(cadastro))
    assert [
        modulo["prioridade"] for modulo in ordenar_por_prioridade(inversa)
    ] == list(range(1, 8))


def testar_regras_booleanas():
    modulo = criar_modulos()[0]
    assert avaliar_pouso(modulo, True, True, "11:00")[0] == "pousado"
    assert avaliar_pouso(modulo, False, True, "11:00")[0] == "em_espera"
    assert avaliar_pouso(modulo, True, False, "11:00")[0] == "em_espera"
    assert avaliar_pouso(modulo, True, True, "09:00")[0] == "em_espera"

    modulo["combustivel_percentual"] = LIMITE_COMBUSTIVEL
    assert avaliar_pouso(modulo, True, True, "11:00")[0] == "pousado"

    modulo["combustivel_percentual"] = LIMITE_COMBUSTIVEL - 1
    assert avaliar_pouso(modulo, True, True, "11:00")[0] == "em_alerta"

    modulo["combustivel_percentual"] = 78
    modulo["sensores_integros"] = False
    assert avaliar_pouso(modulo, True, True, "11:00")[0] == "em_alerta"


def testar_simulacao_e_historico():
    resultado = executar_simulacao()
    assert len(resultado["cadastro"]) == 7
    assert len(resultado["pousados"]) == 3
    assert len(resultado["em_espera"]) == 3
    assert len(resultado["em_alerta"]) == 1
    assert resultado["fila_pouso"] == []

    destinos = resultado["pousados"] + resultado["em_espera"] + resultado["em_alerta"]
    ids = [modulo["id"] for modulo in destinos]
    assert len(ids) == 7
    assert len(set(ids)) == 7
    assert len(resultado["historico"]) == 7

    assert (
        buscar_modulo_por_id(resultado["cadastro"], "AS-002")["status"]
        == "em_alerta"
    )
    assert resultado["historico"][-1]["id"] == "AS-007"
    pilha = resultado["historico"].copy()
    assert pilha.pop()["id"] == "AS-007"
    assert len(resultado["historico"]) == 7

    # Cada execução começa do zero, sem reutilizar estados alterados.
    outro_resultado = executar_simulacao(simular_falha_energia=False)
    assert len(outro_resultado["em_alerta"]) == 0
    assert len(outro_resultado["pousados"]) == 4


def main():
    testar_cadastro_e_buscas()
    testar_fila_e_ordenacao()
    testar_regras_booleanas()
    testar_simulacao_e_historico()
    print("Todos os testes do MGPEB passaram!")


if __name__ == "__main__":
    main()
