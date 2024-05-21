from collections.abc import Iterable
from typing import Any, NewType

from . import operacao


Conta = NewType("Conta", dict[str, Any])


def criar_conta() -> Conta:
    return Conta({"saldo": 0.0,
                  "operacoes": [],
                  "maximo_saques_diarios": 3,
                  "quantidade_saques_do_dia": 0,
                  "valor_limite_saque": 500.0})


def operacoes_conta(conta: Conta) -> Iterable[dict[str, Any]]:
    return (operacao.converter_para_dict(op) for op in conta["operacoes"])


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
