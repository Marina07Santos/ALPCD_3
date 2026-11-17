import json
from pathlib import Path
import requests

cache_file = Path("cache.json")


def get_exercicios(parametros):
    if cache_file.exists(): #usa o cache que ja existe 
        with cache_file.open(encoding="utf-8") as file:
            cache = json.load(file)
    else:
        parametros["limit"] = 100 # Sem cache, consulta todas as paginas
        parametros["offset"] = 0
        cache = {"total_count": 0, "results": []}

        while parametros["offset"] < cache["total_count"] or parametros["offset"] == 0:
            try:
                response = requests.get("https://wger.de/api/v2/exerciseinfo/",params=parametros,headers={"User-Agent": "grupo3"})
                response.raise_for_status()
                page = response.json()
                cache["total_count"] = page["count"]
                cache["results"].extend(page["results"])
                parametros["offset"] += parametros["limit"]
            except requests.exceptions.RequestException as error:
                print(f"Erro ao consultar a API: {error}")
                break

        if cache["total_count"] > 0 and len(cache["results"]) >= cache["total_count"]:
            with cache_file.open("w", encoding="utf-8") as file:
                json.dump(cache, file, ensure_ascii=False, indent=2)

    return cache["results"]