"""
CSS customizado para a aplicação Streamlit.
"""
import streamlit as st


def apply_custom_styles():
    """Aplica estilos CSS customizados."""
    st.markdown(
        """
        <style>
        /* Métricas mais destacadas */
        [data-testid="stMetricValue"] {
            font-size: 1.3rem;
            font-weight: 700;
        }

        /* Header principal */
        .main h1 {
            color: #1f4e79;
        }

        /* Expanders mais limpos */
        .streamlit-expanderHeader {
            font-weight: 600;
        }

        /* Tabela resumo */
        [data-testid="stDataFrame"] {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
        }

        /* Botão primário */
        .stButton > button[kind="primary"] {
            background-color: #1f4e79;
            border: none;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #163a5c;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
