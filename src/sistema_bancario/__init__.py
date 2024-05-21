from typing import NewType, Any

Deposito = NewType("Deposito", dict[str, Any])
Conta = NewType("Conta", list[str])

def criar_deposito(valor: float) -> Deposito:
    return Deposito({"tipo": "Depósito", "valor": valor})

def tipo_operacao(operacao: Deposito) -> str:
    return operacao["tipo"]

def valor_deposito(deposito: Deposito) -> float:
    return deposito["valor"]

def criar_conta() -> Conta:
    return Conta([])

def quantidade_operacoes(conta: Conta) -> int:
    return len(conta)