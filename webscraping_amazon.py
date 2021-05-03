import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

#url = "https://www.amazon.com.br/s?rh=n%3A16243890011&fs=true&ref=lp_16243890011_sar"
 
"""Obtem os dados estaticos do site, as tag's, links e nome de classes foram obtidas com a inspeccao de elemento do browser"""
 
def get_record(item):
  
   atag = item.h2.a
   description = atag.text.strip()
   addr = "https://www.amazon,com" + atag.get('href')
  
   #Caso o produto em exibicao nao tenha preco, rating e classificacoes associadas
   try:
       price_addr = item.find('span', 'a-price')
       price = price_addr.find('span', 'a-offscreen').text
   except AttributeError:
       return
 
   try:
       rating = item.i.text
       review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
   except AttributeError:
       rating = ''
       review_count = ''
 
   data_result = (description, price, rating, review_count, addr) #Salvamos os dados obtidos no array data_result
 
   return data_result
 
"""Funcao main corresponde ao scraper, comeca com a automacao do acesso ao site e os click's
para prosseguir nas paginas do site, as variaveis option não mostram a abertura e manipulacao
do site"""
 
def main(url):
   #option = Options()
   #option.headless = True
   driver = webdriver.Firefox(executable_path = r"C:\Users\deva\Documents\Projetos\210326_WebScraping_Amazon\geckodriver.exe")
   driver.get(url)
 
   data_record = []
   record = []
  
   for page in range(1, 4):  #para acelerar o professo foram visualizadas as 3 primeiras paginas do site
       driver.get(url.format(page))
       soup = BeautifulSoup(driver.page_source, 'html.parser')
       result = soup.find_all('div', {'data-component-type': 's-search-result'})
 
       for item in result:
           data_record = get_record(item)
           if data_record:
               record.append(data_record)
 
   driver.close()
 
   #criacao do arquivo csv com os dados coletados
   with open('results.csv', 'w', newline = '', encoding = 'utf-8') as f:
       writer = csv.writer(f)
       writer.writerow(['Descricao', 'Preco', 'Classificacoes', 'Numero de avaliacoes', 'url do produto'])
       writer.writerows(record)
 
main("https://www.amazon.com.br/s?rh=n%3A16243890011&fs=true&ref=lp_16243890011_sar")