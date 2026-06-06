import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import logging
import datetime
import warnings

warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Gillette-Data-Science")

class MotorModelagemGillette:
    def __init__(self):
        logger.info("Inicializando Motor de Data Science...")
        self.caminho_db = 'dados/banco_gillette_campanha.db'
        # Premissa de negócio: Simulando R$ 10.000 de investimento por patrocínio de vídeo
        self.investimento_por_video = 10000.00 

    def extrair_camada_bronze(self):
        """Lê os dados brutos gerados pela Engenharia de Dados."""
        logger.info("Lendo Camada Bronze do Data Warehouse local...")
        conexao = sqlite3.connect(self.caminho_db)
        df = pd.read_sql_query("SELECT * FROM tb_videos_performance", conexao)
        conexao.close()
        return df

    def engenharia_features_prata(self, df):
        """Cria as métricas de negócio (Camada Prata)."""
        logger.info("Construindo a Camada Prata (Feature Engineering)...")
        
        # 1. Taxa de Engajamento Profundo (TEP)
        df['taxa_engajamento_pct'] = ((df['qtd_likes'] + df['qtd_comentarios']) / df['qtd_visualizacoes'].replace(0, 1)) * 100
        
        # 2. Maturidade da Safra (Idade do Vídeo em dias)
        df['data_publicacao'] = pd.to_datetime(df['data_publicacao'])
        hoje = pd.to_datetime(datetime.date.today(), utc=True)
        df['idade_dias'] = (hoje - df['data_publicacao']).dt.days
        
        return df

    def modelagem_preditiva_ouro(self, df):
        """Aplica Regressão Linear e Fator Sazonal para projetar Cenários."""
        logger.info("Treinando modelo de Machine Learning e calculando Sazonalidade...")
        
        df_treino = df[df['idade_dias'] > 7].copy()
        
        if len(df_treino) < 3:
            logger.warning("Poucos dados maduros. Aplicando heurística de crescimento plano.")
            df['projecao_views_180_dias'] = df['qtd_visualizacoes'] * 1.2
        else:
            # O modelo entende o impacto do tempo nas visualizações (Cauda Longa Padrão)
            X = df_treino[['idade_dias']]
            y = df_treino['qtd_visualizacoes']
            
            modelo = LinearRegression()
            modelo.fit(X, y)
            
            # CENÁRIO 1: Projeção Orgânica (BaseLine)
            predicoes = modelo.predict([[180]] * len(df))
            df['projecao_views_180_dias'] = [max(real, pred) for real, pred in zip(df['qtd_visualizacoes'], predicoes)]

        # CENÁRIO 2: O Ouro da Gillette (Hype Pré-Copa)
        # Aplicamos um multiplicador de 50% (1.5x) sobre a projeção devido ao aumento de tráfego em storytelling de futebol
        fator_hype_copa = 1.50
        df['projecao_views_cenario_copa'] = df['projecao_views_180_dias'] * fator_hype_copa

        # Calculando a eficiência financeira (A queda do CPV)
        df['cpv_atual'] = self.investimento_por_video / df['qtd_visualizacoes'].replace(0, 1)
        df['cpv_preditivo_organico'] = self.investimento_por_video / df['projecao_views_180_dias']
        df['cpv_preditivo_copa'] = self.investimento_por_video / df['projecao_views_cenario_copa']
        
        return df

    def carregar_dados_ouro(self, df):
        """Salva a tabela analítica no banco e exporta um Data Mart físico para o Power BI."""
        logger.info("Salvando a Camada Ouro (tb_analitica_gillette) no banco...")
        conexao = sqlite3.connect(self.caminho_db)
        
        df['data_publicacao'] = df['data_publicacao'].astype(str)
        df.to_sql('tb_analitica_gillette', conexao, if_exists='replace', index=False)
        conexao.close()
        
        # --- A PORTA DOS FUNDOS PARA O POWER BI ---
        caminho_csv = 'dados/data_mart_gillette.csv'
        df.to_csv(caminho_csv, index=False, sep=';', decimal=',')
        logger.info(f"Fase 2 Concluída! Data Mart físico exportado para: {caminho_csv}")

if __name__ == "__main__":
    motor = MotorModelagemGillette()
    df_bronze = motor.extrair_camada_bronze()
    df_prata = motor.engenharia_features_prata(df_bronze)
    df_ouro = motor.modelagem_preditiva_ouro(df_prata)
    motor.carregar_dados_ouro(df_ouro)