# Motor Preditivo de Eficiência de Mídia (Long-Tail) — Gillette

Este projeto é uma solução de Inteligência Competitiva e Data Science desenvolvida para a **Gillette**. O objetivo é estruturar um motor de dados que valide a viabilidade financeira da alocação de orçamento de marketing em criadores de conteúdo de nicho (*Creator Economy* e *Storytelling* denso) em detrimento da exclusividade em mídias de massa tradicionais.

---

## 1. Arquitetura de Dados e Pipeline (Medallion)

A infraestrutura do projeto foi desenhada seguindo as melhores práticas de Engenharia:
* **Camada Bronze (Ingestão):** Extração em lote via YouTube Data API v3, focando em retenção profunda (exclusão de Shorts). Dados armazenados em SQLite.

## 2. Status do Projeto (Roadmap)

- [x] **Fase 0:** Planejamento Estratégico e Setup de Ambiente (Venv, Git).
- [x] **Fase 1 (Data Engineering):** Construção do Extrator de API e povoamento da Camada Bronze.
- [ ] **Fase 2 (Data Science):** Feature Engineering e Regressão Linear (Pendente).
- [ ] **Fase 3 (Business Intelligence):** Dashboard Narrativo (Pendente).

## 3. Estrutura do Repositório

    ├── dados/                      # Data Warehouse Local (SQLite - Oculto via .gitignore)
    ├── src/                        
    │   └── extrator_youtube.py     # Script principal de Ingestão (ETL)
    ├── venv/                       # Ambiente Virtual (Oculto)
    ├── .env                        # Cofre de Credenciais (Requer YOUTUBE_API_KEY)
    ├── .gitignore                  
    ├── requirements.txt            
    └── README.md                   

## 4. Como Configurar e Executar a Fase 1

O pipeline atual é responsável por conectar aos servidores do Google, extrair as métricas brutas de canais de nicho e descarregar no Data Warehouse local.

**Passo a passo da execução:**
1. Clone o repositório e ative o ambiente virtual (`venv`).
2. Instale as dependências: `pip install -r requirements.txt`.
3. Crie um arquivo `.env` na raiz do projeto contendo a sua chave oficial do Google Cloud: `YOUTUBE_API_KEY="sua_chave"`.
4. Execute o motor de extração:
   `python src/extrator_youtube.py`

**Resultado Esperado:** O script fará a paginação da API, removerá vídeos curtos (< 60s) e criará o arquivo `banco_gillette_campanha.db` dentro da pasta `dados/` contendo a `tb_videos_performance`.