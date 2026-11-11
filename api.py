import requests

BASE_URL = "https://wger.de/api/v2/"

HEADERS = {
    "User-Agent": "grupo3"
}

def get(url, parametros=None): #pedido API

    resposta = requests.get(url, params=parametros, headers=HEADERS)

    if resposta.status_code == 200:
        return resposta.json()

    else:
        print(f"Erro no pedido: {resposta.status_code}")
        return None


def get_all(url, parametros):
    parametros["limit"] = 100
    parametros["offset"] = 0

    todos = []

    while True:
        dados = get(url, parametros)
        if dados is None:
            break
        todos.extend(dados["results"])
        parametros["offset"] += 100

        if parametros["offset"] >= dados["count"]:
            break

    return todos