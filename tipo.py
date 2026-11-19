import re
from api import get_exercicios


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
            descricao = re.sub(r"^ | $", "", descricao)

            dict_ingles["nome"] = nome
            dict_ingles["descricao"] = descricao

    return dict_ingles


# diz se o exercicio e compound, isolated, cardio ou other
def get_classificacao(ex):
    categoria = ex["category"]["name"]
    n_musculos = len(ex["muscles"]) + len(ex["muscles_secondary"])

    nome = ""
    texto = ""
    ingles = get_ingles(ex)
    if ingles != {}:
        nome = ingles["nome"].lower()
        texto = nome + " " + ingles["descricao"].lower()
    cardio = re.search(r"\b(run|jog|sprint|bike|cycling|burpee)", texto)
    isolado = re.search(r"\b(curl|extension|raise|fly|crunch|kickback)", texto)
    composto = re.search(r"\b(squat|deadlift|press|row|pull|chin|lunge|dip)", texto)

    if categoria.lower() == "Cardio" or cardio:
        tipo = "cardio"
    elif isolado:
        tipo = "isolated"
    elif composto:
        tipo = "compound"
    elif n_musculos >= 2:
        tipo = "compound"
    elif n_musculos == 1:
        tipo = "isolated"
    else:
        tipo = "other"

    return tipo



def get_tipo_por_id(exercise_id):
    exercicios = get_exercicios({"language": 2})

    for ex in exercicios:
        if ex["id"] == exercise_id:
            return get_classificacao(ex)

    print("O exercício não existe:", exercise_id)
    return ""


# fazer um plano de treinos
def get_treino(musculos, esforco, n):

    treino = {}
    esforco = esforco.lower()

    res = re.split(",", musculos)
    for i, item in enumerate(res):
        res[i] = re.sub(r"^ | $", "", item).lower()

    exercicios = get_exercicios({"language": 2})

    for nome in res:
        lista_exercicios = []

        for ex in exercicios:

            if len(lista_exercicios) >= n:
                break

            

        if lista_exercicios == []:
            print("Sem exercicios para:", nome)
        treino[nome] = lista_exercicios

    return treino