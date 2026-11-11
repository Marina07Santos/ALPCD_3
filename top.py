import json
from api import get_exercicios

n=10

exercicios = get_exercicios({"language": 2})
exercicios = sorted(exercicios, key=lambda ex: ex["created"], reverse=True) #desde o mais recente para o mais antigo

resultado = []
for ex in exercicios[:n]:
    nome =""
    for traducao in ex["translations"]:
        if traducao["language"] == 2:
            nome = traducao["name"]
            break

    equipamento = []
    for equip in ex["equipment"]:
        equipamento.append(equip["name"])

    resultado.append({"name": nome, "category": ex["category"]["name"], "equipment": equipamento})
print(json.dumps(resultado, indent=2))