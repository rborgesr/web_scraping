import json
import pandas as pd

# Configurações de exibição do pandas
pd.set_option('display.max_columns', None)  # Mostrar todas as colunas
pd.set_option('display.max_rows', 100)  # Definir o número de linhas a serem exibidas
pd.set_option('display.width', 1000)  # Ajustar a largura da saída
pd.set_option('display.colheader_justify', 'left')  # Justificar cabeçalhos de coluna à esquerda

# Carrega os dados de anime
animeData = []
for i in range(0, 451, 50):
    with open(f"dados/AnimeInfo/animeInfo{i}.json", encoding='utf-8') as file:
        animeInfo = json.load(file)
        animeData.extend(animeInfo)  # Adiciona todos os itens de uma vez

# Converte a lista para DataFrame
df1 = pd.DataFrame(animeData)
#print(df1.head())

# Carrega os nomes dos animes
animeNames = []
for i in range(0, 451, 50):
    with open(f"dados/AnimeLinks/animeInfoNames{i}.json", encoding='utf-8') as file:
        animeInfoNames = json.load(file)
        animeNames.extend(animeInfoNames)  # Adiciona todos os itens de uma vez

# Converte a lista para DataFrame
df2 = pd.DataFrame(animeNames)
#print(df2.head())

# Cria uma cópia de df1
df3 = df1.copy()

# Verifica se os DataFrames têm o mesmo número de linhas
if len(df3) == len(df2):
    df3["name"] = df2["name"].values
else:
    print("Aviso: O número de linhas em df3 e df2 não coincide!")

# Visualiza a amostra
print(df3.head())

# Salva o DataFrame combinado em um arquivo CSV
df3.to_csv('dados/Processamento/animeInfoCombination.csv', index=False)
