"""
Formulários Streamlit para input de dados.
"""
import streamlit as st

from models.inputs import (
    ClienteBasicInfo,
    ProcessoAtual,
    DoresSelecionadas,
    ParametrosDetalhados,
    InvestimentoAutomacao,
)
from models.results import MetasReducao


def render_dados_basicos() -> tuple[ClienteBasicInfo, ProcessoAtual]:
    """Renderiza formulário de informações do cliente e dados do processo."""
    st.header("1 - Informações do Cliente")

    col1, col2 = st.columns(2)
    with col1:
        nome_cliente = st.text_input("Nome do Cliente", value="", key="nome_cliente")
        nome_projeto = st.text_input("Nome do Projeto", value="", key="nome_projeto")
    with col2:
        nivel_automacao = st.selectbox(
            "Nível de Automação Atual",
            options=["Manual", "Semiautomatizado", "Automatizado"],
            key="nivel_automacao",
        )

    cliente = ClienteBasicInfo(
        nome_cliente=nome_cliente,
        nome_projeto=nome_projeto,
        nivel_automacao=nivel_automacao,
    )

    st.markdown("---")
    st.header("2 - Dados do Processo Atual")

    col1, col2 = st.columns(2)
    with col1:
        cadencia = st.number_input(
            "Cadência de Produção (peças/min)",
            min_value=0.1, value=10.0, step=0.1, key="cadencia",
        )
        horas_turno = st.number_input(
            "Horas por Turno", min_value=1.0, max_value=24.0, value=8.0, step=0.5,
            key="horas_turno",
        )
        turnos_dia = st.number_input(
            "Turnos por Dia", min_value=1, max_value=3, value=2, key="turnos_dia",
        )
        dias_ano = st.number_input(
            "Dias de Operação por Ano", min_value=1, max_value=365, value=250,
            key="dias_ano",
        )
    with col2:
        pessoas_processo = st.number_input(
            "Pessoas no Processo por Turno", min_value=1, value=5,
            key="pessoas_processo",
        )
        pessoas_inspecao = st.number_input(
            "Pessoas em Inspeção por Turno", min_value=0, value=1,
            key="pessoas_inspecao",
        )
        custo_peca = st.number_input(
            "Custo Unitário da Peça (R$)", min_value=0.01, value=100.0, step=1.0,
            key="custo_peca",
        )
        fracao_material = st.slider(
            "Fração de Material (%)", min_value=0, max_value=100, value=60,
            key="fracao_material",
        )

    processo = ProcessoAtual(
        cadencia_producao=cadencia,
        horas_por_turno=horas_turno,
        turnos_por_dia=turnos_dia,
        dias_operacao_ano=dias_ano,
        pessoas_processo_turno=pessoas_processo,
        pessoas_inspecao_turno=pessoas_inspecao,
        custo_unitario_peca=custo_peca,
        fracao_material=fracao_material / 100,
    )

    return cliente, processo


def render_selecao_dores() -> DoresSelecionadas:
    """Renderiza checkboxes de seleção de dores."""
    st.header("3 - Selecione as Dores Aplicáveis")
    st.caption("Marque os custos que se aplicam ao cenário atual do cliente.")

    dores = DoresSelecionadas()

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("Custos Operacionais (CO)", expanded=True):
            dores.co1_folha_pagamento = st.checkbox(
                "CO-1: Folha de Pagamento Direta", key="co1"
            )
            dores.co2_terceirizacao = st.checkbox(
                "CO-2: Terceirização de Produção", key="co2"
            )
            dores.co3_desperdicio = st.checkbox(
                "CO-3: Desperdício de Insumos", key="co3"
            )
            dores.co4_manutencao = st.checkbox(
                "CO-4: Manutenção Corretiva", key="co4"
            )

        with st.expander("Segurança / Ergonomia (SE)", expanded=True):
            dores.se1_absenteismo = st.checkbox(
                "SE-1: Absenteísmo", key="se1"
            )
            dores.se2_turnover = st.checkbox(
                "SE-2: Turnover (Rotatividade)", key="se2"
            )
            dores.se3_treinamentos = st.checkbox(
                "SE-3: Treinamentos Recorrentes", key="se3"
            )
            dores.se4_passivo_juridico = st.checkbox(
                "SE-4: Passivo Jurídico / Multas", key="se4"
            )

    with col2:
        with st.expander("Qualidade (QL)", expanded=True):
            dores.ql1_retrabalho = st.checkbox(
                "QL-1: Retrabalho Interno", key="ql1"
            )
            dores.ql2_refugo = st.checkbox(
                "QL-2: Refugo / Scrap", key="ql2"
            )
            dores.ql3_inspecao_manual = st.checkbox(
                "QL-3: Inspeção Manual 100%", key="ql3"
            )
            dores.ql4_logistica_reversa = st.checkbox(
                "QL-4: Logística Reversa / Garantias", key="ql4"
            )
            dores.ql5_multas_qualidade = st.checkbox(
                "QL-5: Multas Contratuais de Qualidade", key="ql5"
            )

        with st.expander("Produtividade (PR)", expanded=True):
            dores.pr1_horas_extras = st.checkbox(
                "PR-1: Horas Extras Recorrentes", key="pr1"
            )
            dores.pr2_headcount = st.checkbox(
                "PR-2: Aumento de Headcount", key="pr2"
            )
            dores.pr3_vendas_perdidas = st.checkbox(
                "PR-3: Vendas Perdidas", key="pr3"
            )
            dores.pr4_multas_atraso = st.checkbox(
                "PR-4: Multas por Atraso", key="pr4"
            )

    return dores


def render_parametros_detalhados(dores: DoresSelecionadas) -> ParametrosDetalhados:
    """Renderiza campos condicionais baseados em dores selecionadas."""
    st.header("4 - Parâmetros Detalhados")
    st.caption("Preencha os dados para cada dor selecionada.")

    params = ParametrosDetalhados()

    tem_dor = any([
        dores.co2_terceirizacao, dores.co3_desperdicio, dores.co4_manutencao,
        dores.ql1_retrabalho, dores.ql2_refugo,
        dores.ql4_logistica_reversa, dores.ql5_multas_qualidade,
        dores.se1_absenteismo, dores.se2_turnover, dores.se4_passivo_juridico,
        dores.pr1_horas_extras, dores.pr2_headcount,
        dores.pr3_vendas_perdidas, dores.pr4_multas_atraso,
    ])

    if not tem_dor:
        st.info("Nenhuma dor selecionada requer parâmetros adicionais.")
        return params

    # --- CO ---
    if dores.co2_terceirizacao:
        with st.expander("CO-2: Terceirização de Produção", expanded=True):
            params.volume_terceirizado = st.number_input(
                "Volume Terceirizado (peças/mês)", min_value=0.0, value=1000.0,
                key="co2_vol",
            )
            params.custo_unitario_terceirizado = st.number_input(
                "Custo Unitário Terceirizado (R$)", min_value=0.0, value=50.0,
                key="co2_custo",
            )
            params.meses_pico = st.number_input(
                "Meses de Pico por Ano", min_value=1, max_value=12, value=12,
                key="co2_meses",
            )

    if dores.co3_desperdicio:
        with st.expander("CO-3: Desperdício de Insumos", expanded=True):
            params.percentual_desperdicio = st.slider(
                "Percentual de Desperdício (%)", 0.0, 30.0, 2.0, 0.1,
                key="co3_perc",
            ) / 100

    if dores.co4_manutencao:
        with st.expander("CO-4: Manutenção Corretiva", expanded=True):
            params.paradas_nao_planejadas_mes = st.number_input(
                "Paradas Não Planejadas por Mês", min_value=0, value=4,
                key="co4_paradas",
            )
            params.duracao_media_parada_min = st.number_input(
                "Duração Média da Parada (min)", min_value=0.0, value=30.0,
                key="co4_duracao",
            )

    # --- QL ---
    if dores.ql1_retrabalho:
        with st.expander("QL-1: Retrabalho Interno", expanded=True):
            params.percentual_retrabalho = st.slider(
                "Percentual de Retrabalho (%)", 0.0, 20.0, 3.0, 0.1,
                key="ql1_perc",
            ) / 100
            params.fator_retrabalho = st.slider(
                "Fator de Custo do Retrabalho (%)", 0.0, 100.0, 20.0, 1.0,
                key="ql1_fator",
            ) / 100

    if dores.ql2_refugo:
        with st.expander("QL-2: Refugo / Scrap", expanded=True):
            params.percentual_scrap = st.slider(
                "Percentual de Scrap (%)", 0.0, 20.0, 1.0, 0.1,
                key="ql2_perc",
            ) / 100

    if dores.ql4_logistica_reversa:
        with st.expander("QL-4: Logística Reversa / Garantias", expanded=True):
            params.percentual_retorno_garantia = st.slider(
                "Percentual de Retorno em Garantia (%)", 0.0, 10.0, 0.5, 0.1,
                key="ql4_perc",
            ) / 100

    if dores.ql5_multas_qualidade:
        with st.expander("QL-5: Multas Contratuais de Qualidade", expanded=True):
            params.ocorrencias_multa_ano = st.number_input(
                "Ocorrências de Multa por Ano", min_value=0, value=6,
                key="ql5_ocorr",
            )

    # --- SE ---
    if dores.se1_absenteismo:
        with st.expander("SE-1: Absenteísmo", expanded=True):
            params.perfil_risco_absenteismo = st.selectbox(
                "Perfil de Risco",
                options=["baixo", "medio", "alto"],
                format_func=lambda x: {"baixo": "Baixo (0-3 faltas/ano)",
                                        "medio": "Médio (4-6 faltas/ano)",
                                        "alto": "Alto (7-12 faltas/ano)"}[x],
                key="se1_perfil",
            )
            defaults_abs = {"baixo": 3, "medio": 6, "alto": 12}
            params.dias_perdidos_ano = st.number_input(
                "Dias Perdidos por Ano", min_value=0,
                value=defaults_abs[params.perfil_risco_absenteismo],
                key="se1_dias",
            )

    if dores.se2_turnover:
        with st.expander("SE-2: Turnover (Rotatividade)", expanded=True):
            params.perfil_risco_turnover = st.selectbox(
                "Perfil de Risco",
                options=["baixo", "medio", "alto"],
                format_func=lambda x: {"baixo": "Baixo (5%)",
                                        "medio": "Médio (10%)",
                                        "alto": "Alto (20%)"}[x],
                key="se2_perfil",
            )
            params.desligamentos_ano = st.number_input(
                "Desligamentos por Ano", min_value=0, value=3,
                key="se2_desl",
            )

    if dores.se4_passivo_juridico:
        with st.expander("SE-4: Passivo Jurídico / Multas", expanded=True):
            params.ocorrencias_processo_ano = st.number_input(
                "Ocorrências de Processo por Ano", min_value=0, value=2,
                key="se4_ocorr",
            )

    # --- PR ---
    if dores.pr1_horas_extras:
        with st.expander("PR-1: Horas Extras Recorrentes", expanded=True):
            params.horas_extras_mes_pessoa = st.number_input(
                "Horas Extras/Mês por Pessoa", min_value=0.0, value=10.0,
                key="pr1_he",
            )

    if dores.pr2_headcount:
        with st.expander("PR-2: Aumento de Headcount", expanded=True):
            params.pessoas_adicionais = st.number_input(
                "Pessoas Adicionais Necessárias", min_value=0, value=3,
                key="pr2_pessoas",
            )

    if dores.pr3_vendas_perdidas:
        with st.expander("PR-3: Vendas Perdidas", expanded=True):
            params.demanda_nao_atendida_mes = st.number_input(
                "Demanda Não Atendida (peças/mês)", min_value=0.0, value=500.0,
                key="pr3_demanda",
            )
            params.margem_por_peca = st.number_input(
                "Margem por Peça (R$)", min_value=0.0, value=30.0,
                key="pr3_margem",
            )

    if dores.pr4_multas_atraso:
        with st.expander("PR-4: Multas por Atraso", expanded=True):
            params.ocorrencias_atraso_ano = st.number_input(
                "Ocorrências de Atraso por Ano", min_value=0, value=4,
                key="pr4_ocorr",
            )

    return params


def render_metas_reducao(dores: DoresSelecionadas) -> MetasReducao:
    """Renderiza sliders de meta de redução para cada dor selecionada."""
    st.header("5 - Metas de Redução de Custos")
    st.caption("Defina o percentual de redução esperado com a automação.")

    metas = MetasReducao()

    col1, col2 = st.columns(2)

    with col1:
        if dores.co1_folha_pagamento:
            metas.meta_co1 = st.slider(
                "CO-1: Folha de Pagamento (%)", 0, 100, 50, key="m_co1"
            ) / 100
        if dores.co2_terceirizacao:
            metas.meta_co2 = st.slider(
                "CO-2: Terceirização (%)", 0, 100, 80, key="m_co2"
            ) / 100
        if dores.co3_desperdicio:
            metas.meta_co3 = st.slider(
                "CO-3: Desperdício (%)", 0, 100, 70, key="m_co3"
            ) / 100
        if dores.co4_manutencao:
            metas.meta_co4 = st.slider(
                "CO-4: Manutenção (%)", 0, 100, 60, key="m_co4"
            ) / 100
        if dores.se1_absenteismo:
            metas.meta_se1 = st.slider(
                "SE-1: Absenteísmo (%)", 0, 100, 50, key="m_se1"
            ) / 100
        if dores.se2_turnover:
            metas.meta_se2 = st.slider(
                "SE-2: Turnover (%)", 0, 100, 50, key="m_se2"
            ) / 100
        if dores.se3_treinamentos:
            metas.meta_se3 = st.slider(
                "SE-3: Treinamentos (%)", 0, 100, 50, key="m_se3"
            ) / 100
        if dores.se4_passivo_juridico:
            metas.meta_se4 = st.slider(
                "SE-4: Passivo Jurídico (%)", 0, 100, 70, key="m_se4"
            ) / 100

    with col2:
        if dores.ql1_retrabalho:
            metas.meta_ql1 = st.slider(
                "QL-1: Retrabalho (%)", 0, 100, 80, key="m_ql1"
            ) / 100
        if dores.ql2_refugo:
            metas.meta_ql2 = st.slider(
                "QL-2: Refugo (%)", 0, 100, 70, key="m_ql2"
            ) / 100
        if dores.ql3_inspecao_manual:
            metas.meta_ql3 = st.slider(
                "QL-3: Inspeção Manual (%)", 0, 100, 100, key="m_ql3"
            ) / 100
        if dores.ql4_logistica_reversa:
            metas.meta_ql4 = st.slider(
                "QL-4: Logística Reversa (%)", 0, 100, 60, key="m_ql4"
            ) / 100
        if dores.ql5_multas_qualidade:
            metas.meta_ql5 = st.slider(
                "QL-5: Multas Qualidade (%)", 0, 100, 80, key="m_ql5"
            ) / 100
        if dores.pr1_horas_extras:
            metas.meta_pr1 = st.slider(
                "PR-1: Horas Extras (%)", 0, 100, 70, key="m_pr1"
            ) / 100
        if dores.pr2_headcount:
            metas.meta_pr2 = st.slider(
                "PR-2: Headcount (%)", 0, 100, 100, key="m_pr2"
            ) / 100
        if dores.pr3_vendas_perdidas:
            metas.meta_pr3 = st.slider(
                "PR-3: Vendas Perdidas (%)", 0, 100, 80, key="m_pr3"
            ) / 100
        if dores.pr4_multas_atraso:
            metas.meta_pr4 = st.slider(
                "PR-4: Multas Atraso (%)", 0, 100, 80, key="m_pr4"
            ) / 100

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
