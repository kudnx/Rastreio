import requests

def getApiData(cod):
    link = "https://proxyapp.correios.com.br/v1/sro-rastro/" + cod
    response = requests.get(link)
    data = response.json()
    return data