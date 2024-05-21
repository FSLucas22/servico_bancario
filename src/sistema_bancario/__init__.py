from typing import NewType, Any
from . import exceptions
from . import operacao
from . import deposito

Saque = NewType("Saque", operacao.Operacao)
Conta = NewType("Conta", dict[str, Any])


def criar_saque(valor: float) -> Saque:
    return Saque(operacao.Operacao({"tipo": "Saque", "valor": valor}))

def valor_saque(saque: Saque) -> float:
    return saque["valor"]


def criar_conta() -> Conta:
    return Conta({"saldo": 0.0,
                  "operacoes": [],
                  "maximo_saques_diarios": 3,
                  "quantidade_saques_do_dia": 0,
                  "valor_limite_saque": 500.0})

def quantidade_operacoes(conta: Conta) -> int:
    return len(conta["operacoes"])

def saldo_conta(conta: Conta) -> int:
    return conta["saldo"]


def maximo_saques_diarios(conta: Conta) -> int:
    return conta["maximo_saques_diarios"]


def quantidade_saques_do_dia(conta: Conta) -> int:
    return conta["quantidade_saques_do_dia"]


def realizar_deposito(conta: Conta, depo: deposito.Deposito) -> None:
    conta["operacoes"].append(depo)
    conta["saldo"] += deposito.valor_deposito(depo)


def valor_maximo_saque(conta: Conta) -> float:
    return conta["valor_limite_saque"]


def realizar_saque(conta: Conta, saque: Saque) -> None:
    if quantidade_saques_do_dia(conta) >= maximo_saques_diarios(conta):
        raise exceptions.QuantidadeDeSaquesSuperiorAoLimiteException(
            "Quantidade de saques realizados superior ao máximo permitido para o dia"
        )
    
    if valor_maximo_saque(conta) < valor_saque(saque):
        raise exceptions.SaqueAcimaDoValorLimiteException(
            "Valor do saque não pode ser superior ao valor limite da conta")
    
    if saldo_conta(conta) - valor_saque(saque) < 0:
        raise exceptions.SaldoInsuficienteException("Saldo insuficiente para realizar o saque")

    conta["operacoes"].append(saque)
    conta["saldo"] -= valor_saque(saque)
    conta["quantidade_saques_do_dia"] += 1

