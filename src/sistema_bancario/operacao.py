from typing import Any, NewType


Operacao = NewType("Operacao", dict[str, Any])


def tipo_operacao(operacao: Operacao) -> str:
    return operacao["tipo"]
