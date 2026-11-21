import json
import typer
from main import top_exercicios, contar_equipamento, get_tipo_por_id, get_treino, search_exercicios, exportar_para_csv

app = typer.Typer(help="CLI para consultar exercicios da API wger")
# termina com erro se o termo for curto demais (ex: "a" apanha quase tudo)
def validar_termo(termo):
    if len(termo.strip()) < 3:
        print("O termo tem de ter pelo menos 3 letras:", termo)
        raise typer.Exit(1)

# escreve o resultado em JSON (ensure_ascii=False para os acentos aparecerem bem)
def mostrar_json(dados):
    print(json.dumps(dados, indent=2, ensure_ascii=False))


# termina com erro se o N nao for positivo
def validar_n(n):
    if n <= 0:
        print("N tem de ser maior que 0.")
        raise typer.Exit(1)


# a) top
@app.command()
def top(n: int):
    """Lista os N exercicios mais recentes (nome, categoria e equipamento)."""
    validar_n(n)
    mostrar_json(top_exercicios(n))


# b) search
@app.command()
def search(query: str, n: int):
    """Procura exercicios por musculo ou categoria (maximo N resultados)."""
    validar_n(n)
    validar_termo(query)
    resultado = search_exercicios(query, n)
    if resultado == []:
        print("Sem exercicios para:", query)
        raise typer.Exit(1)
    mostrar_json(resultado)


# c) type
@app.command("type")
def tipo_cmd(exercise_id: int):
    """Diz o tipo de esforco de um exercicio: compound, isolated, cardio ou other."""
    resultado = get_tipo_por_id(exercise_id)
    if resultado == "":
        raise typer.Exit(1)  # a get_tipo_por_id ja escreveu a mensagem de erro
    print(resultado)


# d) equipment
@app.command()
def equipment(categoria: str):
    """Conta o equipamento mencionado nas descricoes de uma categoria."""
    validar_termo(categoria)
    resultado = contar_equipamento(categoria)
    if resultado == []:
        print("Sem resultados para a categoria:", categoria)
        raise typer.Exit(1)
    mostrar_json(resultado)


# transforma o plano do workout numa lista de linhas para o CSV (uma por exercicio)
def treino_para_linhas(treino):
    linhas = []
    for musculo in treino:
        for ex in treino[musculo]:
            linha = {}
            linha["muscle"] = musculo
            linha["name"] = ex["name"]
            linha["type"] = ex["type"]
            linha["equipment"] = ", ".join(ex["equipment"])
            linhas.append(linha)
    return linhas


# e) workout
@app.command()
def workout(
    musculos: str,
    esforco: str,
    n: int,
    csv: str = typer.Option(None, "--csv", help="Exportar o plano para um ficheiro CSV"),):
    """Gera um plano de treino: musculos/categorias separados por virgula, tipo de esforco e N por musculo."""
    esforco = esforco.lower()
    if esforco != "compound" and esforco != "isolated" and esforco != "any":
        print("O esforço tem de ser compound, isolated ou any.")
        raise typer.Exit(1)
    validar_n(n)
    for musculo in musculos.split(","):
        validar_termo(musculo)

    treino = get_treino(musculos, esforco, n)

    if csv is None:
        mostrar_json(treino)
    else:
        linhas = treino_para_linhas(treino)
        if linhas == []:
            print("Nada para exportar: o plano nao tem exercicios.")
            raise typer.Exit(1)
        exportar_para_csv(linhas, csv)
        print(f"Ficheiro exportado: {csv} ({len(linhas)} registos)")


if __name__ == "__main__":
    app()