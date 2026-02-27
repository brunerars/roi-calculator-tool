"""
Validações de input do usuário.
"""
from __future__ import annotations

from typing import List

from config.constants import FATOR_ENCARGOS_COMPLETO, FATOR_ENCARGOS_CONSERVADOR, FATOR_ENCARGOS_MEDIO
from models.inputs import ClienteBasicInfo, DoresSelecionadas, InvestimentoAutomacao, ParametrosDetalhados, ProcessoAtual


def validar_cliente(cliente: ClienteBasicInfo) -> List[str]:
    """Valida informações básicas do cliente (V2.0)."""

    erros: List[str] = []

    if not (cliente.nome_cliente or "").strip():
        erros.append("Nome do cliente é obrigatório.")
    if not (cliente.nome_projeto or "").strip():
        erros.append("Nome do projeto é obrigatório.")

    if not (cliente.area_atuacao or "").strip():
        erros.append("Área de atuação é obrigatória.")

    if cliente.porte_empresa not in {"pequena", "media", "grande"}:
        erros.append("Porte da empresa deve ser: pequena, média ou grande.")

    if cliente.fator_encargos not in {FATOR_ENCARGOS_CONSERVADOR, FATOR_ENCARGOS_MEDIO, FATOR_ENCARGOS_COMPLETO}:
        erros.append("Fator de encargos deve ser 1,7 / 1,85 / 2,0.")

    return erros


def validar_processo_atual(processo: ProcessoAtual) -> List[str]:
    """Valida dados do processo atual. Retorna lista de erros."""
    erros: List[str] = []

    tem_cadencia = processo.cadencia_producao is not None and processo.cadencia_producao > 0
    tem_producao_mensal = processo.producao_mensal is not None and processo.producao_mensal > 0
    if not (tem_cadencia or tem_producao_mensal):
        erros.append("Informe cadência de produção (>0) ou produção mensal (>0).")
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
    if processo.salario_medio_operador < 0:
        erros.append("Salário médio do operador não pode ser negativo.")
    if processo.salario_medio_inspetor < 0:
        erros.append("Salário médio do inspetor não pode ser negativo.")
    if processo.salario_medio_supervisor < 0:
        erros.append("Salário médio do supervisor não pode ser negativo.")

    if processo.custo_unitario_peca < 0:
        erros.append("Custo unitário da peça não pode ser negativo.")
    if processo.custo_materia_prima_peca < 0:
        erros.append("Custo de matéria-prima por peça não pode ser negativo.")

    if processo.faturamento_mensal_linha is not None and processo.faturamento_mensal_linha < 0:
        erros.append("Faturamento mensal da linha não pode ser negativo.")

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


def validar_parametros_detalhados(
    params: ParametrosDetalhados,
    dores: DoresSelecionadas,
    processo: ProcessoAtual,
) -> List[str]:
    """Valida parâmetros detalhados (V2.0), de forma condicional às fórmulas selecionadas."""

    erros: List[str] = []

    def _normalize_fraction(campo: str):
        """
        Normaliza percentuais aceitando:
        - fração (0–1): mantém
        - percentual (0–100): converte para 0–1
        """
        valor = getattr(params, campo)
        if valor is None:
            return
        if valor > 1 and valor <= 100:
            setattr(params, campo, valor / 100)

    def _req(campo: str, rotulo: str):
        if getattr(params, campo) is None:
            erros.append(f"{rotulo} é obrigatório.")

    def _nonneg(campo: str, rotulo: str):
        valor = getattr(params, campo)
        if valor is not None and valor < 0:
            erros.append(f"{rotulo} não pode ser negativo.")

    def _fraction(campo: str, rotulo: str):
        valor = getattr(params, campo)
        if valor is not None and not (0 <= valor <= 1):
            erros.append(f"{rotulo} deve estar entre 0% e 100%.")

    # F02
    if dores.f02_horas_extras:
        _req("f02_media_he_mes_por_pessoa", "F02: Média de horas extras por mês por pessoa")
        _nonneg("f02_media_he_mes_por_pessoa", "F02: Média de horas extras por mês por pessoa")

    # F03
    if dores.f03_curva_aprendizagem:
        _req("f03_novas_contratacoes_ano", "F03: Novas contratações por ano")
        _req("f03_salario_novato", "F03: Salário do novato")
        _req("f03_meses_curva", "F03: Meses de curva de aprendizagem")
        _req("f03_percentual_tempo_supervisor", "F03: Percentual de tempo do supervisor")
        _nonneg("f03_novas_contratacoes_ano", "F03: Novas contratações por ano")
        _nonneg("f03_salario_novato", "F03: Salário do novato")
        _nonneg("f03_meses_curva", "F03: Meses de curva de aprendizagem")
        _normalize_fraction("f03_percentual_tempo_supervisor")
        _fraction("f03_percentual_tempo_supervisor", "F03: Percentual de tempo do supervisor")
        _nonneg("f03_salario_supervisor", "F03: Salário do supervisor")

    # F04
    if dores.f04_turnover:
        _req("f04_desligamentos_ano", "F04: Desligamentos por ano")
        _nonneg("f04_desligamentos_ano", "F04: Desligamentos por ano")
        _nonneg("f04_fator_custo_turnover", "F04: Fator de custo de turnover")

    # F05
    if dores.f05_refugo_retrabalho:
        _req("f05_percentual_refugo", "F05: Percentual de refugo")
        _req("f05_percentual_retrabalho", "F05: Percentual de retrabalho")
        _req("f05_horas_retrabalho_por_unidade", "F05: Horas de retrabalho por unidade")
        _normalize_fraction("f05_percentual_refugo")
        _normalize_fraction("f05_percentual_retrabalho")
        _fraction("f05_percentual_refugo", "F05: Percentual de refugo")
        _fraction("f05_percentual_retrabalho", "F05: Percentual de retrabalho")
        _nonneg("f05_horas_retrabalho_por_unidade", "F05: Horas de retrabalho por unidade")

    # F07
    if dores.f07_escapes_qualidade:
        _req("f07_reclamacoes_clientes_ano", "F07: Reclamações de clientes por ano")
        _req("f07_custo_medio_por_reclamacao", "F07: Custo médio por reclamação")
        _nonneg("f07_reclamacoes_clientes_ano", "F07: Reclamações de clientes por ano")
        _nonneg("f07_custo_medio_por_reclamacao", "F07: Custo médio por reclamação")

    # F08
    if dores.f08_custo_oportunidade:
        _req("f08_percentual_demanda_reprimida", "F08: Percentual de demanda reprimida")
        _req("f08_margem_contribuicao", "F08: Margem de contribuição")
        _normalize_fraction("f08_percentual_demanda_reprimida")
        _normalize_fraction("f08_margem_contribuicao")
        _fraction("f08_percentual_demanda_reprimida", "F08: Percentual de demanda reprimida")
        _fraction("f08_margem_contribuicao", "F08: Margem de contribuição")
        if not processo.faturamento_mensal_linha:
            erros.append("F08: Informe o faturamento mensal da linha (senão a fórmula fica zerada).")

    # F09
    if dores.f09_ociosidade_silenciosa:
        _req("f09_minutos_ociosos_por_dia", "F09: Minutos ociosos por dia")
        _nonneg("f09_minutos_ociosos_por_dia", "F09: Minutos ociosos por dia")

    # F10
    if dores.f10_paradas_linha:
        _req("f10_paradas_mes", "F10: Paradas por mês")
        _req("f10_duracao_media_parada_horas", "F10: Duração média da parada (h)")
        _nonneg("f10_paradas_mes", "F10: Paradas por mês")
        _nonneg("f10_duracao_media_parada_horas", "F10: Duração média da parada (h)")
        _nonneg("f10_custo_hora_parada", "F10: Custo hora parada (se informado)")
        if (not processo.faturamento_mensal_linha) and not (params.f10_custo_hora_parada and params.f10_custo_hora_parada > 0):
            erros.append("F10: Informe faturamento mensal da linha ou preencha um Custo hora parada (> 0).")

    # F11
    if dores.f11_setup_changeover:
        _req("f11_setups_mes", "F11: Setups por mês")
        _req("f11_horas_por_setup", "F11: Horas por setup")
        _nonneg("f11_setups_mes", "F11: Setups por mês")
        _nonneg("f11_horas_por_setup", "F11: Horas por setup")
        _nonneg("f11_custo_hora_parada", "F11: Custo hora parada (se informado)")
        if (not processo.faturamento_mensal_linha) and not (params.f11_custo_hora_parada and params.f11_custo_hora_parada > 0):
            erros.append("F11: Informe faturamento mensal da linha ou preencha um Custo hora parada (> 0).")

    # F12
    if dores.f12_riscos_acidentes:
        _req("f12_afastamentos_ano", "F12: Afastamentos por ano")
        _req("f12_custo_medio_afastamento", "F12: Custo médio por afastamento")
        _req("f12_acidentes_com_lesao_ano", "F12: Acidentes com lesão por ano")
        _req("f12_custo_medio_acidente", "F12: Custo médio por acidente")
        _req("f12_probabilidade_processo", "F12: Probabilidade de processo")
        _req("f12_custo_estimado_processo", "F12: Custo estimado do processo")
        _nonneg("f12_afastamentos_ano", "F12: Afastamentos por ano")
        _nonneg("f12_custo_medio_afastamento", "F12: Custo médio por afastamento")
        _nonneg("f12_acidentes_com_lesao_ano", "F12: Acidentes com lesão por ano")
        _nonneg("f12_custo_medio_acidente", "F12: Custo médio por acidente")
        _normalize_fraction("f12_probabilidade_processo")
        _fraction("f12_probabilidade_processo", "F12: Probabilidade de processo")
        _nonneg("f12_custo_estimado_processo", "F12: Custo estimado do processo")

    # F13
    if dores.f13_frota_empilhadeiras:
        _req("f13_num_empilhadeiras", "F13: Número de empilhadeiras")
        _req("f13_custo_operador_mes", "F13: Custo operador/mês")
        _req("f13_custo_equipamento_mes", "F13: Custo equipamento/mês")
        _req("f13_custo_energia_mes", "F13: Custo energia/mês")
        _req("f13_custo_manutencao_mes", "F13: Custo manutenção/mês")
        _nonneg("f13_num_empilhadeiras", "F13: Número de empilhadeiras")
        _nonneg("f13_custo_operador_mes", "F13: Custo operador/mês")
        _nonneg("f13_custo_equipamento_mes", "F13: Custo equipamento/mês")
        _nonneg("f13_custo_energia_mes", "F13: Custo energia/mês")
        _nonneg("f13_custo_manutencao_mes", "F13: Custo manutenção/mês")

    # F14 — 0 supervisores é válido (F14 = R$0 nesse cenário)
    if dores.f14_supervisao:
        _nonneg("f14_num_supervisores", "F14: Número de supervisores")
        _nonneg("f14_salario_supervisor", "F14: Salário do supervisor (se informado)")

    # F15
    if dores.f15_compliance_epis:
        _req("f15_custo_epi_ano_por_pessoa", "F15: Custo de EPI/ano por pessoa")
        _req("f15_custo_exames_ano_por_pessoa", "F15: Custo de exames/ano por pessoa")
        _nonneg("f15_custo_epi_ano_por_pessoa", "F15: Custo de EPI/ano por pessoa")
        _nonneg("f15_custo_exames_ano_por_pessoa", "F15: Custo de exames/ano por pessoa")

    # F16
    if dores.f16_energia_utilidades:
        _req("f16_area_operacao_m2", "F16: Área de operação (m²)")
        _req("f16_custo_energia_m2_ano", "F16: Custo energia por m²/ano")
        _nonneg("f16_area_operacao_m2", "F16: Área de operação (m²)")
        _nonneg("f16_custo_energia_m2_ano", "F16: Custo energia por m²/ano")

    # F17
    if dores.f17_espaco_fisico:
        _req("f17_area_m2", "F17: Área (m²)")
        _req("f17_custo_m2_ano", "F17: Custo m²/ano")
        _req("f17_percentual_reducao_automacao", "F17: Percentual de redução com automação")
        _nonneg("f17_area_m2", "F17: Área (m²)")
        _nonneg("f17_custo_m2_ano", "F17: Custo m²/ano")
        _normalize_fraction("f17_percentual_reducao_automacao")
        _fraction("f17_percentual_reducao_automacao", "F17: Percentual de redução com automação")

    # F18
    if dores.f18_gestao_dados:
        _req("f18_pessoas_envolvidas", "F18: Pessoas envolvidas")
        _req("f18_horas_dia_tarefas_dados", "F18: Horas/dia em tarefas de dados")
        _nonneg("f18_pessoas_envolvidas", "F18: Pessoas envolvidas")
        _nonneg("f18_horas_dia_tarefas_dados", "F18: Horas/dia em tarefas de dados")

    return erros
