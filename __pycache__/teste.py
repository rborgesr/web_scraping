import json
import time
from bs4 import BeautifulSoup as bs
import requests

from ProjetoExtraindoPT2 import animeName  # Certifique-se de importar corretamente o módulo onde animeName está definido

# Loop para processar os arquivos em lotes de 50 links
for limit in range(0, 451, 50):
    animeInfoName = []  # Lista para armazenar os nomes dos animes

    # Abre os arquivos de links para leitura
    with open(f"dados/AnimeLinks/animeLinks{limit}.txt", "r") as file:
        links = file.readlines()

    print('Extraindo os nomes dos animes. Por favor, aguarde...')

    # Loop pelos links para extrair o nome dos animes
    for link in links:
        try:
            rq = requests.get(link.strip())  # Use strip() para remover espaços em branco extras ao redor do link
            soup = bs(rq.text, 'html.parser')
            animeInfoName.append({"name": animeName(soup)})  # Adiciona o nome do anime à lista
            time.sleep(15)  # Aguarda 15 segundos entre as requisições para não sobrecarregar o servidor
        except Exception as e:
            print(f"Erro ao processar {link}: {e}")

    # Salva o resultado em disco no formato json
    with open(f"dados/AnimeLinks/animeInfoNames{limit}.json", "w") as fout:
        json.dump(animeInfoName, fout, indent=2)  # Escreve o JSON formatado com indentação de 2 espaços

    print(f"Web scraping concluído para batch {limit}.\n")

print("Todos os lotes foram processados com sucesso.")
