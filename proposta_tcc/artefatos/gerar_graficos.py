#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
    
arquivo_base = "./base_tratada.csv"

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
'''
def grafico_barras_ano(dados):
    ocorrencias_ano = dados['ano'].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    ocorrencias_ano.plot(kind='bar', color='darkgray')
    plt.title('Ocorrências de furto de cabos por Ano')
    plt.xlabel('Ano')
    plt.ylabel('Número de Ocorrências')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for index, value in enumerate(ocorrencias_ano):
        plt.text(index, value + 50, str(value), ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig('../dados/images/grafico_barras_ocorrencias_ano.png')
'''
def grafico_barras_trimestre_ano(dados):
    dados['trimestre'] = dados['trimestre_ano'].apply(lambda x: f"{int(x.split('/')[0])}º Trimestre")
    contagem_trimestre = dados.groupby(['trimestre', 'ano']).size()
    dados_grafico = contagem_trimestre.unstack(level='ano').fillna(0)
    ordem_trimestres = ['1º Trimestre', '2º Trimestre', '3º Trimestre', '4º Trimestre']
    dados_grafico = dados_grafico.reindex(ordem_trimestres)
    fig, ax = plt.subplots(figsize=(15, 10)) 
    dados_grafico.plot(kind='bar', ax=ax, width=0.8, colormap='viridis')
    ax.set_title('Ocorrências de furto de cabos por Ano e Trimestre', fontsize=16)
    ax.set_xlabel('Trimestre', fontsize=12)
    ax.set_ylabel('Número de Ocorrências', fontsize=12)
    ax.tick_params(axis='x', rotation=0)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    for container in ax.containers:
        ax.bar_label(container, label_type='edge', fontsize=9, padding=3)
    fig.tight_layout()
    fig.savefig('../dados/images/grafico_barras_ocorrencias_trimestre_ano.png')

def main():
    
    # Ler dados csv
    dados = importar_dados(arquivo_base)
    # Tratar os dados
    #grafico_barras_ano(dados)
    grafico_barras_trimestre_ano(dados)
    
    dados = None
    
if __name__ == "__main__":
    main()