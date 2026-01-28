"""
Testes unitários para core/calculator.py (fluxo integrado)
"""
import pytest

from core.calculator import ROICalculator
from models.inputs import (
    ProcessoAtual,
    DoresSelecionadas,
    ParametrosDetalhados,
    InvestimentoAutomacao,
)
from models.results import MetasReducao


@pytest.fixture
def processo_padrao():
    return ProcessoAtual(
        cadencia_producao=10.0,
        horas_por_turno=8.0,
        turnos_por_dia=2,
        dias_operacao_ano=250,
        pessoas_processo_turno=5,
        pessoas_inspecao_turno=1,
        custo_unitario_peca=100.0,
        fracao_material=0.6,
    )


@pytest.fixture
def investimento_padrao():
    return InvestimentoAutomacao(
        valor_investimento_min=400_000.0,
        valor_investimento_max=600_000.0,
    )


class TestBasesComuns:
    def test_producao_anual(self, processo_padrao, investimento_padrao):
        calc = ROICalculator(
            processo=processo_padrao,
            dores=DoresSelecionadas(),
            parametros=ParametrosDetalhados(),
            investimento=investimento_padrao,
            metas=MetasReducao(),
        )
        # 10 × 60 × 8 × 2 × 250 = 2.400.000
        assert calc.bases.producao_anual == 2_400_000

    def test_pessoas_expostas(self, processo_padrao, investimento_padrao):
        calc = ROICalculator(
            processo=processo_padrao,
            dores=DoresSelecionadas(),
            parametros=ParametrosDetalhados(),
            investimento=investimento_padrao,
            metas=MetasReducao(),
        )
        assert calc.bases.pessoas_expostas_processo == 10
        assert calc.bases.pessoas_expostas_inspecao == 2


class TestCalculoCompleto:
    def test_sem_dores_selecionadas(self, processo_padrao, investimento_padrao):
        """Sem dores selecionadas, todos os custos devem ser zero."""
        calc = ROICalculator(
            processo=processo_padrao,
            dores=DoresSelecionadas(),
            parametros=ParametrosDetalhados(),
            investimento=investimento_padrao,
            metas=MetasReducao(),
        )
        resultado = calc.calcular()

        assert resultado.custo_total_anual == 0.0
        assert resultado.ganho_anual_potencial == 0.0
        assert resultado.payback_anos == float("inf")
        assert resultado.investimento_medio == 500_000.0

    def test_com_folha_pagamento(self, processo_padrao, investimento_padrao):
        """CO-1: Folha de pagamento com meta de 50%."""
        dores = DoresSelecionadas(co1_folha_pagamento=True)
        metas = MetasReducao(meta_co1=0.5)

        calc = ROICalculator(
            processo=processo_padrao,
            dores=dores,
            parametros=ParametrosDetalhados(),
            investimento=investimento_padrao,
            metas=metas,
        )
        resultado = calc.calcular()

        # CO-1: 10 pessoas × 5000 × 2 × 12 = 1.200.000
        assert resultado.total_co == 1_200_000
        # Ganho: 1.200.000 × 0.5 = 600.000
        assert resultado.ganho_anual_potencial == 600_000
        # Payback: 500.000 / 600.000 ≈ 0.833
        assert resultado.payback_anos == pytest.approx(0.8333, rel=1e-2)

    def test_multiplas_dores(self, processo_padrao, investimento_padrao):
        """Múltiplas dores selecionadas devem somar corretamente."""
        dores = DoresSelecionadas(
            co1_folha_pagamento=True,
            co3_desperdicio=True,
            ql3_inspecao_manual=True,
        )
        parametros = ParametrosDetalhados(percentual_desperdicio=0.02)
        metas = MetasReducao(meta_co1=0.5, meta_co3=0.8, meta_ql3=1.0)

        calc = ROICalculator(
            processo=processo_padrao,
            dores=dores,
            parametros=parametros,
            investimento=investimento_padrao,
            metas=metas,
        )
        resultado = calc.calcular()

        # CO-1: 1.200.000
        # CO-3: 2.400.000 × 0.02 × 60 = 2.880.000
        assert resultado.total_co == pytest.approx(1_200_000 + 2_880_000)

        # QL-3: 2 pessoas × 5000 × 2 × 12 = 240.000
        assert resultado.total_ql == pytest.approx(240_000)

        # Ganho: (1.200.000 × 0.5) + (2.880.000 × 0.8) + (240.000 × 1.0)
        ganho_esperado = 600_000 + 2_304_000 + 240_000
        assert resultado.ganho_anual_potencial == pytest.approx(ganho_esperado)

    def test_roi_calculado_corretamente(self, processo_padrao, investimento_padrao):
        """ROI deve ser calculado com base em ganho e investimento."""
        dores = DoresSelecionadas(co1_folha_pagamento=True)
        metas = MetasReducao(meta_co1=0.5)

        calc = ROICalculator(
            processo=processo_padrao,
            dores=dores,
            parametros=ParametrosDetalhados(),
            investimento=investimento_padrao,
            metas=metas,
        )
        resultado = calc.calcular()

        # Ganho: 600.000, Investimento: 500.000
        # ROI 1 ano: ((600.000 - 500.000) / 500.000) × 100 = 20%
        assert resultado.roi_1_ano == pytest.approx(20.0)
        # ROI 3 anos: ((1.800.000 - 500.000) / 500.000) × 100 = 260%
        assert resultado.roi_3_anos == pytest.approx(260.0)
        # ROI 5 anos: ((3.000.000 - 500.000) / 500.000) × 100 = 500%
        assert resultado.roi_5_anos == pytest.approx(500.0)

    def test_breakdown_preenchido(self, processo_padrao, investimento_padrao):
        """Breakdown deve conter valores detalhados por subcategoria."""
        dores = DoresSelecionadas(co1_folha_pagamento=True, ql5_multas_qualidade=True)
        parametros = ParametrosDetalhados(ocorrencias_multa_ano=6)

        calc = ROICalculator(
            processo=processo_padrao,
            dores=dores,
            parametros=parametros,
            investimento=investimento_padrao,
            metas=MetasReducao(),
        )
        resultado = calc.calcular()

        assert resultado.breakdown_co["CO-1: Folha de Pagamento"] == 1_200_000
        assert resultado.breakdown_ql["QL-5: Multas Qualidade"] == 3_000


class TestInvestimento:
    def test_investimento_medio(self):
        inv = InvestimentoAutomacao(
            valor_investimento_min=400_000.0,
            valor_investimento_max=600_000.0,
        )
        assert inv.valor_investimento_medio == 500_000.0
