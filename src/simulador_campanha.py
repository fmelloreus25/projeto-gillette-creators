import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Engine-Gillette-MMM-Realista")

class EngineMidiaEnterprise:
    def __init__(self):
        self.investimento = 10000.00
        self.dias_projecao = 180
        
        # Parâmetros Calibrados do Baseline Orgânico (A Realidade do Canal)
        self.max_views_dia_1_organico = 42000
        self.taxa_decaimento_youtube = 0.72 
        
        # Parâmetros Realistas do Cenário de Hype (Copa do Mundo)
        # Objetivo: Lift de ~1.8x sobre o Baseline (Totalizando ~950k views)
        self.dia_do_pico = 30 
        self.janela_hype_sigma = 12.0 
        self.pico_views_diarias_hype = 15000 # Reduzido de 85k para 15k (Tráfego incremental realista)

    def construir_cenarios(self):
        logger.info("Iniciando modelagem com benchmarks realistas de MMM...")
        
        dias = np.arange(1, self.dias_projecao + 1)
        df = pd.DataFrame({'idade_dias': dias})
        
        # 1. Baseline Orgânico
        df['views_diarias_baseline'] = self.max_views_dia_1_organico / (df['idade_dias'] ** self.taxa_decaimento_youtube)
        
        # 2. Lift Incremental (Gaussiana Conservadora)
        expoente = -((df['idade_dias'] - self.dia_do_pico)**2) / (2 * (self.janela_hype_sigma**2))
        df['views_diarias_incremental_hype'] = self.pico_views_diarias_hype * np.exp(expoente)
        
        # 3. Composição de Cenários
        df['views_diarias_totais_hype'] = df['views_diarias_baseline'] + df['views_diarias_incremental_hype']
        
        # 4. Métricas de Eficiência Diária
        df['cpv_diario_baseline'] = self.investimento / df['views_diarias_baseline']
        df['cpv_diario_hype'] = self.investimento / df['views_diarias_totais_hype']
        
        # Conversão de Tipagem
        df['views_diarias_baseline'] = df['views_diarias_baseline'].astype(int)
        df['views_diarias_totais_hype'] = df['views_diarias_totais_hype'].astype(int)
        df['cpv_diario_baseline'] = df['cpv_diario_baseline'].round(4)
        df['cpv_diario_hype'] = df['cpv_diario_hype'].round(4)
        
        total_baseline = df['views_diarias_baseline'].sum()
        total_hype = df['views_diarias_totais_hype'].sum()
        lift_multiplier = total_hype / total_baseline
        
        logger.info(f"Cálculo realista concluído!")
        logger.info(f"-> Total Baseline: {total_baseline:,.0f} views.")
        logger.info(f"-> Total Hype Copa: {total_hype:,.0f} views.")
        logger.info(f"-> Multiplicador Final de Hype: {lift_multiplier:.2f}x (Dentro do benchmark de mercado).")
        
        return df[['idade_dias', 'views_diarias_baseline', 'views_diarias_totais_hype', 'cpv_diario_baseline', 'cpv_diario_hype']]

    def exportar_data_asset(self, df):
        caminho = 'dados/simulacao_gillette_copa.csv'
        df.to_csv(caminho, index=False, sep=';', decimal=',')
        logger.info(f"Data Asset exportado: {caminho}")

if __name__ == "__main__":
    engine = EngineMidiaEnterprise()
    df_final = engine.construir_cenarios()
    engine.exportar_data_asset(df_final)