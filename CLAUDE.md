# ROI CALCULATOR - CUSTO DA INAÇÃO V2.0

## 📋 VISÃO GERAL

Ferramenta web para acelerar propostas comerciais de projetos de automação industrial, quantificando o **Custo da Inação** e gerando apresentações customizadas para decisores (CEOs, CFOs, COOs).

**Conceito Central:** "Quanto custa NÃO automatizar?" — O Custo da Inação é um passivo estratégico, um sangramento contínuo no fluxo de caixa que a empresa financia diariamente ao manter processos manuais.

**Problema:** Vendedores perdem dias criando propostas técnico-financeiras para projetos CAPEX
**Solução:** Input de dados → Motor de Cálculo V2.0 (18 fórmulas) → Dashboard + PPTX customizado em minutos
**Impacto:** Reduzir tempo de proposta de dias para minutos, aumentar taxa de conversão CAPEX

---

## 🎯 OBJETIVOS DO MVP

### Funcionalidades Core
1. ✅ Formulário web para input de dados do cliente
2. ✅ Motor de cálculo V2.0 — **18 fórmulas** organizadas por **5 Dores** e **6 Áreas de Atuação ARV**
3. ✅ Dashboard com resultados (Payback, ROI 1/3/5 anos, breakdown por Dor)
4. ✅ Geração de PPTX customizado (16+ slides)
5. ✅ Download do arquivo gerado
6. ✅ Seleção da Área de Atuação ARV (sugere fórmulas relevantes)

### Fora do Escopo (MVP)
- ❌ Autenticação de usuários
- ❌ Persistência de dados (banco de dados)
- ❌ Versionamento de projetos
- ❌ Compartilhamento por link
- ❌ Edição colaborativa

---

## 🛠️ STACK TÉCNICA

### Core
- **Frontend + Backend:** Streamlit 1.30+
- **Geração PPTX:** python-pptx 0.6+
- **Linguagem:** Python 3.10+
- **Deploy:** Streamlit Cloud (gratuito)

### Bibliotecas Auxiliares
```python
streamlit>=1.30.0
python-pptx>=0.6.21
pandas>=2.0.0
```

---

## 📁 ARQUITETURA E ESTRUTURA DE PASTAS

```
roi-calculator/
├── app.py                          # Entry point Streamlit
├── requirements.txt                # Dependências
├── README.md                       # Documentação do projeto
├── .gitignore                      # Git ignore
│
├── config/
│   ├── __init__.py
│   ├── constants.py                # Constantes V2.0 (encargos, divisores)
│   └── areas.py                    # Mapeamento Áreas ARV → Fórmulas
│
├── models/
│   ├── __init__.py
│   ├── inputs.py                   # Schemas de entrada (V2.0)
│   ├── calculations.py             # Models de cálculo (18 fórmulas)
│   └── results.py                  # Schemas de resultado
│
├── core/
│   ├── __init__.py
│   ├── calculator.py               # Motor de cálculo principal V2.0
│   ├── formulas.py                 # 18 Fórmulas detalhadas (F01-F18)
│   └── validators.py               # Validações de input
│
├── ui/
│   ├── __init__.py
│   ├── forms.py                    # Formulários Streamlit (V2.0)
│   ├── dashboard.py                # Dashboard de resultados
│   └── styles.py                   # CSS customizado
│
├── export/
│   ├── __init__.py
│   ├── pptx_generator.py           # Gerador de PPTX
│   └── template.pptx               # Template base do PowerPoint
│
└── tests/
    ├── __init__.py
    ├── test_calculations.py        # Testes unitários
    └── test_formulas.py            # Testes de fórmulas (F01-F18)
```

---

## ⚙️ PRINCÍPIOS DE CUSTEIO REAL (Regras Base para CFOs)

Estes princípios sustentam TODOS os cálculos. São premissas financeiras defensáveis.

### Regra #1: Fator de Encargos Trabalhistas (REVISADO)

Não usar fator fixo simplificado. O sistema deve permitir seleção do fator:

| Fator | Descrição | Uso |
|-------|-----------|-----|
| **1,7** (Conservador) | INSS, FGTS, 13º, Férias+1/3, SAT/RAT | **PADRÃO do sistema** — Lucro Real/Presumido |
| **1,85** (Médio) | + Vale-transporte, Vale-refeição | Opcional |
| **2,0** (Completo) | + Plano de saúde, Seguro de vida | Opcional |

**Exemplo:** Operador com salário R$ 2.500 → Custo real: R$ 2.500 × 1,7 = **R$ 4.250/mês**

```python
# Custo Total do Colaborador = Salário Bruto × Fator de Encargos
FATOR_ENCARGOS_CONSERVADOR = 1.7   # PADRÃO
FATOR_ENCARGOS_MEDIO = 1.85
FATOR_ENCARGOS_COMPLETO = 2.0
```

### Regra #2: Divisor de Horas do Operador (REVISADO)

- **176 horas** → Divisor para custo da hora do operador (44h/semana × 4 semanas)
- **220 horas** → Manter APENAS para cálculo de horas extras (conforme CLT)

```python
# Custo da Hora do Operador = (Salário Bruto × Fator de Encargos) ÷ 176 horas
HORAS_MES_CUSTO_PRODUCAO = 176  # Para custo hora do operador
HORAS_MES_CLT = 220              # Para cálculo de horas extras (CLT)
```

### Regra #3: Custo da Hora Parada (Custo de Oportunidade)

O custo de uma hora de inatividade = faturamento que DEIXOU de ser gerado (não apenas salários).

```python
# Custo da Hora Parada = Faturamento Mensal da Linha ÷ 176 horas úteis
# Este valor é INPUT do usuário (varia por cliente/linha)
```

---

## 📊 MODELS E SCHEMAS

### 1. config/constants.py

```python
"""
Parâmetros ARV V2.0 (constantes do sistema)
Baseado no documento "Custo da Inação V2.0 Revisado"
"""

# === REGRA #1: Fatores de Encargos Trabalhistas ===
FATOR_ENCARGOS_CONSERVADOR = 1.7   # Lucro Real/Presumido (PADRÃO)
FATOR_ENCARGOS_MEDIO = 1.85        # + VT, VR
FATOR_ENCARGOS_COMPLETO = 2.0      # + Plano saúde, seguro vida

FATOR_ENCARGOS_OPCOES = {
    "Conservador (1,7x) - Encargos obrigatórios": 1.7,
    "Médio (1,85x) - + VT/VR": 1.85,
    "Completo (2,0x) - + Saúde/Seguro": 2.0,
}

# === REGRA #2: Divisores de Horas ===
HORAS_MES_CUSTO_PRODUCAO = 176  # 44h/semana × 4 semanas (custo hora operador)
HORAS_MES_CLT = 220              # Para cálculos de hora extra (CLT)

# === Fatores de Cálculo ===
FATOR_ADICIONAL_HORA_EXTRA = 1.5  # Adicional de 50% sobre hora normal
FATOR_CUSTO_TURNOVER = 1.5        # Benchmark conservador (1,5x a 3,0x salário)

# === Defaults de Input (sugestões para o formulário) ===
SALARIO_OPERADOR_DEFAULT = 2500   # R$ - Salário bruto médio operador
SALARIO_INSPETOR_DEFAULT = 3000   # R$
SALARIO_SUPERVISOR_DEFAULT = 5000 # R$
DIAS_OPERACAO_ANO_DEFAULT = 250   # dias
```

### 2. config/areas.py

```python
"""
Mapeamento das 6 Áreas de Atuação ARV → Fórmulas aplicáveis
Permite sugerir fórmulas relevantes com base na área selecionada
"""

AREAS_ARV = {
    "area_1_linhas_montagem": {
        "nome": "🔧 Linhas de Montagem Automáticas",
        "descricao": "Automação de linhas de montagem industriais",
        "formulas_aplicaveis": [
            "F01", "F02", "F03", "F04",  # Dor 1: Mão de Obra
            "F05", "F06", "F07",          # Dor 2: Qualidade
            "F08", "F09", "F10", "F11",   # Dor 3: Produtividade
            "F12",                         # Dor 4: Segurança
            "F14", "F15", "F16", "F17", "F18",  # Dor 5: Custos Ocultos
        ],
    },
    "area_2_maquinas_especiais": {
        "nome": "⚙️ Soluções em Máquinas Especiais",
        "descricao": "Máquinas customizadas para tarefas únicas",
        "formulas_aplicaveis": [
            "F01", "F03", "F14",  # Dependência de Especialista
            "F11", "F08",         # Flexibilidade/Agilidade
            "F05", "F07",         # Qualidade
            "F10",                # Gargalo de Produção
        ],
    },
    "area_3_controle_qualidade": {
        "nome": "🔍 Controle de Qualidade Automatizado",
        "descricao": "Sistemas de visão e inspeção automatizada",
        "formulas_aplicaveis": [
            "F06", "F14",  # Inspeção Manual
            "F07",         # Escapes de Qualidade
            "F05",         # Refugo/Retrabalho
            "F18",         # Gestão de Dados
        ],
    },
    "area_4_embalagem": {
        "nome": "📦 Automação de Embalagem (Fim de Linha)",
        "descricao": "Encaixotamento, paletização, stretch wrapping",
        "formulas_aplicaveis": [
            "F08", "F02",         # Gargalo na Expedição
            "F01", "F04", "F03",  # Mão de Obra/Rotatividade
            "F12", "F15",         # Segurança/Ergonomia
            "F07", "F18",         # Erros/Dados
        ],
    },
    "area_5_logistica_interna": {
        "nome": "🚚 Automação de Logística Interna",
        "descricao": "AGVs/AMRs, substituição de empilhadeiras",
        "formulas_aplicaveis": [
            "F13",                         # Frota de Empilhadeiras (específica)
            "F09", "F10", "F08", "F12",    # Reutilizáveis
        ],
    },
    "area_6_robotica": {
        "nome": "🤖 Soluções Robóticas Customizadas",
        "descricao": "Processos perigosos, insalubres ou alta precisão",
        "formulas_aplicaveis": [
            "F12", "F15",         # Processos Perigosos
            "F01", "F03", "F04",  # Dependência de Especialista
            "F05", "F07",         # Qualidade Alto Valor
            "F08",                # Escalar Produção
        ],
    },
}
```

### 3. models/inputs.py

```python
"""
Schemas de entrada de dados do cliente — V2.0
"""
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class ClienteBasicInfo:
    """Informações básicas do cliente"""
    nome_cliente: str
    nome_projeto: str
    area_atuacao: str  # Chave de AREAS_ARV (ex: "area_1_linhas_montagem")
    porte_empresa: str  # "pequena", "media", "grande"
    fator_encargos: float = 1.7  # Selecionável: 1.7 / 1.85 / 2.0

@dataclass
class ProcessoAtual:
    """Dados do processo atual do cliente"""
    # Produção
    cadencia_producao: float  # peças/min (ou produção mensal direta)
    producao_mensal: Optional[float] = None  # peças/mês (alternativa à cadência)
    horas_por_turno: float = 8.0  # h
    turnos_por_dia: int = 2  # turnos
    dias_operacao_ano: int = 250  # dias
    
    # Pessoas
    pessoas_processo_turno: int = 5  # operadores por turno
    pessoas_inspecao_turno: int = 1  # inspetores por turno
    pessoas_supervisao_turno: int = 0  # supervisores por turno (usado em F14)
    
    # Custos unitários
    salario_medio_operador: float = 2500.0  # R$ bruto
    salario_medio_inspetor: float = 3000.0  # R$ bruto
    salario_medio_supervisor: float = 5000.0  # R$ bruto
    custo_unitario_peca: float = 100.0  # R$
    custo_materia_prima_peca: float = 15.0  # R$ (custo MP direto por unidade)
    preco_venda_peca: float = 0.0  # R$ (preço de venda — usado para calcular faturamento)
    
    # Financeiro da linha
    # ⚠️ FATURAMENTO: Calcular automaticamente a partir dos inputs de produção:
    #   Faturamento Mensal = Cadência × 60 × Horas/turno × Turnos × (Dias/ano ÷ 12) × Preço Venda/peça
    # O usuário pode sobrescrever manualmente se preferir.
    # Se preco_venda_peca > 0, o sistema DEVE calcular e pré-preencher o faturamento.
    # Se ambos forem 0, exibir warning: "F08, F10 e F11 ficarão zeradas sem faturamento."
    faturamento_mensal_linha: Optional[float] = None  # R$ (auto-calculado ou override manual)

@dataclass
class DoresSelecionadas:
    """
    Dores/fórmulas selecionadas pelo usuário — V2.0
    Reorganizado por 5 Dores (em vez de 4 categorias CO/QL/SE/PR)
    Cada flag mapeia para uma fórmula F01-F18
    """
    # DOR 1: CUSTO ELEVADO DE MÃO DE OBRA
    f01_mao_de_obra_direta: bool = False
    f02_horas_extras: bool = False
    f03_curva_aprendizagem: bool = False
    f04_turnover: bool = False
    
    # DOR 2: BAIXA QUALIDADE
    f05_refugo_retrabalho: bool = False
    f06_inspecao_manual: bool = False
    f07_escapes_qualidade: bool = False
    
    # DOR 3: BAIXA PRODUTIVIDADE
    f08_custo_oportunidade: bool = False
    f09_ociosidade_silenciosa: bool = False
    f10_paradas_linha: bool = False
    f11_setup_changeover: bool = False
    
    # DOR 4: FALTA DE SEGURANÇA E ERGONOMIA
    f12_riscos_acidentes: bool = False
    f13_frota_empilhadeiras: bool = False  # Específica Área 5
    
    # DOR 5: CUSTOS OCULTOS DE GESTÃO E ESTRUTURA
    f14_supervisao: bool = False
    f15_compliance_epis: bool = False
    f16_energia_utilidades: bool = False
    f17_espaco_fisico: bool = False
    f18_gestao_dados: bool = False

@dataclass
class ParametrosDetalhados:
    """
    Parâmetros detalhados para cada fórmula — V2.0
    Campos condicionais: só exibir se a fórmula estiver selecionada
    """
    # F01 - Mão de Obra Direta (usa dados de ProcessoAtual, sem params extras)
    
    # F02 - Horas Extras
    f02_media_he_mes_por_pessoa: Optional[float] = None  # horas extras/mês/pessoa
    
    # F03 - Curva de Aprendizagem
    f03_novas_contratacoes_ano: Optional[int] = None
    f03_salario_novato: Optional[float] = None  # R$
    f03_meses_curva: Optional[int] = None  # meses até produtividade plena
    f03_salario_supervisor: Optional[float] = None  # R$ (supervisor que treina)
    f03_percentual_tempo_supervisor: Optional[float] = None  # % do tempo dedicado
    
    # F04 - Turnover
    f04_desligamentos_ano: Optional[int] = None
    f04_fator_custo_turnover: Optional[float] = 1.5  # 1,5 a 3,0 (benchmark)
    
    # F05 - Refugo e Retrabalho (SEPARADOS na V2.0)
    f05_percentual_refugo: Optional[float] = None  # %
    f05_percentual_retrabalho: Optional[float] = None  # %
    f05_horas_retrabalho_por_unidade: Optional[float] = None  # h
    
    # F06 - Inspeção Manual (usa dados de ProcessoAtual: inspetores, salário)
    
    # F07 - Escapes de Qualidade
    f07_reclamacoes_clientes_ano: Optional[int] = None
    f07_custo_medio_por_reclamacao: Optional[float] = None  # R$ (realista, não R$300)
    
    # F08 - Custo de Oportunidade
    f08_percentual_demanda_reprimida: Optional[float] = None  # %
    f08_margem_contribuicao: Optional[float] = None  # %
    
    # F09 - Ociosidade Silenciosa
    f09_minutos_ociosos_por_dia: Optional[float] = None  # min
    
    # F10 - Paradas de Linha
    f10_paradas_mes: Optional[int] = None
    f10_duracao_media_parada_horas: Optional[float] = None  # h
    f10_custo_hora_parada: Optional[float] = None  # R$ (Regra #3)
    
    # F11 - Setup/Changeover
    f11_setups_mes: Optional[int] = None
    f11_horas_por_setup: Optional[float] = None  # h
    f11_custo_hora_parada: Optional[float] = None  # R$ (Regra #3)
    
    # F12 - Riscos, Acidentes e Doenças (V2.0: 3 componentes)
    f12_afastamentos_ano: Optional[int] = None
    f12_custo_medio_afastamento: Optional[float] = None  # R$
    f12_acidentes_com_lesao_ano: Optional[int] = None
    f12_custo_medio_acidente: Optional[float] = None  # R$
    f12_probabilidade_processo: Optional[float] = None  # % (0.05 = 5%)
    f12_custo_estimado_processo: Optional[float] = None  # R$
    
    # F13 - Frota de Empilhadeiras (V2.0: TCO completo)
    f13_num_empilhadeiras: Optional[int] = None
    f13_custo_operador_mes: Optional[float] = None  # R$ (salário + encargos)
    f13_custo_equipamento_mes: Optional[float] = None  # R$ (aluguel/depreciação)
    f13_custo_energia_mes: Optional[float] = None  # R$
    f13_custo_manutencao_mes: Optional[float] = None  # R$
    
    # F14 - Supervisão (NOVA)
    # ⚠️ Nº de supervisores vem de ProcessoAtual.pessoas_supervisao_turno × turnos_dia
    # Se F14 for selecionada e supervisores_turno = 0, EXIGIR preenchimento.
    # Isso evita inconsistência entre o input do processo e o cálculo.
    f14_salario_supervisor: Optional[float] = None  # R$ (default: ProcessoAtual.salario_medio_supervisor)
    
    # F15 - Compliance/EPIs (NOVA)
    f15_custo_epi_ano_por_pessoa: Optional[float] = None  # R$
    f15_custo_exames_ano_por_pessoa: Optional[float] = None  # R$
    
    # F16 - Energia/Utilidades (NOVA)
    f16_area_operacao_m2: Optional[float] = None  # m²
    f16_custo_energia_m2_ano: Optional[float] = None  # R$/m²/ano
    
    # F17 - Espaço Físico (NOVA)
    f17_area_m2: Optional[float] = None  # m²
    f17_custo_m2_ano: Optional[float] = None  # R$/m²/ano
    f17_percentual_reducao_automacao: Optional[float] = None  # %
    
    # F18 - Gestão Manual de Dados (NOVA)
    f18_pessoas_envolvidas: Optional[int] = None
    f18_horas_dia_tarefas_dados: Optional[float] = None  # h/dia

@dataclass
class InvestimentoAutomacao:
    """Dados de investimento da automação"""
    valor_investimento_min: float  # R$
    valor_investimento_max: float  # R$
    valor_investimento_medio: float  # R$ (calculado ou input)
```

### 4. models/calculations.py

```python
"""
Models de cálculo intermediário — V2.0
Reorganizado por 5 Dores com 18 fórmulas (F01-F18)
"""
from dataclasses import dataclass

@dataclass
class BasesComuns:
    """Cálculos base reutilizados em múltiplas fórmulas"""
    producao_anual: float  # peças/ano — BASE CANÔNICA de volume
    horas_anuais_operacao: float  # h
    pessoas_expostas_processo: int  # total operadores (todos os turnos)
    pessoas_expostas_inspecao: int  # total inspetores (todos os turnos)
    pessoas_expostas_supervisao: int  # total supervisores (todos os turnos)
    custo_hora_operador: float  # R$/h (com encargos, divisor 176h)
    custo_hora_parada: float  # R$/h (baseado em faturamento)
    fator_encargos: float  # 1.7 / 1.85 / 2.0

@dataclass
class CustosDor1MaoDeObra:
    """Dor 1: Custo Elevado de Mão de Obra"""
    f01_mao_de_obra_direta: float = 0.0
    f02_horas_extras: float = 0.0
    f03_curva_aprendizagem: float = 0.0
    f04_turnover: float = 0.0
    total: float = 0.0

@dataclass
class CustosDor2Qualidade:
    """Dor 2: Baixa Qualidade"""
    f05_refugo: float = 0.0
    f05_retrabalho: float = 0.0
    f05_total: float = 0.0  # Refugo + Retrabalho
    f06_inspecao_manual: float = 0.0
    f07_escapes_qualidade: float = 0.0
    total: float = 0.0

@dataclass
class CustosDor3Produtividade:
    """Dor 3: Baixa Produtividade"""
    f08_custo_oportunidade: float = 0.0
    f09_ociosidade: float = 0.0
    f10_paradas_linha: float = 0.0
    f11_setup_changeover: float = 0.0
    total: float = 0.0

@dataclass
class CustosDor4Seguranca:
    """Dor 4: Falta de Segurança e Ergonomia"""
    f12_afastamentos: float = 0.0
    f12_acidentes: float = 0.0
    f12_risco_legal: float = 0.0
    f12_total: float = 0.0
    f13_frota_empilhadeiras: float = 0.0
    total: float = 0.0

@dataclass
class CustosDor5CustosOcultos:
    """Dor 5: Custos Ocultos de Gestão e Estrutura (NOVAS V2.0)"""
    f14_supervisao: float = 0.0
    f15_compliance_epis: float = 0.0
    f16_energia: float = 0.0
    f17_espaco_fisico: float = 0.0
    f18_gestao_dados: float = 0.0
    total: float = 0.0
```

### 5. models/results.py

```python
"""
Schemas de resultados finais — V2.0
"""
from dataclasses import dataclass
from typing import Dict

@dataclass
class ResultadosFinanceiros:
    """Resultados consolidados V2.0"""
    # Custos por Dor
    total_dor1: float  # Mão de Obra
    total_dor2: float  # Qualidade
    total_dor3: float  # Produtividade
    total_dor4: float  # Segurança
    total_dor5: float  # Custos Ocultos
    
    # Totais
    custo_total_anual_inacao: float  # Soma de todas as dores
    ganho_anual_potencial: float  # baseado em % de redução por fórmula
    
    # Investimento
    investimento_medio: float
    
    # Indicadores
    payback_anos: float
    roi_1_ano: float  # %
    roi_3_anos: float  # %
    roi_5_anos: float  # %
    
    # Breakdown detalhado por fórmula
    breakdown_dor1: Dict[str, float]  # {"F01": valor, "F02": valor, ...}
    breakdown_dor2: Dict[str, float]
    breakdown_dor3: Dict[str, float]
    breakdown_dor4: Dict[str, float]
    breakdown_dor5: Dict[str, float]
    
    # Metadata
    area_atuacao: str
    porte_empresa: str
    fator_encargos_usado: float

@dataclass
class MetasReducao:
    """Metas de redução de custos (%) — V2.0, por fórmula"""
    meta_f01: float = 0.0
    meta_f02: float = 0.0
    meta_f03: float = 0.0
    meta_f04: float = 0.0
    meta_f05: float = 0.0
    meta_f06: float = 0.0
    meta_f07: float = 0.0
    meta_f08: float = 0.0
    meta_f09: float = 0.0
    meta_f10: float = 0.0
    meta_f11: float = 0.0
    meta_f12: float = 0.0
    meta_f13: float = 0.0
    meta_f14: float = 0.0
    meta_f15: float = 0.0
    meta_f16: float = 0.0
    meta_f17: float = 0.0
    meta_f18: float = 0.0
```

---

## 🧮 FÓRMULAS V2.0 DETALHADAS (core/formulas.py) — 18 FÓRMULAS

### Bases Comuns

```python
def calcular_producao_anual(cadencia: float, horas_turno: float,
                           turnos_dia: int, dias_ano: int) -> float:
    """
    Produção anual em peças — BASE CANÔNICA de produção.
    Fórmula: Cadência × 60 × Horas/turno × Turnos/dia × Dias/ano
    
    ⚠️ Todas as fórmulas que precisam de volume de produção devem usar
    esta base anual diretamente. NÃO calcular produção mensal separadamente
    e multiplicar por 12, pois dias_ano/12 nem sempre é inteiro,
    gerando divergências (ex: 250/12 = 20,83 vs 21 dias fixo).
    """
    return cadencia * 60 * horas_turno * turnos_dia * dias_ano

def calcular_horas_anuais(horas_turno: float, turnos_dia: int, dias_ano: int) -> float:
    """Horas anuais de operação"""
    return horas_turno * turnos_dia * dias_ano

def calcular_pessoas_expostas(pessoas_turno: int, turnos_dia: int) -> int:
    """Total de pessoas expostas (todos os turnos)"""
    return pessoas_turno * turnos_dia

def calcular_custo_hora_operador(salario: float, fator_encargos: float) -> float:
    """
    Custo por hora do operador COM ENCARGOS
    REGRA V2.0: Divisor 176h (não 220h)
    Fórmula: (Salário × Fator de Encargos) ÷ 176
    """
    return (salario * fator_encargos) / 176

def calcular_faturamento_mensal(cadencia: float, horas_turno: float,
                                 turnos_dia: int, dias_ano: int,
                                 preco_venda_peca: float) -> float:
    """
    Faturamento Mensal da Linha — AUTO-CALCULADO
    Fórmula: (Cadência × 60 × Horas/turno × Turnos × Dias/ano × Preço Venda) ÷ 12
    
    Equivale a: Produção Anual × Preço Venda ÷ 12
    
    ⚠️ Se preco_venda_peca > 0, calcular automaticamente e pré-preencher no formulário.
    O usuário pode sobrescrever manualmente (ex: quando a linha faz múltiplos produtos).
    Se preco_venda = 0 e faturamento manual = 0, exibir warning.
    """
    if preco_venda_peca <= 0:
        return 0.0
    producao_anual = cadencia * 60 * horas_turno * turnos_dia * dias_ano
    return (producao_anual * preco_venda_peca) / 12

def calcular_custo_hora_parada(faturamento_mensal: float) -> float:
    """
    Custo de oportunidade da hora parada (Regra #3)
    Fórmula: Faturamento Mensal ÷ 176 horas úteis
    """
    if faturamento_mensal is None or faturamento_mensal == 0:
        return 0.0
    return faturamento_mensal / 176
```

---

### DOR 1: CUSTO ELEVADO DE MÃO DE OBRA

```python
def calcular_f01_mao_de_obra_direta(num_operadores: int, salario_medio: float,
                                     fator_encargos: float) -> float:
    """
    F01 (Revisada): Custo de Mão de Obra Direta Alocada ao Processo
    
    Fórmula: Nº Operadores × Salário Médio × Fator Encargos × 12 meses
    
    Nota CFO: Custo ESPECÍFICO dos operadores passíveis de automação,
    não a folha total. Fator 1,7 é conservador (encargos obrigatórios).
    
    Exemplos:
    - Pequena (4 op, R$2.500): 4 × 2.500 × 1,7 × 12 = R$ 204.000
    - Grande (20 op, R$3.200): 20 × 3.200 × 1,7 × 12 = R$ 1.305.600
    """
    return num_operadores * salario_medio * fator_encargos * 12

def calcular_f02_horas_extras(num_operadores: int, media_he_mes: float,
                              salario_medio: float, fator_encargos: float) -> float:
    """
    F02 (Revisada): O Custo Real das Horas Extras
    
    Fórmula: Nº Operadores × Média HE/Mês × Valor Hora com Encargos × 1,5 × 12
    Valor Hora com Encargos = (Salário × Fator Encargos) / 176h
    
    CORREÇÃO V2.0: A fórmula original IGNORAVA encargos sobre HE.
    Agora calcula o adicional de 50% sobre custo REAL da hora (salário + encargos).
    Divisor 176h para aderência à realidade de alocação de custos.
    
    Exemplos:
    - Pequena (4 op, R$2.500, 15 HE/mês): R$ 26.080
    - Grande (20 op, R$3.200, 25 HE/mês): R$ 278.182
    """
    custo_hora = (salario_medio * fator_encargos) / 176
    return num_operadores * media_he_mes * custo_hora * 1.5 * 12

def calcular_f03_curva_aprendizagem(num_contratacoes: int, salario_novato: float,
                                     fator_encargos: float, meses_curva: int,
                                     salario_supervisor: float,
                                     pct_tempo_supervisor: float) -> float:
    """
    F03 (Revisada): O Custo da Curva de Aprendizagem
    
    Fórmula: Nº Contratações × [ (Salário Novato × Encargos × Meses Curva) 
              + (Salário Supervisor × Encargos × % Tempo × Meses Curva) ]
    
    NOVO V2.0: Inclui custo do tempo do SUPERVISOR dedicado ao treinamento.
    
    ⚠️ EXIBIÇÃO NO DASHBOARD E PPTX — OBRIGATÓRIO DETALHAR:
    O cálculo deve ser apresentado com breakdown dos componentes, não apenas
    "N contratações × N meses = R$ X". O vendedor precisa entender e explicar.
    
    Formato de exibição:
      Custo Novato: R$ {salario} × {encargos} × {meses} = R$ X /contratação
      Custo Supervisor: R$ {salario_sup} × {encargos} × {%tempo} × {meses} = R$ Y /contratação
      Custo por contratação: R$ X + R$ Y = R$ Z
      Total: {n_contratações} × R$ Z = R$ TOTAL
    """
    custo_novato = salario_novato * fator_encargos * meses_curva
    custo_supervisor = salario_supervisor * fator_encargos * pct_tempo_supervisor * meses_curva
    return num_contratacoes * (custo_novato + custo_supervisor)

def calcular_f04_turnover(num_desligamentos: int, salario_medio: float,
                          fator_custo_turnover: float) -> float:
    """
    F04 (Revisada): O Custo Real do Turnover
    
    Fórmula: Nº Desligamentos × Salário × Fator de Custo de Turnover
    
    CORREÇÃO V2.0: Fator de Custo de Turnover (benchmark: 1,5 a 3,0) consolida:
    - Custos de rescisão (multa 40% FGTS, aviso prévio)
    - Recrutamento e seleção
    - Admissão (exames, documentação)
    - Produtividade perdida durante vaga aberta e treinamento
    Usamos 1,5x como CONSERVADOR.
    
    Exemplos:
    - Pequena (3 desl, R$2.500, 1,5x): R$ 11.250
    - Grande (25 desl, R$3.200, 1,5x): R$ 120.000
    """
    return num_desligamentos * (salario_medio * fator_custo_turnover)
```

---

### DOR 2: BAIXA QUALIDADE

```python
def calcular_f05_refugo_retrabalho(producao_anual: float,
                                    pct_refugo: float, custo_mp_unidade: float,
                                    pct_retrabalho: float, horas_retrab_unidade: float,
                                    custo_hora_operador: float) -> tuple:
    """
    F05 (Revisada): Custo do Refugo e do Retrabalho (SEPARADOS)
    
    Refugo = Produção ANUAL × % Refugo × Custo MP/Unidade
    Retrabalho = Produção ANUAL × % Retrabalho × Horas Retrab. × Custo Hora Operador
    
    ⚠️ USAR PRODUÇÃO ANUAL DIRETAMENTE (cadência × 60 × h/turno × turnos × dias/ano).
    NÃO usar produção_mensal × 12, pois dias_ano/12 ≠ 21 dias/mês fixo
    (ex: 250/12 = 20,83), gerando divergência entre prod_anual e prod_mensal×12.
    Calcular sobre o anual garante consistência com as demais bases.
    
    CORREÇÃO V2.0: Separa refugo (perda de material) de retrabalho (perda de MO).
    Diagnóstico mais preciso da origem da perda.
    
    Retorna: (custo_refugo, custo_retrabalho, total)
    """
    custo_refugo = producao_anual * pct_refugo * custo_mp_unidade
    custo_retrabalho = producao_anual * pct_retrabalho * horas_retrab_unidade * custo_hora_operador
    return (custo_refugo, custo_retrabalho, custo_refugo + custo_retrabalho)

def calcular_f06_inspecao_manual(num_inspetores: int, salario_inspetor: float,
                                 fator_encargos: float) -> float:
    """
    F06 (Mantida): Custo da Inspeção Manual de Qualidade
    
    Fórmula: Nº Inspetores × Salário × Fator Encargos × 12
    
    Nota CFO: Custo de "não qualidade" puro. Sistemas de visão fazem
    100% de inspeção em linha sem custo incremental de MO.
    """
    return num_inspetores * salario_inspetor * fator_encargos * 12

def calcular_f07_escapes_qualidade(reclamacoes_ano: int,
                                    custo_medio_reclamacao: float) -> float:
    """
    F07 (Revisada): Custo dos Escapes de Qualidade (Impacto no Cliente)
    
    Fórmula: Nº Reclamações/Ano × Custo Médio Real por Reclamação
    
    CORREÇÃO V2.0: O benchmark de R$300 era IRREALISTA para indústria.
    Custo Real deve incluir: logística reversa, produto substituto,
    MO para análise, multas contratuais, e risco de perda do cliente (LTV).
    
    Exemplos:
    - Pequena (12 recl, R$2.000): R$ 24.000
    - Grande (150 recl, R$15.000): R$ 2.250.000
    """
    return reclamacoes_ano * custo_medio_reclamacao
```

---

### DOR 3: BAIXA PRODUTIVIDADE

```python
def calcular_f08_custo_oportunidade(faturamento_mensal: float,
                                     pct_demanda_reprimida: float,
                                     margem_contribuicao: float) -> float:
    """
    F08 (Mantida): Custo de Oportunidade (Gargalo de Faturamento)
    
    Fórmula: Faturamento Mensal × % Demanda Reprimida × Margem Contrib. × 12
    
    Nota CFO: Traduz ineficiência em perda DIRETA de crescimento.
    Automação quebra o gargalo → captura receita adicional sem aumento
    proporcional de custos fixos → alavanca margem.
    """
    return faturamento_mensal * pct_demanda_reprimida * margem_contribuicao * 12

def calcular_f09_ociosidade_silenciosa(num_operadores: int, min_ociosos_dia: float,
                                       custo_hora_operador: float,
                                       dias_ano: int) -> float:
    """
    F09 (Revisada): Custo da Ociosidade Silenciosa
    
    Fórmula: Nº Operadores × (Min Ociosos / 60) × Custo Hora Operador × Dias/Ano
    
    Nota CFO: "Micro-tempos" de espera se somam. Custo de MO que não gera valor.
    AGVs e automação logística garantem fluxo contínuo.
    """
    return num_operadores * (min_ociosos_dia / 60) * custo_hora_operador * dias_ano

def calcular_f10_paradas_linha(paradas_mes: int, duracao_media_horas: float,
                               custo_hora_parada: float) -> float:
    """
    F10 (Mantida): Custo das Paradas de Linha (Downtime)
    
    Fórmula: Nº Paradas/Mês × Duração Média (h) × Custo Hora Parada × 12
    
    Nota CFO: Usa Custo da Hora Parada (Regra #3) baseado em faturamento perdido.
    Custo do downtime >> salários dos operadores parados.
    Automação aumenta MTBF (Mean Time Between Failures).
    """
    return paradas_mes * duracao_media_horas * custo_hora_parada * 12

def calcular_f11_setup_changeover(setups_mes: int, horas_setup: float,
                                   custo_hora_parada: float) -> float:
    """
    F11 (Revisada): Custo do Setup / Changeover Manual
    
    Fórmula: Nº Setups/Mês × Horas/Setup × Custo Hora Parada × 12
    
    Nota CFO: Em ambientes High-Mix Low-Volume, setup é o maior
    assassino de produtividade. SMED pode reduzir >90%.
    """
    return setups_mes * horas_setup * custo_hora_parada * 12
```

---

### DOR 4: FALTA DE SEGURANÇA E ERGONOMIA

```python
def calcular_f12_riscos_acidentes(afastamentos_ano: int, custo_afastamento: float,
                                   acidentes_ano: int, custo_acidente: float,
                                   prob_processo: float,
                                   custo_processo: float) -> tuple:
    """
    F12 (Revisada): Custo dos Riscos, Acidentes e Doenças Ocupacionais
    
    Fórmula: Custo Afastamentos + Custo Acidentes + Custo Risco Legal
    - Afastamentos = Nº Afastamentos × Custo Médio
    - Acidentes = Nº Acidentes com Lesão × Custo Médio
    - Risco Legal = Probabilidade de Processo (%) × Custo Estimado
    
    V2.0: 3 componentes separados. Impacta FAP (Fator Acidentário de Prevenção)
    que pode DOBRAR a alíquota RAT de toda a folha.
    
    Retorna: (custo_afastamentos, custo_acidentes, custo_legal, total)
    """
    c_afast = afastamentos_ano * custo_afastamento
    c_acid = acidentes_ano * custo_acidente
    c_legal = prob_processo * custo_processo
    return (c_afast, c_acid, c_legal, c_afast + c_acid + c_legal)

def calcular_f13_frota_empilhadeiras(num_empilhadeiras: int,
                                      custo_operador: float,
                                      custo_equipamento: float,
                                      custo_energia: float,
                                      custo_manutencao: float) -> float:
    """
    F13 (Revisada e Detalhada): Custo Real da Frota de Empilhadeiras
    
    Fórmula: Nº Empilhadeiras × (Operador + Equipamento + Energia + Manutenção) × 12
    
    CORREÇÃO PRINCIPAL V2.0: O custo do OPERADOR (salário + encargos) era IGNORADO.
    Revela custo de inação 3 a 5 vezes MAIOR que o anteriormente calculado.
    AGVs/AMRs eliminam a necessidade do operador dedicado.
    """
    custo_mensal_total = custo_operador + custo_equipamento + custo_energia + custo_manutencao
    return num_empilhadeiras * custo_mensal_total * 12
```

---

### DOR 5: CUSTOS OCULTOS DE GESTÃO E ESTRUTURA (NOVAS V2.0)

```python
def calcular_f14_supervisao(num_supervisores: int, salario_supervisor: float,
                            fator_encargos: float) -> float:
    """
    F14 (NOVA): Custo da Supervisão e Gestão de Pessoas
    
    Fórmula: Nº Supervisores (total turnos) × Salário × Fator Encargos × 12
    
    ⚠️ VALIDAÇÃO: Nº de supervisores = ProcessoAtual.pessoas_supervisao_turno × turnos_dia.
    Se F14 for selecionada mas supervisores_turno = 0 no formulário de processo,
    o sistema DEVE exigir que o usuário informe quantos supervisores há por turno.
    O slide de "Processo Atual" deve refletir o mesmo valor usado no cálculo.
    
    Nota CFO: Processos automatizados são mais autônomos.
    Supervisores podem ser realocados para melhoria contínua.
    """
    return num_supervisores * salario_supervisor * fator_encargos * 12

def calcular_f15_compliance_epis(num_operadores: int, custo_epi_ano: float,
                                  custo_exames_ano: float) -> float:
    """
    F15 (NOVA): Custo de Compliance, EPIs e Exames
    
    Fórmula: Nº Operadores × (Custo EPI/Ano + Custo Exames/Ano)
    
    Nota CFO: Multiplicado pelo headcount, EPIs e ASOs são custo fixo relevante.
    Automação elimina ou reduz drasticamente.
    """
    return num_operadores * (custo_epi_ano + custo_exames_ano)

def calcular_f16_energia(area_m2: float, custo_energia_m2_ano: float) -> float:
    """
    F16 (NOVA): Custo de Energia e Utilidades (Não-Produtivo)
    
    Fórmula: Área (m²) × Custo Energia/m²/Ano
    
    Nota CFO: Robôs não precisam de iluminação, AC ou ventilação complexa.
    Custo de energia para ambiente humano seria reduzido em célula robotizada.
    """
    return area_m2 * custo_energia_m2_ano

def calcular_f17_espaco_fisico(area_m2: float, custo_m2_ano: float,
                                pct_reducao: float) -> float:
    """
    F17 (NOVA): Custo do Espaço Físico (Imobilizado)
    
    Fórmula: Área (m²) × Custo m²/Ano × % Redução com Automação
    
    Nota CFO: Operações automatizadas são mais compactas e verticais.
    Espaço liberado = expansão de produção ou redução de custo fixo.
    """
    return area_m2 * custo_m2_ano * pct_reducao

def calcular_f18_gestao_dados(num_pessoas: int, horas_dia: float,
                               custo_hora_operador: float,
                               dias_ano: int) -> float:
    """
    F18 (NOVA): Custo da Gestão Manual de Dados e Rastreabilidade
    
    Fórmula: Nº Pessoas × Horas/Dia × Custo Hora com Encargos × Dias/Ano
    
    Nota CFO: Coleta manual é lenta e propensa a erros.
    Automação fornece OEE, Cpk em tempo real como subproduto da operação.
    """
    return num_pessoas * horas_dia * custo_hora_operador * dias_ano
```

---

### Indicadores Financeiros

```python
def calcular_payback(investimento: float, ganho_anual: float) -> float:
    """
    Payback Simples em anos
    Fórmula: Investimento / Ganho anual
    """
    if ganho_anual == 0:
        return float('inf')
    return investimento / ganho_anual

def calcular_roi(investimento: float, ganho_anual: float, anos: int) -> float:
    """
    ROI em % para N anos
    Fórmula: ((Ganho × Anos) - Investimento) / Investimento × 100
    """
    if investimento == 0:
        return 0.0
    return ((ganho_anual * anos) - investimento) / investimento * 100

def calcular_ganho_anual(custo_atual: float, meta_reducao: float) -> float:
    """
    Ganho anual baseado em meta de redução
    Fórmula: Custo atual × Meta de redução (%)
    """
    return custo_atual * meta_reducao
```

---

## 🎨 INTERFACE DO USUÁRIO (ui/)

### Fluxo de Telas V2.0

```
1. Tela Inicial
   ├── Título: "Calculadora do Custo da Inação"
   ├── Conceito: "Quanto custa NÃO automatizar?"
   └── Botão "Nova Análise"

2. Informações do Cliente
   ├── Nome do Cliente / Projeto
   ├── Seleção da Área de Atuação ARV (6 opções)
   ├── Porte da Empresa (Pequena / Média / Grande)
   ├── Seleção do Fator de Encargos (1,7 / 1,85 / 2,0)
   └── Botão "Próximo"

3. Dados do Processo Atual
   ├── Produção (cadência ou volume mensal)
   ├── Turnos, Horas, Dias
   ├── Headcount (operadores, inspetores, supervisores)
   ├── Salários médios
   ├── Preço de Venda por Peça (R$)
   ├── Faturamento mensal da linha (AUTO-CALCULADO a partir de produção × preço)
   │   └── Campo editável: usuário pode sobrescrever se necessário
   └── Botão "Próximo"

4. Seleção de Dores / Fórmulas
   ├── Checkboxes organizados por 5 Dores
   ├── Fórmulas PRÉ-SELECIONADAS com base na Área escolhida
   ├── Usuário pode adicionar/remover fórmulas
   └── Botão "Próximo"

5. Parâmetros Detalhados
   ├── Campos condicionais para cada fórmula selecionada
   ├── Tooltips com "Nota do CFO" para cada campo
   └── Botão "Próximo"

6. Metas de Redução
   ├── Sliders de % de redução para cada fórmula selecionada
   └── Botão "Próximo"

7. Investimento
   ├── Valor mínimo e máximo
   └── Botão "Calcular"

8. Dashboard de Resultados
   ├── Métricas principais (Custo Total da Inação, Ganho Potencial, Payback, ROI)
   ├── Breakdown por Dor (5 categorias)
   ├── Breakdown detalhado por Fórmula (F01-F18)
   ├── Tabela consolidada
   └── Botão "Gerar Apresentação"

9. Download
   ├── Preview do PPTX
   └── Botão de download
```

### Componentes Principais (ui/forms.py)

```python
def render_info_cliente() -> ClienteBasicInfo:
    """Renderiza formulário de informações do cliente (V2.0)"""
    st.header("🏭 Informações do Cliente")
    
    nome_cliente = st.text_input("Nome do Cliente")
    nome_projeto = st.text_input("Nome do Projeto")
    
    area = st.selectbox("Área de Atuação ARV", options=[
        ("area_1_linhas_montagem", "🔧 Linhas de Montagem Automáticas"),
        ("area_2_maquinas_especiais", "⚙️ Soluções em Máquinas Especiais"),
        ("area_3_controle_qualidade", "🔍 Controle de Qualidade Automatizado"),
        ("area_4_embalagem", "📦 Automação de Embalagem (Fim de Linha)"),
        ("area_5_logistica_interna", "🚚 Automação de Logística Interna"),
        ("area_6_robotica", "🤖 Soluções Robóticas Customizadas"),
    ], format_func=lambda x: x[1])
    
    porte = st.selectbox("Porte da Empresa", ["Pequena", "Média", "Grande"])
    
    fator = st.selectbox("Fator de Encargos Trabalhistas", 
                         options=list(FATOR_ENCARGOS_OPCOES.keys()))
    
    return ClienteBasicInfo(
        nome_cliente=nome_cliente,
        nome_projeto=nome_projeto,
        area_atuacao=area[0],
        porte_empresa=porte.lower(),
        fator_encargos=FATOR_ENCARGOS_OPCOES[fator],
    )

def render_selecao_dores(area_selecionada: str) -> DoresSelecionadas:
    """
    Renderiza checkboxes organizados por 5 Dores
    PRÉ-SELECIONA fórmulas com base na Área de Atuação ARV
    """
    st.header("🎯 Selecione as Dores Aplicáveis")
    
    formulas_sugeridas = AREAS_ARV[area_selecionada]["formulas_aplicaveis"]
    st.info(f"Fórmulas pré-selecionadas para {AREAS_ARV[area_selecionada]['nome']}")
    
    dores = DoresSelecionadas()
    
    with st.expander("💰 Dor 1: Custo Elevado de Mão de Obra", expanded=True):
        dores.f01_mao_de_obra_direta = st.checkbox(
            "F01: Mão de Obra Direta", value="F01" in formulas_sugeridas)
        dores.f02_horas_extras = st.checkbox(
            "F02: Horas Extras Recorrentes", value="F02" in formulas_sugeridas)
        dores.f03_curva_aprendizagem = st.checkbox(
            "F03: Curva de Aprendizagem", value="F03" in formulas_sugeridas)
        dores.f04_turnover = st.checkbox(
            "F04: Turnover (Rotatividade)", value="F04" in formulas_sugeridas)
    
    with st.expander("🔍 Dor 2: Baixa Qualidade", expanded=True):
        dores.f05_refugo_retrabalho = st.checkbox(
            "F05: Refugo e Retrabalho", value="F05" in formulas_sugeridas)
        dores.f06_inspecao_manual = st.checkbox(
            "F06: Inspeção Manual", value="F06" in formulas_sugeridas)
        dores.f07_escapes_qualidade = st.checkbox(
            "F07: Escapes de Qualidade", value="F07" in formulas_sugeridas)
    
    with st.expander("📊 Dor 3: Baixa Produtividade", expanded=True):
        dores.f08_custo_oportunidade = st.checkbox(
            "F08: Custo de Oportunidade", value="F08" in formulas_sugeridas)
        dores.f09_ociosidade_silenciosa = st.checkbox(
            "F09: Ociosidade Silenciosa", value="F09" in formulas_sugeridas)
        dores.f10_paradas_linha = st.checkbox(
            "F10: Paradas de Linha", value="F10" in formulas_sugeridas)
        dores.f11_setup_changeover = st.checkbox(
            "F11: Setup / Changeover", value="F11" in formulas_sugeridas)
    
    with st.expander("⚠️ Dor 4: Segurança e Ergonomia", expanded=True):
        dores.f12_riscos_acidentes = st.checkbox(
            "F12: Riscos, Acidentes e Doenças", value="F12" in formulas_sugeridas)
        dores.f13_frota_empilhadeiras = st.checkbox(
            "F13: Frota de Empilhadeiras (TCO)", value="F13" in formulas_sugeridas)
    
    with st.expander("🧠 Dor 5: Custos Ocultos de Gestão", expanded=True):
        dores.f14_supervisao = st.checkbox(
            "F14: Supervisão e Gestão", value="F14" in formulas_sugeridas)
        dores.f15_compliance_epis = st.checkbox(
            "F15: Compliance, EPIs e Exames", value="F15" in formulas_sugeridas)
        dores.f16_energia_utilidades = st.checkbox(
            "F16: Energia e Utilidades", value="F16" in formulas_sugeridas)
        dores.f17_espaco_fisico = st.checkbox(
            "F17: Espaço Físico", value="F17" in formulas_sugeridas)
        dores.f18_gestao_dados = st.checkbox(
            "F18: Gestão Manual de Dados", value="F18" in formulas_sugeridas)
    
    return dores
```

### Dashboard de Resultados (ui/dashboard.py)

```python
def render_dashboard(resultados: ResultadosFinanceiros):
    """Renderiza dashboard de resultados V2.0"""
    
    st.header("📈 Análise do Custo da Inação")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Custo Total da Inação (Anual)",
                 f"R$ {resultados.custo_total_anual_inacao:,.2f}")
    with col2:
        st.metric("Ganho Anual Potencial",
                 f"R$ {resultados.ganho_anual_potencial:,.2f}")
    with col3:
        st.metric("Payback",
                 f"{resultados.payback_anos:.1f} anos")
    with col4:
        st.metric("ROI 3 Anos",
                 f"{resultados.roi_3_anos:.0f}%")
    
    # Breakdown por DOR (5 categorias)
    st.subheader("💸 Custo da Inação por Dor")
    
    dores_data = {
        "💰 Mão de Obra": resultados.total_dor1,
        "🔍 Qualidade": resultados.total_dor2,
        "📊 Produtividade": resultados.total_dor3,
        "⚠️ Segurança": resultados.total_dor4,
        "🧠 Custos Ocultos": resultados.total_dor5,
    }
    
    cols = st.columns(5)
    for i, (dor, valor) in enumerate(dores_data.items()):
        with cols[i]:
            st.metric(dor, f"R$ {valor:,.2f}")
    
    # Breakdown detalhado por fórmula
    st.subheader("📋 Detalhamento por Fórmula")
    # Renderizar expanders com breakdown de cada dor...
```

---

## 📄 GERAÇÃO DE PPTX (export/pptx_generator.py)

### Estratégia

1. **Template Base:** Usar `export/template.pptx` como base
2. **Substituição de Tags:** Buscar e substituir `[PREENCHER]` com dados calculados
3. **Preenchimento de Tabelas:** Preencher células de tabelas com valores
4. **Formatação:** Manter formatação original (cores, fontes, layout)
5. **Incluir "Nota do CFO"** nos slides de quantificação para linguagem executiva
6. **Labels amigáveis:** Usar `AREAS_ARV[key]["nome"]` no PPTX (ex: "🔧 Linhas de Montagem"), NÃO a chave interna (ex: "area_1_linhas_montagem"). Idem para porte: "Pequena Empresa", não "pequena".

### Estrutura

```python
from pptx import Presentation
from pptx.util import Pt
from typing import Dict

class PPTXGenerator:
    """Gerador de apresentação PPTX customizada — V2.0"""
    
    def __init__(self, template_path: str):
        self.template_path = template_path
        self.prs = None
    
    def gerar_apresentacao(self, 
                          cliente: ClienteBasicInfo,
                          processo: ProcessoAtual,
                          resultados: ResultadosFinanceiros,
                          metas: MetasReducao,
                          investimento: InvestimentoAutomacao) -> str:
        """
        Gera PPTX customizado baseado nos dados V2.0
        Retorna: caminho do arquivo gerado
        """
        self.prs = Presentation(self.template_path)
        
        # Slide 1: Capa
        self._preencher_capa(cliente)
        
        # Slide 2-3: Dados do Cliente e Processo
        self._preencher_dados_cliente(cliente, processo)
        
        # Slide 4: Área de Atuação ARV selecionada
        self._preencher_area_atuacao(cliente)
        
        # Slide 5: Cenário Crítico (Custo Total da Inação)
        self._preencher_cenario_critico(resultados)
        
        # Slides 6-10: Quantificação por Dor (5 Dores)
        self._preencher_dor1(resultados)  # Mão de Obra
        self._preencher_dor2(resultados)  # Qualidade
        self._preencher_dor3(resultados)  # Produtividade
        self._preencher_dor4(resultados)  # Segurança
        self._preencher_dor5(resultados)  # Custos Ocultos
        
        # Slide 11: Consolidação Financeira
        self._preencher_consolidacao(resultados)
        
        # Slide 12: Escopo Técnico (placeholder)
        self._preencher_escopo()
        
        # Slide 13: Investimento
        self._preencher_investimento(investimento)
        
        # Slide 14: Viabilidade (ROI, Payback)
        self._preencher_viabilidade(resultados, investimento)
        
        # Slide 15: Conclusão — "Da Despesa ao Investimento Estratégico"
        self._preencher_conclusao()
        
        # Slide 16: Próximas Etapas
        
        # Salvar arquivo
        output_path = f"custo_inacao_{cliente.nome_cliente}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
        self.prs.save(output_path)
        
        return output_path
```

---

## ✅ CHECKLIST DE DESENVOLVIMENTO

### Fase 1: Setup Inicial (30min)
- [ ] Criar estrutura de pastas
- [ ] Configurar `requirements.txt`
- [ ] Setup inicial do Streamlit (`app.py`)
- [ ] Criar `.gitignore`
- [ ] Configurar constantes V2.0 em `config/constants.py`
- [ ] Criar mapeamento de áreas em `config/areas.py`

### Fase 2: Models e Core (3-4h)
- [ ] Implementar schemas V2.0 em `models/`
- [ ] Implementar 18 fórmulas (F01-F18) em `core/formulas.py`
- [ ] Implementar calculator V2.0 em `core/calculator.py`
- [ ] Criar validadores em `core/validators.py`
- [ ] Testes unitários de fórmulas (exemplos do PDF para validação)

### Fase 3: Interface (3-4h)
- [ ] Implementar seleção de Área ARV + Fator Encargos
- [ ] Implementar formulário de dados básicos (V2.0)
- [ ] Implementar seleção de dores com pré-seleção por Área
- [ ] Implementar parâmetros detalhados condicionais (18 fórmulas)
- [ ] Implementar metas de redução por fórmula
- [ ] Implementar formulário de investimento
- [ ] Implementar dashboard V2.0 (breakdown por 5 Dores)
- [ ] Aplicar CSS customizado

### Fase 4: Geração de PPTX (3-4h)
- [ ] Preparar template.pptx base V2.0
- [ ] Implementar PPTXGenerator V2.0
- [ ] Slides de quantificação por Dor (5 slides)
- [ ] Incluir "Nota do CFO" nos slides
- [ ] Testar geração completa

### Fase 5: Integração e Testes (1-2h)
- [ ] Integrar fluxo completo
- [ ] Validar com exemplos do PDF (Pequena vs Grande Empresa)
- [ ] Testes end-to-end
- [ ] Tratamento de erros

### Fase 6: Deploy (30min)
- [ ] Configurar Streamlit Cloud
- [ ] Deploy inicial
- [ ] Testes em produção
- [ ] Documentação README

---

## 🚀 COMANDOS DE DESENVOLVIMENTO

### Setup Local
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt
streamlit run app.py
```

### Testes
```bash
pytest tests/
pytest --cov=. tests/
```

### Deploy
```bash
git add .
git commit -m "Deploy MVP V2.0"
git push origin main
```

---

## 📝 NOTAS IMPORTANTES

### Validações de Input
- Cadência > 0
- Horas/turno: 1-24
- Turnos/dia: 1-3
- Dias/ano: 1-365
- Valores monetários >= 0
- Percentuais: 0-100%
- Fator de Encargos: 1.7 / 1.85 / 2.0

### Validações de Consistência (Cross-Field)
- **F05:** Produção deve ser calculada como anual (cadência × 60 × h × turnos × dias). Nunca usar produção_mensal × 12.
- **F14:** Se selecionada, `pessoas_supervisao_turno` em ProcessoAtual DEVE ser > 0. O slide "Processo Atual" deve refletir o mesmo nº de supervisores usado no cálculo.
- **F08/F10/F11:** Dependem de `faturamento_mensal_linha > 0`. Se selecionadas mas faturamento = 0, exibir warning ao usuário indicando que Custo Hora Parada será R$ 0 e estas fórmulas ficarão zeradas.
- **F06:** Nº de inspetores total = `pessoas_inspecao_turno × turnos_dia`. Deve ser consistente com Slide "Processo Atual".

### Tratamento de Erros
- Divisão por zero nos cálculos (especialmente Payback)
- Campos obrigatórios não preenchidos
- Valores fora de range
- Erro na geração de PPTX
- Faturamento mensal = 0 (Custo Hora Parada indefinido)

### Performance
- Cálculos são instantâneos (aritmética simples)
- Geração de PPTX pode levar 2-5s
- Usar `st.spinner()` para feedback visual

### Exemplos de Validação (do PDF V2.0)

| Fórmula | Cenário | Inputs | Resultado Esperado |
|---------|---------|--------|-------------------|
| F01 | Pequena | 4 op, R$2.500, 1,7 | R$ 204.000 |
| F01 | Grande | 20 op, R$3.200, 1,7 | R$ 1.305.600 |
| F04 | Pequena | 3 desl, R$2.500, 1,5x | R$ 11.250 |
| F04 | Grande | 25 desl, R$3.200, 1,5x | R$ 120.000 |
| F07 | Pequena | 12 recl, R$2.000 | R$ 24.000 |
| F07 | Grande | 150 recl, R$15.000 | R$ 2.250.000 |

### Melhorias Futuras (Pós-MVP)
- Persistência em banco de dados
- Autenticação de usuários
- Versionamento de análises
- Comparação entre cenários (Pequena vs Grande Empresa)
- Gráficos interativos (Plotly)
- Export para PDF
- Compartilhamento por link
- Templates customizáveis por Área ARV
- API REST para integração
- Simulação de cenários (otimista / conservador / pessimista)

---

## 🎯 PRIORIDADES

### P0 (Crítico - MVP)
1. Motor de cálculo V2.0 com 18 fórmulas (F01-F18)
2. Fluxo completo: Área ARV → Dores → Cálculo → Dashboard → PPTX
3. Constantes corretas (Fator 1,7 / Divisor 176h)
4. Dashboard com breakdown por 5 Dores
5. Geração de PPTX funcional
6. Deploy funcionando

### P1 (Importante - Pós-MVP)
1. Validações robustas
2. Tooltips com "Nota do CFO" em cada campo
3. Pré-seleção inteligente de fórmulas por Área
4. UX polido
5. Documentação completa

### P2 (Nice to Have)
1. Gráficos visuais (Plotly)
2. Comparação de cenários por porte
3. Export para PDF
4. Temas customizáveis
5. Exemplos pré-carregados (Pequena vs Grande)

---

## 📞 SUPORTE

- **Documentação Streamlit:** https://docs.streamlit.io
- **Documentação python-pptx:** https://python-pptx.readthedocs.io
- **Streamlit Cloud:** https://streamlit.io/cloud
- **Documento Base:** "Custo da Inação V2.0 Revisado" (PDF ARV Systems)

---

**Última atualização:** 2026-02-26
**Versão:** 2.2 (MVP — Motor de Cálculo V2.0 + Correções de Auditoria + Feedback CEO)
**Status:** Pronto para desenvolvimento
**Base:** Documento "Custo da Inação V2.0 Revisado" — ARV Systems
**Changelog V2.2 (feedback CEO 25/02):**
- FIX: Faturamento Mensal agora é AUTO-CALCULADO (Produção Anual × Preço Venda ÷ 12)
- FIX: Adicionado `preco_venda_peca` como input em ProcessoAtual
- FIX: Nova função `calcular_faturamento_mensal()` nas Bases Comuns
- FIX: F03 exige breakdown detalhado na exibição (Custo Novato + Custo Supervisor separados)
**Changelog V2.1:**
- FIX: F05 usa produção ANUAL direta (não mensal×12) para evitar divergência de arredondamento
- FIX: F14 exige supervisores_turno > 0 em ProcessoAtual quando selecionada
- FIX: Adicionado `pessoas_supervisao_turno` ao schema ProcessoAtual
- FIX: Removida `calcular_producao_mensal_from_cadencia` (fonte de inconsistência)
- FIX: PPTX usa labels amigáveis para área/porte (não chaves internas)
- ADD: Seção de validações cross-field