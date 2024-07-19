from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import re

html_doc ="""<html><head><title>Os Agentes Especiais</title></head>
<body>
<p class="title"><b>História dos Agentes Especiais</b></p>
<p class="story">Era uma vez três agentes especiais; e seus nomes eram
<a href="http://www.exemplo.com/james" class="agente" id="link1">James</a>,
<a href="http://www.exemplo.com/julio" class="agente" id="link2">Julio</a> e
<a href="http://www.exemplo.com/jucimar" class="agente" id="link3">Jucimar</a>;
e eles viviam em Londres, na Inglaterra.</p>
<p class="historia">...</p>
<h1>Agentes Especiais</h1>
<ul>
 <li data-id="10784">James Bond, 007: Agente especial para atividades internacionais.</li>
 <li data-id="97865">Julio Herrera, 006: Agente especial contra o. terrorismo.</li>
 <li data-id="45732">Jucimar Moraes, 005: Agente especial para proteger a rainha.</li>
</ul>

</body></html>"""

#Extraindo a tag a
tagsA = SoupStrainer("a")

#Convertendo o resultado anterior em doc html do tipo lmxl
soupA = BeautifulSoup(html_doc, 'lxml', parse_only= tagsA)

print(type(soupA))
print(soupA.prettify())

#o objeto soupA tem atributo classe?
print(soupA.a.has_attr('class'))


# Organizando e analisando dados extraídos da Web

print(soupA.find("a", attrs ={'class':'agente'}))

print(soupA.find("a", id = "link2"))

#Utilizando expressões regulares para filtrar resultados

soup = BeautifulSoup(html_doc, 'lxml')
#print(soup)

print(soup.find_all("p", "historia")) #cria uma lista [] e armazena 

print(soup.find_all(string = 'James')) #cria uma lista trazendo o nome

print(soup.find_all(string = re.compile(r'Ja'))) # puxar as frases q tem Ja no texto

print(soup.ul.find('li', attrs = {'data-id':'45732'}).string) #puxar só o texto sem armazenar em lista

#navegar por hierarquias das classes, pais filhos... .children, parents

#navegando pelas tags .next, next_element, find_next , previous.previous

print(soup.select('a[href*="exemplo.com"]'))

































































