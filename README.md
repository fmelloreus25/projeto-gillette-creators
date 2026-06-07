# Motor Preditivo de Eficiência de Mídia (Long-Tail) — Gillette

Este projeto é uma solução avançada de Inteligência Competitiva e Data Science desenvolvida para a **Gillette**. O objetivo é estruturar um motor matemático que valide a viabilidade financeira da alocação de orçamento de marketing na *Creator Economy* (Storytelling denso de nicho) em detrimento da exclusividade em mídias de massa tradicionais.

---

## 1. O Cenário de Negócio (Pitch Comercial)

Para maximizar o Retorno sobre o Investimento (ROI) durante a Copa do Mundo de 2026, propomos uma estratégia de **SEO e Retenção Profunda**. 
Ao invés de comprar inserções caras no dia do jogo, a Gillette patrocinará um conteúdo perene (Cauda Longa) que será publicado **exatamente 30 dias antes do início da Copa**. Isso permite que o algoritmo do YouTube indexe o vídeo, criando uma base sólida. Quando as buscas globais por futebol explodirem, o vídeo já estará ranqueado, surfando o pico de tráfego a um Custo por Visualização (CPV) marginal.

## 2. Arquitetura de Dados e Machine Learning

A infraestrutura do projeto foi desenhada seguindo as melhores práticas de Engenharia de Dados e Estatística:

* **Camada Bronze (Ingestão):** Extração em lote via YouTube Data API v3, focando em retenção profunda (exclusão de Shorts).
* **Camada Prata e Ouro (Modelagem):** Feature Engineering (Cálculo de TEP - Taxa de Engajamento Profundo) e Regressão Linear.
* **Módulo de Simulação (Distribuição Gaussiana):** Para modelar o "Hype" da Copa do Mundo com precisão, desenvolvemos um simulador isolado (`simulador_campanha.py`). Ele abandona multiplicadores estáticos e aplica uma Curva de Sino (Gaussiana) para prever o pico exato de visualizações no dia 30 e o subsequente decaimento (decay) pós-evento.

### 2.1. Decisão Arquitetural (ADR): Sandbox de Simulação vs. DAX In-Memory

Durante a fase de modelagem no Power BI, foi deliberada a estratégia de processamento da Curva Gaussiana. Havia duas abordagens possíveis:
1. **In-Memory DAX:** Calcular a distribuição normal matematicamente "on the fly" via DAX, sem importar novas tabelas.
2. **Sandbox de Simulação (Fato Isolada):** Gerar os dados em Python e importá-los como uma tabela Fato independente (`Fato_Simulacao_Copa`), ligando-a ao modelo via uma dimensão compartilhada de tempo de vida (`Dim_Idade_Dias`).

**A Escolha:** Optamos pela abordagem **Sandbox de Simulação (Opção 2)**.
* **Justificativa:** Embora a abordagem *In-Memory* otimize o peso do arquivo por não exigir tabelas adicionais, injetar simulações preditivas diretamente no motor DAX sobre os dados reais fere o princípio de **Isolamento de Cenários (What-If)**. Ao manter a simulação em uma tabela Fato separada (de peso irrisório, apenas 180 linhas), garantimos a integridade imaculada dos dados históricos de performance da base. Essa arquitetura (Star Schema avançado) permite auditar a simulação de forma independente e garante a governança do dado real versus o dado hipotético.

## 3. Estrutura do Repositório

    ├── dados/                      # Data Warehouse Local (SQLite e Data Marts em CSV)
    ├── src/                        
    │   ├── extrator_youtube.py     # Script principal de Ingestão (ETL)
    │   ├── modelagem_dados.py      # Motor de Inteligência Base
    │   └── simulador_campanha.py   # Módulo Avançado de Curva Gaussiana (Hype)
    ├── venv/                       # Ambiente Virtual isolado
    ├── .env                        # Cofre de Credenciais
    ├── requirements.txt            # Dependências (Pandas, Numpy, Scikit-Learn)
    └── README.md                   

## 4. Como Executar o Simulador Gaussiano

Para reproduzir a curva matemática de simulação da campanha de 2026:
1. Ative o ambiente virtual e garanta a instalação do pacote numérico: `pip install numpy pandas`.
2. Execute o simulador: `python src/simulador_campanha.py`.
3. O artefato analítico `simulacao_gillette_copa.csv` será gerado na pasta `/dados/`, pronto para ser consumido via Power BI para análise de Time Series.