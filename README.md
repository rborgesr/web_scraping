## 🎥Projeto de Web Scraping - MyAnimeList 🎥
Este projeto realiza a extração de dados diretamente das páginas do site MyAnimeList (sem o uso de APIs), utilizando técnicas de web scraping para coletar informações detalhadas sobre os animes.

## 📋 Visão Geral

O objetivo é capturar dados de animes como títulos, gêneros, notas, sinopse e número de episódios, organizando essas informações para facilitar a análise e o estudo do conteúdo.

## Funcionalidades

Extração de dados de animes diretamente do HTML das páginas do MyAnimeList.
Tratamento e limpeza de dados com Pandas para organizar as informações.
Exportação dos dados em formatos JSON e CSV para posterior análise.

## 🛠️ Ferramentas e Tecnologias

Python: Linguagem principal para desenvolvimento.
BeautifulSoup: Utilizada para parsing HTML e extração de informações.
Requests: Biblioteca para fazer as requisições HTTP às páginas do MyAnimeList.
Pandas: Organização e manipulação de dados em DataFrames.
Jupyter Notebook: Para o desenvolvimento e exploração dos dados coletados.
JSON/CSV: Para salvar os dados extraídos.

## 🚀 Como Funciona
1. Coleta de Dados
O script realiza requisições às páginas de animes no MyAnimeList e usa o BeautifulSoup para capturar dados como:

Título
Gêneros
Nota (Score)
Número de Episódios
Sinopse

2. Limpeza e Tratamento
Após a extração, os dados são organizados em DataFrames com o Pandas.

São aplicados processos de:


Limpeza: Remoção de dados incompletos ou inválidos.

Formatação: Padronização de colunas, como gêneros e notas, para facilitar a análise.

3. Armazenamento dos Dados
Os dados podem ser exportados em:

JSON: Formato leve e flexível, ideal para manipulação posterior.
CSV: Formato tabular, útil para análises no Excel ou ferramentas de visualização.

## 📊 Resultados Esperados
Após a execução do script, os dados de animes serão exportados em formatos JSON e CSV. A partir desses dados, podem ser feitas consultas e análises detalhadas com Python, permitindo:

Uma série deverificações de informação, rankings de produtores, ranking de médias e etc.

Geração de relatórios dinâmicos.

Criação de gráficos que mostram, por exemplo, a distribuição de gêneros, pontuações médias e a quantidade de episódios por anime.

## 🔧 Requisitos
Python 3.x
Bibliotecas: requests, beautifulsoup4, pandas
