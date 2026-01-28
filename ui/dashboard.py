"""
Dashboard de resultados financeiros.
"""
import streamlit as st
import pandas as pd

from models.results import ResultadosFinanceiros


def render_dashboard(resultados: ResultadosFinanceiros):
    """Renderiza dashboard completo de resultados."""
    st.header("Análise de Viabilidade Financeira")
    st.markdown("---")

    # --- Métricas Principais ---
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Custo Total Anual", f"R$ {resultados.custo_total_anual:,.2f}")
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

    st.markdown("---")

    # --- Breakdown por categoria ---
    st.subheader("Breakdown de Custos por Categoria")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("CO - Operacional", f"R$ {resultados.total_co:,.2f}")
        _render_breakdown_expander(resultados.breakdown_co)

    with col2:
        st.metric("QL - Qualidade", f"R$ {resultados.total_ql:,.2f}")
        _render_breakdown_expander(resultados.breakdown_ql)

    with col3:
        st.metric("SE - Segurança", f"R$ {resultados.total_se:,.2f}")
        _render_breakdown_expander(resultados.breakdown_se)

    with col4:
        st.metric("PR - Produtividade", f"R$ {resultados.total_pr:,.2f}")
        _render_breakdown_expander(resultados.breakdown_pr)

    st.markdown("---")

    # --- Tabela resumo ---
    st.subheader("Resumo Consolidado")

    df = pd.DataFrame({
        "Categoria": ["CO - Operacional", "QL - Qualidade",
                       "SE - Segurança", "PR - Produtividade", "TOTAL"],
        "Custo Atual (R$)": [
            resultados.total_co, resultados.total_ql,
            resultados.total_se, resultados.total_pr,
            resultados.custo_total_anual,
        ],
        "Ganho Potencial (R$)": [
            _soma_breakdown_ganho(resultados.breakdown_co),
            _soma_breakdown_ganho(resultados.breakdown_ql),
            _soma_breakdown_ganho(resultados.breakdown_se),
            _soma_breakdown_ganho(resultados.breakdown_pr),
            resultados.ganho_anual_potencial,
        ],
    })

    df["Custo Atual (R$)"] = df["Custo Atual (R$)"].apply(lambda x: f"R$ {x:,.2f}")
    df["Ganho Potencial (R$)"] = df["Ganho Potencial (R$)"].apply(lambda x: f"R$ {x:,.2f}")

    st.dataframe(df, use_container_width=True, hide_index=True)


def _render_breakdown_expander(breakdown: dict[str, float]):
    """Renderiza expander com detalhes de um breakdown."""
    itens_ativos = {k: v for k, v in breakdown.items() if v > 0}
    if not itens_ativos:
        return
    with st.expander("Detalhes"):
        for nome, valor in itens_ativos.items():
            st.write(f"**{nome}:** R$ {valor:,.2f}")


def _soma_breakdown_ganho(breakdown: dict[str, float]) -> float:
    """Soma valores do breakdown (usado como proxy de ganho por categoria)."""
    return sum(breakdown.values())
