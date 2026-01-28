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

    @property
    def total(self) -> float:
        return self.co1_folha + self.co2_terceirizacao + self.co3_desperdicio + self.co4_manutencao


@dataclass
class CustosQualidade:
    """Custos de qualidade calculados"""
    ql1_retrabalho: float = 0.0
    ql2_refugo: float = 0.0
    ql3_inspecao: float = 0.0
    ql4_logistica: float = 0.0
    ql5_multas: float = 0.0

    @property
    def total(self) -> float:
        return (
            self.ql1_retrabalho
            + self.ql2_refugo
            + self.ql3_inspecao
            + self.ql4_logistica
            + self.ql5_multas
        )


@dataclass
class CustosSeguranca:
    """Custos de segurança/ergonomia calculados"""
    se1_absenteismo: float = 0.0
    se2_turnover: float = 0.0
    se3_treinamentos: float = 0.0
    se4_passivo: float = 0.0

    @property
    def total(self) -> float:
        return self.se1_absenteismo + self.se2_turnover + self.se3_treinamentos + self.se4_passivo


@dataclass
class CustosProdutividade:
    """Custos de produtividade calculados"""
    pr1_horas_extras: float = 0.0
    pr2_headcount: float = 0.0
    pr3_vendas_perdidas: float = 0.0
    pr4_multas_atraso: float = 0.0

    @property
    def total(self) -> float:
        return (
            self.pr1_horas_extras
            + self.pr2_headcount
            + self.pr3_vendas_perdidas
            + self.pr4_multas_atraso
        )
