from bs4 import BeautifulSoup
import requests
import os
import re

def importar(path='.',padrao='All',periodo=None):
    
    url='https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/'

    t='''Conexão mal sucedida!
É possivel que sua rede esteja instavel.
Outra possibilidade é que o argumento periodo 
esteja com valor invalido! 
Lembre-se de usar o formato yyyy-mm 
O valor também precisa existir no site do Governo'''

    try:
        response = requests.get(url+periodo+"/")
        
    except:
        print(t)
        return

    if response.status_code!=200:
        print(t)
        return

    # Analisar o conteúdo HTML com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todos os elementos <a> com atributo href
    links = soup.find_all('a', href=True)

    # Criar uma lista com todos os hrefs
    hrefs = [link['href'] for link in links]

    if padrao=='All':
        hrefs=hrefs[4:]
    elif padrao=='Cnae':
        hrefs=[item for item in hrefs if re.match(padrao,item)]

    elif padrao=='Empresa':
        hrefs=[item for item in hrefs if re.match(padrao,item)]

    elif padrao=='Estabelecimento':
        hrefs=[item for item in hrefs if re.match(padrao,item)]

    elif padrao=='Motivo':
        hrefs=[item for item in hrefs if re.match(padrao,item)]

    elif padrao=='Municipio':
        hrefs=[item for item in hrefs if re.match(padrao,item)]

    elif padrao=='Natureza':
        hrefs=[item for item in hrefs if re.match(padrao,item)]

    elif padrao=='Pais':
        hrefs=[item for item in hrefs if re.match(padrao,item)]

    elif padrao=='Qualificacao':
        hrefs=[item for item in hrefs if re.match(padrao,item)]

    elif padrao=='Simples':
        hrefs=[item for item in hrefs if re.match(padrao,item)]

    elif padrao=='Socio':
        hrefs=[item for item in hrefs if re.match(padrao,item)]

    else:
        return f'Não existem arquivos referentes a {padrao}'
        

    for h in hrefs:
        # URL do arquivo CSV
        url = 'https://dadosabertos.rfb.gov.br/CNPJ/dados_abertos_cnpj/'+periodo+"/"+h
        
        # Caminho onde você deseja salvar o arquivo
        pasta_destino = path
        nome_arquivo = h
        
        # Caminho completo do arquivo
        caminho_completo = os.path.join(pasta_destino, nome_arquivo)
        
        # Fazer o download do arquivo
        response = requests.get(url)
        
        # Salvar o arquivo
        with open(caminho_completo, 'wb') as file:
            file.write(response.content)
        
        print(f'Arquivo salvo em: {caminho_completo}')
    
    return 'Feito'