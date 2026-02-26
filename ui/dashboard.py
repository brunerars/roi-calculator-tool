"""
Dashboard de resultados financeiros.
"""
import streamlit as st
import pandas as pd

from models.results import ResultadosFinanceiros
from models.inputs import ProcessoAtual, ParametrosDetalhados


def render_dashboard(resultados: ResultadosFinanceiros, processo: ProcessoAtual = None, parametros: ParametrosDetalhados = None):
    """Renderiza dashboard completo de resultados."""
    st.header("📈 Análise do Custo da Inação")
    st.markdown("---")

    # --- Métricas Principais ---
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Custo Total da Inação (Anual)", f"R$ {resultados.custo_total_anual_inacao:,.2f}")
    with col2:
        st.metric("Ganho Anual Potencial", f"R$ {resultados.ganho_anual_potencial:,.2f}")
    with col3:
        payback_txt = (
            f"{resultados.payback_anos:.2f} anos"
            if resultados.payback_anos != float("inf")
            else "N/A"
        )
        st.metric("Payback Simples", payback_txt)
    with col4:
        st.metric("ROI 5 Anos", f"{resultados.roi_5_anos:.1f}%")

    st.caption(
        f"Área ARV: {resultados.area_atuacao} • Porte: {resultados.porte_empresa} • "
        f"Encargos: {resultados.fator_encargos_usado:.2f}x"
    )

    # --- Bases de Cálculo ---
    with st.expander("📐 Bases de Cálculo"):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Faturamento Mensal da Linha", f"R$ {resultados.faturamento_mensal_linha:,.2f}")
        with c2:
            chp_txt = f"R$ {resultados.custo_hora_parada:,.2f}/h" if resultados.custo_hora_parada > 0 else "Não informado"
            st.metric("Custo Hora Parada", chp_txt)
        with c3:
            st.metric("Fator de Encargos", f"{resultados.fator_encargos_usado:.2f}x")

    st.markdown("---")

    # --- ROI por período (1 a 5 anos) ---
    st.subheader("Retorno sobre Investimento")
    col_inv, col_roi = st.columns([1, 2])
    with col_inv:
        st.metric("Investimento Médio", f"R$ {resultados.investimento_medio:,.2f}")
    with col_roi:
        roi_df = pd.DataFrame(
            {
                "Período": ["1 Ano", "2 Anos", "3 Anos", "4 Anos", "5 Anos"],
                "ROI (%)": [
                    f"{resultados.roi_1_ano:.1f}%",
                    f"{resultados.roi_2_anos:.1f}%",
                    f"{resultados.roi_3_anos:.1f}%",
                    f"{resultados.roi_4_anos:.1f}%",
                    f"{resultados.roi_5_anos:.1f}%",
                ],
            }
        )
        st.dataframe(roi_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --- Breakdown por Dor ---
    st.subheader("💸 Custo da Inação por Dor")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("💰 Mão de Obra", f"R$ {resultados.total_dor1:,.2f}")
        _render_breakdown_expander(resultados.breakdown_dor1)

    with col2:
        st.metric("🔍 Qualidade", f"R$ {resultados.total_dor2:,.2f}")
        _render_breakdown_expander(resultados.breakdown_dor2)

    with col3:
        st.metric("📊 Produtividade", f"R$ {resultados.total_dor3:,.2f}")
        _render_breakdown_expander(resultados.breakdown_dor3)

    with col4:
        st.metric("⚠️ Segurança", f"R$ {resultados.total_dor4:,.2f}")
        _render_breakdown_expander(resultados.breakdown_dor4)

    with col5:
        st.metric("🧠 Custos Ocultos", f"R$ {resultados.total_dor5:,.2f}")
        _render_breakdown_expander(resultados.breakdown_dor5)

    st.markdown("---")

    # --- Tabela resumo ---
    st.subheader("Resumo Consolidado")

    total = resultados.custo_total_anual_inacao or 0.0
    df = pd.DataFrame(
        {
            "Dor": [
                "Dor 1 - Mão de Obra",
                "Dor 2 - Qualidade",
                "Dor 3 - Produtividade",
                "Dor 4 - Segurança",
                "Dor 5 - Custos Ocultos",
                "TOTAL",
            ],
            "Custo Atual (R$)": [
                resultados.total_dor1,
                resultados.total_dor2,
                resultados.total_dor3,
                resultados.total_dor4,
                resultados.total_dor5,
                resultados.custo_total_anual_inacao,
            ],
            "% do Total": [
                (resultados.total_dor1 / total * 100) if total else 0.0,
                (resultados.total_dor2 / total * 100) if total else 0.0,
                (resultados.total_dor3 / total * 100) if total else 0.0,
                (resultados.total_dor4 / total * 100) if total else 0.0,
                (resultados.total_dor5 / total * 100) if total else 0.0,
                100.0 if total else 0.0,
            ],
        }
    )

    df["Custo Atual (R$)"] = df["Custo Atual (R$)"].apply(lambda x: f"R$ {x:,.2f}")
    df["% do Total"] = df["% do Total"].apply(lambda x: f"{x:.1f}%")

    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- Detalhamento dos Cálculos ---
    if processo is not None and parametros is not None:
        st.markdown("---")
        st.subheader("📋 Detalhamento dos Cálculos")
        _render_calculo_detalhado(resultados, processo, parametros)


def _render_breakdown_expander(breakdown: dict[str, float]):
    """Renderiza expander com detalhes de um breakdown."""
    itens_ativos = {k: v for k, v in breakdown.items() if v > 0}
    if not itens_ativos:
        return
    with st.expander("Detalhes"):
        for nome, valor in itens_ativos.items():
            st.write(f"**{nome}:** R$ {valor:,.2f}")


def _render_calculo_detalhado(resultados: ResultadosFinanceiros, processo: ProcessoAtual, parametros: ParametrosDetalhados):
    """Renderiza seção de detalhamento linha a linha de cada fórmula ativa."""

    fator = resultados.fator_encargos_usado
    chp = resultados.custo_hora_parada

    detalhes = []

    # --- Dor 1 ---
    v = resultados.breakdown_dor1.get("F01 - Mão de Obra Direta", 0)
    if v > 0:
        n = processo.pessoas_processo_turno * processo.turnos_por_dia
        detalhes.append((
            "F01 - Mão de Obra Direta",
            f"Nº Operadores × Salário × Fator Encargos × 12",
            f"{n} operadores × R$ {processo.salario_medio_operador:,.2f} × {fator:.2f} × 12",
            v,
        ))

    v = resultados.breakdown_dor1.get("F02 - Horas Extras", 0)
    if v > 0 and parametros.f02_media_he_mes_por_pessoa is not None:
        n = processo.pessoas_processo_turno * processo.turnos_por_dia
        custo_hora = (processo.salario_medio_operador * fator) / 176
        detalhes.append((
            "F02 - Horas Extras",
            "Nº Operadores × HE/mês × Custo Hora × 1,5 × 12",
            f"{n} op × {parametros.f02_media_he_mes_por_pessoa:.0f} HE/mês × R$ {custo_hora:,.2f}/h × 1,5 × 12",
            v,
        ))

    v = resultados.breakdown_dor1.get("F03 - Curva de Aprendizagem", 0)
    if v > 0 and parametros.f03_novas_contratacoes_ano is not None:
        detalhes.append((
            "F03 - Curva de Aprendizagem",
            "Nº Contratações × (Custo Novato + Custo Supervisor durante treinamento)",
            f"{parametros.f03_novas_contratacoes_ano} contratações × {parametros.f03_meses_curva or '?'} meses de curva",
            v,
        ))

    v = resultados.breakdown_dor1.get("F04 - Turnover", 0)
    if v > 0 and parametros.f04_desligamentos_ano is not None:
        fator_turnover = parametros.f04_fator_custo_turnover or 1.5
        detalhes.append((
            "F04 - Turnover",
            "Nº Desligamentos × Salário × Fator Turnover",
            f"{parametros.f04_desligamentos_ano} desl. × R$ {processo.salario_medio_operador:,.2f} × {fator_turnover:.1f}x",
            v,
        ))

    # --- Dor 2 ---
    v = resultados.breakdown_dor2.get("F05 - Refugo", 0)
    if v > 0 and parametros.f05_percentual_refugo is not None:
        detalhes.append((
            "F05 - Refugo",
            "Produção Mensal × % Refugo × Custo MP × 12",
            f"× {parametros.f05_percentual_refugo*100:.1f}% refugo × R$ {processo.custo_materia_prima_peca:,.2f}/peça × 12",
            v,
        ))

    v = resultados.breakdown_dor2.get("F05 - Retrabalho", 0)
    if v > 0 and parametros.f05_percentual_retrabalho is not None:
        custo_hora = (processo.salario_medio_operador * fator) / 176
        detalhes.append((
            "F05 - Retrabalho",
            "Produção Mensal × % Retrabalho × Horas Retrab. × Custo Hora × 12",
            f"× {parametros.f05_percentual_retrabalho*100:.1f}% retrab. × {parametros.f05_horas_retrabalho_por_unidade or '?'} h/un × R$ {custo_hora:,.2f}/h × 12",
            v,
        ))

    v = resultados.breakdown_dor2.get("F06 - Inspeção Manual", 0)
    if v > 0:
        n = processo.pessoas_inspecao_turno * processo.turnos_por_dia
        detalhes.append((
            "F06 - Inspeção Manual",
            "Nº Inspetores × Salário × Fator Encargos × 12",
            f"{n} inspetores × R$ {processo.salario_medio_inspetor:,.2f} × {fator:.2f} × 12",
            v,
        ))

    v = resultados.breakdown_dor2.get("F07 - Escapes de Qualidade", 0)
    if v > 0 and parametros.f07_reclamacoes_clientes_ano is not None:
        detalhes.append((
            "F07 - Escapes de Qualidade",
            "Nº Reclamações/Ano × Custo Médio por Reclamação",
            f"{parametros.f07_reclamacoes_clientes_ano} recl. × R$ {parametros.f07_custo_medio_por_reclamacao:,.2f}",
            v,
        ))

    # --- Dor 3 ---
    v = resultados.breakdown_dor3.get("F08 - Custo de Oportunidade", 0)
    if v > 0 and parametros.f08_percentual_demanda_reprimida is not None:
        detalhes.append((
            "F08 - Custo de Oportunidade",
            "Faturamento Mensal × % Demanda Reprimida × Margem Contrib. × 12",
            f"R$ {resultados.faturamento_mensal_linha:,.2f} × {parametros.f08_percentual_demanda_reprimida*100:.0f}% × {parametros.f08_margem_contribuicao*100:.0f}% × 12",
            v,
        ))

    v = resultados.breakdown_dor3.get("F09 - Ociosidade Silenciosa", 0)
    if v > 0 and parametros.f09_minutos_ociosos_por_dia is not None:
        n = processo.pessoas_processo_turno * processo.turnos_por_dia
        custo_hora = (processo.salario_medio_operador * fator) / 176
        detalhes.append((
            "F09 - Ociosidade Silenciosa",
            "Nº Operadores × (Min Ociosos / 60) × Custo Hora × Dias/Ano",
            f"{n} op × ({parametros.f09_minutos_ociosos_por_dia:.0f} min / 60) × R$ {custo_hora:,.2f}/h × {processo.dias_operacao_ano} dias",
            v,
        ))

    v = resultados.breakdown_dor3.get("F10 - Paradas de Linha", 0)
    if v > 0 and parametros.f10_paradas_mes is not None:
        chp_usado = parametros.f10_custo_hora_parada if (parametros.f10_custo_hora_parada and parametros.f10_custo_hora_parada > 0) else chp
        detalhes.append((
            "F10 - Paradas de Linha",
            "Nº Paradas/Mês × Duração (h) × Custo Hora Parada × 12",
            f"{parametros.f10_paradas_mes} paradas × {parametros.f10_duracao_media_parada_horas:.1f} h × R$ {chp_usado:,.2f}/h × 12",
            v,
        ))

    v = resultados.breakdown_dor3.get("F11 - Setup/Changeover", 0)
    if v > 0 and parametros.f11_setups_mes is not None:
        chp_usado = parametros.f11_custo_hora_parada if (parametros.f11_custo_hora_parada and parametros.f11_custo_hora_parada > 0) else chp
        detalhes.append((
            "F11 - Setup/Changeover",
            "Nº Setups/Mês × Horas/Setup × Custo Hora Parada × 12",
            f"{parametros.f11_setups_mes} setups × {parametros.f11_horas_por_setup:.2f} h × R$ {chp_usado:,.2f}/h × 12",
            v,
        ))

    # --- Dor 4 ---
    v_afast = resultados.breakdown_dor4.get("F12 - Afastamentos", 0)
    v_acid = resultados.breakdown_dor4.get("F12 - Acidentes", 0)
    v_legal = resultados.breakdown_dor4.get("F12 - Risco Legal", 0)
    if (v_afast + v_acid + v_legal) > 0 and parametros.f12_afastamentos_ano is not None:
        detalhes.append((
            "F12 - Riscos, Acidentes e Doenças",
            "Afastamentos + Acidentes + Risco Legal",
            f"{parametros.f12_afastamentos_ano} afast. × R$ {parametros.f12_custo_medio_afastamento:,.2f}  |  "
            f"{parametros.f12_acidentes_com_lesao_ano} acid. × R$ {parametros.f12_custo_medio_acidente:,.2f}  |  "
            f"{(parametros.f12_probabilidade_processo or 0)*100:.0f}% × R$ {parametros.f12_custo_estimado_processo:,.2f}",
            v_afast + v_acid + v_legal,
        ))

    v = resultados.breakdown_dor4.get("F13 - Frota de Empilhadeiras", 0)
    if v > 0 and parametros.f13_num_empilhadeiras is not None:
        detalhes.append((
            "F13 - Frota de Empilhadeiras",
            "Nº Empilhadeiras × (Operador + Equipamento + Energia + Manutenção) × 12",
            f"{parametros.f13_num_empilhadeiras} emp. × (op + equip + energ + manut) × 12",
            v,
        ))

    # --- Dor 5 ---
    v = resultados.breakdown_dor5.get("F14 - Supervisão", 0)
    if v > 0 and parametros.f14_num_supervisores is not None:
        n_total = parametros.f14_num_supervisores * processo.turnos_por_dia
        sal = parametros.f14_salario_supervisor or processo.salario_medio_supervisor
        detalhes.append((
            "F14 - Supervisão",
            "Nº Supervisores (total turnos) × Salário × Fator Encargos × 12",
            f"{n_total} sup. ({parametros.f14_num_supervisores}/turno × {processo.turnos_por_dia} turnos) × R$ {sal:,.2f} × {fator:.2f} × 12",
            v,
        ))

    v = resultados.breakdown_dor5.get("F15 - Compliance/EPIs", 0)
    if v > 0 and parametros.f15_custo_epi_ano_por_pessoa is not None:
        n = processo.pessoas_processo_turno * processo.turnos_por_dia
        detalhes.append((
            "F15 - Compliance/EPIs",
            "Nº Operadores × (Custo EPI/Ano + Custo Exames/Ano)",
            f"{n} op × (R$ {parametros.f15_custo_epi_ano_por_pessoa:,.2f} EPI + R$ {parametros.f15_custo_exames_ano_por_pessoa:,.2f} exames)",
            v,
        ))

    v = resultados.breakdown_dor5.get("F16 - Energia e Utilidades", 0)
    if v > 0 and parametros.f16_area_operacao_m2 is not None:
        detalhes.append((
            "F16 - Energia e Utilidades",
            "Área (m²) × Custo Energia/m²/Ano",
            f"{parametros.f16_area_operacao_m2:,.0f} m² × R$ {parametros.f16_custo_energia_m2_ano:,.2f}/m²/ano",
            v,
        ))

    v = resultados.breakdown_dor5.get("F17 - Espaço Físico", 0)
    if v > 0 and parametros.f17_area_m2 is not None:
        pct = (parametros.f17_percentual_reducao_automacao or 0) * 100
        detalhes.append((
            "F17 - Espaço Físico",
            "Área (m²) × Custo m²/Ano × % Redução com Automação",
            f"{parametros.f17_area_m2:,.0f} m² × R$ {parametros.f17_custo_m2_ano:,.2f}/m²/ano × {pct:.0f}%",
            v,
        ))

    v = resultados.breakdown_dor5.get("F18 - Gestão de Dados", 0)
    if v > 0 and parametros.f18_pessoas_envolvidas is not None:
        custo_hora = (processo.salario_medio_operador * fator) / 176
        detalhes.append((
            "F18 - Gestão de Dados",
            "Nº Pessoas × Horas/Dia × Custo Hora × Dias/Ano",
            f"{parametros.f18_pessoas_envolvidas} pessoas × {parametros.f18_horas_dia_tarefas_dados:.1f} h/dia × R$ {custo_hora:,.2f}/h × {processo.dias_operacao_ano} dias",
            v,
        ))

    if not detalhes:
        st.info("Nenhum cálculo ativo para detalhar.")
        return

    for formula, formula_txt, inputs_txt, resultado in detalhes:
        with st.expander(f"{formula} — R$ {resultado:,.2f}"):
            st.markdown(f"**Fórmula:** `{formula_txt}`")
            st.markdown(f"**Cálculo:** {inputs_txt}")
            st.markdown(f"**Resultado Anual:** R$ {resultado:,.2f}")
