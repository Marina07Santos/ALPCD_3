import re
from api import get_exercicios


def contar_equipamento(categoria):
    exercicios = get_exercicios({"language": 2})

    palavras = ["barbell", "bench", "incline bench", "cable", "machine","dumbbell", "mat", "kettlebell", "pull-up", "band","sz-bar", "swiss ball", "bodyweight"]
    contagem = {}

    for ex in exercicios:
        # so os exercícios da categoria pedida
        if ex["category"]["name"].lower() == categoria.lower():

            # descricoo em ingles
            texto = ""
            for traducao in ex["translations"]:
                if traducao["language"] == 2:
                    texto = traducao["description"]
                    break

            texto = re.sub(r"<[^>]+>", " ", texto).lower()

            # contar cada palavra de equipamento
            for palavra in palavras:
                vezes = len(re.findall(rf"\b{palavra}s?\b", texto))
                if vezes > 0:
                    if palavra in contagem:
                        contagem[palavra] += vezes
                    else:
                        contagem[palavra] = vezes

    # ordenar do maior para o menor
    ordenado = sorted(contagem.items(), key=lambda item: item[1], reverse=True)

    resultado = []
    for palavra, vezes in ordenado:
        resultado.append({palavra: vezes})

    return resultado