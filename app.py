"""
ROI Calculator - MVP
Ferramenta web para acelerar propostas comerciais de projetos de automação industrial.
"""
import streamlit as st

from ui.styles import apply_custom_styles
from ui.forms import (
    render_dados_basicos,
    render_selecao_dores,
    render_parametros_detalhados,
    render_metas_reducao,
    render_investimento,
)
from ui.dashboard import render_dashboard
from core.calculator import ROICalculator
from core.validators import validar_processo_atual, validar_investimento
from export.pptx_generator import PPTXGenerator

st.set_page_config(
    page_title="ROI Calculator - Automação Industrial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_custom_styles()

TOTAL_ETAPAS = 7


def _init_state():
    """Inicializa session_state se necessário."""
    if "etapa" not in st.session_state:
        st.session_state["etapa"] = 0


def _nav_buttons(etapa: int):
    """Renderiza botões de navegação."""
    col1, _, col3 = st.columns([1, 2, 1])

    with col1:
        if etapa > 1:
            if st.button("← Voltar", key=f"voltar_{etapa}"):
                st.session_state["etapa"] = etapa - 1
                st.rerun()

    with col3:
        if etapa < TOTAL_ETAPAS:
            if st.button("Próximo →", key=f"proximo_{etapa}", type="primary"):
                st.session_state["etapa"] = etapa + 1
                st.rerun()


def _render_progress(etapa: int):
    """Renderiza barra de progresso."""
    nomes = [
        "Dados Básicos", "Dores", "Parâmetros",
        "Metas", "Investimento", "Resultados", "Exportar",
    ]
    st.progress(etapa / TOTAL_ETAPAS)
    st.caption(f"Etapa {etapa}/{TOTAL_ETAPAS} — {nomes[etapa - 1]}")


def main():
    _init_state()
    etapa = st.session_state["etapa"]

    # --- Tela Inicial ---
    if etapa == 0:
        st.title("📊 ROI Calculator")
        st.subheader("Análise de Viabilidade Financeira para Automação Industrial")
        st.markdown("---")
        st.markdown(
            """
            Quantifique rapidamente o retorno sobre investimento (ROI) de projetos
            de automação industrial.

            **Fluxo da análise:**
            1. Informações do cliente e processo atual
            2. Seleção das dores aplicáveis
            3. Parâmetros detalhados
            4. Metas de redução de custos
            5. Investimento da automação
            6. Dashboard de resultados
            7. Geração de apresentação PPTX
            """
        )
        if st.button("Nova Análise", type="primary", use_container_width=True):
            st.session_state["etapa"] = 1
            st.rerun()
        return

    # --- Etapas do fluxo ---
    st.title("📊 ROI Calculator")
    _render_progress(etapa)
    st.markdown("---")

    # Etapa 1: Dados Básicos
    if etapa == 1:
        cliente, processo = render_dados_basicos()
        erros = validar_processo_atual(processo)
        if erros:
            for e in erros:
                st.error(e)
        else:
            st.session_state["cliente"] = cliente
            st.session_state["processo"] = processo
        _nav_buttons(etapa)

    # Etapa 2: Seleção de Dores
    elif etapa == 2:
        dores = render_selecao_dores()
        st.session_state["dores"] = dores
        _nav_buttons(etapa)

    # Etapa 3: Parâmetros Detalhados
    elif etapa == 3:
        dores = st.session_state.get("dores")
        if dores is None:
            st.warning("Volte à etapa 2 e selecione as dores.")
        else:
            parametros = render_parametros_detalhados(dores)
            st.session_state["parametros"] = parametros
        _nav_buttons(etapa)

    # Etapa 4: Metas de Redução
    elif etapa == 4:
        dores = st.session_state.get("dores")
        if dores is None:
            st.warning("Volte à etapa 2 e selecione as dores.")
        else:
            metas = render_metas_reducao(dores)
            st.session_state["metas"] = metas
        _nav_buttons(etapa)

    # Etapa 5: Investimento
    elif etapa == 5:
        investimento = render_investimento()
        erros = validar_investimento(investimento)
        if erros:
            for e in erros:
                st.error(e)
        else:
            st.session_state["investimento"] = investimento
        _nav_buttons(etapa)

    # Etapa 6: Dashboard de Resultados
    elif etapa == 6:
        _run_calculo_e_dashboard()
        _nav_buttons(etapa)

    # Etapa 7: Exportar PPTX
    elif etapa == 7:
        _render_exportar()
        _nav_buttons(etapa)


def _render_exportar():
    """Renderiza etapa de exportação do PPTX."""
    st.header("7 - Exportar Apresentação")

    required_keys = ["cliente", "processo", "dores", "resultados", "metas", "investimento"]
    missing = [k for k in required_keys if k not in st.session_state]

    if missing:
        st.warning("Dados incompletos. Volte e preencha todas as etapas anteriores.")
        return

    st.success("Apresentação pronta para ser gerada com 16 slides customizados.")

    if st.button("Gerar Apresentação PPTX", type="primary", use_container_width=True):
        with st.spinner("Gerando apresentação..."):
            try:
                gen = PPTXGenerator()
                buffer = gen.gerar(
                    cliente=st.session_state["cliente"],
                    processo=st.session_state["processo"],
                    dores=st.session_state["dores"],
                    resultados=st.session_state["resultados"],
                    metas=st.session_state["metas"],
                    investimento=st.session_state["investimento"],
                )
                st.session_state["pptx_buffer"] = buffer
            except Exception as e:
                st.error(f"Erro ao gerar apresentação: {e}")

    if "pptx_buffer" in st.session_state:
        nome_cliente = st.session_state["cliente"].nome_cliente or "cliente"
        nome_arquivo = f"analise_{nome_cliente.replace(' ', '_')}.pptx"
        st.download_button(
            label="Baixar Apresentação (.pptx)",
            data=st.session_state["pptx_buffer"],
            file_name=nome_arquivo,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True,
        )


def _run_calculo_e_dashboard():
    """Executa o cálculo e renderiza o dashboard."""
    required_keys = ["processo", "dores", "parametros", "investimento", "metas"]
    missing = [k for k in required_keys if k not in st.session_state]

    if missing:
        st.warning("Dados incompletos. Volte e preencha todas as etapas anteriores.")
        return

    try:
        calc = ROICalculator(
            processo=st.session_state["processo"],
            dores=st.session_state["dores"],
            parametros=st.session_state["parametros"],
            investimento=st.session_state["investimento"],
            metas=st.session_state["metas"],
        )

        resultados = calc.calcular()
        st.session_state["resultados"] = resultados
        render_dashboard(resultados)
    except Exception as e:
        st.error(f"Erro no cálculo: {e}")


if __name__ == "__main__":
    main()
