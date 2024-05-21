from typing import NewType, Any
from . import exceptions

Operacao = NewType("Operacao", dict[str, Any])
Deposito = NewType("Deposito", Operacao)
Saque = NewType("Saque", Operacao)
Conta = NewType("Conta", dict[str, Any])

def criar_deposito(valor: float) -> Deposito:
    if valor <= 0:
        raise exceptions.DepositoInvalidoException("Depósito deve ter valor positivo")
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
    return Conta({"saldo": 0.0,
                  "operacoes": [],
                  "valor_limite_saque": 500.0})

def quantidade_operacoes(conta: Conta) -> int:
    return len(conta["operacoes"])

def saldo_conta(conta: Conta) -> int:
    return conta["saldo"]

def realizar_deposito(conta: Conta, deposito: Deposito) -> None:
    conta["operacoes"].append(deposito)
    conta["saldo"] += valor_deposito(deposito)


def valor_maximo_saque(conta: Conta) -> float:
    return conta["valor_limite_saque"]


def realizar_saque(conta: Conta, saque: Saque) -> None:
    if valor_maximo_saque(conta) < valor_saque(saque):
        raise exceptions.SaqueAcimaDoValorLimiteException(
            "Valor do saque não pode ser superior ao valor limite da conta")
    
    if saldo_conta(conta) - valor_saque(saque) < 0:
        raise exceptions.SaldoInsuficienteException("Saldo insuficiente para realizar o saque")

    conta["operacoes"].append(saque)
    conta["saldo"] -= valor_saque(saque)
