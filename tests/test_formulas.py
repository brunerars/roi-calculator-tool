"""
Testes unitários para core/formulas.py
"""
import math
import pytest

from core.formulas import (
    calcular_producao_anual,
    calcular_horas_anuais,
    calcular_pessoas_expostas,
    calcular_custo_hora_operador,
    calcular_custo_dia_absenteismo,
    calcular_custo_material,
    calcular_co1_folha_pagamento,
    calcular_co2_terceirizacao,
    calcular_co3_desperdicio,
    calcular_co4_manutencao,
    calcular_ql1_retrabalho,
    calcular_ql2_refugo,
    calcular_ql3_inspecao,
    calcular_ql4_logistica,
    calcular_ql5_multas_qualidade,
    calcular_se1_absenteismo,
    calcular_se2_turnover,
    calcular_se3_treinamentos,
    calcular_se4_passivo_juridico,
    calcular_pr1_horas_extras,
    calcular_pr2_headcount,
    calcular_pr3_vendas_perdidas,
    calcular_pr4_multas_atraso,
    calcular_payback,
    calcular_roi,
    calcular_ganho_anual,
)


# ---- Bases Comuns ----

class TestBasesComuns:
    def test_producao_anual(self):
        # 10 peças/min × 60 × 8h × 2 turnos × 250 dias = 2.400.000
        assert calcular_producao_anual(10, 8, 2, 250) == 2_400_000

    def test_horas_anuais(self):
        # 8h × 2 turnos × 250 dias = 4.000
        assert calcular_horas_anuais(8, 2, 250) == 4_000

    def test_pessoas_expostas(self):
        # 5 pessoas × 2 turnos = 10
        assert calcular_pessoas_expostas(5, 2) == 10

    def test_custo_hora_operador(self):
        # 5000 / 220 ≈ 22.73
        assert calcular_custo_hora_operador(5000, 220) == pytest.approx(22.7272, rel=1e-3)

    def test_custo_dia_absenteismo(self):
        # (5000 × 12) / 250 = 240
        assert calcular_custo_dia_absenteismo(5000, 250) == 240.0

    def test_custo_material(self):
        # 100 × 0.6 = 60
        assert calcular_custo_material(100, 0.6) == 60.0


# ---- CO - Custos Operacionais ----

class TestCustosOperacionais:
    def test_co1_folha_pagamento(self):
        # 10 pessoas × 5000 × 2 turnos × 12 = 1.200.000
        assert calcular_co1_folha_pagamento(10, 5000, 2) == 1_200_000

    def test_co2_terceirizacao(self):
        # 1000 × 50 × 3 = 150.000
        assert calcular_co2_terceirizacao(1000, 50, 3) == 150_000

    def test_co3_desperdicio(self):
        # 2.400.000 × 0.02 × 60 = 2.880.000
        assert calcular_co3_desperdicio(2_400_000, 0.02, 60) == 2_880_000

    def test_co4_manutencao(self):
        # (4 × 30 / 60 × 12) × 150 = 3.600
        assert calcular_co4_manutencao(4, 30, 150) == 3_600


# ---- QL - Qualidade ----

class TestQualidade:
    def test_ql1_retrabalho(self):
        # 2.400.000 × 0.03 × 100 × 0.2 = 1.440.000
        assert calcular_ql1_retrabalho(2_400_000, 0.03, 100, 0.2) == 1_440_000

    def test_ql2_refugo(self):
        # 2.400.000 × 0.01 × 100 = 2.400.000
        assert calcular_ql2_refugo(2_400_000, 0.01, 100) == 2_400_000

    def test_ql3_inspecao(self):
        # 2 pessoas × 5000 × 2 turnos × 12 = 240.000
        assert calcular_ql3_inspecao(2, 5000, 2) == 240_000

    def test_ql4_logistica(self):
        # 2.400.000 × 0.005 × 15 = 180.000
        assert calcular_ql4_logistica(2_400_000, 0.005, 15) == 180_000

    def test_ql5_multas_qualidade(self):
        # 6 × 500 = 3.000
        assert calcular_ql5_multas_qualidade(6, 500) == 3_000


# ---- SE - Segurança e Ergonomia ----

class TestSeguranca:
    def test_se1_absenteismo(self):
        # 10 dias × 240 = 2.400
        assert calcular_se1_absenteismo(10, 240) == 2_400

    def test_se2_turnover(self):
        # 3 desligamentos × 10.000 = 30.000
        assert calcular_se2_turnover(3, 10_000) == 30_000

    def test_se3_treinamentos(self):
        # 3 × 1200 = 3.600
        assert calcular_se3_treinamentos(3, 1200) == 3_600

    def test_se4_passivo_juridico(self):
        # 2 × 35.000 = 70.000
        assert calcular_se4_passivo_juridico(2, 35_000) == 70_000


# ---- PR - Produtividade ----

class TestProdutividade:
    def test_pr1_horas_extras(self):
        # 100 HE/mês × 12 × 22.73 × 1.5 = 40.909,09...
        resultado = calcular_pr1_horas_extras(100, 22.7272, 1.5)
        assert resultado == pytest.approx(40_909.0, rel=1e-2)

    def test_pr2_headcount(self):
        # 3 × 5000 × 12 = 180.000
        assert calcular_pr2_headcount(3, 5000) == 180_000

    def test_pr3_vendas_perdidas(self):
        # 500 × 12 × 30 = 180.000
        assert calcular_pr3_vendas_perdidas(500, 30) == 180_000

    def test_pr4_multas_atraso(self):
        # 4 × 1000 = 4.000
        assert calcular_pr4_multas_atraso(4, 1000) == 4_000


# ---- Indicadores Financeiros ----

class TestIndicadores:
    def test_payback(self):
        # 500.000 / 250.000 = 2.0 anos
        assert calcular_payback(500_000, 250_000) == 2.0

    def test_payback_ganho_zero(self):
        assert calcular_payback(500_000, 0) == float("inf")

    def test_roi_1_ano(self):
        # ((250.000 × 1) - 500.000) / 500.000 × 100 = -50%
        assert calcular_roi(500_000, 250_000, 1) == -50.0

    def test_roi_3_anos(self):
        # ((250.000 × 3) - 500.000) / 500.000 × 100 = 50%
        assert calcular_roi(500_000, 250_000, 3) == 50.0

    def test_roi_5_anos(self):
        # ((250.000 × 5) - 500.000) / 500.000 × 100 = 150%
        assert calcular_roi(500_000, 250_000, 5) == 150.0

    def test_roi_investimento_zero(self):
        assert calcular_roi(0, 250_000, 3) == 0.0

    def test_ganho_anual(self):
        # 1.000.000 × 0.3 = 300.000
        assert calcular_ganho_anual(1_000_000, 0.3) == 300_000
