import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import math

url = ('https://www.kabum.com.br/busca/televis%C3%A3o')
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
qtde = soup.find('div', id='listingCount').get_text().strip()
index = qtde.find(' ')
qtde_itens = qtde[:index]
max_pag = math.ceil(int(qtde_itens)/20)

dict_produtos = {'marca' : [], 'preço' : []}
for i in range(1, max_pag+1):
    url_pag = f'https://www.kabum.com.br/busca/televis%C3%A3o?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    produtos = soup.find_all('div', class_=re.compile('productCard'))
    for produto in produtos:
        marca = produto.find('span', class_=re.compile('nameCard')).get_text().strip()
        preço = produto.find('span', class_=re.compile('priceCard')).get_text().strip()
        print(marca, preço)
        dict_produtos['marca'].append(marca)
        dict_produtos['preço'].append(preço)
    print(url_pag)

dataframe = pd.DataFrame(dict_produtos)
dataframe.to_csv('C:/Users/jefer/OneDrive/Documentos/MeusProjetos/preco_produtos.csv', encoding='utf8')

