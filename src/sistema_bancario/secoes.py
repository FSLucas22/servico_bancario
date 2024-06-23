from typing import Any, NewType


Secao = NewType("Secao", dict[str, Any])


def criar_secao() -> Secao:
    return Secao({})


def parametros_secao(secao: Secao) -> tuple[str, ...]:
    return tuple(secao.keys())


def salvar_parametro(secao: Secao, nome: str, valor: Any) -> None:
    secao[nome] = valor


def valor_parametro(secao: Secao, nome: str) -> Any | None:
    return secao.get(nome)


def deletar_parametro(secao: Secao, nome: str) -> None:
    if nome not in secao:
        return
    del secao[nome]
