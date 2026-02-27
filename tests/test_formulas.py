"""
Testes unitários para core/formulas.py
"""
import pytest

from core.formulas import (
    calcular_producao_anual,
    calcular_producao_mensal_from_cadencia,
    calcular_faturamento_mensal,
    calcular_horas_anuais,
    calcular_pessoas_expostas,
    calcular_custo_hora_operador,
    calcular_f01_mao_de_obra_direta,
    calcular_f04_turnover,
    calcular_f05_refugo_retrabalho,
    calcular_f07_escapes_qualidade,
    calcular_payback,
    calcular_roi,
    calcular_ganho_anual,
)


# ---- Bases Comuns ----

class TestBasesComuns:
    def test_producao_anual(self):
        # 10 peças/min × 60 × 8h × 2 turnos × 250 dias = 2.400.000
        assert calcular_producao_anual(10, 8, 2, 250) == 2_400_000

    def test_producao_mensal(self):
        # 10 peças/min × 60 × 8h × 2 turnos × 21 dias = 201.600
        assert calcular_producao_mensal_from_cadencia(10, 8, 2, 21) == 201_600

    def test_horas_anuais(self):
        # 8h × 2 turnos × 250 dias = 4.000
        assert calcular_horas_anuais(8, 2, 250) == 4_000

    def test_pessoas_expostas(self):
        # 5 pessoas × 2 turnos = 10
        assert calcular_pessoas_expostas(5, 2) == 10

    def test_custo_hora_operador(self):
        # (2500 × 1,7) / 176 ≈ 24,15
        assert calcular_custo_hora_operador(2500, 1.7) == pytest.approx(24.1477, rel=1e-3)

    def test_faturamento_mensal_por_producao_mensal(self):
        assert (
            calcular_faturamento_mensal(
                cadencia_producao=None,
                producao_mensal=200_000,
                horas_turno=8,
                turnos_dia=2,
                dias_operacao_ano=250,
                preco_venda_peca=10,
            )
            == 2_000_000
        )

    def test_faturamento_mensal_por_cadencia(self):
        # Produção anual: 10×60×8×2×250 = 2.400.000
        # Faturamento anual: × R$10 = 24.000.000 → mensal /12 = 2.000.000
        assert (
            calcular_faturamento_mensal(
                cadencia_producao=10,
                producao_mensal=None,
                horas_turno=8,
                turnos_dia=2,
                dias_operacao_ano=250,
                preco_venda_peca=10,
            )
            == 2_000_000
        )


class TestExemplosCLAUDEMD:
    def test_f01_exemplo_pequena(self):
        # Pequena (4 op, R$2.500): 4 × 2.500 × 1,7 × 12 = 204.000
        assert calcular_f01_mao_de_obra_direta(4, 2500, 1.7) == 204_000

    def test_f01_exemplo_grande(self):
        # Grande (20 op, R$3.200): 20 × 3.200 × 1,7 × 12 = 1.305.600
        assert calcular_f01_mao_de_obra_direta(20, 3200, 1.7) == 1_305_600

    def test_f04_exemplo_pequena(self):
        # Pequena (3 desl, R$2.500, 1,5x): 11.250
        assert calcular_f04_turnover(3, 2500, 1.5) == 11_250

    def test_f04_exemplo_grande(self):
        # Grande (25 desl, R$3.200, 1,5x): 120.000
        assert calcular_f04_turnover(25, 3200, 1.5) == 120_000

    def test_f07_exemplo_pequena(self):
        # Pequena (12 recl, R$2.000): 24.000
        assert calcular_f07_escapes_qualidade(12, 2000) == 24_000

    def test_f07_exemplo_grande(self):
        # Grande (150 recl, R$15.000): 2.250.000
        assert calcular_f07_escapes_qualidade(150, 15_000) == 2_250_000

    def test_f05_retorna_tupla(self):
        refugo, retrabalho, total = calcular_f05_refugo_retrabalho(
            producao_mensal=100_000,
            pct_refugo=0.01,
            custo_mp_unidade=15,
            pct_retrabalho=0.03,
            horas_retrab_unidade=0.2,
            custo_hora_operador=24,
        )
        assert refugo > 0
        assert retrabalho > 0
        assert total == pytest.approx(refugo + retrabalho)


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
