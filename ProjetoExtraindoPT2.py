import json
import pandas as pd
import re
import time
from bs4 import BeautifulSoup as bs
import requests
import os

# Função para obter todas as informações das tags td e div com seletor CSS spaceit_pad
def getInfoGeral(soup):
    information = soup.select('td div .spaceit_pad')
    side_info_par = []
    for info in information:
        side_info_par.append(info.text.split())
    return side_info_par

# Função para obter o número de pessoas que adicionaram o anime aos favoritos
def getFavorite(information):
    for info in information:
        if info[0] == "Favorites:":
            data = info[1].split(",")
            return int("".join(data))
    return None

# Função para obter o número de episódios
def episodeNumberParser(information):
    for info in information:
        if info[0] == "Episodes:":
            if info[1] != "Unknown":
                return int(info[1])
    return None

# Função para obter o tipo de anime (TV, OVA, etc.)
def typeParser(information):
    for info in information:
        if info[0] == "Type:":
            return info[1]
    return None

# Função para obter o dia em que o anime estreou
def dayPremiered(information):
    for info in information:
        if info[0] == "Premiered:":
            return "".join(info[1:])
    return None

# Função para obter a fonte do anime
def getSource(information):
    for info in information:
        if info[0] == "Source:":
            return " ".join(info[1:])
    return None

# Função para retornar uma lista de gêneros do anime
def getGenres(information):
    for info in information:
        if info[0] == "Genres:":
            genres = " ".join(info[1:])
            return genres.split(",")
    return None

# Função para retornar uma lista de estúdios que estão patrocinando este anime
def getStudios(information):
    for info in information:
        if info[0] == "Studios:":
            return "".join(info[1:])
    return None

# Função para retornar uma lista de empresas que possuem a licença deste anime
def getLicense(information):
    for info in information:
        if info[0] == "Licensors:":
            if info[1] == "None":
                return None
            license = "".join(info[1:])
            return license.split(",")
    return None

# Função para obter a classificação do anime
def getRating(information):
    for info in information:
        if info[0] == "Rating:":
            return "".join(info[1:])
    return None

# Função para obter os nomes dos produtores
def producers_names(soup):
    div_and_a = soup.find_all(["div", "a"], class_=['spaceit_pad'])
    for index, j in enumerate(div_and_a):
        if div_and_a[index].text.split("\n")[1] == "Producers:":
            res = re.sub(" *", "", div_and_a[index].text)
            new_res = res.split("\n")
            for i, j in enumerate(new_res):
                if j == "Producers:":
                    return new_res[i+1].split(",")
            break
    return None

# Função para obter informações de ranking
def getRanking(soup):
    ranking_element = soup.select_one(".ranked strong")
    if ranking_element is not None:
        data = ranking_element.text.split("#")[1]
        return int(data)
    return None

# Função para obter o score do anime
def getScore(soup):
    score_element = soup.select_one(".score-label")
    if score_element is not None:
        return float(score_element.text)
    return None

# Função para obter a popularidade do anime
def getPopularity(soup):
    popularity_element = soup.select_one(".popularity strong")
    if popularity_element is not None:
        data = popularity_element.text.split("#")[1]
        return int(data)
    return None

# Função para obter informações sobre os membros
def getMembers(soup):
    members_element = soup.select_one(".members strong")
    if members_element is not None:
        data = members_element.text.split(",")
        return int("".join(data))
    return None

# Função para obter o número de pessoas que votaram no anime
def votersCount(soup):
    count = soup.select(".js-statistics-info span")
    data = []
    for i in count:
        data.append(i.text)
    if len(data) > 2:
        return int(data[2])
    return None

# Função para obter o nome dos atores de voz
def voiceActorsName(soup):
    actorNames = []
    names = soup.select(".js-anime-character-va-lang .spaceit_pad a")
    for name in names:
        data = "".join(name.text.split())
        actorNames.append(data)
    return actorNames

# Função para obter o idioma dos atores de voz
def voiceActorsLanguage(soup):
    languages = []
    langNames = soup.select(".js-anime-character-language")
    for language in langNames:
        lang = "".join(language.text.split())
        languages.append(lang)
    return languages

# Função que cria um dataframe com as informações dos atores de voz e seus idiomas
def voiceActorNameAndLanguage(soup):
    names = voiceActorsName(soup)
    languages = voiceActorsLanguage(soup)
    namesAndLang = []
    for i in range(len(names)):
        namesAndLang.append([names[i], languages[i]])
    return namesAndLang

# Função que retorna a ocupação dos funcionários
def staffOccupation(soup):
    data = []
    for i in soup.select('td .js-scrollfix-bottom-rel .spaceit_pad small'):
        data.append(''.join(i.text.split()))
    return data

# Função que retorna o nome dos funcionários
def staffName(soup):
    data = []
    for i in soup.select('td .js-scrollfix-bottom-x , a'):
        data.append(''.join(i.text.split()))
    uncleanData = []
    for index, info in enumerate(data):
        if info == "Addstaff":
            uncleanData.append(data[index+1:])
            break
    cleanData = []
    for i in uncleanData:
        for j in i:
            if len(j) > 1:
                cleanData.append(j)
    return cleanData

# Função que concatena nome e ocupação dos funcionários
def staffNameandOccupation(soup):
    name = staffName(soup)
    occupation = staffOccupation(soup)
    nameAndOccupation = []
    min_length = min(len(name), len(occupation))  # Ajuste o comprimento mínimo
    for i in range(min_length):
        nameAndOccupation.append([name[i], occupation[i]])
    return nameAndOccupation

# Função que retorna o nome do anime
def animeName(soup):
    name_element = soup.select_one(".title-name")
    if name_element is not None:
        return name_element.text
    return None


# Loop principal para iterar sobre os links de anime
for limit in range(0, 451, 50):
    animeInfo = []

    # Abre o arquivo com os links
    with open(f"dados/AnimeLinks/animeLinks{limit}.txt", "r") as file:
        links = file.readlines()

    print(f'Fazendo Web Scraping. Arquivo animeLinks{limit}.txt - Aguarde...')

    # Itera sobre cada link
    anime_count = 0  # Contador de animes por arquivo

    for link in links:
        try:
            # Realiza a requisição para obter a página principal do anime
            rq = requests.get(link.strip(), headers={'User-Agent': 'Mozilla/5.0'})
            rq.raise_for_status()  # Verifica se a requisição foi bem-sucedida

            # Realiza a requisição para obter a página de personagens do anime
            rq2 = requests.get(link.strip()[:-2] + "/characters", headers={'User-Agent': 'Mozilla/5.0'})
            rq2.raise_for_status()  # Verifica se a requisição foi bem-sucedida

            # Faz o parse do HTML
            soup = bs(rq.text, "html.parser")
            soup2 = bs(rq2.text, "html.parser")

            # Obtém informações gerais da página principal
            information = getInfoGeral(soup)

            # Cria um dicionário com os dados do anime, se não estiver presente na lista
            anime_data = {
                "name": animeName(soup),
                "producers": producers_names(soup),
                "ranking": getRanking(soup),
                "votersCount": votersCount(soup),
                "score": getScore(soup),
                "popularity": getPopularity(soup),
                "members": getMembers(soup),
                "favorite": getFavorite(information),
                "episodes": episodeNumberParser(information),
                "animeType": typeParser(information),
                "premiredDate": dayPremiered(information),
                "animeSource": getSource(information),
                "genres": getGenres(information),
                "studios": getStudios(information),
                "licenses": getLicense(information),
                "rating": getRating(information),
                "voiceActorNameandlanguage": voiceActorNameAndLanguage(soup2),
                "staffNameandOccupation": staffNameandOccupation(soup2)
            }

            # Verifica se o anime já está na lista antes de adicionar
            if anime_data not in animeInfo:
                animeInfo.append(anime_data)
                anime_count += 1

        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar {link.strip()}: {e}")
        except Exception as e:
            print(f"Erro ao processar {link.strip()}: {e}")

    # Grava os dados em um arquivo JSON
    if animeInfo:
        with open(f"dados/Animeinfo/animeInfo{limit}.json", "w", encoding="utf-8") as fout:
            json.dump(animeInfo, fout, ensure_ascii=False, indent=4)
    
    print(f"Finalizado. Arquivo animeInfo{limit}.json criado com {anime_count} animes.")

    # Aguarda alguns segundos antes de continuar para não sobrecarregar o servidor
    time.sleep(15)
