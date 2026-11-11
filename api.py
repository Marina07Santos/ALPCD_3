import requests

BASE_URL = "https://wger.de/api/v2/"

HEADERS = {
    "User-Agent": "grupo3"
}

def get(endpoint, params=None): #pedido API

    url = BASE_URL + endpoint.strip("/") + "/"

    resposta = requests.get(url, params=params, headers=HEADERS)

    if resposta.status_code == 200:
        return resposta.json()

    elif resposta.status_code == 404:
        raise RuntimeError("Recurso não encontrado: " + url)

    else:
        raise RuntimeError("Erro na solicitação: " + str(resposta.status_code))


def get_all(endpoint, params=None):

    parametros = dict(params or {})
    parametros["limit"] = 100
    parametros["offset"] = 0

    todos = []

    while True:
        dados = get(endpoint, parametros)
        todos.extend(dados["results"])

        parametros["offset"] += 100

        if parametros["offset"] >= dados["count"]:
            break

    return todos