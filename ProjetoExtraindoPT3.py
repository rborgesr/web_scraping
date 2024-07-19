import json
import time
from bs4 import BeautifulSoup as bs
import requests

# Função que retorna o nome do anime
def animeName(soup):
    name_element = soup.select_one(".title-name")
    if name_element is not None:
        return name_element.text.strip()  # Use strip() para remover espaços em branco
    return None

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for limit in range(0, 451, 50):
    # Lista para armazenar informações dos animes
    animeInfoName = []

    # Abre os arquivos de links para leitura
    try:
        with open(f"dados/AnimeLinks/animeLinks{limit}.txt", "r", encoding="utf-8") as file:
            links = file.readlines()
    except FileNotFoundError:
        print(f"Arquivo dados/AnimeLinks/animeLinks{limit}.txt não encontrado.")
        continue

    # Remove links duplicados
    links = list(set(link.strip() for link in links))

    print('Extraindo os nomes dos animes. Por favor, aguarde.')

    # Conjunto para verificar duplicatas de nome
    seen_names = set()

    # Loop pelos links para extrair o nome dos animes
    for link in links:
        print(f"Processando link: {link}")

        try:
            rq = requests.get(link, headers=headers)
            rq.raise_for_status()
            soup = bs(rq.text, 'html.parser')

            # Verificar se o HTML foi retornado corretamente
            if not soup:
                print(f"Falha ao obter HTML para o link: {link}")
                continue

            # Verificar se o seletor encontra o elemento correto
            name_element = soup.select_one(".title-name")
            if not name_element:
                print(f"Elemento .title-name não encontrado no link: {link}")
                continue

            anime_name = animeName(soup)
            if anime_name:
                if anime_name not in seen_names:
                    animeInfoName.append({"name": anime_name})
                    seen_names.add(anime_name)
                    print(f"Nome do anime encontrado: {anime_name}")
                else:
                    print(f"Nome do anime já processado: {anime_name}")
            else:
                print(f"Nome do anime não encontrado para o link: {link}")

        except requests.RequestException as e:
            print(f"Erro ao acessar {link}: {e}")
            continue

        time.sleep(7)

    # Salva o resultado em disco no formato JSON com codificação UTF-8
    with open(f"dados/AnimeLinks/animeInfoNames{limit}.json", "w", encoding="utf-8") as fout:
        json.dump(animeInfoName, fout, ensure_ascii=False, indent=4)

    print(f"\nWeb scraping concluído com sucesso para o limite {limit}.")

print("\nTodos os limites foram processados.")
