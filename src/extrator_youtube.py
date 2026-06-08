import pandas as pd
import numpy as np
import logging

# Configuração de Log Profissional
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Engine-Gillette-MMM")

class EngineMidiaEnterprise:
    def __init__(self):
        self.investimento = 10000.00
        self.dias_projecao = 180
        
        # Parâmetros do Cenário de Hype (Copa do Mundo)
        self.dia_do_pico = 30 
        self.janela_hype_sigma = 12.0 
        self.pico_views_diarias_hype = 85000 
        
        # Parâmetros de Calibragem do Baseline Orgânico (Baseado no histórico do Canal)
        # O canal tem ~4.2M de views em 10 vídeos, média de ~420k por vídeo.
        # Vamos calibrar o vídeo fantasma para atingir ~450k views orgânicas totais em 180 dias.
        self.max_views_dia_1_organico = 42000
        self.taxa_decaimento_youtube = 0.72 # Inclinação padrão para queda após 48h

    def construir_cenarios(self):
        logger.info("Iniciando modelagem matemática de Marketing Mix Modeling (MMM)...")
        
        dias = np.arange(1, self.dias_projecao + 1)
        df = pd.DataFrame({'idade_dias': dias})
        
        # 1. Baseline Orgânico: Lei de Potência Humana (Decaimento Real de Notificação do YouTube)
        df['views_diarias_baseline'] = self.max_views_dia_1_organico / (df['idade_dias'] ** self.taxa_decaimento_youtube)
        
        # 2. Lift Incremental: Gaussiana Sazonal Aditiva (O Boom da Campanha)
        expoente = -((df['idade_dias'] - self.dia_do_pico)**2) / (2 * (self.janela_hype_sigma**2))
        df['views_diarias_incremental_hype'] = self.pico_views_diarias_hype * np.exp(expoente)
        
        # 3. Composição de Cenários (Garantindo que o Hype some acima do Orgânico)
        df['views_diarias_totais_hype'] = df['views_diarias_baseline'] + df['views_diarias_incremental_hype']
        
        # 4. Métricas de Eficiência Diária (Mídia)
        df['cpv_diario_baseline'] = self.investimento / df['views_diarias_baseline']
        df['cpv_diario_hype'] = self.investimento / df['views_diarias_totais_hype']
        
        # Conversão de Tipagem Executiva
        df['views_diarias_baseline'] = df['views_diarias_baseline'].astype(int)
        df['views_diarias_totais_hype'] = df['views_diarias_totais_hype'].astype(int)
        df['cpv_diario_baseline'] = df['cpv_diario_baseline'].round(4)
        df['cpv_diario_hype'] = df['cpv_diario_hype'].round(4)
        
        # Validação de Sanidade em Logs para o Engenheiro de Dados
        total_baseline = df['views_diarias_baseline'].sum()
        total_hype = df['views_diarias_totais_hype'].sum()
        logger.info(f"Cálculo concluído com sucesso!")
        logger.info(f"-> Total Acumulado Vídeo Normal (Baseline): {total_baseline:,.0f} views.")
        logger.info(f"-> Total Acumulado Vídeo Copa (Hype): {total_hype:,.0f} views.")
        
        return df[['idade_dias', 'views_diarias_baseline', 'views_diarias_totais_hype', 'cpv_diario_baseline', 'cpv_diario_hype']]

    def exportar_data_asset(self, df):
        caminho = 'dados/simulacao_gillette_copa.csv'
        df.to_csv(caminho, index=False, sep=';', decimal=',')
        logger.info(f"Data Asset exportado e pronto para Governança em: {caminho}")

if __name__ == "__main__":
    engine = EngineMidiaEnterprise()
    df_final = engine.construir_cenarios()
    engine.exportar_data_asset(df_final)