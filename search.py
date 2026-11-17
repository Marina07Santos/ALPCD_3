from api import get_exercicios
import json
import csv

exercicios = get_exercicios({"language": 2})


def filtrar_exercicios(lista_exercicios, termo_ou_palavras, por_palavras=False):
    res = []
    for ex in lista_exercicios:
        cat_name = ex["category"]["name"].lower()
        musculos_nomes = []
        for m in ex["muscles"]:
            musculos_nomes.append(m["name"].lower())
            musculos_nomes.append(m["name_en"].lower())
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
            nome = "" 
            for traducao in ex["translations"]:
                if traducao["language"] == 2:
                    nome = traducao["name"]
                    break
            equipamento = []
            for equip in ex["equipment"]:
                equipamento.append(equip["name"])
            limpo = {
                "name": nome, 
                "category": ex["category"]["name"], 
                "equipment": equipamento
            }
            if nome != "":
                res.append(limpo)
    return res

def search_exercicios(termo, n):
    termo_limpo = termo.lower().strip()
    resultado = filtrar_exercicios(exercicios, termo_limpo, por_palavras=False)
    if len(resultado) == 0 and " " in termo_limpo:
        palavras = termo_limpo.split()
        resultado = filtrar_exercicios(exercicios, palavras, por_palavras=True)
    resultado_final = []
    contador = 0
    for item in resultado:
        if contador >= n:
            break
        resultado_final.append(item)
        contador += 1
    return resultado_final




def exportar_para_csv(exercicios, nome_ficheiro="treino.csv"):
    if not exercicios:
        return
    chaves = exercicios[0].keys()
    with open(nome_ficheiro, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=chaves)
        writer.writeheader()
        for ex in exercicios:
            writer.writerow(ex)