import json
from pathlib import Path
import requests

cache_file = Path("cache.json")

def get_exercicios(parametros):
    parametros_pedido = parametros.copy()  # Criar uma copia dos parametros

    if cache_file.exists(): # Verificar se existe cache para estes parametros
        with cache_file.open(encoding="utf-8") as file:
            cache = json.load(file)

        if cache.get("parametros") == parametros_pedido:
            return cache["results"]

    parametros_pedido["limit"] = 100
    parametros_pedido["offset"] = 0

    cache = {"parametros": parametros.copy(), "total_count": 0 ,"results": []}

    while parametros_pedido["offset"] < cache["total_count"] or parametros_pedido["offset"] == 0:     # Consultar todas as paginas
        try:
            response = requests.get("https://wger.de/api/v2/exerciseinfo/",
                params=parametros_pedido,
                headers={"User-Agent": "grupo3"}
            )

            response.raise_for_status()
            pagina = response.json()

            cache["total_count"] = pagina["count"]
            cache["results"].extend(pagina["results"])

            parametros_pedido["offset"] += parametros_pedido["limit"]

        except requests.exceptions.RequestException as error:
            print(f"Erro ao consultar a API: {error}")
            return []

    # Guardar os resultados na cache
    if len(cache["results"]) >= cache["total_count"]:
        with cache_file.open("w", encoding="utf-8") as file:
            json.dump(cache, file, ensure_ascii=False, indent=2)

    return cache["results"]