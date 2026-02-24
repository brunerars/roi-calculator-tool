"""
Testes unitários para core/calculator.py (fluxo integrado)
"""
import pytest

from core.calculator import ROICalculator
from models.inputs import (
    ClienteBasicInfo,
    ProcessoAtual,
    DoresSelecionadas,
    ParametrosDetalhados,
    InvestimentoAutomacao,
)
from models.results import MetasReducao


@pytest.fixture
def cliente_padrao():
    return ClienteBasicInfo(
        nome_cliente="Cliente X",
        nome_projeto="Projeto Y",
        area_atuacao="area_1_linhas_montagem",
        porte_empresa="media",
        fator_encargos=1.7,
    )


@pytest.fixture
def processo_padrao():
    return ProcessoAtual(
        cadencia_producao=10.0,
        producao_mensal=None,
        horas_por_turno=8.0,
        turnos_por_dia=2,
        dias_operacao_ano=250,
        pessoas_processo_turno=5,
        pessoas_inspecao_turno=1,
        salario_medio_operador=2500.0,
        salario_medio_inspetor=3000.0,
        salario_medio_supervisor=5000.0,
        custo_unitario_peca=100.0,
        custo_materia_prima_peca=15.0,
        faturamento_mensal_linha=1_760_000.0,  # custo hora parada = 10k/h
    )


@pytest.fixture
def investimento_padrao():
    return InvestimentoAutomacao(
        valor_investimento_min=400_000.0,
        valor_investimento_max=600_000.0,
    )


class TestBasesComuns:
    def test_producao_anual(self, cliente_padrao, processo_padrao, investimento_padrao):
        calc = ROICalculator(
            cliente=cliente_padrao,
            processo=processo_padrao,
            dores=DoresSelecionadas(),
            parametros=ParametrosDetalhados(),
            investimento=investimento_padrao,
            metas=MetasReducao(),
        )
        # 10 × 60 × 8 × 2 × 250 = 2.400.000
        assert calc.bases.producao_anual == 2_400_000
        # 10 × 60 × 8 × 2 × 21 = 201.600
        assert calc.bases.producao_mensal == 201_600

    def test_pessoas_expostas(self, cliente_padrao, processo_padrao, investimento_padrao):
        calc = ROICalculator(
            cliente=cliente_padrao,
            processo=processo_padrao,
            dores=DoresSelecionadas(),
            parametros=ParametrosDetalhados(),
            investimento=investimento_padrao,
            metas=MetasReducao(),
        )
        assert calc.bases.pessoas_expostas_processo == 10
        assert calc.bases.pessoas_expostas_inspecao == 2


class TestCalculoCompleto:
    def test_sem_dores_selecionadas(self, cliente_padrao, processo_padrao, investimento_padrao):
        """Sem dores selecionadas, todos os custos devem ser zero."""
        calc = ROICalculator(
            cliente=cliente_padrao,
            processo=processo_padrao,
            dores=DoresSelecionadas(),
            parametros=ParametrosDetalhados(),
            investimento=investimento_padrao,
            metas=MetasReducao(),
        )
        resultado = calc.calcular()

        assert resultado.custo_total_anual_inacao == 0.0
        assert resultado.ganho_anual_potencial == 0.0
        assert resultado.payback_anos == float("inf")
        assert resultado.investimento_medio == 500_000.0

    def test_com_f01_mao_de_obra(self, cliente_padrao, processo_padrao, investimento_padrao):
        """F01: Mão de obra direta com meta de 50%."""
        dores = DoresSelecionadas(f01_mao_de_obra_direta=True)
        metas = MetasReducao(meta_f01=0.5)

        calc = ROICalculator(
            cliente=cliente_padrao,
            processo=processo_padrao,
            dores=dores,
            parametros=ParametrosDetalhados(),
            investimento=investimento_padrao,
            metas=metas,
        )
        resultado = calc.calcular()

        # F01: 10 × 2500 × 1,7 × 12 = 510.000
        assert resultado.total_dor1 == 510_000
        # Ganho: 510.000 × 0.5 = 255.000
        assert resultado.ganho_anual_potencial == 255_000
        # Payback: 500.000 / 255.000 ≈ 1.96
        assert resultado.payback_anos == pytest.approx(1.9607, rel=1e-2)

    def test_breakdown_preenchido(self, cliente_padrao, processo_padrao, investimento_padrao):
        """Múltiplas dores selecionadas devem somar corretamente."""
        dores = DoresSelecionadas(
            f01_mao_de_obra_direta=True,
            f07_escapes_qualidade=True,
        )
        parametros = ParametrosDetalhados(
            f07_reclamacoes_clientes_ano=12,
            f07_custo_medio_por_reclamacao=2000.0,
        )

        calc = ROICalculator(
            cliente=cliente_padrao,
            processo=processo_padrao,
            dores=dores,
            parametros=parametros,
            investimento=investimento_padrao,
            metas=MetasReducao(),
        )
        resultado = calc.calcular()

        assert resultado.breakdown_dor1["F01"] == 510_000
        assert resultado.breakdown_dor2["F07"] == 24_000


class TestInvestimento:
    def test_investimento_medio(self):
        inv = InvestimentoAutomacao(
            valor_investimento_min=400_000.0,
            valor_investimento_max=600_000.0,
        )
        assert inv.valor_investimento_medio == 500_000.0
