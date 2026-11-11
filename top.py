import json
from api import get_exercicios

n=10

exercicios = get_exercicios({"language": 2})
exercicios = sorted(exercicios, key=lambda ex: ex["created"] reverse=True) #desde o mais recente para o mais antigo

resultado = []
for ex in exercicios[:n]:
    nome =""
    for traducao in ["translation"]:
        if traducao["language"] == 2:
            nome = traducao["name"]
            break
