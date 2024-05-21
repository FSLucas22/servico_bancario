from typing import NewType, Any

Operacao = NewType("Operacao", dict[str, Any])
Deposito = NewType("Deposito", Operacao)
Saque = NewType("Saque", Operacao)
Conta = NewType("Conta", list[str])

def criar_deposito(valor: float) -> Deposito:
    return Deposito(Operacao({"tipo": "Depósito", "valor": valor}))

def criar_saque(valor: float) -> Saque:
    return Saque(Operacao({"tipo": "Saque", "valor": valor}))

def valor_saque(saque: Saque) -> float:
    return saque["valor"]

def tipo_operacao(operacao: Operacao) -> str:
    return operacao["tipo"]

def valor_deposito(deposito: Deposito) -> float:
    return deposito["valor"]

def criar_conta() -> Conta:
    return Conta([])

def quantidade_operacoes(conta: Conta) -> int:
    return len(conta)
