from typing import Any, NewType


Secao = NewType("Secao", dict[str, Any])


def criar_secao() -> Secao:
    return Secao({})


def parametros_secao(secao: Secao) -> tuple[str]:
    return tuple(secao.keys())


def salvar_parametro(secao: Secao, nome: str, valor: Any) -> str:
    secao[nome] = valor


def valor_parametro(secao: Secao, nome: str) -> str:
    return secao.get(nome)
