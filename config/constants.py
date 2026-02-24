"""
Parâmetros ARV V2.0 (constantes do sistema).
Baseado no documento "Custo da Inação V2.0 Revisado" (ver `CLAUDE.md`).
"""

# =============================================================================
# REGRA #1: Fatores de Encargos Trabalhistas
# =============================================================================

FATOR_ENCARGOS_CONSERVADOR = 1.7  # Lucro Real/Presumido (PADRÃO)
FATOR_ENCARGOS_MEDIO = 1.85  # + VT, VR
FATOR_ENCARGOS_COMPLETO = 2.0  # + Saúde, Seguro

FATOR_ENCARGOS_OPCOES: dict[str, float] = {
    "Conservador (1,7x) - Encargos obrigatórios": FATOR_ENCARGOS_CONSERVADOR,
    "Médio (1,85x) - + VT/VR": FATOR_ENCARGOS_MEDIO,
    "Completo (2,0x) - + Saúde/Seguro": FATOR_ENCARGOS_COMPLETO,
}

# =============================================================================
# REGRA #2: Divisores de horas
# =============================================================================

# Para custo real/hora (alocação de custo de produção)
HORAS_MES_CUSTO_PRODUCAO = 176  # 44h/semana × 4 semanas

# Para cálculos CLT/horas extras (quando aplicável)
HORAS_MES_CLT = 220

# =============================================================================
# Fatores de cálculo (benchmarks conservadores)
# =============================================================================

FATOR_ADICIONAL_HORA_EXTRA = 1.5  # adicional de 50% sobre hora normal
FATOR_CUSTO_TURNOVER_DEFAULT = 1.5  # 1,5 a 3,0 (benchmark)

# =============================================================================
# Defaults de input (sugestões para formulário)
# =============================================================================

SALARIO_OPERADOR_DEFAULT = 2500.0  # R$
SALARIO_INSPETOR_DEFAULT = 3000.0  # R$
SALARIO_SUPERVISOR_DEFAULT = 5000.0  # R$

DIAS_OPERACAO_ANO_DEFAULT = 250
DIAS_OPERACAO_MES_DEFAULT = 21  # usado para estimativa de produção mensal via cadência
