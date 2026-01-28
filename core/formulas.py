"""
Fórmulas detalhadas para cálculo de custos e indicadores financeiros.
"""


# =============================================================================
# BASES COMUNS
# =============================================================================

def calcular_producao_anual(
    cadencia: float, horas_turno: float, turnos_dia: int, dias_ano: int
) -> float:
    """Produção anual em peças.
    Fórmula: Cadência × 60 × Horas/turno × Turnos/dia × Dias/ano
    """
    return cadencia * 60 * horas_turno * turnos_dia * dias_ano


def calcular_horas_anuais(
    horas_turno: float, turnos_dia: int, dias_ano: int
) -> float:
    """Horas anuais de operação.
    Fórmula: Horas/turno × Turnos/dia × Dias/ano
    """
    return horas_turno * turnos_dia * dias_ano


def calcular_pessoas_expostas(pessoas_turno: int, turnos_dia: int) -> int:
    """Total de pessoas expostas ao processo.
    Fórmula: Pessoas/turno × Turnos/dia
    """
    return pessoas_turno * turnos_dia


def calcular_custo_hora_operador(salario: float, horas_mes: float) -> float:
    """Custo por hora do operador.
    Fórmula: Salário / Horas trabalhadas no mês
    """
    return salario / horas_mes


def calcular_custo_dia_absenteismo(salario: float, dias_ano: int) -> float:
    """Custo por dia de absenteísmo.
    Fórmula: (Salário × 12) / Dias de operação por ano
    """
    return (salario * 12) / dias_ano


def calcular_custo_material(custo_unitario: float, fracao_material: float) -> float:
    """Custo de material por peça.
    Fórmula: Custo unitário × Fração de material
    """
    return custo_unitario * fracao_material


# =============================================================================
# CO - CUSTOS OPERACIONAIS
# =============================================================================

def calcular_co1_folha_pagamento(
    pessoas_expostas: int, salario: float, turnos_dia: int
) -> float:
    """CO-1: Folha de Pagamento Direta.
    Fórmula: Pessoas × Salário × Turnos × 12
    """
    return pessoas_expostas * salario * turnos_dia * 12


def calcular_co2_terceirizacao(
    volume: float, custo_unitario: float, meses: int
) -> float:
    """CO-2: Terceirização de Produção.
    Fórmula: Volume × Custo × Meses
    """
    return volume * custo_unitario * meses


def calcular_co3_desperdicio(
    producao_anual: float, percentual_desperdicio: float, custo_material: float
) -> float:
    """CO-3: Desperdício de Insumos.
    Fórmula: Produção anual × % desperdício × Custo material
    """
    return producao_anual * percentual_desperdicio * custo_material


def calcular_co4_manutencao(
    paradas_mes: int, duracao_min: float, custo_hora_parada: float
) -> float:
    """CO-4: Manutenção Corretiva.
    Fórmula: (Paradas × Min / 60 × 12) × Custo hora parada
    """
    return (paradas_mes * duracao_min / 60 * 12) * custo_hora_parada


# =============================================================================
# QL - QUALIDADE
# =============================================================================

def calcular_ql1_retrabalho(
    producao_anual: float,
    percentual_retrabalho: float,
    custo_peca: float,
    fator_retrabalho: float,
) -> float:
    """QL-1: Retrabalho Interno.
    Fórmula: Produção anual × % retrabalho × Custo peça × Fator retrabalho
    """
    return producao_anual * percentual_retrabalho * custo_peca * fator_retrabalho


def calcular_ql2_refugo(
    producao_anual: float, percentual_scrap: float, custo_peca: float
) -> float:
    """QL-2: Refugo / Scrap.
    Fórmula: Produção anual × % refugo × Custo peça
    """
    return producao_anual * percentual_scrap * custo_peca


def calcular_ql3_inspecao(
    pessoas_inspecao: int, salario: float, turnos_dia: int
) -> float:
    """QL-3: Inspeção Manual 100%.
    Fórmula: Pessoas inspeção × Salário × Turnos × 12
    """
    return pessoas_inspecao * salario * turnos_dia * 12


def calcular_ql4_logistica(
    producao_anual: float, percentual_retorno: float, custo_logistica: float
) -> float:
    """QL-4: Logística Reversa / Garantias.
    Fórmula: Produção anual × % retorno × Custo logística
    """
    return producao_anual * percentual_retorno * custo_logistica


def calcular_ql5_multas_qualidade(ocorrencias: int, multa_media: float) -> float:
    """QL-5: Multas Contratuais de Qualidade.
    Fórmula: Ocorrências × Multa média
    """
    return ocorrencias * multa_media


# =============================================================================
# SE - SEGURANÇA E ERGONOMIA
# =============================================================================

def calcular_se1_absenteismo(dias_perdidos: int, custo_dia: float) -> float:
    """SE-1: Absenteísmo.
    Fórmula: Dias perdidos × Custo/dia
    """
    return dias_perdidos * custo_dia


def calcular_se2_turnover(desligamentos: int, custo_rescisao: float) -> float:
    """SE-2: Turnover (Rotatividade).
    Fórmula: Desligamentos × Custo rescisão
    """
    return desligamentos * custo_rescisao


def calcular_se3_treinamentos(desligamentos: int, custo_treinamento: float) -> float:
    """SE-3: Treinamentos Recorrentes.
    Fórmula: Desligamentos × Custo treinamento
    """
    return desligamentos * custo_treinamento


def calcular_se4_passivo_juridico(ocorrencias: int, provisao: float) -> float:
    """SE-4: Passivo Jurídico / Multas.
    Fórmula: Ocorrências × Provisão
    """
    return ocorrencias * provisao


# =============================================================================
# PR - PRODUTIVIDADE
# =============================================================================

def calcular_pr1_horas_extras(
    he_totais_mes: float, custo_hora: float, fator_he: float
) -> float:
    """PR-1: Horas Extras Recorrentes.
    Fórmula: HE totais/mês × 12 × Custo hora × Fator HE
    """
    return he_totais_mes * 12 * custo_hora * fator_he


def calcular_pr2_headcount(pessoas_adicionais: int, custo_mensal: float) -> float:
    """PR-2: Aumento de Headcount.
    Fórmula: Pessoas × Custo mensal × 12
    """
    return pessoas_adicionais * custo_mensal * 12


def calcular_pr3_vendas_perdidas(demanda_mes: float, margem_peca: float) -> float:
    """PR-3: Vendas Perdidas (Custo de Oportunidade).
    Fórmula: Demanda não atendida/mês × 12 × Margem
    """
    return demanda_mes * 12 * margem_peca


def calcular_pr4_multas_atraso(ocorrencias: int, multa: float) -> float:
    """PR-4: Multas por Atraso.
    Fórmula: Ocorrências × Multa
    """
    return ocorrencias * multa


# =============================================================================
# INDICADORES FINANCEIROS
# =============================================================================

def calcular_payback(investimento: float, ganho_anual: float) -> float:
    """Payback Simples em anos.
    Fórmula: Investimento / Ganho anual
    """
    if ganho_anual == 0:
        return float("inf")
    return investimento / ganho_anual


def calcular_roi(investimento: float, ganho_anual: float, anos: int) -> float:
    """ROI em % para N anos.
    Fórmula: ((Ganho × Anos) - Investimento) / Investimento × 100
    """
    if investimento == 0:
        return 0.0
    return ((ganho_anual * anos) - investimento) / investimento * 100


def calcular_ganho_anual(custo_atual: float, meta_reducao: float) -> float:
    """Ganho anual baseado em meta de redução.
    Fórmula: Custo atual × Meta de redução (%)
    """
    return custo_atual * meta_reducao
