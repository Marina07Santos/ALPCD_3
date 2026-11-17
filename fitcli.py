import json
import typer

from top import top_exercicios
from equipment import contar_equipamento
from tipo import get_tipo_por_id, get_treino

app = typer.Typer()


@app.command()
def top(n: int):
    print(json.dumps(top_exercicios(n), indent=2))


@app.command()
def equipment(categoria: str):
    print(json.dumps(contar_equipamento(categoria), indent=2))


@app.command("type")
def tipo_cmd(exercise_id: int):
    print(get_tipo_por_id(exercise_id))


@app.command()
def workout(musculos: str, esforco: str, n: int):
    print(json.dumps(get_treino(musculos, esforco, n), indent=2))


if __name__ == "__main__":
    app()