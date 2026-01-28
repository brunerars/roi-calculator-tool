"""
Gerador de apresentação PPTX customizada (16 slides).
Cria a apresentação programaticamente com python-pptx.
"""
import io
from datetime import datetime

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.chart import XL_CHART_TYPE

from models.inputs import (
    ClienteBasicInfo,
    ProcessoAtual,
    DoresSelecionadas,
    InvestimentoAutomacao,
)
from models.results import ResultadosFinanceiros, MetasReducao

# Paleta de cores
AZUL_ESCURO = RGBColor(0x1F, 0x4E, 0x79)
AZUL_MEDIO = RGBColor(0x2E, 0x75, 0xB6)
AZUL_CLARO = RGBColor(0x9D, 0xC3, 0xE6)
BRANCO = RGBColor(0xFF, 0xFF, 0xFF)
CINZA_ESCURO = RGBColor(0x33, 0x33, 0x33)
CINZA_MEDIO = RGBColor(0x77, 0x77, 0x77)
VERDE = RGBColor(0x00, 0xB0, 0x50)
VERMELHO = RGBColor(0xC0, 0x00, 0x00)
LARANJA = RGBColor(0xED, 0x7D, 0x31)

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)


class PPTXGenerator:
    """Gerador de apresentação PPTX customizada."""

    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = SLIDE_WIDTH
        self.prs.slide_height = SLIDE_HEIGHT

    def gerar(
        self,
        cliente: ClienteBasicInfo,
        processo: ProcessoAtual,
        dores: DoresSelecionadas,
        resultados: ResultadosFinanceiros,
        metas: MetasReducao,
        investimento: InvestimentoAutomacao,
    ) -> io.BytesIO:
        """Gera PPTX completo e retorna como BytesIO."""
        self._slide_01_capa(cliente)
        self._slide_02_agenda()
        self._slide_03_contexto(cliente)
        self._slide_04_processo_atual(processo)
        self._slide_05_dados_operacionais(processo)
        self._slide_06_analise_estrategica(dores)
        self._slide_07_cenario_critico(resultados)
        self._slide_08_custos_operacionais(resultados)
        self._slide_09_custos_qualidade(resultados)
        self._slide_10_custos_seguranca(resultados)
        self._slide_11_custos_produtividade(resultados)
        self._slide_12_consolidacao(resultados)
        self._slide_13_escopo_tecnico()
        self._slide_14_investimento(investimento)
        self._slide_15_viabilidade(resultados, investimento)
        self._slide_16_proximas_etapas()

        buffer = io.BytesIO()
        self.prs.save(buffer)
        buffer.seek(0)
        return buffer

    # =========================================================================
    # Helpers
    # =========================================================================

    def _add_slide(self):
        """Adiciona slide em branco."""
        layout = self.prs.slide_layouts[6]  # blank
        return self.prs.slides.add_slide(layout)

    def _add_textbox(self, slide, left, top, width, height, text,
                     font_size=18, bold=False, color=CINZA_ESCURO,
                     alignment=PP_ALIGN.LEFT, font_name="Calibri"):
        """Adiciona caixa de texto ao slide."""
        txbox = slide.shapes.add_textbox(left, top, width, height)
        tf = txbox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(font_size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.font.name = font_name
        p.alignment = alignment
        return txbox

    def _add_title_bar(self, slide, title_text):
        """Adiciona barra de título azul no topo do slide."""
        # Fundo azul
        shape = slide.shapes.add_shape(
            1, Inches(0), Inches(0), SLIDE_WIDTH, Inches(1.2),
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = AZUL_ESCURO
        shape.line.fill.background()

        # Texto do título
        self._add_textbox(
            slide, Inches(0.5), Inches(0.2), Inches(12), Inches(0.8),
            title_text, font_size=28, bold=True, color=BRANCO,
        )

    def _add_subtitle(self, slide, text, top=Inches(1.4)):
        """Adiciona subtítulo abaixo da barra."""
        self._add_textbox(
            slide, Inches(0.5), top, Inches(12), Inches(0.5),
            text, font_size=16, color=CINZA_MEDIO,
        )

    def _add_metric_box(self, slide, left, top, width, height,
                        label, value, color=AZUL_ESCURO):
        """Adiciona caixa de métrica com label e valor."""
        # Borda
        shape = slide.shapes.add_shape(1, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = BRANCO
        shape.line.color.rgb = color
        shape.line.width = Pt(2)

        # Label
        self._add_textbox(
            slide, left + Inches(0.15), top + Inches(0.1),
            width - Inches(0.3), Inches(0.4),
            label, font_size=11, color=CINZA_MEDIO,
            alignment=PP_ALIGN.CENTER,
        )
        # Valor
        self._add_textbox(
            slide, left + Inches(0.15), top + Inches(0.45),
            width - Inches(0.3), Inches(0.6),
            value, font_size=20, bold=True, color=color,
            alignment=PP_ALIGN.CENTER,
        )

    def _add_table(self, slide, left, top, width, height, rows, cols,
                   data, col_widths=None):
        """Adiciona tabela ao slide."""
        table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
        table = table_shape.table

        if col_widths:
            for i, w in enumerate(col_widths):
                table.columns[i].width = w

        for r in range(rows):
            for c in range(cols):
                cell = table.cell(r, c)
                cell.text = str(data[r][c])
                for paragraph in cell.text_frame.paragraphs:
                    paragraph.font.size = Pt(11)
                    paragraph.font.name = "Calibri"
                    if r == 0:
                        paragraph.font.bold = True
                        paragraph.font.color.rgb = BRANCO
                        paragraph.alignment = PP_ALIGN.CENTER
                    else:
                        paragraph.font.color.rgb = CINZA_ESCURO
                        if c > 0:
                            paragraph.alignment = PP_ALIGN.RIGHT

                # Header row styling
                if r == 0:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = AZUL_ESCURO
                else:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = (
                        RGBColor(0xF2, 0xF2, 0xF2) if r % 2 == 0
                        else BRANCO
                    )

        return table

    def _fmt(self, valor: float) -> str:
        """Formata valor monetário."""
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def _fmt_pct(self, valor: float) -> str:
        """Formata percentual."""
        return f"{valor:.1f}%"

    # =========================================================================
    # Slides
    # =========================================================================

    def _slide_01_capa(self, cliente: ClienteBasicInfo):
        slide = self._add_slide()

        # Fundo azul escuro
        bg = slide.shapes.add_shape(
            1, Inches(0), Inches(0), SLIDE_WIDTH, SLIDE_HEIGHT,
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = AZUL_ESCURO
        bg.line.fill.background()

        # Título principal
        self._add_textbox(
            slide, Inches(1), Inches(2), Inches(11), Inches(1),
            "Análise de Viabilidade Financeira",
            font_size=40, bold=True, color=BRANCO, alignment=PP_ALIGN.CENTER,
        )

        # Subtítulo
        self._add_textbox(
            slide, Inches(1), Inches(3.2), Inches(11), Inches(0.6),
            "Automação Industrial — Estudo de ROI",
            font_size=24, color=AZUL_CLARO, alignment=PP_ALIGN.CENTER,
        )

        # Linha separadora
        line = slide.shapes.add_shape(
            1, Inches(4), Inches(4.1), Inches(5), Inches(0.03),
        )
        line.fill.solid()
        line.fill.fore_color.rgb = AZUL_CLARO
        line.line.fill.background()

        # Info cliente
        self._add_textbox(
            slide, Inches(1), Inches(4.5), Inches(11), Inches(0.5),
            f"Cliente: {cliente.nome_cliente}",
            font_size=20, color=BRANCO, alignment=PP_ALIGN.CENTER,
        )
        self._add_textbox(
            slide, Inches(1), Inches(5.1), Inches(11), Inches(0.5),
            f"Projeto: {cliente.nome_projeto}",
            font_size=18, color=AZUL_CLARO, alignment=PP_ALIGN.CENTER,
        )

        # Data
        data_str = datetime.now().strftime("%d/%m/%Y")
        self._add_textbox(
            slide, Inches(1), Inches(6.2), Inches(11), Inches(0.4),
            data_str, font_size=14, color=AZUL_CLARO, alignment=PP_ALIGN.CENTER,
        )

    def _slide_02_agenda(self):
        slide = self._add_slide()
        self._add_title_bar(slide, "Agenda")

        itens = [
            "1. Contexto e Objetivo",
            "2. Processo Atual",
            "3. Análise Estratégica de Dores",
            "4. Quantificação de Custos",
            "5. Consolidação Financeira",
            "6. Escopo Técnico da Solução",
            "7. Investimento e Viabilidade",
            "8. Próximas Etapas",
        ]

        for i, item in enumerate(itens):
            self._add_textbox(
                slide,
                Inches(1.5), Inches(1.8 + i * 0.6),
                Inches(10), Inches(0.5),
                item, font_size=20, color=AZUL_ESCURO if i % 2 == 0 else CINZA_ESCURO,
            )

    def _slide_03_contexto(self, cliente: ClienteBasicInfo):
        slide = self._add_slide()
        self._add_title_bar(slide, "Contexto e Objetivo")

        self._add_textbox(
            slide, Inches(0.8), Inches(1.8), Inches(11.5), Inches(1),
            f"O presente estudo tem como objetivo quantificar o impacto financeiro "
            f"dos custos operacionais atuais do processo de {cliente.nome_projeto} "
            f"e demonstrar a viabilidade do investimento em automação industrial.",
            font_size=16, color=CINZA_ESCURO,
        )

        self._add_textbox(
            slide, Inches(0.8), Inches(3.2), Inches(5), Inches(0.4),
            "Nível de automação atual:", font_size=14, bold=True, color=AZUL_ESCURO,
        )
        self._add_textbox(
            slide, Inches(6), Inches(3.2), Inches(5), Inches(0.4),
            cliente.nivel_automacao, font_size=14, color=CINZA_ESCURO,
        )

        self._add_textbox(
            slide, Inches(0.8), Inches(4.2), Inches(11.5), Inches(1.5),
            "Metodologia:\n"
            "• Levantamento de dados operacionais junto ao cliente\n"
            "• Quantificação de 4 categorias de custos (17 subcategorias)\n"
            "• Definição de metas de redução com automação\n"
            "• Cálculo de ROI e payback do investimento",
            font_size=14, color=CINZA_ESCURO,
        )

    def _slide_04_processo_atual(self, processo: ProcessoAtual):
        slide = self._add_slide()
        self._add_title_bar(slide, "Processo Atual — Parâmetros de Produção")

        dados = [
            ("Cadência de Produção", f"{processo.cadencia_producao} peças/min"),
            ("Horas por Turno", f"{processo.horas_por_turno}h"),
            ("Turnos por Dia", str(processo.turnos_por_dia)),
            ("Dias de Operação por Ano", str(processo.dias_operacao_ano)),
            ("Pessoas no Processo (por turno)", str(processo.pessoas_processo_turno)),
            ("Pessoas em Inspeção (por turno)", str(processo.pessoas_inspecao_turno)),
            ("Custo Unitário da Peça", self._fmt(processo.custo_unitario_peca)),
            ("Fração de Material", self._fmt_pct(processo.fracao_material * 100)),
        ]

        table_data = [["Parâmetro", "Valor"]] + [[d[0], d[1]] for d in dados]
        self._add_table(
            slide, Inches(2), Inches(1.8), Inches(9), Inches(4),
            len(table_data), 2, table_data,
            col_widths=[Inches(5.5), Inches(3.5)],
        )

    def _slide_05_dados_operacionais(self, processo: ProcessoAtual):
        slide = self._add_slide()
        self._add_title_bar(slide, "Dados Operacionais Calculados")

        prod_anual = (
            processo.cadencia_producao * 60
            * processo.horas_por_turno * processo.turnos_por_dia
            * processo.dias_operacao_ano
        )
        horas_anuais = (
            processo.horas_por_turno * processo.turnos_por_dia
            * processo.dias_operacao_ano
        )
        pessoas_total = processo.pessoas_processo_turno * processo.turnos_por_dia

        box_w = Inches(3.5)
        box_h = Inches(1.2)
        gap = Inches(0.5)
        start_x = Inches(0.8)

        self._add_metric_box(
            slide, start_x, Inches(2), box_w, box_h,
            "Produção Anual", f"{prod_anual:,.0f} peças",
        )
        self._add_metric_box(
            slide, start_x + box_w + gap, Inches(2), box_w, box_h,
            "Horas Anuais de Operação", f"{horas_anuais:,.0f} horas",
        )
        self._add_metric_box(
            slide, start_x + 2 * (box_w + gap), Inches(2), box_w, box_h,
            "Pessoas Expostas (Total)", f"{pessoas_total} pessoas",
        )

        custo_material = processo.custo_unitario_peca * processo.fracao_material
        self._add_metric_box(
            slide, start_x, Inches(3.8), box_w, box_h,
            "Custo Material / Peça", self._fmt(custo_material),
        )
        self._add_metric_box(
            slide, start_x + box_w + gap, Inches(3.8), box_w, box_h,
            "Custo Unitário da Peça", self._fmt(processo.custo_unitario_peca),
        )
        self._add_metric_box(
            slide, start_x + 2 * (box_w + gap), Inches(3.8), box_w, box_h,
            "Turnos x Dias/Ano",
            f"{processo.turnos_por_dia} turnos x {processo.dias_operacao_ano} dias",
        )

    def _slide_06_analise_estrategica(self, dores: DoresSelecionadas):
        slide = self._add_slide()
        self._add_title_bar(slide, "Análise Estratégica — Dores Identificadas")
        self._add_subtitle(slide, "Custos mapeados no cenário atual do cliente")

        categorias = {
            "Custos Operacionais (CO)": [
                ("CO-1: Folha de Pagamento", dores.co1_folha_pagamento),
                ("CO-2: Terceirização", dores.co2_terceirizacao),
                ("CO-3: Desperdício", dores.co3_desperdicio),
                ("CO-4: Manutenção Corretiva", dores.co4_manutencao),
            ],
            "Qualidade (QL)": [
                ("QL-1: Retrabalho", dores.ql1_retrabalho),
                ("QL-2: Refugo / Scrap", dores.ql2_refugo),
                ("QL-3: Inspeção Manual", dores.ql3_inspecao_manual),
                ("QL-4: Logística Reversa", dores.ql4_logistica_reversa),
                ("QL-5: Multas Qualidade", dores.ql5_multas_qualidade),
            ],
            "Segurança (SE)": [
                ("SE-1: Absenteísmo", dores.se1_absenteismo),
                ("SE-2: Turnover", dores.se2_turnover),
                ("SE-3: Treinamentos", dores.se3_treinamentos),
                ("SE-4: Passivo Jurídico", dores.se4_passivo_juridico),
            ],
            "Produtividade (PR)": [
                ("PR-1: Horas Extras", dores.pr1_horas_extras),
                ("PR-2: Headcount", dores.pr2_headcount),
                ("PR-3: Vendas Perdidas", dores.pr3_vendas_perdidas),
                ("PR-4: Multas Atraso", dores.pr4_multas_atraso),
            ],
        }

        col_x = [Inches(0.5), Inches(3.6), Inches(6.7), Inches(9.8)]
        for idx, (cat_name, itens) in enumerate(categorias.items()):
            x = col_x[idx]
            self._add_textbox(
                slide, x, Inches(2.2), Inches(2.8), Inches(0.4),
                cat_name, font_size=12, bold=True, color=AZUL_ESCURO,
            )
            for i, (nome, ativo) in enumerate(itens):
                marcador = "●" if ativo else "○"
                cor = AZUL_MEDIO if ativo else CINZA_MEDIO
                self._add_textbox(
                    slide, x, Inches(2.8 + i * 0.45), Inches(2.8), Inches(0.4),
                    f"{marcador} {nome}", font_size=11, color=cor,
                )

    def _slide_07_cenario_critico(self, resultados: ResultadosFinanceiros):
        slide = self._add_slide()
        self._add_title_bar(slide, "Cenário Crítico — Visão Geral dos Custos")

        # Grande métrica central
        self._add_metric_box(
            slide, Inches(3.5), Inches(1.8), Inches(6), Inches(1.5),
            "CUSTO TOTAL ANUAL IDENTIFICADO",
            self._fmt(resultados.custo_total_anual),
            color=VERMELHO,
        )

        # 4 categorias
        box_w = Inches(2.8)
        start_x = Inches(0.7)
        gap = Inches(0.3)
        top = Inches(4)

        categorias = [
            ("CO - Operacional", resultados.total_co),
            ("QL - Qualidade", resultados.total_ql),
            ("SE - Segurança", resultados.total_se),
            ("PR - Produtividade", resultados.total_pr),
        ]

        for i, (label, valor) in enumerate(categorias):
            self._add_metric_box(
                slide, start_x + i * (box_w + gap), top, box_w, Inches(1.2),
                label, self._fmt(valor), color=AZUL_MEDIO,
            )

    def _slide_custos_categoria(self, titulo, breakdown, total):
        """Slide genérico de custos por categoria."""
        slide = self._add_slide()
        self._add_title_bar(slide, titulo)

        # Tabela de breakdown
        rows_data = [["Subcategoria", "Custo Anual (R$)"]]
        for nome, valor in breakdown.items():
            rows_data.append([nome, self._fmt(valor)])
        rows_data.append(["TOTAL", self._fmt(total)])

        n_rows = len(rows_data)
        table = self._add_table(
            slide, Inches(2), Inches(1.8), Inches(9), Inches(0.5 * n_rows + 0.3),
            n_rows, 2, rows_data,
            col_widths=[Inches(5.5), Inches(3.5)],
        )

        # Destacar linha total
        last_row = n_rows - 1
        for c in range(2):
            cell = table.cell(last_row, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = AZUL_ESCURO
            for p in cell.text_frame.paragraphs:
                p.font.bold = True
                p.font.color.rgb = BRANCO

    def _slide_08_custos_operacionais(self, resultados: ResultadosFinanceiros):
        self._slide_custos_categoria(
            "Quantificação — Custos Operacionais (CO)",
            resultados.breakdown_co, resultados.total_co,
        )

    def _slide_09_custos_qualidade(self, resultados: ResultadosFinanceiros):
        self._slide_custos_categoria(
            "Quantificação — Qualidade (QL)",
            resultados.breakdown_ql, resultados.total_ql,
        )

    def _slide_10_custos_seguranca(self, resultados: ResultadosFinanceiros):
        self._slide_custos_categoria(
            "Quantificação — Segurança e Ergonomia (SE)",
            resultados.breakdown_se, resultados.total_se,
        )

    def _slide_11_custos_produtividade(self, resultados: ResultadosFinanceiros):
        self._slide_custos_categoria(
            "Quantificação — Produtividade (PR)",
            resultados.breakdown_pr, resultados.total_pr,
        )

    def _slide_12_consolidacao(self, resultados: ResultadosFinanceiros):
        slide = self._add_slide()
        self._add_title_bar(slide, "Consolidação Financeira")

        # Tabela consolidada
        table_data = [
            ["Categoria", "Custo Anual (R$)", "% do Total"],
            [
                "CO - Custos Operacionais",
                self._fmt(resultados.total_co),
                self._fmt_pct(
                    resultados.total_co / resultados.custo_total_anual * 100
                    if resultados.custo_total_anual > 0 else 0
                ),
            ],
            [
                "QL - Qualidade",
                self._fmt(resultados.total_ql),
                self._fmt_pct(
                    resultados.total_ql / resultados.custo_total_anual * 100
                    if resultados.custo_total_anual > 0 else 0
                ),
            ],
            [
                "SE - Segurança / Ergonomia",
                self._fmt(resultados.total_se),
                self._fmt_pct(
                    resultados.total_se / resultados.custo_total_anual * 100
                    if resultados.custo_total_anual > 0 else 0
                ),
            ],
            [
                "PR - Produtividade",
                self._fmt(resultados.total_pr),
                self._fmt_pct(
                    resultados.total_pr / resultados.custo_total_anual * 100
                    if resultados.custo_total_anual > 0 else 0
                ),
            ],
            ["TOTAL", self._fmt(resultados.custo_total_anual), "100.0%"],
        ]

        table = self._add_table(
            slide, Inches(1.5), Inches(1.8), Inches(10), Inches(3.2),
            len(table_data), 3, table_data,
            col_widths=[Inches(4.5), Inches(3), Inches(2.5)],
        )

        # Destacar última linha
        last_row = len(table_data) - 1
        for c in range(3):
            cell = table.cell(last_row, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = AZUL_ESCURO
            for p in cell.text_frame.paragraphs:
                p.font.bold = True
                p.font.color.rgb = BRANCO

        # Métrica de ganho potencial
        self._add_metric_box(
            slide, Inches(3.5), Inches(5.5), Inches(6), Inches(1.2),
            "GANHO ANUAL POTENCIAL COM AUTOMAÇÃO",
            self._fmt(resultados.ganho_anual_potencial),
            color=VERDE,
        )

    def _slide_13_escopo_tecnico(self):
        slide = self._add_slide()
        self._add_title_bar(slide, "Escopo Técnico da Solução")
        self._add_subtitle(slide, "Detalhamento técnico a ser definido em fase de projeto")

        itens = [
            "• Definição de tecnologias e equipamentos",
            "• Layout da célula de automação",
            "• Integração com sistemas existentes (MES/ERP)",
            "• Especificação de sensores e atuadores",
            "• Requisitos de infraestrutura",
            "• Cronograma de implantação",
            "• Plano de comissionamento e start-up",
        ]

        for i, item in enumerate(itens):
            self._add_textbox(
                slide, Inches(1.5), Inches(2.2 + i * 0.55),
                Inches(10), Inches(0.5),
                item, font_size=16, color=CINZA_ESCURO,
            )

    def _slide_14_investimento(self, investimento: InvestimentoAutomacao):
        slide = self._add_slide()
        self._add_title_bar(slide, "Investimento")

        box_w = Inches(3.5)
        gap = Inches(0.5)
        start_x = Inches(1.5)
        top = Inches(2.5)

        self._add_metric_box(
            slide, start_x, top, box_w, Inches(1.3),
            "Investimento Mínimo",
            self._fmt(investimento.valor_investimento_min),
            color=AZUL_MEDIO,
        )
        self._add_metric_box(
            slide, start_x + box_w + gap, top, box_w, Inches(1.3),
            "Investimento Máximo",
            self._fmt(investimento.valor_investimento_max),
            color=AZUL_MEDIO,
        )
        self._add_metric_box(
            slide, start_x + 2 * (box_w + gap), top, box_w, Inches(1.3),
            "Investimento Médio",
            self._fmt(investimento.valor_investimento_medio),
            color=AZUL_ESCURO,
        )

        self._add_textbox(
            slide, Inches(1), Inches(4.8), Inches(11), Inches(1),
            "Nota: Os valores apresentados são estimativas iniciais e podem variar "
            "conforme detalhamento técnico do projeto.",
            font_size=13, color=CINZA_MEDIO, alignment=PP_ALIGN.CENTER,
        )

    def _slide_15_viabilidade(self, resultados: ResultadosFinanceiros,
                              investimento: InvestimentoAutomacao):
        slide = self._add_slide()
        self._add_title_bar(slide, "Viabilidade Financeira")

        # Payback
        payback_txt = (
            f"{resultados.payback_anos:.1f} anos"
            if resultados.payback_anos != float("inf")
            else "N/A"
        )

        box_w = Inches(2.7)
        gap = Inches(0.35)
        start_x = Inches(0.7)
        top = Inches(2)

        self._add_metric_box(
            slide, start_x, top, box_w, Inches(1.3),
            "Payback Simples", payback_txt, color=AZUL_ESCURO,
        )
        self._add_metric_box(
            slide, start_x + (box_w + gap), top, box_w, Inches(1.3),
            "ROI 1 Ano", self._fmt_pct(resultados.roi_1_ano), color=AZUL_MEDIO,
        )
        self._add_metric_box(
            slide, start_x + 2 * (box_w + gap), top, box_w, Inches(1.3),
            "ROI 3 Anos", self._fmt_pct(resultados.roi_3_anos), color=VERDE,
        )
        self._add_metric_box(
            slide, start_x + 3 * (box_w + gap), top, box_w, Inches(1.3),
            "ROI 5 Anos", self._fmt_pct(resultados.roi_5_anos), color=VERDE,
        )

        # Tabela comparativa
        table_data = [
            ["", "Investimento Médio", "Ganho Anual", "Ganho Acumulado"],
            ["Ano 1",
             self._fmt(investimento.valor_investimento_medio),
             self._fmt(resultados.ganho_anual_potencial),
             self._fmt(resultados.ganho_anual_potencial)],
            ["Ano 3", "—",
             self._fmt(resultados.ganho_anual_potencial),
             self._fmt(resultados.ganho_anual_potencial * 3)],
            ["Ano 5", "—",
             self._fmt(resultados.ganho_anual_potencial),
             self._fmt(resultados.ganho_anual_potencial * 5)],
        ]

        self._add_table(
            slide, Inches(1.5), Inches(4), Inches(10), Inches(2),
            4, 4, table_data,
            col_widths=[Inches(1.5), Inches(3), Inches(2.5), Inches(3)],
        )

    def _slide_16_proximas_etapas(self):
        slide = self._add_slide()
        self._add_title_bar(slide, "Próximas Etapas")

        etapas = [
            ("1.", "Validação dos dados e premissas apresentados"),
            ("2.", "Detalhamento técnico do escopo da solução"),
            ("3.", "Proposta comercial formal"),
            ("4.", "Aprovação e kick-off do projeto"),
            ("5.", "Desenvolvimento e implantação"),
            ("6.", "Comissionamento e start-up"),
        ]

        for i, (num, texto) in enumerate(etapas):
            # Número em destaque
            self._add_textbox(
                slide, Inches(2), Inches(2 + i * 0.7),
                Inches(0.5), Inches(0.5),
                num, font_size=20, bold=True, color=AZUL_ESCURO,
            )
            # Texto
            self._add_textbox(
                slide, Inches(2.7), Inches(2 + i * 0.7),
                Inches(8), Inches(0.5),
                texto, font_size=18, color=CINZA_ESCURO,
            )

        # Contato
        self._add_textbox(
            slide, Inches(1), Inches(6.3), Inches(11), Inches(0.5),
            "Estamos à disposição para esclarecer quaisquer dúvidas.",
            font_size=14, color=CINZA_MEDIO, alignment=PP_ALIGN.CENTER,
        )
