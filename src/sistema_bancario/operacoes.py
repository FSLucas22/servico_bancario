from typing import Any, NewType


Operacao = NewType("Operacao", dict[str, Any])


def tipo_operacao(operacao: Operacao) -> str:
    return operacao["tipo"]


def converter_para_dict(operacao: Operacao) -> dict[str, Any]:
    return operacao["conversor"]()
