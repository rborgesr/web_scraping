import json 
import pandas as pd

pd.set_option('display.max_columns', None)  # Mostrar todas as colunas
pd.set_option('display.max_rows', 100)  # Definir o número de linhas a serem exibidas
pd.set_option('display.width', 1000)  # Ajustar a largura da saída
pd.set_option('display.colheader_justify', 'left')  # Justificar cabeçalhos de coluna à esquerda

# Cria a lista
animeData = []

# Loop para carregar os arquivos de disco na lista
for i in range(0, 451, 50):
    with open(f"dados/AnimeInfo/animeInfo{i}.json", encoding='utf-8') as file:
        animeInfo = json.load(file)
        for j in range(50):
            animeData.append(animeInfo[j])

# Converte a lista para dataframe
df1 = pd.DataFrame(animeData)

# Visualiza a amostra
print(df1.head())

# Info
#print(dfl.info())
