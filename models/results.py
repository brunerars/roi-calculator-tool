"""
Schemas de resultados finais — V2.0.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class MetasReducao:
    """Metas de redução de custos por fórmula (%) — V2.0 (armazenadas como fração 0–1)."""

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


@dataclass
class ResultadosFinanceiros:
    """Resultados consolidados V2.0 (Custo da Inação)."""

    # Custos por Dor (atuais)
    total_dor1: float
    total_dor2: float
    total_dor3: float
    total_dor4: float
    total_dor5: float

    # Totais
    custo_total_anual_inacao: float
    ganho_anual_potencial: float

    # Investimento
    investimento_medio: float

    # Indicadores
    payback_anos: float
    roi_1_ano: float
    roi_2_anos: float
    roi_3_anos: float
    roi_4_anos: float
    roi_5_anos: float

    # Bases de cálculo (para exibição no dashboard e PPTX)
    custo_hora_parada: float
    faturamento_mensal_linha: float

    # Breakdown por Dor (chaves como F01/F02/... e subchaves quando aplicável)
    breakdown_dor1: Dict[str, float]
    breakdown_dor2: Dict[str, float]
    breakdown_dor3: Dict[str, float]
    breakdown_dor4: Dict[str, float]
    breakdown_dor5: Dict[str, float]

    # Metadata
    area_atuacao: str
    porte_empresa: str
    fator_encargos_usado: float
