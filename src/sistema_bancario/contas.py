from collections.abc import Iterable
from typing import Any, Final, NewType

from . import operacoes
from . import usuarios


AGENCIA: Final[str] = "0001"


Conta = NewType("Conta", dict[str, Any])


def criar_conta(usuario: usuarios.Usuario,
                numero: int | None = None,
                agencia: str = AGENCIA) -> Conta:
    return Conta({"usuario": usuario,
                  "numero": numero,
                  "agencia": agencia,
                  "saldo": 0.0,
                  "operacoes": [],
                  "maximo_saques_diarios": 3,
                  "quantidade_saques_do_dia": 0,
                  "valor_limite_saque": 500.0})


def operacoes_conta(conta: Conta) -> Iterable[dict[str, Any]]:
    return (operacoes.converter_para_dict(op) for op in conta["operacoes"])


def quantidade_operacoes(conta: Conta) -> int:
    return len(conta["operacoes"])


def saldo_conta(conta: Conta) -> int:
    return conta["saldo"]


def maximo_saques_diarios(conta: Conta) -> int:
    return conta["maximo_saques_diarios"]


def usuario_conta(conta: Conta) -> usuarios.Usuario:
    return conta["usuario"]


def numero_conta(conta: Conta) -> int:
    return conta["numero"]


def agencia_conta(conta: Conta) -> int:
    return conta["agencia"]


def aumentar_quantidade_saques(conta: Conta) -> None:
    conta["quantidade_saques_do_dia"] += 1


def quantidade_saques_do_dia(conta: Conta) -> int:
    return conta["quantidade_saques_do_dia"]


def valor_maximo_saque(conta: Conta) -> float:
    return conta["valor_limite_saque"]


def adicionar_saldo(conta: Conta, saldo: float) -> None:
    conta["saldo"] += saldo


def adicionar_operacao(conta: Conta, operacao: operacoes.Operacao) -> None:
    conta["operacoes"].append(operacao)
