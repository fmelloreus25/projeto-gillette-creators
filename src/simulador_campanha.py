import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Simulador-MMM-Enterprise")

class SimuladorAdstockCopa:
    def __init__(self):
        self.investimento = 10000.00
        self.dias_projecao = 180
        
        # O Cenário de Negócio
        self.dia_do_pico = 30 
        self.janela_hype_sigma = 12.0 # Curva levemente mais estreita para concentrar o boom
        
        # Volumes Calibrados com o Histórico (Teto de 714k do Canal)
        self.max_views_diarias_organico = 35000 
        self.pico_views_diarias_hype = 85000 # No ápice da Copa, fará 85k views NUM ÚNICO DIA

    def gerar_time_series(self):
        logger.info("Iniciando recalibragem estatística de Mídia (Eventos Marginais Diários)...")
        
        dias = np.arange(1, self.dias_projecao + 1)
        df_simulacao = pd.DataFrame({'idade_dias': dias})
        
        # 1. Base Orgânica: Decaimento de Pareto (Forte no início, estabiliza numa cauda longa)
        # O expoente 0.65 cria a rampa natural do YouTube
        df_simulacao['views_diarias_organicas'] = self.max_views_diarias_organico / (df_simulacao['idade_dias'] ** 0.65)
        
        # 2. O Evento Sazonal (Gaussiana Aditiva)
        expoente = -((df_simulacao['idade_dias'] - self.dia_do_pico)**2) / (2 * (self.janela_hype_sigma**2))
        df_simulacao['views_diarias_hype'] = self.pico_views_diarias_hype * np.exp(expoente)
        
        # 3. O Total Diário Gerado
        df_simulacao['views_projetadas_hype'] = df_simulacao['views_diarias_organicas'] + df_simulacao['views_diarias_hype']
        
        # 4. A Prova Financeira (Custo da Mídia)
        df_simulacao['cpv_diario'] = self.investimento / df_simulacao['views_projetadas_hype']
        
        # Formatação Executiva
        df_simulacao['views_base_acumulada_teste'] = df_simulacao['views_projetadas_hype'].cumsum() # Apenas para o cientista validar se o teto faz sentido
        df_simulacao['views_projetadas_hype'] = df_simulacao['views_projetadas_hype'].astype(int)
        df_simulacao['cpv_diario'] = df_simulacao['cpv_diario'].round(4)
        
        return df_simulacao[['idade_dias', 'views_projetadas_hype', 'cpv_diario']]

    def exportar_resultado(self, df):
        caminho = 'dados/simulacao_gillette_copa.csv'
        df.to_csv(caminho, index=False, sep=';', decimal=',')
        logger.info(f"Dados Marginais gerados! Teto total do modelo: {df['views_projetadas_hype'].sum():,.0f} visualizações.")

if __name__ == "__main__":
    simulador = SimuladorAdstockCopa()
    df_resultado = simulador.gerar_time_series()
    simulador.exportar_resultado(df_resultado)