# ROI Calculator — Automação Industrial

Ferramenta web para quantificar o retorno sobre investimento (ROI) de projetos de automação industrial e gerar apresentações PPTX customizadas.

## Funcionalidades

- Formulário de input com dados do cliente e processo
- Seleção de 17 dores/custos em 4 categorias (CO, QL, SE, PR)
- Motor de cálculo com fórmulas detalhadas
- Dashboard com métricas (Payback, ROI 1/3/5 anos)
- Geração de apresentação PPTX com 16 slides

## Stack

- Python 3.10+
- Streamlit
- python-pptx
- pandas

## Setup Local

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
streamlit run app.py
```

## Testes

```bash
pip install pytest
python -m pytest tests/ -v
```

## Estrutura

```
├── app.py                   # Entry point
├── config/constants.py      # Parâmetros do sistema
├── models/                  # Dataclasses (inputs, calculations, results)
├── core/                    # Motor de cálculo, fórmulas, validadores
├── ui/                      # Formulários, dashboard, estilos
├── export/                  # Gerador PPTX (16 slides)
└── tests/                   # Testes unitários
```
