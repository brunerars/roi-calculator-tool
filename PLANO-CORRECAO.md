Plano de Correção Atualizado — ROI Calculator (V2.0) + Saneamento de Cálculos
0) Objetivo do plano (atualizado)

Parar a sangria agora: tornar os cálculos consistentes, defensáveis e previsíveis (sem explosões por % errado, divisores errados e fontes de faturamento conflitantes), mantendo a estrutura do MVP em Streamlit + python-pptx.

P0 — Correções críticas do motor (antes de UI/PPTX)

Sem isso, o sistema sempre vai gerar números “absurdos” e você vai ficar apagando incêndio na proposta.

P0.1 — Unificar regras-base e eliminar “duas verdades” nos divisores

Seu novo plano define:

176h para custo hora operador

220h apenas para cálculo de HE (CLT)

“Hora parada” = faturamento ÷ 176 (regra #3)

✅ Atualização no plano de correção:

Separar claramente 3 tipos de hora (isso resolve 80% das inconsistências):

hora_operador_custeio: divisor 176

hora_extra_clt: divisor 220 (ou 220 para hora base CLT, e depois aplica adicional)

hora_parada_linha: não pode ser “sempre 176” se o processo opera 2 turnos / 3 turnos / dias diferentes.

📌 Decisão importante (para parar absurdos):
Mesmo que a regra #3 do documento diga “÷176”, isso gera discrepância quando o cliente tem 2 turnos.
Recomendação CFO-grade:

manter 176 como “horas úteis padrão”, mas calcular hora parada real por operação:

horas_mes_operacao = horas_turno * turnos_por_dia * (dias_operacao_ano/12)

hora_parada = faturamento_mensal / horas_mes_operacao

Se vocês insistirem em usar 176 por padrão (porque está no documento), então o sistema precisa:

expor isso no dashboard como “Regra ARV (176h)”

e oferecer um toggle “usar horas reais do processo” (recomendado)
Senão, vai continuar aparecendo “inconsistente” dependendo da linha.

✅ Entregável:

config/constants.py com os 3 conceitos

core/formulas.py com funções separadas e documentadas

P0.2 — Normalização obrigatória de percentuais (anti-explosão)

Hoje, o maior causador de “absurdos” é usuário digitar:

10 (achando 10%) e o sistema tratar como 1000%

✅ Atualização no plano:
Criar utilitário to_pct(x) em core/validators.py (ou core/utils.py) e usar em:

refugo, retrabalho, demanda reprimida, margem, prob processo, redução, etc.

Regras:

se x > 1 → x = x/100

validar 0 <= x <= 1

se inválido, bloquear cálculo e mostrar erro amigável no Streamlit

✅ Entregável:

core/validators.py: normalização + validação

testes em tests/test_validators.py

P0.3 — Fonte única de “faturamento mensal” (resolver o bug estrutural)

No seu novo schema você incluiu:

ProcessoAtual.faturamento_mensal_linha: Optional[float]

✅ Atualização no plano:
Definir prioridade única (e aplicar em todo lugar):

faturamento_mensal_linha (input direto) ✅

se não houver, derivar de producao_mensal * preco (se existir)

se não houver, derivar via cadência → produção anual → /12 → ×preço

E NUNCA zerar faturamento só porque preço unitário está vazio se faturamento mensal foi informado.

✅ Entregável:

função resolver_faturamento_mensal(...) no core/calculator.py

BasesComuns.faturamento_mensal explicitamente armazenado

P0.4 — Travas de coerência (alertas, não “deixa passar”)

Atualização direta no plano: criar “checagens CFO” antes de gerar resultado e PPTX:

Exemplos (automáticos):

preço peça = 0 mas faturamento mensal > 0 → alerta “incoerência”

horas_turno * turnos_dia > 24 → invalida

dias_ano > 365 → invalida

custo hora parada informado e faturamento mensal também informado → escolher um e avisar

✅ Entregável:

core/validators.py com validate_inputs() retornando lista de erros e warnings

UI mostrando warnings e impedindo export se houver erros

P0.5 — F10/F11: padronizar “custo hora parada”

No novo schema você colocou:

f10_custo_hora_parada e f11_custo_hora_parada (input manual)

Isso é perigoso: você passa a ter 3 fontes possíveis:

faturamento mensal

custo hora parada manual

custo hora parada derivado

✅ Atualização no plano:
Definir regra:

Se usuário informar custo_hora_parada manual, ele sobrepõe

Senão, calcular a partir do faturamento mensal

E gravar no resultado “fonte do custo hora parada” (manual vs derivado)

✅ Entregável:

BasesComuns.custo_hora_parada + BasesComuns.origem_custo_hora_parada

P0 — Testes obrigatórios (para travar regressões)

Você já previu testes; agora vira crítico.

P0.6 — Testes unitários para “sanidade de escala”

Além de “resultado esperado do PDF”, criar testes do tipo:

se pct_refugo = 10, deve virar 0.10

se faturamento_mensal = 10M e turnos=2, hora parada não pode ser “dobro” de cenário 1 turno (depende do modo)

payback não pode ser negativo

roi deve ser consistente com payback

✅ Entregável:

tests/test_sanity_ranges.py com testes de faixa (range)

P1 — Ajustes de modelo para evitar “ROI inflado” (sem matar o comercial)

Seu plano está forte no discurso CFO, então vale proteger o modelo.

P1.1 — Hora parada baseada em faturamento com opção de margem

Seu plano define hora parada com faturamento bruto. CFOs costumam preferir margem.

✅ Atualização no plano:
Adicionar campo opcional:

margem_contribuicao (já existe em F08) também pode ser usado como “ajuste” da hora parada:

custo_hora_parada = (faturamento_mensal * margem) / horas_mes

Ou:

Toggle “Hora parada em faturamento” vs “Hora parada em margem”.

Isso reduz os “absurdos” sem perder o argumento.

P1.2 — Ganho anual potencial: por fórmula (não “% do total”)

Seu novo plano já prevê metas por fórmula em MetasReducao.

✅ Atualização no plano:
Cálculo do ganho anual:

ganho = Σ (Fxx * meta_xx) somente para fórmulas selecionadas

guardar breakdown do ganho por fórmula (para explicar o ROI)

Isso elimina o “ganho mágico”.

P1 — UI com validação e tooltips (amarrado ao saneamento)

A UI deve impedir os inputs que detonam as contas.

P1.3 — UI deve pedir percentuais em “%” e armazenar como fração

Ex.: slider 0–100% exibindo “10%” e o backend recebe 0.10.
Isso evita o erro humano.

P2 — PPTX só depois de o motor estar estável

Seu plano tem PPTX na fase 4. Mantém, mas com 2 ajustes:

P2.1 — PPTX deve imprimir “premissas e fontes”

Inserir no slide de bases:

divisor hora operador (176)

divisor hora extra (220)

hora parada: (modo usado) + origem (manual/derivada)

fator encargos selecionado

Isso reduz “parece inconsistente” na hora da reunião.

Sequência de execução (plano final atualizado)
Semana/rodada 1 (P0 – hoje/amanhã)

Implementar validators.py (percentuais + ranges + coerência)

Refatorar formulas.py:

separar horas (176 vs 220 vs operação)

resolver faturamento mensal com prioridade correta

custo hora parada com regra definida

Rodar testes de sanidade + exemplos do PDF

Só então: plugar na UI

Semana/rodada 2 (P1)

Metas por fórmula (ganho anual explicado)

Toggle margem vs faturamento para hora parada (se quiser CFO-grade)

Dashboard com breakdown do ganho

Semana/rodada 3 (P2)

PPTX com premissas e fontes explícitas