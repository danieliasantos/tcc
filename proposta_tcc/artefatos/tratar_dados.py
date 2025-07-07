#!/usr/bin/env python
import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
    
arquivo_base = "./base/base.csv"

# Importar os dados
def importar_dados(arquivo_base):
    try:
        dados = pd.read_csv(arquivo_base, sep=';')
        return dados
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {arquivo_base}")
        return None
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None

"""
    Função para tratar os dados de coordenadas do dicionário, removendo linhas e colunas e adicionando geometria do QGIS.
    Entrada: dataframe de ocorrências 'dados'
    Retorno: dataframe com as coordenadas tratadas.
"""
def tratar_dados(dados):
    try:    
        # Ordenar os dados por data
        dados['data_hora'] = pd.to_datetime(dados['data_hora'], format='%d/%m/%Y %H:%M:%S')
        dados.sort_values(by='data_hora', ascending=True, inplace=True)
        # Regex para testar se o valor da coluna está no formato Latitude e Longitude
        regex = r'^-?\d{1,2}[\.|\,]\d+$'
        # Substitui todas as vírgulas por ponto
        dados['latitude'] = dados['latitude'].str.replace(',', '.', regex=False).astype(float)
        dados['longitude'] = dados['longitude'].str.replace(',', '.', regex=False).astype(float)
        # Cria uma coluna adicional, que recebe um booleano conforme o resultado da comparação com o Regex
        dados['matchInverso'] = dados['latitude'].astype(str).str.contains(regex)
        dados['matchInverso'] = dados['longitude'].astype(str).str.contains(regex)
        # Remove as linhas com valor falso na coluna MatchInverso
        dados.drop(dados.loc[dados.matchInverso == False].index, inplace=True)
        dados.drop(columns=['matchInverso'], inplace=True)
        # Remover todas as linhas em que a Latitude está fora do intervalo de Belo Horizonte
        dados.drop(dados[dados['latitude'].astype(float) > -19].index, inplace = True)
        dados.drop(dados[dados['latitude'].astype(float) < -22].index, inplace = True)        
        # Remover todas as linhas em que a Longitude está fora do intervalo de Belo Horizonte
        dados.drop(dados[dados['longitude'].astype(float) > -43].index, inplace = True)
        dados.drop(dados[dados['longitude'].astype(float) < -45].index, inplace = True)
        # Cria uma coluna adicional com o ano
        dados['ano'] = dados['data_hora'].dt.year
    except Exception as e:
        print(f"Erro ao tratar os dados: {e}")
        return None
    
"""
    Função para criar pontos com as coordenadas geográficas para viabilizar o processamento
    Entrada: dicionário de dataframes com as colunas Longitude e Latitude
    Função: Cria a coluna Geometry, usando a biblioteca GeoDataFrame, com pontos XY a partir das colunas Longitude e Latitude. 
            Remove as colunas Longitude e Latitude.
            Remove linhas em que não foi possível criar os pontos geométricos
    Saída: dataframe com a nova coluna Geometry
"""
def converter_geopandas(dados):
    # Adicionar coluna de geometria
    dados['Geometry'] = gpd.GeoDataFrame(geometry=gpd.points_from_xy(dados['longitude'], dados['latitude']))
    # Remover colunas latitude, longitude
    dados.drop(columns=['latitude', 'longitude'], inplace=True)
    # Remover todas as linhas em que a conversao nao foi possivel
    dados.drop(dados[dados['Geometry'] == None].index, inplace = True)
    dados.drop(dados[dados['Geometry'].astype(str) == "POINT EMPTY"].index, inplace = True)

def main():
    
    # Ler dados de Excel
    dados = importar_dados(arquivo_base)
    # Tratar os dados
    tratar_dados(dados)
    #Criar pontos com as coordenadas geográficas
    converter_geopandas(dados)
    # Exportar camadas para CSV
    dados.to_csv("base_tratada.csv", sep=";", index=False, encoding='utf-8')
    
    coluna_de_agrupamento = 'ano'
    diretorio_saida = './base/dados_por_ano/'
    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)
    for ano, grupo in dados.groupby(coluna_de_agrupamento):
        nome_arquivo = os.path.join(diretorio_saida, f'base_tratada_{ano}.csv')
        grupo.to_csv(nome_arquivo, sep=";", index=False, encoding='utf-8')
    
    dados = None
    
if __name__ == "__main__":
    main()