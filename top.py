from api import get_exercicios

def top_exercicios(n):
    
    exercicios = get_exercicios({"language": 2})
    exercicios = sorted(exercicios, key=lambda ex: ex["created"], reverse=True) #ordenar do mais recente para o mais antigo

    resultado = []
    for ex in exercicios:
        if len(resultado) >= n:
            break
        nome = ""
        for traducao in ex["translations"]:
            if traducao["language"] == 2:
                nome = traducao["name"]
                break

        if nome != "":
            equipamento = []
            for equip in ex["equipment"]:
                equipamento.append(equip["name"])

            resultado.append({"name": nome, "category": ex["category"]["name"], "equipment": equipamento})

    return resultado