"""
Mapeamento das 6 Áreas de Atuação ARV → Fórmulas aplicáveis.

Usado para pré-selecionar fórmulas na UI com base na área escolhida.
"""

AREAS_ARV: dict[str, dict] = {
    "area_1_linhas_montagem": {
        "nome": "🔧 Linhas de Montagem Automáticas",
        "descricao": "Automação de linhas de montagem industriais",
        "formulas_aplicaveis": [
            "F01",
            "F02",
            "F03",
            "F04",  # Dor 1: Mão de Obra
            "F05",
            "F06",
            "F07",  # Dor 2: Qualidade
            "F08",
            "F09",
            "F10",
            "F11",  # Dor 3: Produtividade
            "F12",  # Dor 4: Segurança
            "F14",
            "F15",
            "F16",
            "F17",
            "F18",  # Dor 5: Custos Ocultos
        ],
    },
    "area_2_maquinas_especiais": {
        "nome": "⚙️ Soluções em Máquinas Especiais",
        "descricao": "Máquinas customizadas para tarefas únicas",
        "formulas_aplicaveis": [
            "F01",
            "F03",
            "F14",  # Dependência de Especialista
            "F11",
            "F08",  # Flexibilidade/Agilidade
            "F05",
            "F07",  # Qualidade
            "F10",  # Gargalo de Produção
        ],
    },
    "area_3_controle_qualidade": {
        "nome": "🔍 Controle de Qualidade Automatizado",
        "descricao": "Sistemas de visão e inspeção automatizada",
        "formulas_aplicaveis": [
            "F06",
            "F14",  # Inspeção Manual / Supervisão
            "F07",  # Escapes de Qualidade
            "F05",  # Refugo/Retrabalho
            "F18",  # Gestão de Dados
        ],
    },
    "area_4_embalagem": {
        "nome": "📦 Automação de Embalagem (Fim de Linha)",
        "descricao": "Encaixotamento, paletização, stretch wrapping",
        "formulas_aplicaveis": [
            "F08",
            "F02",  # Gargalo na Expedição / HE
            "F01",
            "F04",
            "F03",  # Mão de Obra/Rotatividade
            "F12",
            "F15",  # Segurança/Ergonomia
            "F07",
            "F18",  # Erros/Dados
        ],
    },
    "area_5_logistica_interna": {
        "nome": "🚚 Automação de Logística Interna",
        "descricao": "AGVs/AMRs, substituição de empilhadeiras",
        "formulas_aplicaveis": [
            "F13",  # Frota de Empilhadeiras (específica)
            "F09",
            "F10",
            "F08",
            "F12",  # Reutilizáveis
        ],
    },
    "area_6_robotica": {
        "nome": "🤖 Soluções Robóticas Customizadas",
        "descricao": "Processos perigosos, insalubres ou alta precisão",
        "formulas_aplicaveis": [
            "F12",
            "F15",  # Processos Perigosos
            "F01",
            "F03",
            "F04",  # Dependência de Especialista
            "F05",
            "F07",  # Qualidade Alto Valor
            "F08",  # Escalar Produção
        ],
    },
}

