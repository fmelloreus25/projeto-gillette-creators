# Gillette Creator Economy: Motor Preditivo de Mídia & Simulação Financeira (MMM)

## 📌 1. Sumário Executivo
Este projeto implementa uma solução de **Marketing Mix Modeling (MMM)** e inteligência de dados de ponta a ponta para avaliar a viabilidade financeira e o retorno sobre o investimento (ROI) de uma campanha de marketing de influência com a marca **Gillette**. 

O estudo de caso utiliza dados históricos de retenção e tráfego do criador de conteúdo **Andrey** para simular o comportamento de um ativo de mídia patrocinado escalado sob o efeito sazonal de alto impacto da **Copa do Mundo de 2026**. 

A solução combina um motor de engenharia e modelagem matemática construído em **Python** com um simulador dinâmico de tomada de decisão (What-If Analysis) desenvolvido em **Power BI**, provando tecnicamente como um investimento fixo de **$10.000,00** pode ser otimizado através da ciência de dados.

---

## 📊 2. Arquitetura da Solução e Data Pipeline
O projeto foi estruturado seguindo os princípios de uma arquitetura de dados moderna e modular (*Lakehouse/Data Mart Local*), dividida em camadas lógicas para garantir governança, performance e reprodutibilidade:

    projeto_gillette/
    ├── dados/                           # Armazenamento de Data Assets
    │   ├── banco_gillette_campanha.db   # Camada Bronze & Prata (SQLite Data Lake)
    │   ├── data_mart_gillette.csv       # Camada Ouro (Histórico Tratado)
    │   └── simulacao_gillette_copa.csv  # Camada Ouro (Modelagem Preditiva)
    ├── src/                             # Código Fonte (Módulos Python)
    │   ├── extrator_youtube.py          # Ingestão de dados brutos
    │   ├── modelagem_dados.py           # Pipeline de transformação (Medallion)
    │   └── simulador_campanha.py        # Motor matemático das curvas
    ├── projeto-gillette.pbix            # Camada de Visualização & Analytics (Power BI)
    └── README.md                        # Documentação Técnica Executiva

### O Pipeline de Dados (Camadas Medallion):
* **Camada Bronze (Bruta):** O script `extrator_youtube.py` consome e consolida o histórico real de performance de vídeos do canal. Os dados são injetados diretamente em tabelas relacionais em um banco de dados SQLite.
* **Camada Prata (Limpeza e Feature Engineering):** No módulo `modelagem_dados.py`, os dados brutos passam por processos de higienização de strings, tratamento de anomalias temporárias, conversão de tipos e cálculo da **TEP** (Taxa de Engajamento Profundo).
* **Camada Ouro (Modelagem e Consumo):** O motor de simulação aplica os modelos estatísticos preditivos para gerar os eventos marginais diários de tráfego ao longo de 180 dias de projeção, exportando os Data Marts limpos em `.csv` prontos para ingestão de alta performance no Power BI.

---

## 📐 3. Modelagem Matemática e Engenharia de Mídia
Para simular com precisão o comportamento do tráfego do YouTube e o impacto do patrocínio da Gillette, o motor preditivo rejeitou médias lineares simples e adotou modelos de comportamento humano e efeito Adstock de mercado.

### A Curva de Tráfego do Dashboard:
* **Linha Azul (Baseline Orgânico):** Representa o comportamento esperado de um vídeo comum e não impulsionado.
* **Linha Amarela (Projeção Sazonal/Hype Copa):** Representa o efeito aditivo e o descolamento de tráfego gerado pela campanha patrocinada da Gillette surfando a janela de atenção da Copa do Mundo.

           Views Diárias
              ^             /\  <- Linha Amarela (Hype Sazonal)
              |            /  \
              |  /\       /    \
              | /  \_____/------\---------> Linha Azul (Baseline Orgânico)
              +-----------------------------> Idade do Vídeo (Dias)
                Dia 1    Dia 30 (Pico Copa)

### As Equações do Modelo:

#### 1. Baseline Orgânico (Lei de Potência / Decaimento do YouTube)
O comportamento de visualizações diárias de um vídeo orgânico segue uma curva de decaimento acentuada nas primeiras 48 horas (notificações) estabilizando-se em uma cauda longa. Esse fenômeno é modelado através de uma **Lei de Potência (Power Law)**:

$$Views_{Baseline}(t) = \frac{V_{max}}{t^{\alpha}}$$

Onde:
* $t$: Idade do vídeo em dias ($1 \le t \le 180$).
* $V_{max}$: O pico de visualizações do Dia 1 (calibrado historicamente em 42.000 views).
* $\alpha$: Fator de inclinação do decaimento do algoritmo (calibrado em 0.72).

> **Resultado:** O modelo gerou um acumulado consolidado de **~515 mil views orgânicas totais** ao fim de 180 dias, alinhado à média histórica real do canal.

#### 2. Lift Incremental (Curva Gaussiana Aditiva de Hype)
O impacto promocional e o ganho de tração algorítmica gerados pela Copa do Mundo foram modelados utilizando uma **Função Gaussiana (Distribuição Normal)**. O modelo assume que o "Boom" de tráfego cresce e decai organicamente ao redor de uma data centralizada (Efeito Halo):

$$Views_{Hype}(t) = P_{max} \times e^{-\frac{(t - t_{pico})^2}{2\sigma^2}}$$

Onde:
* $P_{max}$: O teto máximo de views diárias injetadas pelo hype (calibrado em 85.000 views/dia).
* $t_{pico}$: O dia exato do ápice do evento (definido no Dia 30 da campanha).
* $\sigma$ (Sigma): O desvio padrão que controla a largura da janela de atenção da Copa (calibrado em 12.0 dias).

> **Resultado:** O tráfego acumulado sob o cenário de Hype atingiu o patamar de **3.054.779 de visualizações totais**, um descolamento estatístico de **5,9x** sobre o comportamento orgânico da mídia.

---

## 💸 4. Engenharia Financeira e Simulação Dinâmica de ROI
Toda a base matemática gerada pelo Python foi consumida no Power BI através de uma arquitetura de métricas baseada em **Measure Branching** no DAX. O painel financeiro implementa uma análise de cenários flexível (What-If) controlada por parâmetros executivos: a **Taxa de Conversão de Vendas** (0,1% a 5,0%) e o **Ticket Médio do Produto** ($2,00 a $150,00).

### O Ponto de Equilíbrio (Breakeven Analysis)
A grande vantagem competitiva deste simulador reside na capacidade de mapear o risco real da operação de marketing. Em um cenário altamente conservador, o modelo prova a robustez e a segurança do investimento:

* **Investimento Fixo de Mídia:** $10.000,00
* **Taxa de Engajamento Profundo (TEP) do Canal:** 10,00% (Garantindo uma audiência de **306.000 usuários engajados** de fundo de funil).
* **Ticket Mínimo Simulado:** $25,00

A equação do Ponto de Equilíbrio determina que a campanha atinge o custo zero (*breakeven*) com a conversão de apenas **400 unidades** do produto:

$$Breakeven = \frac{Investimento}{Ticket\ M\text{é}dio} = \frac{10000}{25} = 400\ \text{vendas}$$

Dado o universo de 306.000 usuários engajados gerados pelo motor de Hype, a taxa de conversão necessária para mitigar totalmente o risco financeiro da Gillette é de míseros **0,13%**:

$$Taxa\ Breakeven = \frac{400}{306000} \approx 0,13\%$$

Se a infraestrutura de e-commerce da marca garantir o padrão saudável de mercado de **1,0% de conversão**, o modelo prediz um volume de **3.060 vendas**, gerando uma Receita Bruta de **$107.100,00** e um **ROI Líquido de 971%**.

---

## 🖥️ 5. Visualizações do Painel (Screenshots)

### Página 1: Eficiência de Mídia e Calibragem de Adstock
<img src="images/dashboard_page1.png" width="100%">
*Foco visual: Comparativo de CPM (Mercado vs. Hype) e expansão das curvas das equações matemáticas até o dia 180.*

### Página 2: Simulador Dinâmico de Funil de Conversão e ROI
<img src="images/dashboard_page2.png" width="100%">
*Foco visual: Controles deslizantes (Sliders) de conversão e ticket interagindo diretamente com os cards de topo e o Gráfico de Cascata de fluxo de caixa.*

---

## 🛠️ 6. Como Executar o Projeto

### Pré-requisitos
* Python 3.10+
* Power BI Desktop

### 1. Clonar o repositório e instalar dependências:
    git clone [https://github.com/seu-usuario/projeto-gillette.git](https://github.com/seu-usuario/projeto-gillette.git)
    cd projeto-gillette
    pip install -r requirements.txt

### 2. Rodar o motor matemático de engenharia de dados:
    python src/modelagem_dados.py
*(Este comando lerá o banco SQLite local, executará as equações e atualizará os arquivos CSV estruturados dentro da pasta `dados/`)*

### 3. Atualizar o Painel:
Abra o arquivo `projeto-gillette.pbix` no Power BI Desktop e clique no botão **Atualizar (Refresh)** na página inicial. Toda a malha de visualizações e parâmetros What-If se recalibrará automaticamente com o novo output do Python.