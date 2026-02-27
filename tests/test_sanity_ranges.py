import pytest

from core.formulas import (
    calcular_custo_hora_parada,
    calcular_f02_horas_extras,
    calcular_horas_operacao_mes,
)
from core.validators import validar_parametros_detalhados
from models.inputs import DoresSelecionadas, ParametrosDetalhados, ProcessoAtual


def test_chp_cai_quando_aumenta_turnos():
    faturamento = 2_000_000.0
    horas_turno = 8.0
    dias_ano = 250

    horas_mes_1 = calcular_horas_operacao_mes(horas_turno, 1, dias_ano)
    horas_mes_2 = calcular_horas_operacao_mes(horas_turno, 2, dias_ano)

    chp_1 = calcular_custo_hora_parada(faturamento, horas_mes_1)
    chp_2 = calcular_custo_hora_parada(faturamento, horas_mes_2)

    assert horas_mes_2 == pytest.approx(horas_mes_1 * 2, rel=1e-9)
    assert chp_2 == pytest.approx(chp_1 / 2, rel=1e-9)


def test_f02_usa_divisor_clt_220():
    num_op = 10
    he_mes = 10.0
    salario = 2200.0
    encargos = 2.0

    custo_hora_base = (salario * encargos) / 220.0
    esperado = num_op * he_mes * custo_hora_base * 1.5 * 12

    assert calcular_f02_horas_extras(num_op, he_mes, salario, encargos) == pytest.approx(esperado, rel=1e-9)


def test_validadores_normalizam_percentuais_0_100_para_fracao():
    dores = DoresSelecionadas()
    dores.f08_custo_oportunidade = True

    processo = ProcessoAtual(
        cadencia_producao=10.0,
        producao_mensal=None,
        horas_por_turno=8.0,
        turnos_por_dia=2,
        dias_operacao_ano=250,
        pessoas_processo_turno=5,
        pessoas_inspecao_turno=1,
        supervisores_por_turno=0,
        salario_medio_operador=2500.0,
        salario_medio_inspetor=3000.0,
        salario_medio_supervisor=5000.0,
        custo_unitario_peca=100.0,
        custo_materia_prima_peca=15.0,
        preco_venda_peca=None,
        faturamento_mensal_linha=1_000_000.0,
    )

    params = ParametrosDetalhados(
        f08_percentual_demanda_reprimida=10,  # 10%
        f08_margem_contribuicao=30,  # 30%
    )

    erros = validar_parametros_detalhados(params, dores, processo)
    assert erros == []
    assert params.f08_percentual_demanda_reprimida == pytest.approx(0.10, rel=1e-9)
    assert params.f08_margem_contribuicao == pytest.approx(0.30, rel=1e-9)

