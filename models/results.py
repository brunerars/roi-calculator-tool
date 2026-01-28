"""
Schemas de resultados finais
"""
from dataclasses import dataclass, field
from typing import Dict


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
    breakdown_co: Dict[str, float] = field(default_factory=dict)
    breakdown_ql: Dict[str, float] = field(default_factory=dict)
    breakdown_se: Dict[str, float] = field(default_factory=dict)
    breakdown_pr: Dict[str, float] = field(default_factory=dict)
