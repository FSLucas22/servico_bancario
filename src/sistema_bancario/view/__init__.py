from . import operacoes
from . import cadastro


def falha(msg: str) -> None:
    print(msg)


def sucesso(msg: str) -> None:
    print(msg)


def mostra_menu(cabecalho: str, menu: dict[str, str]) -> None:
    print(cabecalho)
    for opcao, descricao in menu.items():
        print(f"[{opcao}] - {descricao}")
