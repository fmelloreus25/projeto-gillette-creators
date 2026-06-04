import os
import sqlite3
import logging
import pandas as pd
import isodate
from googleapiclient.discovery import build
from dotenv import load_dotenv

# 1. Configuração de Observabilidade (Logs corporativos)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Gillette-Data-Eng")

class MotorExtracaoYouTube:
    def __init__(self):
        logger.info("Inicializando Motor de Extração YouTube...")
        load_dotenv()
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        
        if not self.api_key:
            logger.error("API Key não encontrada no arquivo .env!")
            raise ValueError("Credenciais ausentes.")
            
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.caminho_db = 'dados/banco_gillette_campanha.db'

    def buscar_videos_canal(self, handle_canal, max_resultados=50):
        """Busca os vídeos mais recentes de um canal específico usando o Handle (@)."""
        logger.info(f"Acessando API para o canal: {handle_canal}")
        
        # Faz a requisição ao servidor do Google usando o parâmetro forHandle
        resposta_canal = self.youtube.channels().list(
            part='contentDetails',
            forHandle=handle_canal
        ).execute()
        
        # Verifica se o Google enviou o pacote vazio
        if 'items' not in resposta_canal:
            logger.error("O Google não encontrou o canal. Verifique se o @ está correto.")
            raise ValueError("Canal não encontrado no banco de dados do YouTube.")
            
        playlist_id = resposta_canal['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # Busca os vídeos da playlist
        resposta_playlist = self.youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=max_resultados
        ).execute()
        
        ids_videos = [item['contentDetails']['videoId'] for item in resposta_playlist['items']]
        return ids_videos

    def extrair_metricas_detalhadas(self, ids_videos):
        """Puxa as métricas de negócio (Views, Likes, Comentários, Duração) para cada vídeo."""
        logger.info(f"Extraindo métricas detalhadas de {len(ids_videos)} vídeos...")
        
        resposta_videos = self.youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=','.join(ids_videos)
        ).execute()
        
        dados = []
        for video in resposta_videos['items']:
            # Conversão do formato de tempo do YouTube (ISO 8601) para segundos inteiros
            duracao_iso = video['contentDetails']['duration']
            duracao_segundos = isodate.parse_duration(duracao_iso).total_seconds()
            
            # Sanity Check: A tese da Gillette é retenção profunda. Vamos ignorar Shorts (< 60s)
            if duracao_segundos < 60:
                continue
                
            estatisticas = video.get('statistics', {})
            
            dados.append({
                'id_video': video['id'],
                'titulo_video': video['snippet']['title'],
                'data_publicacao': video['snippet']['publishedAt'],
                'duracao_segundos': int(duracao_segundos),
                'qtd_visualizacoes': int(estatisticas.get('viewCount', 0)),
                'qtd_likes': int(estatisticas.get('likeCount', 0)),
                'qtd_comentarios': int(estatisticas.get('commentCount', 0))
            })
            
        df = pd.DataFrame(dados)
        logger.info(f"Extração concluída. {len(df)} vídeos de formato longo processados.")
        return df

    def carregar_dados_bronze(self, df):
        """Salva o DataFrame no Data Warehouse Local (Camada Bronze)."""
        logger.info("Estabelecendo conexão com o Data Warehouse local...")
        conexao = sqlite3.connect(self.caminho_db)
        
        # Salva ou substitui a tabela
        df.to_sql('tb_videos_performance', conexao, if_exists='replace', index=False)
        conexao.close()
        logger.info("Sucesso! Camada Bronze (tb_videos_performance) atualizada no banco SQLite.")

if __name__ == "__main__":
    # Handle oficial do canal "Por Onde Andrey"
    HANDLE_CANAL = "@_andreyray"
    
    # 1. Instancia o Extrator
    extrator = MotorExtracaoYouTube()
    
    # 2. Executa a Ingestão (ETL)
    lista_ids = extrator.buscar_videos_canal(HANDLE_CANAL, max_resultados=50)
    df_bronze = extrator.extrair_metricas_detalhadas(lista_ids)
    
    # 3. Carrega no Banco de Dados
    extrator.carregar_dados_bronze(df_bronze)