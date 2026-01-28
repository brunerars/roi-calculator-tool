# ROI CALCULATOR - MVP

## 📋 VISÃO GERAL

Ferramenta web para acelerar propostas comerciais de projetos de automação industrial, quantificando rapidamente o ROI e gerando apresentações customizadas.

**Problema:** Vendedores perdem dias criando propostas técnico-financeiras para projetos CAPEX
**Solução:** Input de dados → Cálculo automático → Dashboard + PPTX customizado em minutos
**Impacto:** Reduzir tempo de proposta de dias para minutos, aumentar taxa de conversão CAPEX

---

## 🎯 OBJETIVOS DO MVP

### Funcionalidades Core
1. ✅ Formulário web para input de dados do cliente
2. ✅ Motor de cálculo de custos e ganhos (4 categorias, 17 subcategorias)
3. ✅ Dashboard com resultados (Payback, ROI 1/3/5 anos)
4. ✅ Geração de PPTX customizado (16 slides)
5. ✅ Download do arquivo gerado

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
│   └── constants.py                # Constantes (parâmetros ARV)
│
├── models/
│   ├── __init__.py
│   ├── inputs.py                   # Schemas de entrada
│   ├── calculations.py             # Models de cálculo
│   └── results.py                  # Schemas de resultado
│
├── core/
│   ├── __init__.py
│   ├── calculator.py               # Motor de cálculo principal
│   ├── formulas.py                 # Fórmulas detalhadas
│   └── validators.py               # Validações de input
│
├── ui/
│   ├── __init__.py
│   ├── forms.py                    # Formulários Streamlit
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
    └── test_formulas.py            # Testes de fórmulas
```

---

## 📊 MODELS E SCHEMAS

### 1. config/constants.py

```python
"""
Parâmetros ARV (constantes do sistema)
"""

# Parâmetros de Custo Base
SALARIO_COLABORADOR = 5000  # R$
HORAS_TRABALHADAS_MES = 220  # h

# Custos Operacionais
CUSTO_HORA_PARADA = 150  # R$/h
CUSTO_LOGISTICA_REVERSA = 15  # R$
MULTA_MEDIA_QUALIDADE = 500  # R$
CUSTO_TREINAMENTO = 1200  # R$
MULTA_ATRASO = 1000  # R$

# Fatores
FATOR_RESCISAO = 2  # múltiplo do salário
FATOR_PASSIVO_TRABALHISTA = 7  # múltiplo (7 a 12 salários)
FATOR_HORA_EXTRA = 1.5  # múltiplo
```

### 2. models/inputs.py

```python
"""
Schemas de entrada de dados do cliente
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class ClienteBasicInfo:
    """Informações básicas do cliente"""
    nome_cliente: str
    nome_projeto: str
    nivel_automacao: str  # "Manual", "Semiautomatizado", "Automatizado"
    
@dataclass
class ProcessoAtual:
    """Dados do processo atual do cliente"""
    cadencia_producao: float  # peças/min
    horas_por_turno: float  # h
    turnos_por_dia: int  # turnos
    dias_operacao_ano: int  # dias
    pessoas_processo_turno: int  # pessoas
    pessoas_inspecao_turno: int  # pessoas
    custo_unitario_peca: float  # R$
    fracao_material: float  # % (0.6 = 60%)

@dataclass
class DoresSelecionadas:
    """Dores/custos selecionados pelo usuário"""
    # Custos Operacionais
    co1_folha_pagamento: bool = False
    co2_terceirizacao: bool = False
    co3_desperdicio: bool = False
    co4_manutencao: bool = False
    
    # Qualidade
    ql1_retrabalho: bool = False
    ql2_refugo: bool = False
    ql3_inspecao_manual: bool = False
    ql4_logistica_reversa: bool = False
    ql5_multas_qualidade: bool = False
    
    # Segurança/Ergonomia
    se1_absenteismo: bool = False
    se2_turnover: bool = False
    se3_treinamentos: bool = False
    se4_passivo_juridico: bool = False
    
    # Produtividade
    pr1_horas_extras: bool = False
    pr2_headcount: bool = False
    pr3_vendas_perdidas: bool = False
    pr4_multas_atraso: bool = False

@dataclass
class ParametrosDetalhados:
    """Parâmetros detalhados para cálculos específicos"""
    # CO-2
    volume_terceirizado: Optional[float] = None
    custo_unitario_terceirizado: Optional[float] = None
    meses_pico: Optional[int] = None
    
    # CO-3
    percentual_desperdicio: Optional[float] = None  # %
    
    # CO-4
    paradas_nao_planejadas_mes: Optional[int] = None
    duracao_media_parada_min: Optional[float] = None
    
    # QL-1
    percentual_retrabalho: Optional[float] = None  # %
    fator_retrabalho: Optional[float] = None  # 0.2 = 20%
    
    # QL-2
    percentual_scrap: Optional[float] = None  # %
    
    # QL-4
    percentual_retorno_garantia: Optional[float] = None  # %
    
    # QL-5
    ocorrencias_multa_ano: Optional[int] = None
    
    # SE-1
    perfil_risco_absenteismo: Optional[str] = None  # "baixo", "medio", "alto"
    dias_perdidos_ano: Optional[int] = None
    
    # SE-2
    perfil_risco_turnover: Optional[str] = None  # "baixo", "medio", "alto"
    desligamentos_ano: Optional[int] = None
    
    # SE-4
    ocorrencias_processo_ano: Optional[int] = None
    
    # PR-1
    horas_extras_mes_pessoa: Optional[float] = None
    
    # PR-2
    pessoas_adicionais: Optional[int] = None
    
    # PR-3
    demanda_nao_atendida_mes: Optional[float] = None
    margem_por_peca: Optional[float] = None
    
    # PR-4
    ocorrencias_atraso_ano: Optional[int] = None

@dataclass
class InvestimentoAutomacao:
    """Dados de investimento da automação"""
    valor_investimento_min: float  # R$
    valor_investimento_max: float  # R$
    valor_investimento_medio: float  # R$ (calculado)
```

### 3. models/calculations.py

```python
"""
Models de cálculo intermediário
"""
from dataclasses import dataclass

@dataclass
class BasesComuns:
    """Cálculos base reutilizados"""
    producao_anual: float  # peças/ano
    horas_anuais_operacao: float  # h
    pessoas_expostas_processo: int  # pessoas
    pessoas_expostas_inspecao: int  # pessoas
    custo_material_por_peca: float  # R$
    custo_hora_operador: float  # R$/h
    custo_dia_absenteismo: float  # R$/dia
    custo_rescisao: float  # R$
    provisao_trabalhista: float  # R$

@dataclass
class CustosOperacionais:
    """Custos operacionais calculados"""
    co1_folha: float = 0.0
    co2_terceirizacao: float = 0.0
    co3_desperdicio: float = 0.0
    co4_manutencao: float = 0.0
    total: float = 0.0

@dataclass
class CustosQualidade:
    """Custos de qualidade calculados"""
    ql1_retrabalho: float = 0.0
    ql2_refugo: float = 0.0
    ql3_inspecao: float = 0.0
    ql4_logistica: float = 0.0
    ql5_multas: float = 0.0
    total: float = 0.0

@dataclass
class CustosSeguranca:
    """Custos de segurança/ergonomia calculados"""
    se1_absenteismo: float = 0.0
    se2_turnover: float = 0.0
    se3_treinamentos: float = 0.0
    se4_passivo: float = 0.0
    total: float = 0.0

@dataclass
class CustosProdutividade:
    """Custos de produtividade calculados"""
    pr1_horas_extras: float = 0.0
    pr2_headcount: float = 0.0
    pr3_vendas_perdidas: float = 0.0
    pr4_multas_atraso: float = 0.0
    total: float = 0.0
```

### 4. models/results.py

```python
"""
Schemas de resultados finais
"""
from dataclasses import dataclass
from typing import Dict

@dataclass
class ResultadosFinanceiros:
    """Resultados consolidados"""
    # Custos por categoria
    total_co: float
    total_ql: float
    total_se: float
    total_pr: float
    
    # Totais
    custo_total_anual: float
    ganho_anual_potencial: float  # baseado em % de redução
    
    # Investimento
    investimento_medio: float
    
    # Indicadores
    payback_anos: float
    roi_1_ano: float  # %
    roi_3_anos: float  # %
    roi_5_anos: float  # %
    
    # Breakdown detalhado
    breakdown_co: Dict[str, float]
    breakdown_ql: Dict[str, float]
    breakdown_se: Dict[str, float]
    breakdown_pr: Dict[str, float]

@dataclass
class MetasReducao:
    """Metas de redução de custos (%)"""
    # Custos Operacionais
    meta_co1: float = 0.0
    meta_co2: float = 0.0
    meta_co3: float = 0.0
    meta_co4: float = 0.0
    
    # Qualidade
    meta_ql1: float = 0.0
    meta_ql2: float = 0.0
    meta_ql3: float = 0.0
    meta_ql4: float = 0.0
    meta_ql5: float = 0.0
    
    # Segurança
    meta_se1: float = 0.0
    meta_se2: float = 0.0
    meta_se3: float = 0.0
    meta_se4: float = 0.0
    
    # Produtividade
    meta_pr1: float = 0.0
    meta_pr2: float = 0.0
    meta_pr3: float = 0.0
    meta_pr4: float = 0.0
```

---

## 🧮 FÓRMULAS DETALHADAS (core/formulas.py)

### Bases Comuns

```python
def calcular_producao_anual(cadencia: float, horas_turno: float, 
                           turnos_dia: int, dias_ano: int) -> float:
    """
    Produção anual em peças
    Fórmula: Cadência × 60 × Horas/turno × Turnos/dia × Dias/ano
    """
    return cadencia * 60 * horas_turno * turnos_dia * dias_ano

def calcular_horas_anuais(horas_turno: float, turnos_dia: int, dias_ano: int) -> float:
    """
    Horas anuais de operação
    Fórmula: Horas/turno × Turnos/dia × Dias/ano
    """
    return horas_turno * turnos_dia * dias_ano

def calcular_pessoas_expostas(pessoas_turno: int, turnos_dia: int) -> int:
    """
    Total de pessoas expostas ao processo
    Fórmula: Pessoas/turno × Turnos/dia
    """
    return pessoas_turno * turnos_dia

def calcular_custo_hora_operador(salario: float, horas_mes: float) -> float:
    """
    Custo por hora do operador
    Fórmula: Salário / Horas trabalhadas no mês
    """
    return salario / horas_mes

def calcular_custo_dia_absenteismo(salario: float, dias_ano: int) -> float:
    """
    Custo por dia de absenteísmo
    Fórmula: (Salário × 12) / Dias de operação por ano
    """
    return (salario * 12) / dias_ano

def calcular_custo_material(custo_unitario: float, fracao_material: float) -> float:
    """
    Custo de material por peça
    Fórmula: Custo unitário × Fração de material
    """
    return custo_unitario * fracao_material
```

### CO - Custos Operacionais

```python
def calcular_co1_folha_pagamento(pessoas_expostas: int, salario: float, 
                                 turnos_dia: int) -> float:
    """
    CO-1: Folha de Pagamento Direta
    Fórmula: Pessoas × Salário × Turnos × 12
    """
    return pessoas_expostas * salario * turnos_dia * 12

def calcular_co2_terceirizacao(volume: float, custo_unitario: float, 
                                meses: int) -> float:
    """
    CO-2: Terceirização de Produção
    Fórmula: Volume × Custo × Meses
    """
    return volume * custo_unitario * meses

def calcular_co3_desperdicio(producao_anual: float, percentual_desperdicio: float,
                             custo_material: float) -> float:
    """
    CO-3: Desperdício de Insumos
    Fórmula: Produção anual × % desperdício × Custo material
    """
    return producao_anual * percentual_desperdicio * custo_material

def calcular_co4_manutencao(paradas_mes: int, duracao_min: float, 
                            custo_hora_parada: float) -> float:
    """
    CO-4: Manutenção Corretiva
    Fórmula: (Paradas × Min / 60 × 12) × Custo hora parada
    """
    return (paradas_mes * duracao_min / 60 * 12) * custo_hora_parada
```

### QL - Qualidade

```python
def calcular_ql1_retrabalho(producao_anual: float, percentual_retrabalho: float,
                           custo_peca: float, fator_retrabalho: float) -> float:
    """
    QL-1: Retrabalho Interno
    Fórmula: Produção anual × % retrabalho × Custo peça × Fator retrabalho
    """
    return producao_anual * percentual_retrabalho * custo_peca * fator_retrabalho

def calcular_ql2_refugo(producao_anual: float, percentual_scrap: float,
                        custo_peca: float) -> float:
    """
    QL-2: Refugo / Scrap
    Fórmula: Produção anual × % refugo × Custo peça
    """
    return producao_anual * percentual_scrap * custo_peca

def calcular_ql3_inspecao(pessoas_inspecao: int, salario: float, 
                         turnos_dia: int) -> float:
    """
    QL-3: Inspeção Manual 100%
    Fórmula: Pessoas inspeção × Salário × Turnos × 12
    """
    return pessoas_inspecao * salario * turnos_dia * 12

def calcular_ql4_logistica(producao_anual: float, percentual_retorno: float,
                          custo_logistica: float) -> float:
    """
    QL-4: Logística Reversa / Garantias
    Fórmula: Produção anual × % retorno × Custo logística
    """
    return producao_anual * percentual_retorno * custo_logistica

def calcular_ql5_multas_qualidade(ocorrencias: int, multa_media: float) -> float:
    """
    QL-5: Multas Contratuais de Qualidade
    Fórmula: Ocorrências × Multa média
    """
    return ocorrencias * multa_media
```

### SE - Segurança e Ergonomia

```python
def calcular_se1_absenteismo(dias_perdidos: int, custo_dia: float) -> float:
    """
    SE-1: Absenteísmo
    Fórmula: Dias perdidos × Custo/dia
    
    Perfil de risco:
    - Baixo: 0-3 faltas/ano
    - Médio: 4-6 faltas/ano
    - Alto: 7-12 faltas/ano
    """
    return dias_perdidos * custo_dia

def calcular_se2_turnover(desligamentos: int, custo_rescisao: float) -> float:
    """
    SE-2: Turnover (Rotatividade)
    Fórmula: Desligamentos × Custo rescisão
    
    Taxa por perfil:
    - Baixo: 5%
    - Médio: 10%
    - Alto: 20%
    """
    return desligamentos * custo_rescisao

def calcular_se3_treinamentos(desligamentos: int, custo_treinamento: float) -> float:
    """
    SE-3: Treinamentos Recorrentes
    Fórmula: Desligamentos × Custo treinamento
    """
    return desligamentos * custo_treinamento

def calcular_se4_passivo_juridico(ocorrencias: int, provisao: float) -> float:
    """
    SE-4: Passivo Jurídico / Multas
    Fórmula: Ocorrências × Provisão
    """
    return ocorrencias * provisao
```

### PR - Produtividade

```python
def calcular_pr1_horas_extras(he_totais_mes: float, custo_hora: float,
                              fator_he: float) -> float:
    """
    PR-1: Horas Extras Recorrentes
    Fórmula: HE totais/mês × 12 × Custo hora × Fator HE
    """
    return he_totais_mes * 12 * custo_hora * fator_he

def calcular_pr2_headcount(pessoas_adicionais: int, custo_mensal: float) -> float:
    """
    PR-2: Aumento de Headcount
    Fórmula: Pessoas × Custo mensal × 12
    """
    return pessoas_adicionais * custo_mensal * 12

def calcular_pr3_vendas_perdidas(demanda_mes: float, margem_peca: float) -> float:
    """
    PR-3: Vendas Perdidas (Custo de Oportunidade)
    Fórmula: Demanda não atendida/mês × 12 × Margem
    """
    return demanda_mes * 12 * margem_peca

def calcular_pr4_multas_atraso(ocorrencias: int, multa: float) -> float:
    """
    PR-4: Multas por Atraso
    Fórmula: Ocorrências × Multa
    """
    return ocorrencias * multa
```

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

### Fluxo de Telas

```
1. Tela Inicial
   ├── Título e descrição do projeto
   └── Botão "Nova Análise"

2. Formulário de Dados Básicos
   ├── Informações do Cliente
   ├── Dados do Processo Atual
   └── Botão "Próximo"

3. Seleção de Dores
   ├── Checkboxes por categoria (CO, QL, SE, PR)
   └── Botão "Próximo"

4. Parâmetros Detalhados
   ├── Campos condicionais baseados em dores selecionadas
   └── Botão "Próximo"

5. Metas de Redução
   ├── Sliders de % de redução para cada dor
   └── Botão "Próximo"

6. Investimento
   ├── Valor mínimo e máximo
   └── Botão "Calcular"

7. Dashboard de Resultados
   ├── Métricas principais (Payback, ROI)
   ├── Breakdown por categoria
   ├── Gráficos (opcional)
   └── Botão "Gerar Apresentação"

8. Download
   ├── Preview do PPTX
   └── Botão de download
```

### Componentes Principais (ui/forms.py)

```python
def render_dados_basicos() -> ProcessoAtual:
    """Renderiza formulário de dados básicos do processo"""
    st.header("📊 Dados do Processo Atual")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cadencia = st.number_input("Cadência de Produção (peças/min)", 
                                   min_value=0.1, value=10.0)
        horas_turno = st.number_input("Horas por Turno", 
                                      min_value=1, value=8)
        turnos_dia = st.number_input("Turnos por Dia", 
                                     min_value=1, max_value=3, value=2)
        dias_ano = st.number_input("Dias de Operação por Ano", 
                                   min_value=1, max_value=365, value=250)
    
    with col2:
        pessoas_processo = st.number_input("Pessoas no Processo por Turno", 
                                          min_value=1, value=5)
        pessoas_inspecao = st.number_input("Pessoas em Inspeção por Turno", 
                                          min_value=0, value=1)
        custo_peca = st.number_input("Custo Unitário da Peça (R$)", 
                                    min_value=0.01, value=100.0)
        fracao_material = st.slider("Fração de Material (%)", 
                                    min_value=0, max_value=100, value=60) / 100
    
    return ProcessoAtual(...)

def render_selecao_dores() -> DoresSelecionadas:
    """Renderiza checkboxes de seleção de dores"""
    st.header("🎯 Selecione as Dores Aplicáveis")
    
    dores = DoresSelecionadas()
    
    with st.expander("💰 Custos Operacionais (CO)", expanded=True):
        dores.co1_folha_pagamento = st.checkbox("CO-1: Folha de Pagamento Direta")
        dores.co2_terceirizacao = st.checkbox("CO-2: Terceirização de Produção")
        dores.co3_desperdicio = st.checkbox("CO-3: Desperdício de Insumos")
        dores.co4_manutencao = st.checkbox("CO-4: Manutenção Corretiva")
    
    # Repetir para QL, SE, PR...
    
    return dores

def render_parametros_detalhados(dores: DoresSelecionadas) -> ParametrosDetalhados:
    """Renderiza campos condicionais baseados em dores selecionadas"""
    st.header("🔧 Parâmetros Detalhados")
    
    params = ParametrosDetalhados()
    
    # Renderizar apenas para dores selecionadas
    if dores.co2_terceirizacao:
        st.subheader("CO-2: Terceirização")
        params.volume_terceirizado = st.number_input("Volume Terceirizado")
        params.custo_unitario_terceirizado = st.number_input("Custo Unitário")
        params.meses_pico = st.number_input("Meses de Pico", value=12)
    
    # Repetir para todas as dores selecionadas...
    
    return params

def render_metas_reducao(dores: DoresSelecionadas) -> MetasReducao:
    """Renderiza sliders de meta de redução"""
    st.header("🎯 Metas de Redução de Custos")
    
    metas = MetasReducao()
    
    if dores.co1_folha_pagamento:
        metas.meta_co1 = st.slider("CO-1: Folha de Pagamento (%)", 
                                   0, 100, 50) / 100
    
    # Repetir para todas as dores selecionadas...
    
    return metas
```

### Dashboard de Resultados (ui/dashboard.py)

```python
def render_dashboard(resultados: ResultadosFinanceiros):
    """Renderiza dashboard de resultados"""
    
    st.header("📈 Análise de Viabilidade Financeira")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Custo Total Anual", 
                 f"R$ {resultados.custo_total_anual:,.2f}")
    
    with col2:
        st.metric("Ganho Anual Potencial", 
                 f"R$ {resultados.ganho_anual_potencial:,.2f}")
    
    with col3:
        st.metric("Payback", 
                 f"{resultados.payback_anos:.2f} anos")
    
    with col4:
        st.metric("ROI 3 Anos", 
                 f"{resultados.roi_3_anos:.1f}%")
    
    # Breakdown por categoria
    st.subheader("💸 Breakdown de Custos por Categoria")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("CO - Operacional", 
                 f"R$ {resultados.total_co:,.2f}")
        with st.expander("Detalhes"):
            for key, value in resultados.breakdown_co.items():
                st.write(f"**{key}:** R$ {value:,.2f}")
    
    # Repetir para QL, SE, PR...
    
    # Tabela resumo
    st.subheader("📊 Resumo Consolidado")
    import pandas as pd
    
    df = pd.DataFrame({
        'Categoria': ['CO', 'QL', 'SE', 'PR', 'TOTAL'],
        'Custo Atual': [resultados.total_co, resultados.total_ql, 
                       resultados.total_se, resultados.total_pr,
                       resultados.custo_total_anual],
        'Ganho Potencial': [...],  # Calcular baseado em metas
    })
    
    st.dataframe(df, use_container_width=True)
```

---

## 📄 GERAÇÃO DE PPTX (export/pptx_generator.py)

### Estratégia

1. **Template Base:** Usar `export/template.pptx` como base (copiar do arquivo original)
2. **Substituição de Tags:** Buscar e substituir `[PREENCHER]` com dados calculados
3. **Preenchimento de Tabelas:** Preencher células de tabelas com valores
4. **Formatação:** Manter formatação original (cores, fontes, layout)

### Estrutura

```python
from pptx import Presentation
from pptx.util import Pt
from typing import Dict

class PPTXGenerator:
    """Gerador de apresentação PPTX customizada"""
    
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
        Gera PPTX customizado baseado nos dados
        Retorna: caminho do arquivo gerado
        """
        self.prs = Presentation(self.template_path)
        
        # Slide 1: Capa
        self._preencher_capa(cliente)
        
        # Slide 2-5: Dados do Cliente
        self._preencher_dados_cliente(cliente, processo)
        
        # Slide 6: Análise Estratégica (dores selecionadas)
        self._preencher_dores(...)
        
        # Slide 7: Cenário Crítico
        self._preencher_cenario_critico(resultados)
        
        # Slides 8-11: Quantificação (CO, QL, SE, PR)
        self._preencher_quantificacao(resultados, metas)
        
        # Slide 12: Consolidação Financeira
        self._preencher_consolidacao(resultados)
        
        # Slide 13: Escopo Técnico (placeholder)
        self._preencher_escopo()
        
        # Slide 14: Investimento
        self._preencher_investimento(investimento)
        
        # Slide 15: Viabilidade (ROI, Payback)
        self._preencher_viabilidade(resultados, investimento)
        
        # Slide 16: Próximas Etapas (template padrão)
        
        # Salvar arquivo
        output_path = f"analise_{cliente.nome_cliente}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
        self.prs.save(output_path)
        
        return output_path
    
    def _substituir_texto_slide(self, slide, placeholders: Dict[str, str]):
        """Substitui placeholders [PREENCHER] em um slide"""
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                for placeholder, valor in placeholders.items():
                    if placeholder in shape.text:
                        text_frame = shape.text_frame
                        for paragraph in text_frame.paragraphs:
                            for run in paragraph.runs:
                                if placeholder in run.text:
                                    run.text = run.text.replace(placeholder, valor)
    
    def _preencher_tabela(self, table, dados: Dict):
        """Preenche células de uma tabela"""
        # Implementar lógica de preenchimento de tabelas
        pass
    
    # Métodos específicos para cada slide...
```

---

## ✅ CHECKLIST DE DESENVOLVIMENTO

### Fase 1: Setup Inicial (30min)
- [ ] Criar estrutura de pastas
- [ ] Configurar `requirements.txt`
- [ ] Setup inicial do Streamlit (`app.py`)
- [ ] Criar `.gitignore`
- [ ] Configurar constantes em `config/constants.py`

### Fase 2: Models e Core (2-3h)
- [ ] Implementar schemas em `models/`
- [ ] Implementar fórmulas em `core/formulas.py`
- [ ] Implementar calculator em `core/calculator.py`
- [ ] Criar validadores em `core/validators.py`
- [ ] Testes unitários de fórmulas

### Fase 3: Interface (3-4h)
- [ ] Implementar formulário de dados básicos
- [ ] Implementar seleção de dores
- [ ] Implementar parâmetros detalhados (condicionais)
- [ ] Implementar metas de redução
- [ ] Implementar formulário de investimento
- [ ] Implementar dashboard de resultados
- [ ] Aplicar CSS customizado

### Fase 4: Geração de PPTX (3-4h)
- [ ] Preparar template.pptx base
- [ ] Implementar PPTXGenerator
- [ ] Implementar substituição de texto
- [ ] Implementar preenchimento de tabelas
- [ ] Implementar preenchimento de cada slide (1-16)
- [ ] Testar geração completa

### Fase 5: Integração e Testes (1-2h)
- [ ] Integrar fluxo completo
- [ ] Testes end-to-end
- [ ] Validação de outputs
- [ ] Ajustes de UX
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
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar aplicação
streamlit run app.py
```

### Testes
```bash
# Rodar testes
pytest tests/

# Com coverage
pytest --cov=. tests/
```

### Deploy
```bash
# Push para GitHub
git add .
git commit -m "Deploy MVP"
git push origin main

# Streamlit Cloud irá detectar automaticamente
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

### Tratamento de Erros
- Divisão por zero nos cálculos
- Campos obrigatórios não preenchidos
- Valores fora de range
- Erro na geração de PPTX

### Performance
- Cálculos são instantâneos (aritmética simples)
- Geração de PPTX pode levar 2-5s
- Usar `st.spinner()` para feedback visual

### Melhorias Futuras (Pós-MVP)
- Persistência em banco de dados
- Autenticação de usuários
- Versionamento de análises
- Comparação entre cenários
- Gráficos interativos (Plotly)
- Export para PDF
- Compartilhamento por link
- Templates customizáveis
- API REST para integração

---

## 🎯 PRIORIDADES

### P0 (Crítico - MVP)
1. Fluxo completo de input → cálculo → output
2. Geração de PPTX funcional
3. Dashboard de resultados claro
4. Deploy funcionando

### P1 (Importante - Pós-MVP)
1. Validações robustas
2. Mensagens de erro amigáveis
3. UX polido
4. Documentação completa

### P2 (Nice to Have)
1. Gráficos visuais
2. Comparação de cenários
3. Export para PDF
4. Temas customizáveis

---

## 📞 SUPORTE

- **Documentação Streamlit:** https://docs.streamlit.io
- **Documentação python-pptx:** https://python-pptx.readthedocs.io
- **Streamlit Cloud:** https://streamlit.io/cloud

---

**Última atualização:** 2026-01-27  
**Versão:** 1.0 (MVP)  
**Status:** Pronto para desenvolvimento
