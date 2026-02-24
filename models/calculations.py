"""
Models de cálculo intermediário — V2.0.

Reorganizado por 5 Dores com 18 fórmulas (F01–F18).
"""

from dataclasses import dataclass


@dataclass
class BasesComuns:
    """Cálculos base reutilizados em múltiplas fórmulas."""

    producao_anual: float  # peças/ano
    producao_mensal: float  # peças/mês
    horas_anuais_operacao: float  # h/ano
    pessoas_expostas_processo: int  # total operadores (todos os turnos)
    pessoas_expostas_inspecao: int  # total inspetores (todos os turnos)
    custo_hora_operador: float  # R$/h (com encargos, divisor 176h)
    custo_hora_parada: float  # R$/h (baseado em faturamento)
    fator_encargos: float  # 1.7 / 1.85 / 2.0


@dataclass
class CustosDor1MaoDeObra:
    """Dor 1: Custo Elevado de Mão de Obra."""

    f01_mao_de_obra_direta: float = 0.0
    f02_horas_extras: float = 0.0
    f03_curva_aprendizagem: float = 0.0
    f04_turnover: float = 0.0
    total: float = 0.0


@dataclass
class CustosDor2Qualidade:
    """Dor 2: Baixa Qualidade."""

    f05_refugo: float = 0.0
    f05_retrabalho: float = 0.0
    f05_total: float = 0.0
    f06_inspecao_manual: float = 0.0
    f07_escapes_qualidade: float = 0.0
    total: float = 0.0


@dataclass
class CustosDor3Produtividade:
    """Dor 3: Baixa Produtividade."""

    f08_custo_oportunidade: float = 0.0
    f09_ociosidade: float = 0.0
    f10_paradas_linha: float = 0.0
    f11_setup_changeover: float = 0.0
    total: float = 0.0


@dataclass
class CustosDor4Seguranca:
    """Dor 4: Falta de Segurança e Ergonomia."""

    f12_afastamentos: float = 0.0
    f12_acidentes: float = 0.0
    f12_risco_legal: float = 0.0
    f12_total: float = 0.0
    f13_frota_empilhadeiras: float = 0.0
    total: float = 0.0


@dataclass
class CustosDor5CustosOcultos:
    """Dor 5: Custos Ocultos de Gestão e Estrutura."""

    f14_supervisao: float = 0.0
    f15_compliance_epis: float = 0.0
    f16_energia: float = 0.0
    f17_espaco_fisico: float = 0.0
    f18_gestao_dados: float = 0.0
    total: float = 0.0
