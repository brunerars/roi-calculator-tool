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

    @property
    def valor_investimento_medio(self) -> float:
        return (self.valor_investimento_min + self.valor_investimento_max) / 2
