import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from bs4 import BeautifulSoup

lista_de_skills = ["Python", "Java", ".NET"]
quantidade_de_vagas_list = []

ini = time.time()

#Configuração do webdrive
wd = webdriver.Chrome()
wd.set_window_size(1050,1800)
wd.get("https://www.linkedin.com/")

#Configuração da conta
file_con = open('config.txt')
lines = file_con.readlines()
username = lines[0]
password = lines[1]


def fazer_login(username, password): #Pega as informações lidas e usa como credenciais para o login
    id_username = wd.find_element_by_id('session_key')
    id_username.send_keys(username)
    id_password = wd.find_element_by_id('session_password')
    id_password.send_keys(password)
    id_password.submit()
    time.sleep(5)

def buscar_vagas(skills): #Busca as vagas que estão em lista_de_vagas
    wd.get("https://www.linkedin.com/jobs/search/")
    time.sleep(5)
    id_procura_empresa = wd.find_element_by_xpath('//*[@id="jobs-search-box-keyword-id-ember40"]')
    id_procura_empresa.click()
    id_procura_empresa.send_keys(skills)
    id_botao = wd.find_element_by_xpath('//*[@id="global-nav-search"]/div/div[2]/button[1]')
    id_botao.click()
    time.sleep(2)

def gerar_csv(nome_do_arquivo,lista_base):
    nome_do_arquivo = pd.DataFrame(lista_base)
    nome_do_arquivo.to_csv(f'{nome_do_arquivo}.csv', index = False, encoding = 'utf-8-sig')

info_das_vagas_list = []


fazer_login(username,password)

for skills in lista_de_skills:
    quantidade_de_vagas_dict = {}
    soup = BeautifulSoup(wd.page_source, 'html.parser')#Configuração do BS4

    buscar_vagas(skills)

    quantidade_de_vagas_dict['linguagem'] = skills
    try:
        quantidade_de_vagas_dict['quantidade'] = soup.find('div', {"class": "jobs-search-results-list__title-heading"}).find('small', {"class": "display-flex t-12 t-black--light t-normal"}).get_text().split()
    except AttributeError:
        quantidade_de_vagas_dict['quantidade'] = "ERRO"
    quantidade_de_vagas_dict['quantidade'] = " ".join(quantidade_de_vagas_dict['quantidade'])
    quantidade_de_vagas_dict['quantidade'] = quantidade_de_vagas_dict['quantidade'].replace(",", " ")
    quantidade_de_vagas_list.append(quantidade_de_vagas_dict)

    lista_de_vagas = soup.find('ul', {"class": "jobs-search-results__list list-style-none"}).find_all('li', {"class": "jobs-search-results__list-item occludable-update p0 relative ember-view"})


    for vagas in lista_de_vagas:
        info_das_vagas_dict = {}
        
        try:#Captura o título da vaga
            info_das_vagas_dict['titulo'] = vagas.find('a', {"class": "disabled ember-view job-card-container__link job-card-list__title"}).get_text().split()
        except AttributeError:
            info_das_vagas_dict['titulo'] = 'ERRO'
        info_das_vagas_dict['titulo'] = " ".join(info_das_vagas_dict['titulo'])
        info_das_vagas_dict['titulo'] = info_das_vagas_dict['titulo'].replace(",", " ")

        try:#Captura a empresa que está oferecendo a vaga
            info_das_vagas_dict['empresa'] = vagas.find('a', {"class": "job-card-container__link job-card-container__company-name ember-view"}).get_text().split()
        except AttributeError:
            info_das_vagas_dict['empresa'] = 'ERRO'
        info_das_vagas_dict['empresa'] = " ".join(info_das_vagas_dict['empresa'])
        info_das_vagas_dict['empresa'] = info_das_vagas_dict['empresa'].replace(",", " ")

        try:#Captura o local da vaga
            info_das_vagas_dict['local'] = vagas.find('li', {"class": "job-card-container__metadata-item"}).get_text().split()
        except AttributeError:
            info_das_vagas_dict['local'] = 'ERRO'
        info_das_vagas_dict['local'] = " ".join(info_das_vagas_dict['local'])
        info_das_vagas_dict['local'] = info_das_vagas_dict['local'].replace(",", " ")

        info_das_vagas_list.append(info_das_vagas_dict)

gerar_csv("dados_das_vagas", info_das_vagas_list)
gerar_csv("quantidade_de_vagas", quantidade_de_vagas_list)
fim = time.time()
print("Tempo de execução: ", fim - ini)
