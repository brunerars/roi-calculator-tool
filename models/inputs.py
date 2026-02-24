"""
Schemas de entrada de dados do cliente — V2.0 (Custo da Inação).
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ClienteBasicInfo:
    """Informações básicas do cliente (V2.0)."""

    nome_cliente: str
    nome_projeto: str
    area_atuacao: str  # chave em `config.areas.AREAS_ARV`
    porte_empresa: str  # "pequena" | "media" | "grande"
    fator_encargos: float = 1.7  # 1.7 / 1.85 / 2.0


@dataclass
class ProcessoAtual:
    """Dados do processo atual (V2.0)."""

    # Produção
    cadencia_producao: Optional[float] = None  # peças/min (alternativa à produção mensal)
    producao_mensal: Optional[float] = None  # peças/mês
    horas_por_turno: float = 8.0
    turnos_por_dia: int = 2
    dias_operacao_ano: int = 250

    # Pessoas
    pessoas_processo_turno: int = 5
    pessoas_inspecao_turno: int = 1

    # Custos (salários brutos)
    salario_medio_operador: float = 2500.0
    salario_medio_inspetor: float = 3000.0
    salario_medio_supervisor: float = 5000.0

    # Custos unitários
    custo_unitario_peca: float = 100.0  # R$
    custo_materia_prima_peca: float = 15.0  # R$ (custo MP direto por unidade)

    # Financeiro da linha (para custo hora parada)
    faturamento_mensal_linha: Optional[float] = None  # R$


@dataclass
class DoresSelecionadas:
    """
    Dores/Fórmulas selecionadas — V2.0.
    Flags mapeiam para F01–F18.
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
    f13_frota_empilhadeiras: bool = False  # específica da Área 5

    # DOR 5: CUSTOS OCULTOS DE GESTÃO E ESTRUTURA
    f14_supervisao: bool = False
    f15_compliance_epis: bool = False
    f16_energia_utilidades: bool = False
    f17_espaco_fisico: bool = False
    f18_gestao_dados: bool = False


@dataclass
class ParametrosDetalhados:
    """Parâmetros detalhados por fórmula (V2.0)."""

    # F02 - Horas Extras
    f02_media_he_mes_por_pessoa: Optional[float] = None  # HE/mês/pessoa

    # F03 - Curva de Aprendizagem
    f03_novas_contratacoes_ano: Optional[int] = None
    f03_salario_novato: Optional[float] = None  # R$
    f03_meses_curva: Optional[int] = None  # meses
    f03_salario_supervisor: Optional[float] = None  # R$
    f03_percentual_tempo_supervisor: Optional[float] = None  # fração (0–1)

    # F04 - Turnover
    f04_desligamentos_ano: Optional[int] = None
    f04_fator_custo_turnover: Optional[float] = 1.5  # 1,5 a 3,0

    # F05 - Refugo e Retrabalho
    f05_percentual_refugo: Optional[float] = None  # fração (0–1)
    f05_percentual_retrabalho: Optional[float] = None  # fração (0–1)
    f05_horas_retrabalho_por_unidade: Optional[float] = None  # h/unidade

    # F07 - Escapes de Qualidade
    f07_reclamacoes_clientes_ano: Optional[int] = None
    f07_custo_medio_por_reclamacao: Optional[float] = None  # R$

    # F08 - Custo de Oportunidade
    f08_percentual_demanda_reprimida: Optional[float] = None  # fração (0–1)
    f08_margem_contribuicao: Optional[float] = None  # fração (0–1)

    # F09 - Ociosidade Silenciosa
    f09_minutos_ociosos_por_dia: Optional[float] = None  # min/dia

    # F10 - Paradas de Linha
    f10_paradas_mes: Optional[int] = None
    f10_duracao_media_parada_horas: Optional[float] = None  # h
    f10_custo_hora_parada: Optional[float] = None  # R$/h (Regra #3)

    # F11 - Setup/Changeover
    f11_setups_mes: Optional[int] = None
    f11_horas_por_setup: Optional[float] = None  # h
    f11_custo_hora_parada: Optional[float] = None  # R$/h (Regra #3)

    # F12 - Riscos, Acidentes e Doenças
    f12_afastamentos_ano: Optional[int] = None
    f12_custo_medio_afastamento: Optional[float] = None  # R$
    f12_acidentes_com_lesao_ano: Optional[int] = None
    f12_custo_medio_acidente: Optional[float] = None  # R$
    f12_probabilidade_processo: Optional[float] = None  # fração (0–1)
    f12_custo_estimado_processo: Optional[float] = None  # R$

    # F13 - Frota de Empilhadeiras (TCO)
    f13_num_empilhadeiras: Optional[int] = None
    f13_custo_operador_mes: Optional[float] = None  # R$
    f13_custo_equipamento_mes: Optional[float] = None  # R$
    f13_custo_energia_mes: Optional[float] = None  # R$
    f13_custo_manutencao_mes: Optional[float] = None  # R$

    # F14 - Supervisão
    f14_num_supervisores: Optional[int] = None
    f14_salario_supervisor: Optional[float] = None  # R$

    # F15 - Compliance/EPIs
    f15_custo_epi_ano_por_pessoa: Optional[float] = None  # R$
    f15_custo_exames_ano_por_pessoa: Optional[float] = None  # R$

    # F16 - Energia/Utilidades
    f16_area_operacao_m2: Optional[float] = None  # m²
    f16_custo_energia_m2_ano: Optional[float] = None  # R$/m²/ano

    # F17 - Espaço Físico
    f17_area_m2: Optional[float] = None  # m²
    f17_custo_m2_ano: Optional[float] = None  # R$/m²/ano
    f17_percentual_reducao_automacao: Optional[float] = None  # fração (0–1)

    # F18 - Gestão de Dados
    f18_pessoas_envolvidas: Optional[int] = None
    f18_horas_dia_tarefas_dados: Optional[float] = None  # h/dia


@dataclass
class InvestimentoAutomacao:
    """Dados de investimento da automação (V2.0)."""

    valor_investimento_min: float  # R$
    valor_investimento_max: float  # R$

    @property
    def valor_investimento_medio(self) -> float:
        return (self.valor_investimento_min + self.valor_investimento_max) / 2
