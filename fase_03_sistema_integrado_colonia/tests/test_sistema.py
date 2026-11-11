"""Testes automatizados da Fase 03: python -m unittest discover -s tests -v"""

import unittest

from dados import criar_colonia
from decisoes import decidir_operacao
from energia import calcular_balanco, calcular_consumo, calcular_geracao
from main import executar_simulacao
from previsao import ajustar_reta, prever_energia_eolica


class TesteEstruturaDados(unittest.TestCase):
    def test_hierarquia_e_modulos(self):
        colonia = criar_colonia()
        self.assertEqual(len(colonia["modulos_origem_fase_02"]), 7)
        self.assertIn("energetico", colonia["sistemas"])
        self.assertIn("operacional", colonia["sistemas"])
        self.assertEqual(len(colonia["sistemas"]["operacional"]["consumidores"]), 7)

    def test_cenarios_nao_compartilham_estado(self):
        primeiro = criar_colonia()
        primeiro["sistemas"]["operacional"]["consumidores"][0]["ligado"] = False
        segundo = criar_colonia()
        self.assertTrue(segundo["sistemas"]["operacional"]["consumidores"][0]["ligado"])

    def test_cenario_inexistente(self):
        with self.assertRaises(ValueError):
            criar_colonia("inexistente")


class TestePrevisao(unittest.TestCase):
    def test_reta_exata(self):
        a, b = ajustar_reta([8, 10, 12], [20, 25, 30])
        self.assertAlmostEqual(a, 2.5)
        self.assertAlmostEqual(b, 0.0)

    def test_previsao_cenario_nominal(self):
        colonia = criar_colonia()
        previsao = prever_energia_eolica(colonia["historico_eolico"], 11)
        self.assertAlmostEqual(previsao["geracao_prevista_kwh"], 27.2)
        self.assertFalse(previsao["extrapolacao"])

    def test_previsao_sinaliza_extrapolacao(self):
        colonia = criar_colonia()
        p = prever_energia_eolica(colonia["historico_eolico"], 20)
        self.assertTrue(p["extrapolacao"])

    def test_sem_variacao_no_vento(self):
        with self.assertRaises(ValueError):
            ajustar_reta([10, 10, 10], [20, 30, 40])

    def test_dados_incompativeis_ou_negativos(self):
        with self.assertRaises(ValueError):
            ajustar_reta([8, 10], [20])
        with self.assertRaises(ValueError):
            prever_energia_eolica(criar_colonia()["historico_eolico"], -1)


class TesteEnergia(unittest.TestCase):
    def test_consumo_e_geracao(self):
        consumidores = criar_colonia()["sistemas"]["operacional"]["consumidores"]
        self.assertEqual(calcular_consumo(consumidores), 74.0)
        self.assertEqual(calcular_geracao(50, 27.2), 77.2)

    def test_carregamento_bateria(self):
        b = calcular_balanco(80, 50, 60, 100)
        self.assertEqual(b["armazenado_kwh"], 30)
        self.assertEqual(b["reserva_final_kwh"], 90)

    def test_excedente_sem_capacidade(self):
        b = calcular_balanco(100, 40, 95, 100)
        self.assertEqual(b["armazenado_kwh"], 5)
        self.assertEqual(b["excedente_nao_armazenado_kwh"], 55)

    def test_deficit_consume_reserva(self):
        b = calcular_balanco(30, 40, 15, 100)
        self.assertEqual(b["utilizado_bateria_kwh"], 10)
        self.assertEqual(b["reserva_final_kwh"], 5)
        self.assertEqual(b["demanda_nao_atendida_kwh"], 0)

    def test_deficit_insuficiente(self):
        b = calcular_balanco(10, 40, 5, 100)
        self.assertEqual(b["reserva_final_kwh"], 0)
        self.assertEqual(b["demanda_nao_atendida_kwh"], 25)

    def test_entrada_invalida(self):
        with self.assertRaises(ValueError):
            calcular_balanco(30, 40, 110, 100)
        with self.assertRaises(ValueError):
            calcular_geracao(-1, 10)


class TesteDecisoesIntegradas(unittest.TestCase):
    def test_nominal_armazena_excedente(self):
        r = executar_simulacao("nominal")
        self.assertEqual(r["decisao"]["modo"], "normal")
        self.assertEqual(r["balanco"]["armazenado_kwh"], 3.2)
        self.assertEqual(r["balanco"]["demanda_nao_atendida_kwh"], 0)

    def test_economia_prioriza_criticos(self):
        r = executar_simulacao("economia")
        d = r["decisao"]
        self.assertEqual(d["modo"], "economia")
        self.assertEqual(d["consumo_original_kwh"], 74)
        self.assertEqual(d["consumo_final_kwh"], 49)
        self.assertTrue(d["criticos_preservados_no_plano"])
        self.assertFalse(d["risco_critico"])
        self.assertEqual(r["balanco"]["demanda_nao_atendida_kwh"], 0)
        for item in d["sistemas_apos_decisao"]:
            if item["categoria"] == "nao_essencial":
                self.assertFalse(item["ligado"])

    def test_contingencia_pode_suspender_ajustaveis(self):
        r = executar_simulacao("contingencia")
        d = r["decisao"]
        self.assertEqual(d["modo"], "contingencia")
        self.assertEqual(d["consumo_final_kwh"], 38)
        self.assertEqual(r["balanco"]["demanda_nao_atendida_kwh"], 0)
        self.assertTrue(d["criticos_preservados_no_plano"])
        for item in d["sistemas_apos_decisao"]:
            if item["categoria"] == "ajustavel":
                self.assertFalse(item["ligado"])

    def test_alerta_critico_sem_falsa_garantia(self):
        r = executar_simulacao("alerta_critico")
        self.assertEqual(r["decisao"]["modo"], "alerta_critico")
        self.assertTrue(r["decisao"]["risco_critico"])
        self.assertGreater(r["balanco"]["demanda_nao_atendida_kwh"], 0)

    def test_excedente_identifica_energia_nao_armazenada(self):
        r = executar_simulacao("excedente")
        self.assertEqual(r["balanco"]["reserva_final_kwh"], 100)
        self.assertGreater(r["balanco"]["excedente_nao_armazenado_kwh"], 0)

    def test_decisao_nao_modifica_consumidores_originais(self):
        consumidores = criar_colonia()["sistemas"]["operacional"]["consumidores"]
        decidir_operacao(consumidores, 20, 10, 100)
        self.assertEqual(calcular_consumo(consumidores), 74)

    def test_conservacao_do_balanco(self):
        for cenario in ["nominal", "economia", "contingencia", "alerta_critico", "excedente"]:
            b = executar_simulacao(cenario)["balanco"]
            oferta = b["geracao_kwh"] + b["utilizado_bateria_kwh"]
            destino = (b["consumo_kwh"] - b["demanda_nao_atendida_kwh"]
                       + b["armazenado_kwh"] + b["excedente_nao_armazenado_kwh"])
            self.assertAlmostEqual(oferta, destino, places=2, msg=cenario)


if __name__ == "__main__":
    unittest.main()

