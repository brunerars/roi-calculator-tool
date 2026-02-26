"""
Motor de cálculo principal — V2.0.

Orquestra as fórmulas F01–F18 e gera resultados consolidados por 5 Dores.
"""

from __future__ import annotations

from config.constants import DIAS_OPERACAO_MES_DEFAULT, FATOR_CUSTO_TURNOVER_DEFAULT
from core.formulas import (
    calcular_custo_hora_operador,
    calcular_custo_hora_parada,
    calcular_f01_mao_de_obra_direta,
    calcular_f02_horas_extras,
    calcular_f03_curva_aprendizagem,
    calcular_f04_turnover,
    calcular_f05_refugo_retrabalho,
    calcular_f06_inspecao_manual,
    calcular_f07_escapes_qualidade,
    calcular_f08_custo_oportunidade,
    calcular_f09_ociosidade_silenciosa,
    calcular_f10_paradas_linha,
    calcular_f11_setup_changeover,
    calcular_f12_riscos_acidentes,
    calcular_f13_frota_empilhadeiras,
    calcular_f14_supervisao,
    calcular_f15_compliance_epis,
    calcular_f16_energia,
    calcular_f17_espaco_fisico,
    calcular_f18_gestao_dados,
    calcular_ganho_anual,
    calcular_horas_anuais,
    calcular_payback,
    calcular_pessoas_expostas,
    calcular_producao_anual,
    calcular_producao_mensal_from_cadencia,
    calcular_roi,
)
from models.calculations import (
    BasesComuns,
    CustosDor1MaoDeObra,
    CustosDor2Qualidade,
    CustosDor3Produtividade,
    CustosDor4Seguranca,
    CustosDor5CustosOcultos,
)
from models.inputs import ClienteBasicInfo, DoresSelecionadas, InvestimentoAutomacao, ParametrosDetalhados, ProcessoAtual
from models.results import MetasReducao, ResultadosFinanceiros


class ROICalculator:
    """Motor de cálculo de Custo da Inação (V2.0)."""

    def __init__(
        self,
        cliente: ClienteBasicInfo,
        processo: ProcessoAtual,
        dores: DoresSelecionadas,
        parametros: ParametrosDetalhados,
        investimento: InvestimentoAutomacao,
        metas: MetasReducao,
    ):
        self.cliente = cliente
        self.processo = processo
        self.dores = dores
        self.parametros = parametros
        self.investimento = investimento
        self.metas = metas

        self.bases = self._calcular_bases()

    def _calcular_bases(self) -> BasesComuns:
        """Calcula as bases comuns reutilizadas (V2.0)."""
        p = self.processo
        fator_encargos = self.cliente.fator_encargos

        pessoas_processo = calcular_pessoas_expostas(p.pessoas_processo_turno, p.turnos_por_dia)
        pessoas_inspecao = calcular_pessoas_expostas(p.pessoas_inspecao_turno, p.turnos_por_dia)

        # Produção mensal/anual: usa produção mensal informada; senão, estima via cadência.
        if p.producao_mensal is not None and p.producao_mensal > 0:
            producao_mensal = p.producao_mensal
            producao_anual = producao_mensal * 12
        elif p.cadencia_producao is not None and p.cadencia_producao > 0:
            producao_mensal = calcular_producao_mensal_from_cadencia(
                p.cadencia_producao,
                p.horas_por_turno,
                p.turnos_por_dia,
                dias_mes=DIAS_OPERACAO_MES_DEFAULT,
            )
            producao_anual = calcular_producao_anual(
                p.cadencia_producao,
                p.horas_por_turno,
                p.turnos_por_dia,
                p.dias_operacao_ano,
            )
        else:
            producao_mensal = 0.0
            producao_anual = 0.0

        return BasesComuns(
            producao_anual=producao_anual,
            producao_mensal=producao_mensal,
            horas_anuais_operacao=calcular_horas_anuais(p.horas_por_turno, p.turnos_por_dia, p.dias_operacao_ano),
            pessoas_expostas_processo=pessoas_processo,
            pessoas_expostas_inspecao=pessoas_inspecao,
            custo_hora_operador=calcular_custo_hora_operador(p.salario_medio_operador, fator_encargos),
            custo_hora_parada=calcular_custo_hora_parada(p.faturamento_mensal_linha),
            fator_encargos=fator_encargos,
        )

    def calcular(self) -> ResultadosFinanceiros:
        """Executa o cálculo completo (V2.0) e retorna resultados consolidados."""

        d = self.dores
        p = self.processo
        params = self.parametros
        b = self.bases
        fator_encargos = self.cliente.fator_encargos

        dor1 = CustosDor1MaoDeObra()
        dor2 = CustosDor2Qualidade()
        dor3 = CustosDor3Produtividade()
        dor4 = CustosDor4Seguranca()
        dor5 = CustosDor5CustosOcultos()

        # --- Dor 1 ---
        if d.f01_mao_de_obra_direta:
            dor1.f01_mao_de_obra_direta = calcular_f01_mao_de_obra_direta(
                b.pessoas_expostas_processo,
                p.salario_medio_operador,
                fator_encargos,
            )

        if d.f02_horas_extras and params.f02_media_he_mes_por_pessoa is not None:
            dor1.f02_horas_extras = calcular_f02_horas_extras(
                b.pessoas_expostas_processo,
                params.f02_media_he_mes_por_pessoa,
                p.salario_medio_operador,
                fator_encargos,
            )

        if d.f03_curva_aprendizagem and (
            params.f03_novas_contratacoes_ano is not None
            and (params.f03_salario_novato is not None or p.salario_medio_operador is not None)
            and params.f03_meses_curva is not None
            and (params.f03_salario_supervisor is not None or p.salario_medio_supervisor is not None)
            and params.f03_percentual_tempo_supervisor is not None
        ):
            dor1.f03_curva_aprendizagem = calcular_f03_curva_aprendizagem(
                num_contratacoes=params.f03_novas_contratacoes_ano,
                salario_novato=params.f03_salario_novato or p.salario_medio_operador,
                fator_encargos=fator_encargos,
                meses_curva=params.f03_meses_curva,
                salario_supervisor=params.f03_salario_supervisor or p.salario_medio_supervisor,
                pct_tempo_supervisor=params.f03_percentual_tempo_supervisor,
            )

        if d.f04_turnover and params.f04_desligamentos_ano is not None:
            dor1.f04_turnover = calcular_f04_turnover(
                num_desligamentos=params.f04_desligamentos_ano,
                salario_medio=p.salario_medio_operador,
                fator_custo_turnover=params.f04_fator_custo_turnover or FATOR_CUSTO_TURNOVER_DEFAULT,
            )

        dor1.total = dor1.f01_mao_de_obra_direta + dor1.f02_horas_extras + dor1.f03_curva_aprendizagem + dor1.f04_turnover

        # --- Dor 2 ---
        if d.f05_refugo_retrabalho and (
            params.f05_percentual_refugo is not None
            and params.f05_percentual_retrabalho is not None
            and params.f05_horas_retrabalho_por_unidade is not None
        ):
            refugo, retrabalho, total = calcular_f05_refugo_retrabalho(
                producao_mensal=b.producao_mensal,
                pct_refugo=params.f05_percentual_refugo,
                custo_mp_unidade=p.custo_materia_prima_peca,
                pct_retrabalho=params.f05_percentual_retrabalho,
                horas_retrab_unidade=params.f05_horas_retrabalho_por_unidade,
                custo_hora_operador=b.custo_hora_operador,
            )
            dor2.f05_refugo = refugo
            dor2.f05_retrabalho = retrabalho
            dor2.f05_total = total

        if d.f06_inspecao_manual:
            dor2.f06_inspecao_manual = calcular_f06_inspecao_manual(
                num_inspetores=b.pessoas_expostas_inspecao,
                salario_inspetor=p.salario_medio_inspetor,
                fator_encargos=fator_encargos,
            )

        if d.f07_escapes_qualidade and (
            params.f07_reclamacoes_clientes_ano is not None and params.f07_custo_medio_por_reclamacao is not None
        ):
            dor2.f07_escapes_qualidade = calcular_f07_escapes_qualidade(
                reclamacoes_ano=params.f07_reclamacoes_clientes_ano,
                custo_medio_reclamacao=params.f07_custo_medio_por_reclamacao,
            )

        dor2.total = dor2.f05_total + dor2.f06_inspecao_manual + dor2.f07_escapes_qualidade

        # --- Dor 3 ---
        if d.f08_custo_oportunidade and (
            p.faturamento_mensal_linha is not None
            and params.f08_percentual_demanda_reprimida is not None
            and params.f08_margem_contribuicao is not None
        ):
            dor3.f08_custo_oportunidade = calcular_f08_custo_oportunidade(
                faturamento_mensal=p.faturamento_mensal_linha,
                pct_demanda_reprimida=params.f08_percentual_demanda_reprimida,
                margem_contribuicao=params.f08_margem_contribuicao,
            )

        if d.f09_ociosidade_silenciosa and params.f09_minutos_ociosos_por_dia is not None:
            dor3.f09_ociosidade = calcular_f09_ociosidade_silenciosa(
                num_operadores=b.pessoas_expostas_processo,
                min_ociosos_dia=params.f09_minutos_ociosos_por_dia,
                custo_hora_operador=b.custo_hora_operador,
                dias_ano=p.dias_operacao_ano,
            )

        if d.f10_paradas_linha and (
            params.f10_paradas_mes is not None and params.f10_duracao_media_parada_horas is not None
        ):
            dor3.f10_paradas_linha = calcular_f10_paradas_linha(
                paradas_mes=params.f10_paradas_mes,
                duracao_media_horas=params.f10_duracao_media_parada_horas,
                custo_hora_parada=params.f10_custo_hora_parada if (params.f10_custo_hora_parada is not None and params.f10_custo_hora_parada > 0) else b.custo_hora_parada,
            )

        if d.f11_setup_changeover and (params.f11_setups_mes is not None and params.f11_horas_por_setup is not None):
            dor3.f11_setup_changeover = calcular_f11_setup_changeover(
                setups_mes=params.f11_setups_mes,
                horas_setup=params.f11_horas_por_setup,
                custo_hora_parada=params.f11_custo_hora_parada if (params.f11_custo_hora_parada is not None and params.f11_custo_hora_parada > 0) else b.custo_hora_parada,
            )

        dor3.total = dor3.f08_custo_oportunidade + dor3.f09_ociosidade + dor3.f10_paradas_linha + dor3.f11_setup_changeover

        # --- Dor 4 ---
        if d.f12_riscos_acidentes and (
            params.f12_afastamentos_ano is not None
            and params.f12_custo_medio_afastamento is not None
            and params.f12_acidentes_com_lesao_ano is not None
            and params.f12_custo_medio_acidente is not None
            and params.f12_probabilidade_processo is not None
            and params.f12_custo_estimado_processo is not None
        ):
            afast, acid, legal, total = calcular_f12_riscos_acidentes(
                afastamentos_ano=params.f12_afastamentos_ano,
                custo_afastamento=params.f12_custo_medio_afastamento,
                acidentes_ano=params.f12_acidentes_com_lesao_ano,
                custo_acidente=params.f12_custo_medio_acidente,
                prob_processo=params.f12_probabilidade_processo,
                custo_processo=params.f12_custo_estimado_processo,
            )
            dor4.f12_afastamentos = afast
            dor4.f12_acidentes = acid
            dor4.f12_risco_legal = legal
            dor4.f12_total = total

        if d.f13_frota_empilhadeiras and (
            params.f13_num_empilhadeiras is not None
            and params.f13_custo_operador_mes is not None
            and params.f13_custo_equipamento_mes is not None
            and params.f13_custo_energia_mes is not None
            and params.f13_custo_manutencao_mes is not None
        ):
            dor4.f13_frota_empilhadeiras = calcular_f13_frota_empilhadeiras(
                num_empilhadeiras=params.f13_num_empilhadeiras,
                custo_operador=params.f13_custo_operador_mes,
                custo_equipamento=params.f13_custo_equipamento_mes,
                custo_energia=params.f13_custo_energia_mes,
                custo_manutencao=params.f13_custo_manutencao_mes,
            )

        dor4.total = dor4.f12_total + dor4.f13_frota_empilhadeiras

        # --- Dor 5 ---
        if d.f14_supervisao and params.f14_num_supervisores is not None:
            dor5.f14_supervisao = calcular_f14_supervisao(
                num_supervisores=params.f14_num_supervisores * p.turnos_por_dia,
                salario_supervisor=params.f14_salario_supervisor or p.salario_medio_supervisor,
                fator_encargos=fator_encargos,
            )

        if d.f15_compliance_epis and (
            params.f15_custo_epi_ano_por_pessoa is not None and params.f15_custo_exames_ano_por_pessoa is not None
        ):
            dor5.f15_compliance_epis = calcular_f15_compliance_epis(
                num_operadores=b.pessoas_expostas_processo,
                custo_epi_ano=params.f15_custo_epi_ano_por_pessoa,
                custo_exames_ano=params.f15_custo_exames_ano_por_pessoa,
            )

        if d.f16_energia_utilidades and (params.f16_area_operacao_m2 is not None and params.f16_custo_energia_m2_ano is not None):
            dor5.f16_energia = calcular_f16_energia(
                area_m2=params.f16_area_operacao_m2,
                custo_energia_m2_ano=params.f16_custo_energia_m2_ano,
            )

        if d.f17_espaco_fisico and (
            params.f17_area_m2 is not None
            and params.f17_custo_m2_ano is not None
            and params.f17_percentual_reducao_automacao is not None
        ):
            dor5.f17_espaco_fisico = calcular_f17_espaco_fisico(
                area_m2=params.f17_area_m2,
                custo_m2_ano=params.f17_custo_m2_ano,
                pct_reducao=params.f17_percentual_reducao_automacao,
            )

        if d.f18_gestao_dados and (params.f18_pessoas_envolvidas is not None and params.f18_horas_dia_tarefas_dados is not None):
            dor5.f18_gestao_dados = calcular_f18_gestao_dados(
                num_pessoas=params.f18_pessoas_envolvidas,
                horas_dia=params.f18_horas_dia_tarefas_dados,
                custo_hora_operador=b.custo_hora_operador,
                dias_ano=p.dias_operacao_ano,
            )

        dor5.total = dor5.f14_supervisao + dor5.f15_compliance_epis + dor5.f16_energia + dor5.f17_espaco_fisico + dor5.f18_gestao_dados

        custo_total = dor1.total + dor2.total + dor3.total + dor4.total + dor5.total

        m = self.metas
        ganho_anual = 0.0
        ganho_anual += calcular_ganho_anual(dor1.f01_mao_de_obra_direta, m.meta_f01)
        ganho_anual += calcular_ganho_anual(dor1.f02_horas_extras, m.meta_f02)
        ganho_anual += calcular_ganho_anual(dor1.f03_curva_aprendizagem, m.meta_f03)
        ganho_anual += calcular_ganho_anual(dor1.f04_turnover, m.meta_f04)
        ganho_anual += calcular_ganho_anual(dor2.f05_total, m.meta_f05)
        ganho_anual += calcular_ganho_anual(dor2.f06_inspecao_manual, m.meta_f06)
        ganho_anual += calcular_ganho_anual(dor2.f07_escapes_qualidade, m.meta_f07)
        ganho_anual += calcular_ganho_anual(dor3.f08_custo_oportunidade, m.meta_f08)
        ganho_anual += calcular_ganho_anual(dor3.f09_ociosidade, m.meta_f09)
        ganho_anual += calcular_ganho_anual(dor3.f10_paradas_linha, m.meta_f10)
        ganho_anual += calcular_ganho_anual(dor3.f11_setup_changeover, m.meta_f11)
        ganho_anual += calcular_ganho_anual(dor4.f12_total, m.meta_f12)
        ganho_anual += calcular_ganho_anual(dor4.f13_frota_empilhadeiras, m.meta_f13)
        ganho_anual += calcular_ganho_anual(dor5.f14_supervisao, m.meta_f14)
        ganho_anual += calcular_ganho_anual(dor5.f15_compliance_epis, m.meta_f15)
        ganho_anual += calcular_ganho_anual(dor5.f16_energia, m.meta_f16)
        ganho_anual += calcular_ganho_anual(dor5.f17_espaco_fisico, m.meta_f17)
        ganho_anual += calcular_ganho_anual(dor5.f18_gestao_dados, m.meta_f18)

        investimento_medio = self.investimento.valor_investimento_medio

        return ResultadosFinanceiros(
            total_dor1=dor1.total,
            total_dor2=dor2.total,
            total_dor3=dor3.total,
            total_dor4=dor4.total,
            total_dor5=dor5.total,
            custo_total_anual_inacao=custo_total,
            ganho_anual_potencial=ganho_anual,
            investimento_medio=investimento_medio,
            payback_anos=calcular_payback(investimento_medio, ganho_anual),
            roi_1_ano=calcular_roi(investimento_medio, ganho_anual, 1),
            roi_2_anos=calcular_roi(investimento_medio, ganho_anual, 2),
            roi_3_anos=calcular_roi(investimento_medio, ganho_anual, 3),
            roi_4_anos=calcular_roi(investimento_medio, ganho_anual, 4),
            roi_5_anos=calcular_roi(investimento_medio, ganho_anual, 5),
            custo_hora_parada=b.custo_hora_parada,
            faturamento_mensal_linha=p.faturamento_mensal_linha or 0.0,
            breakdown_dor1={
                "F01 - Mão de Obra Direta": dor1.f01_mao_de_obra_direta,
                "F02 - Horas Extras": dor1.f02_horas_extras,
                "F03 - Curva de Aprendizagem": dor1.f03_curva_aprendizagem,
                "F04 - Turnover": dor1.f04_turnover,
            },
            breakdown_dor2={
                "F05 - Refugo": dor2.f05_refugo,
                "F05 - Retrabalho": dor2.f05_retrabalho,
                "F06 - Inspeção Manual": dor2.f06_inspecao_manual,
                "F07 - Escapes de Qualidade": dor2.f07_escapes_qualidade,
            },
            breakdown_dor3={
                "F08 - Custo de Oportunidade": dor3.f08_custo_oportunidade,
                "F09 - Ociosidade Silenciosa": dor3.f09_ociosidade,
                "F10 - Paradas de Linha": dor3.f10_paradas_linha,
                "F11 - Setup/Changeover": dor3.f11_setup_changeover,
            },
            breakdown_dor4={
                "F12 - Afastamentos": dor4.f12_afastamentos,
                "F12 - Acidentes": dor4.f12_acidentes,
                "F12 - Risco Legal": dor4.f12_risco_legal,
                "F13 - Frota de Empilhadeiras": dor4.f13_frota_empilhadeiras,
            },
            breakdown_dor5={
                "F14 - Supervisão": dor5.f14_supervisao,
                "F15 - Compliance/EPIs": dor5.f15_compliance_epis,
                "F16 - Energia e Utilidades": dor5.f16_energia,
                "F17 - Espaço Físico": dor5.f17_espaco_fisico,
                "F18 - Gestão de Dados": dor5.f18_gestao_dados,
            },
            area_atuacao=self.cliente.area_atuacao,
            porte_empresa=self.cliente.porte_empresa,
            fator_encargos_usado=fator_encargos,
        )
