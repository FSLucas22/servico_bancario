from . import exceptions
from . import operacoes
from typing import NewType, Any


Deposito = NewType("Deposito", operacoes.Operacao)


def criar_deposito(valor: float) -> Deposito:
    if valor <= 0:
        raise exceptions.DepositoInvalidoException("Depósito deve ter valor positivo")
    
    def conversor() -> dict[str, Any]:
        return {"tipo": "Depósito", "valor": valor}
    
    return Deposito(operacoes.Operacao({"tipo": "Depósito",
                                        "valor": valor, 
                                        "conversor": conversor}))


def valor_deposito(deposito: Deposito) -> float:
    return deposito["valor"]
