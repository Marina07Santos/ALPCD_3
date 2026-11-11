import requests

def get_exercicios(parametros):
    """Vai buscar todos os exercícios, página a página."""
    parametros["limit"] = 100
    parametros["offset"] = 0

    todos = []
