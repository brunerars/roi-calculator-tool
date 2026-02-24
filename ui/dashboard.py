"""
Dashboard de resultados financeiros.
"""
import streamlit as st
import pandas as pd

from models.results import ResultadosFinanceiros


def render_dashboard(resultados: ResultadosFinanceiros):
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
        st.metric("ROI 3 Anos", f"{resultados.roi_3_anos:.1f}%")

    st.markdown("---")

    # --- ROI por período ---
    st.subheader("Retorno sobre Investimento")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Investimento Médio", f"R$ {resultados.investimento_medio:,.2f}")
    with col2:
        st.metric("ROI 1 Ano", f"{resultados.roi_1_ano:.1f}%")
    with col3:
        st.metric("ROI 3 Anos", f"{resultados.roi_3_anos:.1f}%")
    with col4:
        st.metric("ROI 5 Anos", f"{resultados.roi_5_anos:.1f}%")

    st.caption(
        f"Área ARV: {resultados.area_atuacao} • Porte: {resultados.porte_empresa} • "
        f"Encargos: {resultados.fator_encargos_usado:.2f}x"
    )

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


def _render_breakdown_expander(breakdown: dict[str, float]):
    """Renderiza expander com detalhes de um breakdown."""
    itens_ativos = {k: v for k, v in breakdown.items() if v > 0}
    if not itens_ativos:
        return
    with st.expander("Detalhes"):
        for nome, valor in itens_ativos.items():
            st.write(f"**{nome}:** R$ {valor:,.2f}")
