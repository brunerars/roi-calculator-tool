"""
Validações de input do usuário.
"""
from typing import List, Tuple

from models.inputs import ProcessoAtual, ParametrosDetalhados, InvestimentoAutomacao


def validar_processo_atual(processo: ProcessoAtual) -> List[str]:
    """Valida dados do processo atual. Retorna lista de erros."""
    erros: List[str] = []

    if processo.cadencia_producao <= 0:
        erros.append("Cadência de produção deve ser maior que zero.")
    if not (1 <= processo.horas_por_turno <= 24):
        erros.append("Horas por turno deve estar entre 1 e 24.")
    if not (1 <= processo.turnos_por_dia <= 3):
        erros.append("Turnos por dia deve estar entre 1 e 3.")
    if not (1 <= processo.dias_operacao_ano <= 365):
        erros.append("Dias de operação por ano deve estar entre 1 e 365.")
    if processo.pessoas_processo_turno < 1:
        erros.append("Deve haver pelo menos 1 pessoa no processo por turno.")
    if processo.pessoas_inspecao_turno < 0:
        erros.append("Pessoas em inspeção não pode ser negativo.")
    if processo.custo_unitario_peca <= 0:
        erros.append("Custo unitário da peça deve ser maior que zero.")
    if not (0 <= processo.fracao_material <= 1):
        erros.append("Fração de material deve estar entre 0% e 100%.")

    return erros


def validar_investimento(investimento: InvestimentoAutomacao) -> List[str]:
    """Valida dados de investimento. Retorna lista de erros."""
    erros: List[str] = []

    if investimento.valor_investimento_min <= 0:
        erros.append("Valor mínimo de investimento deve ser maior que zero.")
    if investimento.valor_investimento_max <= 0:
        erros.append("Valor máximo de investimento deve ser maior que zero.")
    if investimento.valor_investimento_min > investimento.valor_investimento_max:
        erros.append("Valor mínimo não pode ser maior que o valor máximo.")

    return erros


def validar_parametros_detalhados(params: ParametrosDetalhados) -> List[str]:
    """Valida parâmetros detalhados. Retorna lista de erros."""
    erros: List[str] = []

    # Percentuais devem estar entre 0 e 1
    campos_percentuais: List[Tuple[str, str]] = [
        ("percentual_desperdicio", "Percentual de desperdício"),
        ("percentual_retrabalho", "Percentual de retrabalho"),
        ("percentual_scrap", "Percentual de scrap"),
        ("percentual_retorno_garantia", "Percentual de retorno em garantia"),
    ]

    for campo, nome in campos_percentuais:
        valor = getattr(params, campo)
        if valor is not None and not (0 <= valor <= 1):
            erros.append(f"{nome} deve estar entre 0% e 100%.")

    # Valores numéricos não podem ser negativos
    campos_positivos: List[Tuple[str, str]] = [
        ("volume_terceirizado", "Volume terceirizado"),
        ("custo_unitario_terceirizado", "Custo unitário terceirizado"),
        ("meses_pico", "Meses de pico"),
        ("paradas_nao_planejadas_mes", "Paradas não planejadas por mês"),
        ("duracao_media_parada_min", "Duração média de parada"),
        ("ocorrencias_multa_ano", "Ocorrências de multa por ano"),
        ("dias_perdidos_ano", "Dias perdidos por ano"),
        ("desligamentos_ano", "Desligamentos por ano"),
        ("ocorrencias_processo_ano", "Ocorrências de processo por ano"),
        ("horas_extras_mes_pessoa", "Horas extras por mês por pessoa"),
        ("pessoas_adicionais", "Pessoas adicionais"),
        ("demanda_nao_atendida_mes", "Demanda não atendida por mês"),
        ("margem_por_peca", "Margem por peça"),
        ("ocorrencias_atraso_ano", "Ocorrências de atraso por ano"),
    ]

    for campo, nome in campos_positivos:
        valor = getattr(params, campo)
        if valor is not None and valor < 0:
            erros.append(f"{nome} não pode ser negativo.")

    return erros
