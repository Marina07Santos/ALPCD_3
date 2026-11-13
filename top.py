from api import get_exercicios

def top_exercicios(n):
    
    exercicios = get_exercicios({"language": 2})
    exercicios = sorted(exercicios, key=lambda ex: ex["created"], reverse=True) #ordenar do mais recente para o mais antigo

    resultado = []
    for ex in exercicios[:n]:
        nome = ""
        for traducao in ex["translations"]:
            if traducao["language"] == 2:
                nome = traducao["name"]
                break

        equipamento = []
        for equip in ex["equipment"]:
            equipamento.append(equip["name"])

        resultado.append({"name": nome, "category": ex["category"]["name"], "equipment": equipamento})

    return resultado