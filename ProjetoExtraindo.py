import json
import pandas as pd
import re
import time
from bs4 import BeautifulSoup as bs
import requests
import os


## Funções Para Extração de Dados Via Web Scraping

# Função para obter tudo que estiver nas tags td e div e com seletor CSS
# Assim extraímos informações gerais da página
##def getInfoGeral(soup):
#        information = soup.select("td div .spaceit_pad")
#        side_info_par = []
 #       for info in information:
  #          side_info_par.append(info.text.split()),
   #     return side_info_par


for limit in range(0, 451, 50):
    
# lista para os links
    links = []

    # URL
    url = f"https://myanimelist.net/topanime.php?limit={limit}"

    # Medindo o tempo de execução
    start_time = time.time()  # Marca o início

    # Request
    rq = requests.get(url)
    print(rq.status_code)

    #Parse do html
    soup = bs(rq.text, "html.parser")

    #Seleção do que desejamos
    listsofA = soup.select("a.hoverinfo_trigger")

    #Loop para extrair o atributo href da tag a
    for a in listsofA:
        links.append(a.get("href"))

     # Verifica e cria diretório se não existir
     #   os.makedirs('dados/AnimeLinks', exist_ok=True)

    #Abre o arquivo em disco
    file = open(f"dados/AnimeLinks/animeLinks{limit}.txt", "w", encoding='utf-8')

    #Loop para salvar em disco
    for link in links:
        file.writelines(link +'\n')

        end_time = time.time()  # Marca o fim
        total_time = end_time - start_time

    #Mensagem que mostra quantos links foram salvos
    print(f"Armazenados {len(links)} links no arquivo animeLinks{limit}.txt")
    print(f"Tempo total para armazenar: {total_time:.2f} segundos")

    #Fecha o arquivo
    file.close()
    #Sleep
    time.sleep(10)
































































































































































