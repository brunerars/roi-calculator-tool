"""
Fórmulas detalhadas — V2.0 (Custo da Inação).
"""

from __future__ import annotations

from typing import Tuple

from config.constants import HORAS_MES_CUSTO_PRODUCAO


# =============================================================================
# BASES COMUNS
# =============================================================================


def calcular_producao_anual(cadencia: float, horas_turno: float, turnos_dia: int, dias_ano: int) -> float:
    """
    Produção anual em peças.
    Fórmula: Cadência × 60 × Horas/turno × Turnos/dia × Dias/ano
    """

    return cadencia * 60 * horas_turno * turnos_dia * dias_ano


def calcular_producao_mensal_from_cadencia(
    cadencia: float,
    horas_turno: float,
    turnos_dia: int,
    dias_mes: float = 21,
) -> float:
    """Produção mensal estimada via cadência."""

    return cadencia * 60 * horas_turno * turnos_dia * dias_mes


def calcular_horas_anuais(horas_turno: float, turnos_dia: int, dias_ano: int) -> float:
    """Horas anuais de operação."""

    return horas_turno * turnos_dia * dias_ano


def calcular_pessoas_expostas(pessoas_turno: int, turnos_dia: int) -> int:
    """Total de pessoas expostas (todos os turnos)."""

    return pessoas_turno * turnos_dia


def calcular_custo_hora_operador(salario: float, fator_encargos: float) -> float:
    """
    Custo por hora do operador COM ENCARGOS.
    REGRA V2.0: divisor 176h (não 220h).
    Fórmula: (Salário × Fator Encargos) ÷ 176
    """

    return (salario * fator_encargos) / HORAS_MES_CUSTO_PRODUCAO


def calcular_custo_hora_parada(faturamento_mensal: float | None) -> float:
    """
    Custo de oportunidade da hora parada (Regra #3).
    Fórmula: Faturamento Mensal ÷ 176 horas úteis
    """

    if faturamento_mensal is None or faturamento_mensal == 0:
        return 0.0
    return faturamento_mensal / HORAS_MES_CUSTO_PRODUCAO


# =============================================================================
# DOR 1: CUSTO ELEVADO DE MÃO DE OBRA
# =============================================================================


def calcular_f01_mao_de_obra_direta(num_operadores: int, salario_medio: float, fator_encargos: float) -> float:
    """
    F01: Custo de Mão de Obra Direta Alocada ao Processo.
    Fórmula: Nº Operadores × Salário Médio × Fator Encargos × 12
    """

    return num_operadores * salario_medio * fator_encargos * 12


def calcular_f02_horas_extras(num_operadores: int, media_he_mes: float, salario_medio: float, fator_encargos: float) -> float:
    """
    F02: Custo real das horas extras (com encargos).
    Fórmula: Nº Operadores × HE/mês × Custo Hora com Encargos × 1,5 × 12
    """

    custo_hora = (salario_medio * fator_encargos) / HORAS_MES_CUSTO_PRODUCAO
    return num_operadores * media_he_mes * custo_hora * 1.5 * 12


def calcular_f03_curva_aprendizagem(
    num_contratacoes: int,
    salario_novato: float,
    fator_encargos: float,
    meses_curva: int,
    salario_supervisor: float,
    pct_tempo_supervisor: float,
) -> float:
    """
    F03: Custo da curva de aprendizagem (inclui supervisor).
    Fórmula:
      Nº Contratações × [ (Salário Novato × Encargos × Meses)
                        + (Salário Supervisor × Encargos × %Tempo × Meses) ]
    """

    custo_novato = salario_novato * fator_encargos * meses_curva
    custo_supervisor = salario_supervisor * fator_encargos * pct_tempo_supervisor * meses_curva
    return num_contratacoes * (custo_novato + custo_supervisor)


def calcular_f04_turnover(num_desligamentos: int, salario_medio: float, fator_custo_turnover: float) -> float:
    """
    F04: Custo real do turnover.
    Fórmula: Nº Desligamentos × Salário × Fator de custo de turnover (benchmark 1,5–3,0)
    """

    return num_desligamentos * (salario_medio * fator_custo_turnover)


# =============================================================================
# DOR 2: BAIXA QUALIDADE
# =============================================================================


def calcular_f05_refugo_retrabalho(
    producao_mensal: float,
    pct_refugo: float,
    custo_mp_unidade: float,
    pct_retrabalho: float,
    horas_retrab_unidade: float,
    custo_hora_operador: float,
) -> Tuple[float, float, float]:
    """
    F05: Custo do refugo e do retrabalho (separados).
    Refugo = Produção Mensal × % Refugo × Custo MP/Unidade × 12
    Retrabalho = Produção Mensal × % Retrabalho × Horas Retrab. × Custo Hora × 12
    """

    custo_refugo = producao_mensal * pct_refugo * custo_mp_unidade * 12
    custo_retrabalho = producao_mensal * pct_retrabalho * horas_retrab_unidade * custo_hora_operador * 12
    return (custo_refugo, custo_retrabalho, custo_refugo + custo_retrabalho)


def calcular_f06_inspecao_manual(num_inspetores: int, salario_inspetor: float, fator_encargos: float) -> float:
    """F06: Custo da inspeção manual. Fórmula: Nº Inspetores × Salário × Encargos × 12."""

    return num_inspetores * salario_inspetor * fator_encargos * 12


def calcular_f07_escapes_qualidade(reclamacoes_ano: int, custo_medio_reclamacao: float) -> float:
    """F07: Custo dos escapes de qualidade. Fórmula: Reclamações/Ano × Custo Médio."""

    return reclamacoes_ano * custo_medio_reclamacao


# =============================================================================
# DOR 3: BAIXA PRODUTIVIDADE
# =============================================================================


def calcular_f08_custo_oportunidade(faturamento_mensal: float, pct_demanda_reprimida: float, margem_contribuicao: float) -> float:
    """
    F08: Custo de oportunidade (gargalo de faturamento).
    Fórmula: Faturamento Mensal × % Demanda reprimida × Margem de contribuição × 12
    """

    return faturamento_mensal * pct_demanda_reprimida * margem_contribuicao * 12


def calcular_f09_ociosidade_silenciosa(num_operadores: int, min_ociosos_dia: float, custo_hora_operador: float, dias_ano: int) -> float:
    """
    F09: Custo da ociosidade silenciosa.
    Fórmula: Nº Operadores × (Min ociosos/60) × Custo Hora × Dias/Ano
    """

    return num_operadores * (min_ociosos_dia / 60) * custo_hora_operador * dias_ano


def calcular_f10_paradas_linha(paradas_mes: int, duracao_media_horas: float, custo_hora_parada: float) -> float:
    """F10: Custo das paradas de linha. Fórmula: Paradas/Mês × Duração(h) × Custo Hora Parada × 12."""

    return paradas_mes * duracao_media_horas * custo_hora_parada * 12


def calcular_f11_setup_changeover(setups_mes: int, horas_setup: float, custo_hora_parada: float) -> float:
    """F11: Custo do setup/changeover. Fórmula: Setups/Mês × Horas/Setup × Custo Hora Parada × 12."""

    return setups_mes * horas_setup * custo_hora_parada * 12


# =============================================================================
# DOR 4: FALTA DE SEGURANÇA E ERGONOMIA
# =============================================================================


def calcular_f12_riscos_acidentes(
    afastamentos_ano: int,
    custo_afastamento: float,
    acidentes_ano: int,
    custo_acidente: float,
    prob_processo: float,
    custo_processo: float,
) -> Tuple[float, float, float, float]:
    """
    F12: Custo dos riscos, acidentes e doenças (3 componentes).
    Retorna: (afastamentos, acidentes, risco_legal, total)
    """

    c_afast = afastamentos_ano * custo_afastamento
    c_acid = acidentes_ano * custo_acidente
    c_legal = prob_processo * custo_processo
    return (c_afast, c_acid, c_legal, c_afast + c_acid + c_legal)


def calcular_f13_frota_empilhadeiras(
    num_empilhadeiras: int,
    custo_operador: float,
    custo_equipamento: float,
    custo_energia: float,
    custo_manutencao: float,
) -> float:
    """
    F13: Custo real da frota de empilhadeiras (TCO).
    Fórmula: Nº Empilhadeiras × (Operador + Equipamento + Energia + Manutenção) × 12
    """

    custo_mensal_total = custo_operador + custo_equipamento + custo_energia + custo_manutencao
    return num_empilhadeiras * custo_mensal_total * 12


# =============================================================================
# DOR 5: CUSTOS OCULTOS DE GESTÃO E ESTRUTURA
# =============================================================================


def calcular_f14_supervisao(num_supervisores: int, salario_supervisor: float, fator_encargos: float) -> float:
    """F14: Custo de supervisão. Fórmula: Nº Supervisores × Salário × Encargos × 12."""

    return num_supervisores * salario_supervisor * fator_encargos * 12


def calcular_f15_compliance_epis(num_operadores: int, custo_epi_ano: float, custo_exames_ano: float) -> float:
    """F15: Custo de compliance/EPIs/exames. Fórmula: Nº Operadores × (EPI/Ano + Exames/Ano)."""

    return num_operadores * (custo_epi_ano + custo_exames_ano)


def calcular_f16_energia(area_m2: float, custo_energia_m2_ano: float) -> float:
    """F16: Custo de energia/utilidades não-produtivo. Fórmula: Área(m²) × Custo Energia/m²/ano."""

    return area_m2 * custo_energia_m2_ano


def calcular_f17_espaco_fisico(area_m2: float, custo_m2_ano: float, pct_reducao: float) -> float:
    """F17: Custo do espaço físico. Fórmula: Área × Custo m²/ano × % redução."""

    return area_m2 * custo_m2_ano * pct_reducao


def calcular_f18_gestao_dados(num_pessoas: int, horas_dia: float, custo_hora_operador: float, dias_ano: int) -> float:
    """F18: Custo da gestão manual de dados. Fórmula: Nº Pessoas × Horas/Dia × Custo Hora × Dias/Ano."""

    return num_pessoas * horas_dia * custo_hora_operador * dias_ano


# =============================================================================
# INDICADORES FINANCEIROS
# =============================================================================


def calcular_payback(investimento: float, ganho_anual: float) -> float:
    """Payback simples em anos. Fórmula: Investimento ÷ Ganho anual."""

    if ganho_anual == 0:
        return float("inf")
    return investimento / ganho_anual


def calcular_roi(investimento: float, ganho_anual: float, anos: int) -> float:
    """ROI em % para N anos. Fórmula: ((Ganho×Anos) − Investimento) ÷ Investimento × 100."""

    if investimento == 0:
        return 0.0
    return ((ganho_anual * anos) - investimento) / investimento * 100


def calcular_ganho_anual(custo_atual: float, meta_reducao: float) -> float:
    """Ganho anual potencial. Fórmula: Custo atual × Meta de redução (fração 0–1)."""

    return custo_atual * meta_reducao
