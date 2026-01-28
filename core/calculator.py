"""
Motor de cálculo principal.
Orquestra as fórmulas e gera os resultados financeiros consolidados.
"""
from config.constants import (
    SALARIO_COLABORADOR,
    HORAS_TRABALHADAS_MES,
    CUSTO_HORA_PARADA,
    CUSTO_LOGISTICA_REVERSA,
    MULTA_MEDIA_QUALIDADE,
    CUSTO_TREINAMENTO,
    MULTA_ATRASO,
    FATOR_RESCISAO,
    FATOR_PASSIVO_TRABALHISTA,
    FATOR_HORA_EXTRA,
)
from core.formulas import (
    calcular_producao_anual,
    calcular_horas_anuais,
    calcular_pessoas_expostas,
    calcular_custo_hora_operador,
    calcular_custo_dia_absenteismo,
    calcular_custo_material,
    calcular_co1_folha_pagamento,
    calcular_co2_terceirizacao,
    calcular_co3_desperdicio,
    calcular_co4_manutencao,
    calcular_ql1_retrabalho,
    calcular_ql2_refugo,
    calcular_ql3_inspecao,
    calcular_ql4_logistica,
    calcular_ql5_multas_qualidade,
    calcular_se1_absenteismo,
    calcular_se2_turnover,
    calcular_se3_treinamentos,
    calcular_se4_passivo_juridico,
    calcular_pr1_horas_extras,
    calcular_pr2_headcount,
    calcular_pr3_vendas_perdidas,
    calcular_pr4_multas_atraso,
    calcular_payback,
    calcular_roi,
    calcular_ganho_anual,
)
from models.inputs import (
    ProcessoAtual,
    DoresSelecionadas,
    ParametrosDetalhados,
    InvestimentoAutomacao,
)
from models.calculations import (
    BasesComuns,
    CustosOperacionais,
    CustosQualidade,
    CustosSeguranca,
    CustosProdutividade,
)
from models.results import MetasReducao, ResultadosFinanceiros


class ROICalculator:
    """Motor de cálculo de ROI para automação industrial."""

    def __init__(
        self,
        processo: ProcessoAtual,
        dores: DoresSelecionadas,
        parametros: ParametrosDetalhados,
        investimento: InvestimentoAutomacao,
        metas: MetasReducao,
    ):
        self.processo = processo
        self.dores = dores
        self.parametros = parametros
        self.investimento = investimento
        self.metas = metas

        self.bases = self._calcular_bases()

    def _calcular_bases(self) -> BasesComuns:
        """Calcula as bases comuns reutilizadas."""
        p = self.processo
        return BasesComuns(
            producao_anual=calcular_producao_anual(
                p.cadencia_producao, p.horas_por_turno, p.turnos_por_dia, p.dias_operacao_ano
            ),
            horas_anuais_operacao=calcular_horas_anuais(
                p.horas_por_turno, p.turnos_por_dia, p.dias_operacao_ano
            ),
            pessoas_expostas_processo=calcular_pessoas_expostas(
                p.pessoas_processo_turno, p.turnos_por_dia
            ),
            pessoas_expostas_inspecao=calcular_pessoas_expostas(
                p.pessoas_inspecao_turno, p.turnos_por_dia
            ),
            custo_material_por_peca=calcular_custo_material(
                p.custo_unitario_peca, p.fracao_material
            ),
            custo_hora_operador=calcular_custo_hora_operador(
                SALARIO_COLABORADOR, HORAS_TRABALHADAS_MES
            ),
            custo_dia_absenteismo=calcular_custo_dia_absenteismo(
                SALARIO_COLABORADOR, p.dias_operacao_ano
            ),
            custo_rescisao=SALARIO_COLABORADOR * FATOR_RESCISAO,
            provisao_trabalhista=SALARIO_COLABORADOR * FATOR_PASSIVO_TRABALHISTA,
        )

    def calcular_custos_operacionais(self) -> CustosOperacionais:
        """Calcula custos operacionais (CO)."""
        co = CustosOperacionais()
        d = self.dores
        p = self.parametros
        b = self.bases

        if d.co1_folha_pagamento:
            co.co1_folha = calcular_co1_folha_pagamento(
                b.pessoas_expostas_processo,
                SALARIO_COLABORADOR,
                self.processo.turnos_por_dia,
            )

        if d.co2_terceirizacao and p.volume_terceirizado and p.custo_unitario_terceirizado:
            co.co2_terceirizacao = calcular_co2_terceirizacao(
                p.volume_terceirizado,
                p.custo_unitario_terceirizado,
                p.meses_pico or 12,
            )

        if d.co3_desperdicio and p.percentual_desperdicio is not None:
            co.co3_desperdicio = calcular_co3_desperdicio(
                b.producao_anual,
                p.percentual_desperdicio,
                b.custo_material_por_peca,
            )

        if d.co4_manutencao and p.paradas_nao_planejadas_mes and p.duracao_media_parada_min:
            co.co4_manutencao = calcular_co4_manutencao(
                p.paradas_nao_planejadas_mes,
                p.duracao_media_parada_min,
                CUSTO_HORA_PARADA,
            )

        return co

    def calcular_custos_qualidade(self) -> CustosQualidade:
        """Calcula custos de qualidade (QL)."""
        ql = CustosQualidade()
        d = self.dores
        p = self.parametros
        b = self.bases

        if d.ql1_retrabalho and p.percentual_retrabalho is not None:
            ql.ql1_retrabalho = calcular_ql1_retrabalho(
                b.producao_anual,
                p.percentual_retrabalho,
                self.processo.custo_unitario_peca,
                p.fator_retrabalho or 0.2,
            )

        if d.ql2_refugo and p.percentual_scrap is not None:
            ql.ql2_refugo = calcular_ql2_refugo(
                b.producao_anual,
                p.percentual_scrap,
                self.processo.custo_unitario_peca,
            )

        if d.ql3_inspecao_manual:
            ql.ql3_inspecao = calcular_ql3_inspecao(
                b.pessoas_expostas_inspecao,
                SALARIO_COLABORADOR,
                self.processo.turnos_por_dia,
            )

        if d.ql4_logistica_reversa and p.percentual_retorno_garantia is not None:
            ql.ql4_logistica = calcular_ql4_logistica(
                b.producao_anual,
                p.percentual_retorno_garantia,
                CUSTO_LOGISTICA_REVERSA,
            )

        if d.ql5_multas_qualidade and p.ocorrencias_multa_ano is not None:
            ql.ql5_multas = calcular_ql5_multas_qualidade(
                p.ocorrencias_multa_ano,
                MULTA_MEDIA_QUALIDADE,
            )

        return ql

    def calcular_custos_seguranca(self) -> CustosSeguranca:
        """Calcula custos de segurança/ergonomia (SE)."""
        se = CustosSeguranca()
        d = self.dores
        p = self.parametros
        b = self.bases

        if d.se1_absenteismo and p.dias_perdidos_ano is not None:
            se.se1_absenteismo = calcular_se1_absenteismo(
                p.dias_perdidos_ano,
                b.custo_dia_absenteismo,
            )

        if d.se2_turnover and p.desligamentos_ano is not None:
            se.se2_turnover = calcular_se2_turnover(
                p.desligamentos_ano,
                b.custo_rescisao,
            )

        if d.se3_treinamentos and p.desligamentos_ano is not None:
            se.se3_treinamentos = calcular_se3_treinamentos(
                p.desligamentos_ano,
                CUSTO_TREINAMENTO,
            )

        if d.se4_passivo_juridico and p.ocorrencias_processo_ano is not None:
            se.se4_passivo = calcular_se4_passivo_juridico(
                p.ocorrencias_processo_ano,
                b.provisao_trabalhista,
            )

        return se

    def calcular_custos_produtividade(self) -> CustosProdutividade:
        """Calcula custos de produtividade (PR)."""
        pr = CustosProdutividade()
        d = self.dores
        p = self.parametros
        b = self.bases

        if d.pr1_horas_extras and p.horas_extras_mes_pessoa is not None:
            he_totais = p.horas_extras_mes_pessoa * b.pessoas_expostas_processo
            pr.pr1_horas_extras = calcular_pr1_horas_extras(
                he_totais,
                b.custo_hora_operador,
                FATOR_HORA_EXTRA,
            )

        if d.pr2_headcount and p.pessoas_adicionais is not None:
            pr.pr2_headcount = calcular_pr2_headcount(
                p.pessoas_adicionais,
                SALARIO_COLABORADOR,
            )

        if d.pr3_vendas_perdidas and p.demanda_nao_atendida_mes and p.margem_por_peca:
            pr.pr3_vendas_perdidas = calcular_pr3_vendas_perdidas(
                p.demanda_nao_atendida_mes,
                p.margem_por_peca,
            )

        if d.pr4_multas_atraso and p.ocorrencias_atraso_ano is not None:
            pr.pr4_multas_atraso = calcular_pr4_multas_atraso(
                p.ocorrencias_atraso_ano,
                MULTA_ATRASO,
            )

        return pr

    def _calcular_ganho_por_categoria(
        self, co: CustosOperacionais, ql: CustosQualidade,
        se: CustosSeguranca, pr: CustosProdutividade,
    ) -> float:
        """Calcula ganho anual potencial com base nas metas de redução."""
        m = self.metas
        ganho = 0.0

        # CO
        ganho += calcular_ganho_anual(co.co1_folha, m.meta_co1)
        ganho += calcular_ganho_anual(co.co2_terceirizacao, m.meta_co2)
        ganho += calcular_ganho_anual(co.co3_desperdicio, m.meta_co3)
        ganho += calcular_ganho_anual(co.co4_manutencao, m.meta_co4)

        # QL
        ganho += calcular_ganho_anual(ql.ql1_retrabalho, m.meta_ql1)
        ganho += calcular_ganho_anual(ql.ql2_refugo, m.meta_ql2)
        ganho += calcular_ganho_anual(ql.ql3_inspecao, m.meta_ql3)
        ganho += calcular_ganho_anual(ql.ql4_logistica, m.meta_ql4)
        ganho += calcular_ganho_anual(ql.ql5_multas, m.meta_ql5)

        # SE
        ganho += calcular_ganho_anual(se.se1_absenteismo, m.meta_se1)
        ganho += calcular_ganho_anual(se.se2_turnover, m.meta_se2)
        ganho += calcular_ganho_anual(se.se3_treinamentos, m.meta_se3)
        ganho += calcular_ganho_anual(se.se4_passivo, m.meta_se4)

        # PR
        ganho += calcular_ganho_anual(pr.pr1_horas_extras, m.meta_pr1)
        ganho += calcular_ganho_anual(pr.pr2_headcount, m.meta_pr2)
        ganho += calcular_ganho_anual(pr.pr3_vendas_perdidas, m.meta_pr3)
        ganho += calcular_ganho_anual(pr.pr4_multas_atraso, m.meta_pr4)

        return ganho

    def calcular(self) -> ResultadosFinanceiros:
        """Executa o cálculo completo e retorna resultados consolidados."""
        co = self.calcular_custos_operacionais()
        ql = self.calcular_custos_qualidade()
        se = self.calcular_custos_seguranca()
        pr = self.calcular_custos_produtividade()

        custo_total = co.total + ql.total + se.total + pr.total
        ganho_anual = self._calcular_ganho_por_categoria(co, ql, se, pr)
        investimento_medio = self.investimento.valor_investimento_medio

        return ResultadosFinanceiros(
            total_co=co.total,
            total_ql=ql.total,
            total_se=se.total,
            total_pr=pr.total,
            custo_total_anual=custo_total,
            ganho_anual_potencial=ganho_anual,
            investimento_medio=investimento_medio,
            payback_anos=calcular_payback(investimento_medio, ganho_anual),
            roi_1_ano=calcular_roi(investimento_medio, ganho_anual, 1),
            roi_3_anos=calcular_roi(investimento_medio, ganho_anual, 3),
            roi_5_anos=calcular_roi(investimento_medio, ganho_anual, 5),
            breakdown_co={
                "CO-1: Folha de Pagamento": co.co1_folha,
                "CO-2: Terceirização": co.co2_terceirizacao,
                "CO-3: Desperdício": co.co3_desperdicio,
                "CO-4: Manutenção": co.co4_manutencao,
            },
            breakdown_ql={
                "QL-1: Retrabalho": ql.ql1_retrabalho,
                "QL-2: Refugo": ql.ql2_refugo,
                "QL-3: Inspeção": ql.ql3_inspecao,
                "QL-4: Logística Reversa": ql.ql4_logistica,
                "QL-5: Multas Qualidade": ql.ql5_multas,
            },
            breakdown_se={
                "SE-1: Absenteísmo": se.se1_absenteismo,
                "SE-2: Turnover": se.se2_turnover,
                "SE-3: Treinamentos": se.se3_treinamentos,
                "SE-4: Passivo Jurídico": se.se4_passivo,
            },
            breakdown_pr={
                "PR-1: Horas Extras": pr.pr1_horas_extras,
                "PR-2: Headcount": pr.pr2_headcount,
                "PR-3: Vendas Perdidas": pr.pr3_vendas_perdidas,
                "PR-4: Multas Atraso": pr.pr4_multas_atraso,
            },
        )
