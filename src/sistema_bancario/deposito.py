from . import exceptions
from . import operacao
from typing import NewType


Deposito = NewType("Deposito", operacao.Operacao)


def criar_deposito(valor: float) -> Deposito:
    if valor <= 0:
        raise exceptions.DepositoInvalidoException("Depósito deve ter valor positivo")
    return Deposito(operacao.Operacao({"tipo": "Depósito", "valor": valor}))


def valor_deposito(deposito: Deposito) -> float:
    return deposito["valor"]
