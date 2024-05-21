from . import exceptions
from . import operacao
from typing import NewType


Saque = NewType('Saque', operacao.Operacao)


def criar_saque(valor: float) -> Saque:
    return Saque(operacao.Operacao({"tipo": "Saque", "valor": valor}))


def valor_saque(saque: Saque) -> float:
    return saque["valor"]
