# Motor Preditivo de Eficiência de Mídia (Long-Tail) — Gillette

Este projeto é uma solução de Inteligência Competitiva e Data Science desenvolvida para a **Gillette**. O objetivo é estruturar um motor de dados que valide a viabilidade financeira da alocação de orçamento de marketing em criadores de conteúdo de nicho (*Creator Economy* e *Storytelling* denso) em detrimento da exclusividade em mídias de massa tradicionais.

O projeto utiliza métricas reais extraídas do YouTube para criar um modelo matemático que projeta o **Custo por Visualização (CPV)** e o **ROI Perpétuo** de campanhas digitais.

---

## 1. Arquitetura de Dados e Pipeline (Medallion)

A infraestrutura do projeto foi desenhada seguindo as melhores práticas de Engenharia e Ciência de Dados corporativa:
*   **Camada Bronze (Ingestão):** Extração em lote (*Batch ETL*) via YouTube Data API v3, com sanitização de *Shorts* para garantir foco em retenção profunda.
*   **Camada Prata (Feature Engineering):** Construção de variáveis de negócio, incluindo Taxa de Engajamento Profundo (TEP) e *Cohorts* de maturação de conteúdo (Idade do Vídeo).
*   **Camada Ouro (Data Mart e ML):** Aplicação de algoritmos de Regressão Linear para projetar a curva de crescimento perpétuo (*Long-Tail*) e calcular o custo financeiro preditivo.

## 2. Estrutura do Repositório

```text
├── dados/                      # Data Warehouse Local (SQLite - Oculto via .gitignore)
├── src/                        # Scripts Python (ETL e Machine Learning)
├── venv/                       # Ambiente Virtual (Oculto via .gitignore)
├── .env                        # Gerenciamento de Segredos e API Keys
├── .gitignore                  # Governança de versionamento
├── requirements.txt            # Dependências do projeto
└── README.md                   # Documentação do Kick-off Estratégico
```