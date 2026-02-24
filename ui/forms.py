"""
Formulários Streamlit para input de dados.
"""
from __future__ import annotations

import streamlit as st

from config.areas import AREAS_ARV
from config.constants import (
    DIAS_OPERACAO_ANO_DEFAULT,
    FATOR_CUSTO_TURNOVER_DEFAULT,
    FATOR_ENCARGOS_OPCOES,
    HORAS_MES_CUSTO_PRODUCAO,
    SALARIO_INSPETOR_DEFAULT,
    SALARIO_OPERADOR_DEFAULT,
    SALARIO_SUPERVISOR_DEFAULT,
)
from models.inputs import (
    ClienteBasicInfo,
    ProcessoAtual,
    DoresSelecionadas,
    ParametrosDetalhados,
    InvestimentoAutomacao,
)
from models.results import MetasReducao


def render_dados_basicos() -> tuple[ClienteBasicInfo, ProcessoAtual]:
    """Renderiza formulário V2.0 (cliente + processo atual)."""

    st.header("1 - Informações do Cliente")

    col1, col2, col3 = st.columns(3)
    with col1:
        nome_cliente = st.text_input("Nome do Cliente", value="", key="nome_cliente")
        nome_projeto = st.text_input("Nome do Projeto", value="", key="nome_projeto")

    with col2:
        area = st.selectbox(
            "Área de Atuação ARV",
            options=list(AREAS_ARV.keys()),
            format_func=lambda k: AREAS_ARV[k]["nome"],
            key="area_atuacao",
        )
        st.caption(AREAS_ARV.get(area, {}).get("descricao", ""))

    with col3:
        porte_label = st.selectbox("Porte da Empresa", ["Pequena", "Média", "Grande"], key="porte_empresa")
        porte = {"Pequena": "pequena", "Média": "media", "Grande": "grande"}[porte_label]
        fator_label = st.selectbox(
            "Fator de Encargos Trabalhistas",
            options=list(FATOR_ENCARGOS_OPCOES.keys()),
            key="fator_encargos",
        )
        fator = FATOR_ENCARGOS_OPCOES[fator_label]

    cliente = ClienteBasicInfo(
        nome_cliente=nome_cliente,
        nome_projeto=nome_projeto,
        area_atuacao=area,
        porte_empresa=porte,
        fator_encargos=fator,
    )

    st.markdown("---")
    st.header("2 - Dados do Processo Atual")

    modo_producao = st.radio(
        "Como você quer informar a produção?",
        options=["Cadência (peças/min)", "Produção mensal (peças/mês)"],
        horizontal=True,
        key="modo_producao",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if modo_producao == "Cadência (peças/min)":
            cadencia = st.number_input("Cadência de Produção (peças/min)", min_value=0.0, value=10.0, step=0.1, key="cadencia")
            producao_mensal = None
        else:
            producao_mensal = st.number_input("Produção Mensal (peças/mês)", min_value=0.0, value=200_000.0, step=1_000.0, key="producao_mensal")
            cadencia = None

        horas_turno = st.number_input("Horas por Turno", min_value=1.0, max_value=24.0, value=8.0, step=0.5, key="horas_turno")
        turnos_dia = st.number_input("Turnos por Dia", min_value=1, max_value=3, value=2, key="turnos_dia")
        dias_ano = st.number_input("Dias de Operação por Ano", min_value=1, max_value=365, value=DIAS_OPERACAO_ANO_DEFAULT, key="dias_ano")

    with col2:
        pessoas_processo = st.number_input("Operadores no Processo por Turno", min_value=0, value=5, key="pessoas_processo")
        pessoas_inspecao = st.number_input("Inspetores por Turno", min_value=0, value=1, key="pessoas_inspecao")
        faturamento_mensal = st.number_input(
            "Faturamento Mensal da Linha (R$) — para Custo Hora Parada",
            min_value=0.0,
            value=0.0,
            step=10_000.0,
            key="faturamento_mensal_linha",
        )
        st.caption(f"Custo hora parada estimado: R$ {(faturamento_mensal / HORAS_MES_CUSTO_PRODUCAO) if faturamento_mensal else 0:,.2f}")

    with col3:
        salario_operador = st.number_input("Salário Médio Operador (R$ bruto)", min_value=0.0, value=SALARIO_OPERADOR_DEFAULT, step=100.0, key="salario_operador")
        salario_inspetor = st.number_input("Salário Médio Inspetor (R$ bruto)", min_value=0.0, value=SALARIO_INSPETOR_DEFAULT, step=100.0, key="salario_inspetor")
        salario_supervisor = st.number_input("Salário Médio Supervisor (R$ bruto)", min_value=0.0, value=SALARIO_SUPERVISOR_DEFAULT, step=100.0, key="salario_supervisor")

        custo_unitario = st.number_input("Custo Unitário da Peça (R$)", min_value=0.0, value=100.0, step=1.0, key="custo_unitario_peca")
        custo_mp = st.number_input("Custo Matéria-Prima por Peça (R$)", min_value=0.0, value=15.0, step=0.5, key="custo_mp_peca")

    processo = ProcessoAtual(
        cadencia_producao=cadencia,
        producao_mensal=producao_mensal,
        horas_por_turno=horas_turno,
        turnos_por_dia=turnos_dia,
        dias_operacao_ano=dias_ano,
        pessoas_processo_turno=pessoas_processo,
        pessoas_inspecao_turno=pessoas_inspecao,
        salario_medio_operador=salario_operador,
        salario_medio_inspetor=salario_inspetor,
        salario_medio_supervisor=salario_supervisor,
        custo_unitario_peca=custo_unitario,
        custo_materia_prima_peca=custo_mp,
        faturamento_mensal_linha=faturamento_mensal if faturamento_mensal > 0 else None,
    )

    return cliente, processo


def render_selecao_dores(area_selecionada: str) -> DoresSelecionadas:
    """
    Renderiza checkboxes organizados por 5 Dores.
    Pré-seleciona fórmulas com base na área de atuação ARV.
    """

    st.header("3 - Selecione as Dores Aplicáveis")
    formulas_sugeridas = AREAS_ARV[area_selecionada]["formulas_aplicaveis"]
    st.info(f"Fórmulas pré-selecionadas para {AREAS_ARV[area_selecionada]['nome']}")

    dores = DoresSelecionadas()

    with st.expander("💰 Dor 1: Custo Elevado de Mão de Obra", expanded=True):
        dores.f01_mao_de_obra_direta = st.checkbox("F01: Mão de Obra Direta", value="F01" in formulas_sugeridas, key="f01")
        dores.f02_horas_extras = st.checkbox("F02: Horas Extras Recorrentes", value="F02" in formulas_sugeridas, key="f02")
        dores.f03_curva_aprendizagem = st.checkbox("F03: Curva de Aprendizagem", value="F03" in formulas_sugeridas, key="f03")
        dores.f04_turnover = st.checkbox("F04: Turnover (Rotatividade)", value="F04" in formulas_sugeridas, key="f04")

    with st.expander("🔍 Dor 2: Baixa Qualidade", expanded=True):
        dores.f05_refugo_retrabalho = st.checkbox("F05: Refugo e Retrabalho", value="F05" in formulas_sugeridas, key="f05")
        dores.f06_inspecao_manual = st.checkbox("F06: Inspeção Manual", value="F06" in formulas_sugeridas, key="f06")
        dores.f07_escapes_qualidade = st.checkbox("F07: Escapes de Qualidade", value="F07" in formulas_sugeridas, key="f07")

    with st.expander("📊 Dor 3: Baixa Produtividade", expanded=True):
        dores.f08_custo_oportunidade = st.checkbox("F08: Custo de Oportunidade", value="F08" in formulas_sugeridas, key="f08")
        dores.f09_ociosidade_silenciosa = st.checkbox("F09: Ociosidade Silenciosa", value="F09" in formulas_sugeridas, key="f09")
        dores.f10_paradas_linha = st.checkbox("F10: Paradas de Linha", value="F10" in formulas_sugeridas, key="f10")
        dores.f11_setup_changeover = st.checkbox("F11: Setup / Changeover", value="F11" in formulas_sugeridas, key="f11")

    with st.expander("⚠️ Dor 4: Segurança e Ergonomia", expanded=True):
        dores.f12_riscos_acidentes = st.checkbox("F12: Riscos, Acidentes e Doenças", value="F12" in formulas_sugeridas, key="f12")
        dores.f13_frota_empilhadeiras = st.checkbox("F13: Frota de Empilhadeiras (TCO)", value="F13" in formulas_sugeridas, key="f13")

    with st.expander("🧠 Dor 5: Custos Ocultos de Gestão", expanded=True):
        dores.f14_supervisao = st.checkbox("F14: Supervisão e Gestão", value="F14" in formulas_sugeridas, key="f14")
        dores.f15_compliance_epis = st.checkbox("F15: Compliance, EPIs e Exames", value="F15" in formulas_sugeridas, key="f15")
        dores.f16_energia_utilidades = st.checkbox("F16: Energia e Utilidades", value="F16" in formulas_sugeridas, key="f16")
        dores.f17_espaco_fisico = st.checkbox("F17: Espaço Físico", value="F17" in formulas_sugeridas, key="f17")
        dores.f18_gestao_dados = st.checkbox("F18: Gestão Manual de Dados", value="F18" in formulas_sugeridas, key="f18")

    return dores


def render_parametros_detalhados(
    dores: DoresSelecionadas,
    processo: ProcessoAtual,
    cliente: ClienteBasicInfo,
) -> ParametrosDetalhados:
    """Renderiza parâmetros detalhados condicionais por fórmula (V2.0)."""

    st.header("4 - Parâmetros Detalhados")
    st.caption("Os campos abaixo só aparecem para as fórmulas selecionadas.")

    params = ParametrosDetalhados()

    # Dor 1
    if dores.f02_horas_extras:
        with st.expander("F02: Horas Extras", expanded=True):
            params.f02_media_he_mes_por_pessoa = st.number_input(
                "Média de horas extras por mês por pessoa",
                min_value=0.0,
                value=10.0,
                step=1.0,
                key="p_f02_he",
            )

    if dores.f03_curva_aprendizagem:
        with st.expander("F03: Curva de Aprendizagem", expanded=True):
            params.f03_novas_contratacoes_ano = st.number_input(
                "Novas contratações por ano",
                min_value=0,
                value=3,
                step=1,
                key="p_f03_contrat",
            )
            params.f03_salario_novato = st.number_input(
                "Salário do novato (R$)",
                min_value=0.0,
                value=float(processo.salario_medio_operador),
                step=100.0,
                key="p_f03_sal_nov",
            )
            params.f03_meses_curva = st.number_input(
                "Meses até produtividade plena",
                min_value=1,
                value=3,
                step=1,
                key="p_f03_meses",
            )
            params.f03_salario_supervisor = st.number_input(
                "Salário do supervisor que treina (R$)",
                min_value=0.0,
                value=float(processo.salario_medio_supervisor),
                step=100.0,
                key="p_f03_sal_sup",
            )
            params.f03_percentual_tempo_supervisor = (
                st.slider(
                    "Percentual do tempo do supervisor dedicado ao treinamento (%)",
                    min_value=0,
                    max_value=100,
                    value=20,
                    key="p_f03_pct",
                )
                / 100
            )

    if dores.f04_turnover:
        with st.expander("F04: Turnover (Rotatividade)", expanded=True):
            params.f04_desligamentos_ano = st.number_input(
                "Desligamentos por ano",
                min_value=0,
                value=3,
                step=1,
                key="p_f04_desl",
            )
            params.f04_fator_custo_turnover = st.number_input(
                "Fator de custo de turnover (benchmark 1,5 a 3,0)",
                min_value=1.0,
                value=float(FATOR_CUSTO_TURNOVER_DEFAULT),
                step=0.1,
                key="p_f04_fator",
            )

    # Dor 2
    if dores.f05_refugo_retrabalho:
        with st.expander("F05: Refugo e Retrabalho", expanded=True):
            params.f05_percentual_refugo = (
                st.slider("Percentual de refugo (%)", 0.0, 30.0, 1.0, 0.1, key="p_f05_ref") / 100
            )
            params.f05_percentual_retrabalho = (
                st.slider("Percentual de retrabalho (%)", 0.0, 30.0, 3.0, 0.1, key="p_f05_ret") / 100
            )
            params.f05_horas_retrabalho_por_unidade = st.number_input(
                "Horas de retrabalho por unidade (h)",
                min_value=0.0,
                value=0.2,
                step=0.05,
                key="p_f05_h",
            )

    if dores.f07_escapes_qualidade:
        with st.expander("F07: Escapes de Qualidade", expanded=True):
            params.f07_reclamacoes_clientes_ano = st.number_input(
                "Reclamações de clientes por ano",
                min_value=0,
                value=12,
                step=1,
                key="p_f07_recl",
            )
            params.f07_custo_medio_por_reclamacao = st.number_input(
                "Custo médio real por reclamação (R$)",
                min_value=0.0,
                value=2000.0,
                step=100.0,
                key="p_f07_custo",
            )

    # Dor 3
    if dores.f08_custo_oportunidade:
        with st.expander("F08: Custo de Oportunidade", expanded=True):
            params.f08_percentual_demanda_reprimida = (
                st.slider("Percentual de demanda reprimida (%)", 0, 100, 10, key="p_f08_dem") / 100
            )
            params.f08_margem_contribuicao = (
                st.slider("Margem de contribuição (%)", 0, 100, 30, key="p_f08_marg") / 100
            )

    if dores.f09_ociosidade_silenciosa:
        with st.expander("F09: Ociosidade Silenciosa", expanded=True):
            params.f09_minutos_ociosos_por_dia = st.number_input(
                "Minutos ociosos por dia (min)",
                min_value=0.0,
                value=15.0,
                step=1.0,
                key="p_f09_min",
            )

    if dores.f10_paradas_linha:
        with st.expander("F10: Paradas de Linha", expanded=True):
            params.f10_paradas_mes = st.number_input("Paradas por mês", min_value=0, value=4, step=1, key="p_f10_par")
            params.f10_duracao_media_parada_horas = st.number_input(
                "Duração média por parada (h)", min_value=0.0, value=1.0, step=0.25, key="p_f10_dur"
            )
            default_chp = (processo.faturamento_mensal_linha or 0.0) / HORAS_MES_CUSTO_PRODUCAO
            params.f10_custo_hora_parada = st.number_input(
                "Custo hora parada (R$/h) — deixe como 0 para usar o faturamento",
                min_value=0.0,
                value=float(default_chp),
                step=10.0,
                key="p_f10_chp",
            )

    if dores.f11_setup_changeover:
        with st.expander("F11: Setup / Changeover", expanded=True):
            params.f11_setups_mes = st.number_input("Setups por mês", min_value=0, value=10, step=1, key="p_f11_set")
            params.f11_horas_por_setup = st.number_input("Horas por setup (h)", min_value=0.0, value=0.5, step=0.25, key="p_f11_h")
            default_chp = (processo.faturamento_mensal_linha or 0.0) / HORAS_MES_CUSTO_PRODUCAO
            params.f11_custo_hora_parada = st.number_input(
                "Custo hora parada (R$/h) — deixe como 0 para usar o faturamento",
                min_value=0.0,
                value=float(default_chp),
                step=10.0,
                key="p_f11_chp",
            )

    # Dor 4
    if dores.f12_riscos_acidentes:
        with st.expander("F12: Riscos, Acidentes e Doenças", expanded=True):
            params.f12_afastamentos_ano = st.number_input("Afastamentos por ano", min_value=0, value=2, step=1, key="p_f12_afast")
            params.f12_custo_medio_afastamento = st.number_input(
                "Custo médio por afastamento (R$)", min_value=0.0, value=8000.0, step=500.0, key="p_f12_cafast"
            )
            params.f12_acidentes_com_lesao_ano = st.number_input("Acidentes com lesão por ano", min_value=0, value=1, step=1, key="p_f12_acid")
            params.f12_custo_medio_acidente = st.number_input(
                "Custo médio por acidente (R$)", min_value=0.0, value=15000.0, step=1000.0, key="p_f12_cacid"
            )
            params.f12_probabilidade_processo = st.slider("Probabilidade de processo (%)", 0, 100, 5, key="p_f12_prob") / 100
            params.f12_custo_estimado_processo = st.number_input(
                "Custo estimado do processo (R$)", min_value=0.0, value=50_000.0, step=5_000.0, key="p_f12_cproc"
            )

    if dores.f13_frota_empilhadeiras:
        with st.expander("F13: Frota de Empilhadeiras (TCO)", expanded=True):
            params.f13_num_empilhadeiras = st.number_input("Número de empilhadeiras", min_value=0, value=2, step=1, key="p_f13_n")
            params.f13_custo_operador_mes = st.number_input(
                "Custo operador/mês (salário + encargos) (R$)",
                min_value=0.0,
                value=float(processo.salario_medio_operador * cliente.fator_encargos),
                step=100.0,
                key="p_f13_op",
            )
            params.f13_custo_equipamento_mes = st.number_input("Custo equipamento/mês (R$)", min_value=0.0, value=2500.0, step=100.0, key="p_f13_eq")
            params.f13_custo_energia_mes = st.number_input("Custo energia/mês (R$)", min_value=0.0, value=300.0, step=50.0, key="p_f13_en")
            params.f13_custo_manutencao_mes = st.number_input(
                "Custo manutenção/mês (R$)", min_value=0.0, value=600.0, step=50.0, key="p_f13_man"
            )

    # Dor 5
    if dores.f14_supervisao:
        with st.expander("F14: Supervisão e Gestão", expanded=True):
            params.f14_num_supervisores = st.number_input("Número de supervisores", min_value=0, value=1, step=1, key="p_f14_n")
            params.f14_salario_supervisor = st.number_input(
                "Salário do supervisor (R$)",
                min_value=0.0,
                value=float(processo.salario_medio_supervisor),
                step=100.0,
                key="p_f14_sal",
            )

    if dores.f15_compliance_epis:
        with st.expander("F15: Compliance, EPIs e Exames", expanded=True):
            params.f15_custo_epi_ano_por_pessoa = st.number_input(
                "Custo EPI/ano por pessoa (R$)", min_value=0.0, value=600.0, step=50.0, key="p_f15_epi"
            )
            params.f15_custo_exames_ano_por_pessoa = st.number_input(
                "Custo exames/ano por pessoa (R$)", min_value=0.0, value=400.0, step=50.0, key="p_f15_ex"
            )

    if dores.f16_energia_utilidades:
        with st.expander("F16: Energia e Utilidades", expanded=True):
            params.f16_area_operacao_m2 = st.number_input("Área de operação (m²)", min_value=0.0, value=200.0, step=10.0, key="p_f16_a")
            params.f16_custo_energia_m2_ano = st.number_input(
                "Custo de energia por m²/ano (R$/m²/ano)", min_value=0.0, value=150.0, step=10.0, key="p_f16_c"
            )

    if dores.f17_espaco_fisico:
        with st.expander("F17: Espaço Físico", expanded=True):
            params.f17_area_m2 = st.number_input("Área (m²)", min_value=0.0, value=200.0, step=10.0, key="p_f17_a")
            params.f17_custo_m2_ano = st.number_input("Custo m²/ano (R$/m²/ano)", min_value=0.0, value=500.0, step=10.0, key="p_f17_c")
            params.f17_percentual_reducao_automacao = (
                st.slider("Percentual de redução com automação (%)", 0, 100, 20, key="p_f17_pct") / 100
            )

    if dores.f18_gestao_dados:
        with st.expander("F18: Gestão Manual de Dados", expanded=True):
            params.f18_pessoas_envolvidas = st.number_input("Pessoas envolvidas", min_value=0, value=2, step=1, key="p_f18_p")
            params.f18_horas_dia_tarefas_dados = st.number_input(
                "Horas/dia em tarefas de dados", min_value=0.0, max_value=24.0, value=1.0, step=0.25, key="p_f18_h"
            )

    return params


def render_metas_reducao(dores: DoresSelecionadas) -> MetasReducao:
    """Renderiza sliders de meta de redução para cada dor selecionada."""
    st.header("5 - Metas de Redução de Custos")
    st.caption("Defina o percentual de redução esperado com a automação.")

    metas = MetasReducao()

    with st.expander("💰 Dor 1: Mão de Obra", expanded=True):
        if dores.f01_mao_de_obra_direta:
            metas.meta_f01 = st.slider("F01: Mão de Obra Direta (%)", 0, 100, 50, key="m_f01") / 100
        if dores.f02_horas_extras:
            metas.meta_f02 = st.slider("F02: Horas Extras (%)", 0, 100, 70, key="m_f02") / 100
        if dores.f03_curva_aprendizagem:
            metas.meta_f03 = st.slider("F03: Curva de Aprendizagem (%)", 0, 100, 50, key="m_f03") / 100
        if dores.f04_turnover:
            metas.meta_f04 = st.slider("F04: Turnover (%)", 0, 100, 50, key="m_f04") / 100

    with st.expander("🔍 Dor 2: Qualidade", expanded=True):
        if dores.f05_refugo_retrabalho:
            metas.meta_f05 = st.slider("F05: Refugo e Retrabalho (%)", 0, 100, 70, key="m_f05") / 100
        if dores.f06_inspecao_manual:
            metas.meta_f06 = st.slider("F06: Inspeção Manual (%)", 0, 100, 100, key="m_f06") / 100
        if dores.f07_escapes_qualidade:
            metas.meta_f07 = st.slider("F07: Escapes de Qualidade (%)", 0, 100, 70, key="m_f07") / 100

    with st.expander("📊 Dor 3: Produtividade", expanded=True):
        if dores.f08_custo_oportunidade:
            metas.meta_f08 = st.slider("F08: Custo de Oportunidade (%)", 0, 100, 50, key="m_f08") / 100
        if dores.f09_ociosidade_silenciosa:
            metas.meta_f09 = st.slider("F09: Ociosidade Silenciosa (%)", 0, 100, 50, key="m_f09") / 100
        if dores.f10_paradas_linha:
            metas.meta_f10 = st.slider("F10: Paradas de Linha (%)", 0, 100, 50, key="m_f10") / 100
        if dores.f11_setup_changeover:
            metas.meta_f11 = st.slider("F11: Setup/Changeover (%)", 0, 100, 50, key="m_f11") / 100

    with st.expander("⚠️ Dor 4: Segurança e Ergonomia", expanded=True):
        if dores.f12_riscos_acidentes:
            metas.meta_f12 = st.slider("F12: Riscos/Acidentes (%)", 0, 100, 50, key="m_f12") / 100
        if dores.f13_frota_empilhadeiras:
            metas.meta_f13 = st.slider("F13: Frota de Empilhadeiras (%)", 0, 100, 80, key="m_f13") / 100

    with st.expander("🧠 Dor 5: Custos Ocultos", expanded=True):
        if dores.f14_supervisao:
            metas.meta_f14 = st.slider("F14: Supervisão (%)", 0, 100, 50, key="m_f14") / 100
        if dores.f15_compliance_epis:
            metas.meta_f15 = st.slider("F15: Compliance/EPIs (%)", 0, 100, 50, key="m_f15") / 100
        if dores.f16_energia_utilidades:
            metas.meta_f16 = st.slider("F16: Energia/Utilidades (%)", 0, 100, 30, key="m_f16") / 100
        if dores.f17_espaco_fisico:
            metas.meta_f17 = st.slider("F17: Espaço Físico (%)", 0, 100, 30, key="m_f17") / 100
        if dores.f18_gestao_dados:
            metas.meta_f18 = st.slider("F18: Gestão de Dados (%)", 0, 100, 50, key="m_f18") / 100

    return metas


def render_investimento() -> InvestimentoAutomacao:
    """Renderiza formulário de investimento da automação."""
    st.header("6 - Investimento da Automação")

    col1, col2, col3 = st.columns(3)
    with col1:
        inv_min = st.number_input(
            "Valor Mínimo (R$)", min_value=0.0, value=400_000.0,
            step=10_000.0, key="inv_min",
        )
    with col2:
        inv_max = st.number_input(
            "Valor Máximo (R$)", min_value=0.0, value=600_000.0,
            step=10_000.0, key="inv_max",
        )
    with col3:
        medio = (inv_min + inv_max) / 2
        st.metric("Valor Médio (R$)", f"R$ {medio:,.2f}")

    return InvestimentoAutomacao(
        valor_investimento_min=inv_min,
        valor_investimento_max=inv_max,
    )
