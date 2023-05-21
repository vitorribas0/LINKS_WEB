import requests
from bs4 import BeautifulSoup
import pandas as pd

secao = 'Freezer Horizontal Electrolux H550 513L Litros Branco'#O Texto que vai ser procurado na página web
# Faz a letura da planilha"
planilha = pd.read_excel("Link2.xlsx")#Coloque a planilha a mesma pasta e na variavel coloque o nome da planilha

# URL da página de login
login_url = "https://ava4.cs.edu.br/login/index.php"#Caso tiver login ná página, coloque o link dá página de login aqui

# Meu login
username = "45884034865"
password = "45884034865"

# login e senha
login_data = {
    "username": username,
    "password": password
}

# Cria uma lista para armazenar os resultados
resultados = []

# Cria uma sessão para manter a autenticação
session = requests.Session()

# Envia uma solicitação POST para efetuar login
login_response = session.post(login_url, data=login_data)

# Verifica se o login foi bem-sucedido
if login_response.status_code == 200:
    # Percorre os valores da coluna "Link"
    for url in planilha["Link"]:
        # Envia uma solicitação GET usando a sessão autenticada
        response = session.get(url)

        # Verifica se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Extrai o conteúdo da página
            content = response.text

            # Cria um objeto BeautifulSoup para analisar o HTML
            soup = BeautifulSoup(content, "html.parser")

            # Verifica se a página contém a palavra "Seção 1"
            if 'Seção 1' and 'Seção 2' and 'Seção 3' in soup.get_text():
                resultados.append({"Link": url, "Contém Seção 1": "Não tem conteúdo"})
            else:
                resultados.append({"Link": url, "Contém Seção 1": "Tem conteúdo"})
        else:
            print(f"Falha ao acessar a página: {url}")
else:
    print("Falha ao efetuar login")

# Cria uma planilha com os resultados
planilha_resultado = pd.DataFrame(resultados)
planilha_resultado.to_excel("resultado.xlsx", index=False)
print("Resultados salvos em 'resultado.xlsx'.")
