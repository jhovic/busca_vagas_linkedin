import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from bs4 import BeautifulSoup

ini = time.time()
#Configuração do webdrive

wd = webdriver.Chrome()
wd.set_window_size(1050,1800)
wd.get("https://www.linkedin.com/")

#Configuração das credenciais

file_con = open('config.txt')
lines = file_con.readlines()
username = lines[0]
password = lines[1]

#Login
id_username = wd.find_element_by_id('session_key')
id_username.send_keys(username)
id_password = wd.find_element_by_id('session_password')
id_password.send_keys(password)
id_password.submit()
time.sleep(5)

vagasgeral = ["Python", "Java", ".NET"]
vagas_list = []
vagas_info_list = []

for a in vagasgeral:
    #Buscando a empresa
    #Definindo qual empresa buscar
    

    #Clica na barra de pesquisar e procura a empresa selecionada
    wd.get("https://www.linkedin.com/jobs/search/")
    time.sleep(5)
    id_procura_empresa = wd.find_element_by_xpath('//*[@id="jobs-search-box-keyword-id-ember40"]')
    id_procura_empresa.click()
    id_procura_empresa.send_keys(a)
    id_botao = wd.find_element_by_xpath('//*[@id="global-nav-search"]/div/div[2]/button[1]')
    id_botao.click()
    time.sleep(2)

    
    
    soup = BeautifulSoup(wd.page_source, 'html.parser')

    vagas = soup.find('ul', {"class": "jobs-search-results__list list-style-none"}).find_all('li', {"class": "jobs-search-results__list-item occludable-update p0 relative ember-view"})

    
    vagas_info_dict = {}
    vagas_info_dict['linguagem'] = a
    vagas_info_dict['quantidade'] = soup.find('div', {"class": "jobs-search-results-list__title-heading"}).find('small', {"class": "display-flex t-12 t-black--light t-normal"}).get_text().split()
    vagas_info_dict['quantidade'] = " ".join(vagas_info_dict['quantidade'])
    vagas_info_dict['quantidade'] = vagas_info_dict['quantidade'].replace(",", " ")
    vagas_info_list.append(vagas_info_dict)


    for i in vagas:
        info = {}
        #Captura o título da vaga
        try:
            info['titulo'] = i.find('a', {"class": "disabled ember-view job-card-container__link job-card-list__title"}).get_text().split()
        except AttributeError:
            info['titulo'] = 'ERRO'
        info['titulo'] = " ".join(info['titulo'])
        info['titulo'] = info['titulo'].replace(",", " ")

        #Captura a empresa que está oferecendo a vaga
        try:
            info['empresa'] = i.find('a', {"class": "job-card-container__link job-card-container__company-name ember-view"}).get_text().split()
        except AttributeError:
            info['empresa'] = 'ERRO'
        info['empresa'] = " ".join(info['empresa'])
        info['empresa'] = info['empresa'].replace(",", " ")

        #Captura o local da vaga
        try:
            info['local'] = i.find('li', {"class": "job-card-container__metadata-item"}).get_text().split()
        except AttributeError:
            info['local'] = 'ERRO'
        info['local'] = " ".join(info['local'])
        info['local'] = info['local'].replace(",", " ")

        vagas_list.append(info)

dados_df = pd.DataFrame(vagas_list)
dados_df.to_csv('vagas_dados.csv', index = False, encoding = 'utf-8-sig')

quantidade_vaga_df = pd.DataFrame(vagas_info_list)
quantidade_vaga_df.to_csv('vagas_qtd.csv', index = False, encoding = 'utf-8-sig')

#sep=';', columns= 3, header= ['titulo', 'empresa', 'local'], index = False,

print(dados_df)

fim = time.time()
print("Tempo de execução: ", fim - ini)

while True:
    time.sleep(1)