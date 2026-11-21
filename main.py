import csv
import json
import re
from pathlib import Path

import requests

cache_file = Path("cache.json")



# API
def get_exercicios(parametros):

    # se a cache existir e tiver sido feita com estes parametros, usa a cache
    if cache_file.exists():
        with cache_file.open(encoding="utf-8") as file:
            cache = json.load(file)
        if cache.get("parametros") == parametros:
            return cache["results"]

    url = "https://wger.de/api/v2/exerciseinfo/"
    headers = {"User-Agent": "grupo3"}

    parametros_pedido = parametros.copy()
    parametros_pedido["limit"] = 100
    parametros_pedido["offset"] = 0

    results = []
    total_count = 0

    # primeira pagina
    try:
        resposta = requests.get(url, params=parametros_pedido, headers=headers, timeout=10)
    except requests.exceptions.RequestException as erro:
        print("Erro de ligacao a API:", erro)
        return []
    if resposta.status_code == 200:
        variavel = resposta.json()
        results.extend(variavel["results"])
        total_count = variavel["count"]
        parametros_pedido["offset"] += 100
    else:
        print("Erro no pedido:", resposta.status_code)

    # restantes paginas
    while parametros_pedido["offset"] < total_count:
        try:
            resposta = requests.get(url, params=parametros_pedido, headers=headers, timeout=10)
        except requests.exceptions.RequestException as erro:
            print("Erro de ligacao a API:", erro)
            break
        if resposta.status_code == 200:
            variavel = resposta.json()
            results.extend(variavel["results"])
        else:
            print("Erro no pedido:", resposta.status_code)
        parametros_pedido["offset"] += 100

    # guardar na cache (so se vieram os exercicios todos)
    if total_count > 0 and len(results) >= total_count:
        cache = {"parametros": parametros, "total_count": total_count, "results": results}
        with cache_file.open("w", encoding="utf-8") as file:
            json.dump(cache, file, ensure_ascii=False, indent=2)

    return results


# os exercicios estao em varias linguas, filtramos para ingles
def get_ingles(dados):
    dict_ingles = {}

    traducoes = dados["translations"]
    for traducao in traducoes:
        lingua = traducao["language"]
        if lingua == 2:
            nome = traducao["name"]
            descricao = traducao["description"] or ""

            # limpar a descricao: tirar tags HTML e espacos a mais
            descricao = re.sub(r"<.*?>", " ", descricao)
            descricao = re.sub(r"\s+", " ", descricao)
            descricao = descricao.strip()

            dict_ingles["nome"] = nome
            dict_ingles["descricao"] = descricao

    return dict_ingles

# lista com os nomes do equipamento de um exercicio
def get_equipamento(ex):
    equipamento = []
    for equip in ex["equipment"]:
        equipamento.append(equip["name"])
    return equipamento

#top
def top_exercicios(n):
    exercicios = get_exercicios({"language": 2})
    exercicios = sorted(exercicios, key=lambda ex: ex["created"], reverse=True) #ordenar do mais recente para o mais antigo

    resultado = []
    for ex in exercicios:
        if len(resultado) >= n:
            break

        ingles = get_ingles(ex)
        if ingles != {}:
            resultado.append({"name": ingles["nome"], "category": ex["category"]["name"], "equipment": get_equipamento(ex)})

    return resultado

#search + CSV 
def filtrar_exercicios(lista_exercicios, termo_ou_palavras, por_palavras=False):
    res = []
    for ex in lista_exercicios:
        cat_name = ex["category"]["name"].lower()
        musculos_nomes = []
        for m in ex["muscles"]:
            if m["name_en"] != "":
                musculos_nomes.append(m["name_en"].lower())
            else:
                musculos_nomes.append(m["name"].lower())
        match_categoria = False
        match_musculo = False
        if not por_palavras:
            if termo_ou_palavras in cat_name:
                match_categoria = True
            for m in musculos_nomes:
                if termo_ou_palavras in m:
                    match_musculo = True
                    break
        else:
            for p in termo_ou_palavras:
                if p in cat_name:
                    match_categoria = True
                    break
            for p in termo_ou_palavras:
                for m in musculos_nomes:
                    if p in m:
                        match_musculo = True
                        break
                if match_musculo:
                    break
        if match_categoria or match_musculo:
            ingles = get_ingles(ex)
            if ingles != {}:
                res.append({"name": ingles["nome"], "category": ex["category"]["name"], "equipment": get_equipamento(ex)})
    return res


def search_exercicios(termo, n):
    exercicios = get_exercicios({"language": 2})
    termo_limpo = termo.lower().strip()
    resultado = filtrar_exercicios(exercicios, termo_limpo, por_palavras=False)
    if len(resultado) == 0 and " " in termo_limpo:
        palavras = termo_limpo.split()
        resultado = filtrar_exercicios(exercicios, palavras, por_palavras=True)
    return resultado[:n]

def exportar_para_csv(exercicios, nome_ficheiro="treino.csv"):
    if not exercicios:
        return
    chaves = exercicios[0].keys()
    with open(nome_ficheiro, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=chaves)
        writer.writeheader()
        for ex in exercicios:
            writer.writerow(ex)

# type

# procura palavras-chave num texto; devolve o tipo ou None se nao encontrar nenhuma
def procurar_tipo(texto):
    if re.search(r"\b(run|jog|sprint|bike|cycling|burpee|jumping jack)", texto):
        return "cardio"
    if re.search(r"\b(curl|hammercurl|extension|raise|fly|butterfly|cross-?over|crunch|kickback|adduction|abduction|calf press|pushdown|chin tuck)", texto):
        return "isolated"
    if re.search(r"\b(squat|deadlift|press|row|pull|chin|lunge|dip|snatch|thruster|power clean|ohp|rdl)", texto):
        return "compound"
    return None

# diz se o exercicio e compound, isolated, cardio ou other
def get_classificacao(ex):
    categoria = ex["category"]["name"]
    n_musculos = len(ex["muscles"]) + len(ex["muscles_secondary"])

    nome = ""
    texto = ""
    ingles = get_ingles(ex)
    if ingles != {}:
        nome = ingles["nome"].lower()
        texto = ingles["descricao"].lower()
    if re.search(r"\b(stretch|foam roll|breathing|meditation|balance|circles|yoga)", nome):  # alongamentos, mobilidade e respiracao nao sao exercicios de forca (so pelo nome)
        return "other"
    if categoria.lower() == "cardio":
        return "cardio"

    # primeiro o nome, que e mais fiavel; so se nao decidir, a descricao
    tipo = procurar_tipo(nome)
    if tipo is None:
        tipo = procurar_tipo(texto)

    # se nao houver palavras-chave, decide pelo numero de musculos
    if tipo is None:
        if n_musculos >= 2:
            tipo = "compound"
        elif n_musculos == 1:
            tipo = "isolated"
        else:
            tipo = "other"

    return tipo

# comando type: diz o tipo de esforco a partir do id do exercicio
def get_tipo_por_id(exercise_id):
    exercicios = get_exercicios({"language": 2})

    for ex in exercicios:
        if ex["id"] == exercise_id:
            return get_classificacao(ex)

    print("O exercício não existe:", exercise_id)
    return ""


# equipment 
def contar_equipamento(categoria):
    exercicios = get_exercicios({"language": 2})

    palavras = ["barbell", "bench", "incline bench", "cable", "machine", "dumbbell", "mat", "kettlebell", "pull-up", "band", "sz-bar", "swiss ball", "bodyweight"]
    contagem = {}

    for ex in exercicios:
        if categoria.lower() in ex["category"]["name"].lower(): # so os exercicios da categoria pedida (como no search)

            # descricao em ingles (ja limpa pela get_ingles)
            ingles = get_ingles(ex)
            if ingles != {}:
                texto = ingles["descricao"].lower()

                # contar primeiro as mais compridas ("incline bench" antes de "bench") e tira-las do texto, para nao serem contadas duas vezes
                for palavra in sorted(palavras, key=len, reverse=True):
                    padrao = rf"\b{palavra}(?:e?s)?\b"
                    vezes = len(re.findall(padrao, texto))
                    if vezes > 0:
                        if palavra in contagem:
                            contagem[palavra] += vezes
                        else:
                            contagem[palavra] = vezes
                        texto = re.sub(padrao, " ", texto)

    ordenado = sorted(contagem.items(), key=lambda item: item[1], reverse=True)

    resultado = []
    for palavra, vezes in ordenado:
        resultado.append({palavra: vezes})

    return resultado


#workout 
# fazer um plano de treinos
def get_treino(musculos, esforco, n):
    treino = {}

    res = re.split(",", musculos)
    for i, item in enumerate(res):
        res[i] = re.sub(r"^ +| +$", "", item).lower()

    exercicios = get_exercicios({"language": 2})

    for nome in res:
        lista_exercicios = []

        for ex in exercicios:
            if len(lista_exercicios) >= n:
                break

            # reutiliza o filtro do search (musculo ou categoria)
            if filtrar_exercicios([ex], nome) != []:
                ingles = get_ingles(ex)
                tipo = get_classificacao(ex)

                if esforco == "any" or tipo == esforco:
                    lista_exercicios.append({"name": ingles["nome"], "type": tipo, "equipment": get_equipamento(ex)})

        if lista_exercicios == []:
            print("Sem exercicios para:", nome)
        treino[nome] = lista_exercicios

    return treino
