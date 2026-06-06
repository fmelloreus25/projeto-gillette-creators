import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Simulador-Gillette-Agencia")

class SimuladorHypeCopa:
    def __init__(self):
        # Premissas do Contrato
        self.investimento = 10000.00
        self.dias_projecao = 180
        
        # O Cenário de Negócio: Postagem 30 dias antes da Copa
        self.dia_do_pico = 30 
        
        # A Força do Hype: O evento multiplica o tráfego em até 3x (1 + 2) no ápice
        self.forca_do_hype = 2.0 
        
        # Sigma (Janela): 15 dias. Isso cria uma curva que começa a subir forte no dia 10,
        # atinge o topo no dia 30, e vai decaindo suavemente até o fim do torneio (dia 60).
        self.janela_hype = 15.0 

    def gerar_time_series(self):
        logger.info("Iniciando simulação do funil de retenção (30 Dias Pré-Copa)...")
        
        dias = np.arange(1, self.dias_projecao + 1)
        df_simulacao = pd.DataFrame({'idade_dias': dias})
        
        # 1. Base Orgânica: O vídeo traciona rápido e cria uma base sólida (Indexação do YouTube)
        df_simulacao['views_base'] = 50000 * np.log1p(df_simulacao['idade_dias'])
        
        # 2. Curva Gaussiana (O Algoritmo do Hype)
        expoente = -((df_simulacao['idade_dias'] - self.dia_do_pico)**2) / (2 * (self.janela_hype**2))
        df_simulacao['multiplicador_gaussiano'] = 1 + (self.forca_do_hype * np.exp(expoente))
        
        # 3. O Resultado Entregue à Gillette
        df_simulacao['views_projetadas_hype'] = df_simulacao['views_base'] * df_simulacao['multiplicador_gaussiano']
        
        # 4. A Queda do CPV (A Prova Financeira)
        df_simulacao['cpv_diario'] = self.investimento / df_simulacao['views_projetadas_hype']
        
        # Formatação para o Business Intelligence
        df_simulacao['views_base'] = df_simulacao['views_base'].astype(int)
        df_simulacao['views_projetadas_hype'] = df_simulacao['views_projetadas_hype'].astype(int)
        df_simulacao['multiplicador_gaussiano'] = df_simulacao['multiplicador_gaussiano'].round(3)
        df_simulacao['cpv_diario'] = df_simulacao['cpv_diario'].round(4)
        
        return df_simulacao

    def exportar_resultado(self, df):
        caminho = 'dados/simulacao_gillette_copa.csv'
        df.to_csv(caminho, index=False, sep=';', decimal=',')
        logger.info(f"Pitch gerado com sucesso! Arquivo exportado para: {caminho}")

if __name__ == "__main__":
    simulador = SimuladorHypeCopa()
    df_resultado = simulador.gerar_time_series()
    simulador.exportar_resultado(df_resultado)