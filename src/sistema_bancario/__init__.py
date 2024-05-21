from typing import Callable, NewType, Any
from . import exceptions
from . import operacao
from . import deposito
from . import saque


Conta = NewType("Conta", dict[str, Any])


def criar_conta() -> Conta:
    return Conta({"saldo": 0.0,
                  "operacoes": [],
                  "maximo_saques_diarios": 3,
                  "quantidade_saques_do_dia": 0,
                  "valor_limite_saque": 500.0})


def operacoes_conta(conta: Conta) -> list[dict[str, Any]]:
    return [operacao.converter_para_dict(op) for op in conta["operacoes"]]


def quantidade_operacoes(conta: Conta) -> int:
    return len(conta["operacoes"])


def saldo_conta(conta: Conta) -> int:
    return conta["saldo"]


def maximo_saques_diarios(conta: Conta) -> int:
    return conta["maximo_saques_diarios"]


def aumentar_quantidade_saques(conta: Conta) -> None:
    conta["quantidade_saques_do_dia"] += 1


def quantidade_saques_do_dia(conta: Conta) -> int:
    return conta["quantidade_saques_do_dia"]


def valor_maximo_saque(conta: Conta) -> float:
    return conta["valor_limite_saque"]


def adicionar_saldo(conta: Conta, saldo: float) -> None:
    conta["saldo"] += saldo


def adicionar_operacao(conta: Conta, operacao: operacao.Operacao) -> None:
    conta["operacoes"].append(operacao)


def realizar_deposito(conta: Conta, depo: deposito.Deposito) -> None:
    adicionar_operacao(conta, depo)
    adicionar_saldo(conta, deposito.valor_deposito(depo))


def realizar_saque(conta: Conta, ssaque: saque.Saque) -> None:
    if quantidade_saques_do_dia(conta) >= maximo_saques_diarios(conta):
        raise exceptions.QuantidadeDeSaquesSuperiorAoLimiteException(
            "Quantidade de saques realizados superior ao máximo permitido para o dia"
        )
    
    if valor_maximo_saque(conta) < saque.valor_saque(ssaque):
        raise exceptions.SaqueAcimaDoValorLimiteException(
            "Valor do saque não pode ser superior ao valor limite da conta")
    
    if saldo_conta(conta) - saque.valor_saque(ssaque) < 0:
        raise exceptions.SaldoInsuficienteException("Saldo insuficiente para realizar o saque")

    adicionar_operacao(conta, ssaque)
    adicionar_saldo(conta,  (-1) * saque.valor_saque(ssaque))
    aumentar_quantidade_saques(conta)    


def percorrer_operacoes(conta: Conta, recebedor: Callable[[dict[str, Any]], None]):
    for op in operacoes_conta(conta):
        recebedor(op)
