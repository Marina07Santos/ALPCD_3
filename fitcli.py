import json
import typer
from top import top_exercicios

app = typer.Typer()


@app.callback()
def main():
    pass


@app.command()
def top(n: int):
    resultado = top_exercicios(n)
    print(json.dumps(resultado, indent=2))


if __name__ == "__main__":
    app()