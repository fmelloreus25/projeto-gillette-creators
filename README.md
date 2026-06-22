# Gillette Creator Economy: Motor Preditivo de Mídia & Simulação Financeira (MMM)

## 📌 1. Sumário Executivo
Este projeto implementa uma solução de **Marketing Mix Modeling (MMM)** e inteligência de dados de ponta a ponta para avaliar a viabilidade financeira, o fluxo de caixa operacional e o **Earned Media Value (EMV)** de uma campanha de marketing de influência com a marca **Gillette**. 

O estudo de caso utiliza dados históricos de retenção e tráfego do criador de conteúdo **Andrey** para simular o comportamento de um ativo de mídia patrocinado escalado sob o efeito sazonal de alto impacto da **Copa do Mundo de 2026**. 

A solução combina um motor de engenharia e modelagem matemática construído em **Python** com um simulador dinâmico de tomada de decisão (What-If Analysis) desenvolvido em **Power BI**, provando tecnicamente como um investimento fixo de **$30.000,00** em um pacote de influência pode ser otimizado através da ciência de dados e da **arbitragem de atenção**.

---

## 📊 2. Arquitetura da Solução e Data Pipeline
O projeto foi estruturado seguindo os princípios de uma arquitetura de dados moderna e modular (*Lakehouse/Data Mart Local*), dividida em camadas lógicas para garantir governança, performance e reprodutibilidade:

    projeto_gillette/
    ├── dados/                             # Armazenamento de Data Assets
    │   ├── banco_gillette_campanha.db     # Camada Bronze & Prata (SQLite Data Lake)
    │   ├── data_mart_gillette.csv         # Camada Ouro (Histórico Tratado)
    │   └── simulacao_gillette_copa.csv    # Camada Ouro (Modelagem Preditiva)
    ├── src/                               # Código Fonte (Módulos Python)
    │   ├── extrator_youtube.py            # Ingestão de dados brutos
    │   ├── modelagem_dados.py             # Pipeline de transformação (Medallion)
    │   └── simulador_campanha.py          # Motor matemático das curvas
    ├── projeto-gillette.pbix              # Camada de Visualização & Analytics (Power BI)
    └── README.md                          # Documentação Técnica Executiva


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

### As Equações do Modelo:

#### 1. Baseline Orgânico (Lei de Potência / Decaimento do YouTube)
O comportamento de visualizações diárias de um vídeo orgânico segue uma curva de decaimento acentuada nas primeiras 48 horas (notificações) estabilizando-se em uma cauda longa. Esse fenômeno é modelado através de uma **Lei de Potência (Power Law)**:

$$Views_{Baseline}(t)=\frac{V_{max}}{t^{\alpha}}$$

*Onde $t$ é a idade do vídeo em dias, $V_{max}$ é o pico do Dia 1 e $\alpha$ é o fator de inclinação do decaimento algorítmico.*

> **Resultado:** O modelo gerou um acumulado consolidado de **~515 mil views orgânicas totais** ao fim de 180 dias.

#### 2. Lift Incremental (Curva Gaussiana Aditiva de Hype)
O impacto promocional gerado pela Copa do Mundo foi modelado utilizando uma **Função Gaussiana (Distribuição Normal)**, assumindo que o "Boom" de tráfego cresce e decai organicamente ao redor do ápice do evento esportivo (Efeito Halo):

$$Views_{Hype}(t)=P_{max} \times e^{-\frac{(t - t_{pico})^2}{2\sigma^2}}$$

*Onde $P_{max}$ é o teto máximo de views injetadas, $t_{pico}$ é o dia do ápice do evento (Dia 30) e $\sigma$ é o desvio padrão da janela de atenção.*

> **Resultado:** O tráfego acumulado sob o cenário de Hype atingiu **3.054.779 de visualizações totais**, um descolamento estatístico de **5,9x** sobre o comportamento orgânico da mídia.

---

## 💸 4. A Tese de Negócios: Arbitragem de Mídia e Valor de Marca (EMV)
A genialidade deste projeto não reside apenas em prever o funil de vendas diretas, mas em provar o valor do **Brand Awareness** financeiramente. O motor DAX do Power BI foi programado para comparar o custo real da nossa operação com o custo do leilão tradicional de anúncios.

### A Defesa do Déficit Operacional (Gráfico de Cascata)
O painel escancara um risco comum na Creator Economy: **Vendas diretas raramente pagam o custo integral do projeto no curto prazo**. 
* Com o pacote de influência custando **$30.000,00**, e simulando uma conversão crua de **0,10%** com um ticket médio de **$10,00**, o Gráfico de Cascata reporta um fluxo de caixa negativo imediato (Déficit operacional de ~$29 Mil). 

### A Virada de Mesa: Earned Media Value (EMV)
Para justificar o investimento C-Level, o simulador calcula o custo equivalente da mesma atenção qualificada na plataforma de anúncios do Google (TrueView/YouTube Ads).

A fórmula dinâmica processada via DAX considera a taxa padrão de mercado de 20% de *View-Through Rate* (VTR) exigida pelo Google para cobrar por uma visualização qualificada:

$$Custo_{Ads}=\left( \frac{Tr\acute{a}fego \times Reten\text{\c{c}}\tilde{a}o}{VTR} \right) \times \left( \frac{CPM_{Google}}{1000} \right)$$

Ao cruzar os parâmetros dos *sliders* executivos (ex: Retenção de 60% e um CPM inflacionado de Hype a $55,00), o dashboard revela que **comprar os mesmos 96 Mil usuários engajados no Google Ads custaria cerca de $159.000,00**. 

> **O Xeque-Mate:** Pagando apenas os $30.000,00 acordados com o criador, a marca realizou uma arbitragem de mídia brutal, gerando uma economia imediata (EMV) de **$129.040,00** para os cofres da Gillette.

---

## 🖥️ 5. Visualizações do Painel (Screenshots)

### Página 1: Eficiência de Mídia e Calibragem de Adstock
*(Insira a imagem `dashboard_page1.png` aqui na pasta images e ajuste o link)*
*Foco visual: Comparativo de CPM (Mercado vs. Hype) e expansão preditiva das curvas de tráfego.*

### Página 2: Simulador Dinâmico e Defesa de Investimento
*(Insira a imagem `dashboard_page2.png` aqui na pasta images e ajuste o link)*
*Foco visual: Painel de What-If Analysis à esquerda. No centro, a transparência do déficit de caixa na Cascata. Na base, a prova matemática do sucesso da campanha através da economia gerada (EMV) comparada ao leilão do Google Ads.*

---

## 🛠️ 6. Como Executar o Projeto

### Pré-requisitos
* Python 3.10+
* Power BI Desktop

### 1. Clonar o repositório e instalar dependências:
```bash
git clone [https://github.com/fmelloreus25/projeto-gillette-creators.git](https://github.com/fmelloreus25/projeto-gillette-creators.git)
cd projeto-gillette-creators
pip install -r requirements.txt

2. Rodar o motor matemático de engenharia de dados:

python src/modelagem_dados.py

(Este comando lerá o banco SQLite local, executará as equações complexas e atualizará os arquivos CSV estruturados dentro da pasta dados/)

3. Atualizar o Simulador Executivo:
Abra o arquivo projeto-gillette.pbix no Power BI Desktop e clique no botão Atualizar 

(Refresh) na página inicial. Toda a malha de visualizações, medidas DAX e parâmetros What-If se recalibrará automaticamente com o novo output gerado pelo Python.