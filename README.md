# Calculadora do Custo da Inação — V2.0

Ferramenta web (Streamlit) para acelerar propostas comerciais de automação industrial quantificando o **Custo da Inação** (“quanto custa NÃO automatizar?”) e gerando uma apresentação **PPTX** executiva.

## Conceito (V2.0)

- **Custo da Inação**: custo anual de manter um processo manual (perdas por mão de obra, qualidade, produtividade, segurança e custos ocultos).
- **Estrutura**: **5 Dores** + **18 fórmulas** (F01–F18).
- **Premissas CFO-friendly**:
  - **Encargos trabalhistas selecionáveis**: 1,7 / 1,85 / 2,0
  - **Custo-hora operador (custeio)**: divisor **176h**
  - **Horas extras (CLT)**: hora base com divisor **220h** (+ adicional de 50%)
  - **Custo-hora parada (CHP)**: baseado em **horas reais de operação do processo**:
    - \( CHP = \frac{faturamento\_mensal}{horas\_turno \times turnos\_dia \times (dias\_ano/12)} \)
  - **Percentuais**: o sistema valida/normaliza campos críticos para evitar erros de unidade (ex.: 10% digitado como `10` → `0.10`).

## Funcionalidades

- Formulário V2.0 (cliente + processo atual)
- **Seleção de Área ARV** com **pré-seleção** de fórmulas aplicáveis
- Parâmetros detalhados condicionais por fórmula (F01–F18)
- Metas de redução por fórmula
- Faturamento mensal pode ser **auto-calculado** (via preço de venda) com opção de **override manual** (checkbox)
- Dashboard: Custo total anual, ganho anual potencial, payback, ROI (1–5 anos) + breakdown por Dor e por fórmula
- Exportação de **PPTX** programático (16+ slides) com narrativa “Custo da Inação”

## Stack

- Python 3.10+
- Streamlit
- python-pptx
- pandas

## Rodando localmente

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
streamlit run app.py
```

## Testes

```bash
python -m pytest tests/ -v
```

## Deploy (VPS + Docker Swarm + Traefik)

Este repositório inclui CI/CD via GitHub Actions que:

- Builda e publica a imagem no `ghcr.io`
- Faz deploy automático no VPS via `docker stack deploy` (stack `roi-calculator`)

### Pré-requisitos no VPS

- Docker Swarm inicializado
- Traefik já configurado no Swarm (SSL automático)
- Rede overlay externa existente: `network_public`

### Secrets no GitHub (Actions)

Estes secrets precisam existir no repositório:

- `VPS_HOST`
- `VPS_USER`
- `VPS_SSH_KEY`

### Como funciona

- Workflow: `.github/workflows/deploy.yml`
- Compose de produção: `docker-compose.prod.yml`
- Domínio: `roi-calculator.arvsystems.cloud`
- Porta interna do container (Streamlit): `8501`

### Rollback

Cada build gera uma tag com SHA curto. Para reverter manualmente no VPS:

```bash
docker service update --image ghcr.io/<owner>/roi-calculator:<sha> roi-calculator_roi-calculator
```

## Estrutura

```
├── app.py                   # Entry point
├── config/                  # Constantes V2.0 + Áreas ARV → fórmulas
├── models/                  # Dataclasses V2.0 (inputs, calculations, results)
├── core/                    # Motor V2.0 (F01–F18), calculator, validators
├── ui/                      # Formulários + dashboard
├── export/                  # Gerador PPTX (programático)
└── tests/                   # Testes unitários
```
