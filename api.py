import requests

def get_exercicios(parametros):
    parametros["limit"] = 100
    parametros["offset"] = 0

    todos = []

    while True:
            pedido = requests.get("https://wger.de/api/v2/exerciseinfo/", params=parametros, headers={"User-Agent": "grupo3"})

            if pedido.status_code == 200:
                dados = pedido.json()
                todos.extend(dados["results"])
            else:
                print("Erro no request:", pedido.status_code)
                break

            if len(todos) >= dados["count"]:
                break
            else:
                parametros["offset"] += 100

    return todos