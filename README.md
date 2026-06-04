# Motor Preditivo de Eficiência de Mídia (Long-Tail) — Gillette

Este projeto é uma solução de Inteligência Competitiva e Data Science desenvolvida para a **Gillette**. O objetivo é estruturar um motor de dados que valide a viabilidade financeira da alocação de orçamento de marketing em criadores de conteúdo de nicho (*Creator Economy* e *Storytelling* denso) em detrimento da exclusividade em mídias de massa tradicionais.

---

## 1. Arquitetura de Dados e Pipeline (Medallion)

A infraestrutura do projeto foi desenhada seguindo as melhores práticas de Engenharia e Ciência de Dados:
* **Camada Bronze (Ingestão):** Extração em lote via YouTube Data API v3, focando em retenção profunda (exclusão de Shorts).
* **Camadas Prata e Ouro (Modelagem):** Feature Engineering (Cálculo de TEP - Taxa de Engajamento Profundo) e aplicação de Machine Learning (Regressão Linear) para projeção de Cauda Longa e Cenário Sazonal (Hype Copa do Mundo).

## 2. Status do Projeto (Roadmap)

- [x] **Fase 0:** Planejamento Estratégico e Setup de Ambiente (Venv, Git).
- [x] **Fase 1 (Data Engineering):** Construção do Extrator de API e povoamento da Camada Bronze.
- [x] **Fase 2 (Data Science):** Feature Engineering e ML de Projeção Sazonal/Orgânica.
- [ ] **Fase 3 (Business Intelligence):** Dashboard Narrativo (Pendente).

## 3. Estrutura do Repositório

    ├── dados/                      # Data Warehouse Local (SQLite - Oculto)
    ├── src/                        
    │   ├── extrator_youtube.py     # Script principal de Ingestão (ETL)
    │   └── modelagem_dados.py      # Motor de Inteligência e Cenários Preditivos
    ├── venv/                       # Ambiente Virtual (Oculto)
    ├── .env                        # Cofre de Credenciais
    ├── .gitignore                  
    ├── requirements.txt            
    └── README.md                   

## 4. Como Configurar e Executar as Fases 1 e 2

O pipeline conecta aos servidores do Google, extrai as métricas, aplica os algoritmos de regressão e gera os cenários de custo para a diretoria.

**Passo a passo da execução:**
1. Clone o repositório e ative o ambiente virtual (`venv`).
2. Instale as dependências: `pip install -r requirements.txt`.
3. Crie um arquivo `.env` na raiz do projeto: `YOUTUBE_API_KEY="sua_chave"`.
4. Execute a Ingestão (Fase 1): `python src/extrator_youtube.py`
5. Execute a Modelagem (Fase 2): `python src/modelagem_dados.py`

**Resultado:** O arquivo `banco_gillette_campanha.db` abrigará a Tabela Bronze (dados brutos) e a Tabela Ouro Analítica (projeções prontas para o BI).