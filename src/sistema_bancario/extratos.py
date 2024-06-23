from typing import Any, Iterable, NewType


Extrato = NewType("Extrato", dict[str, Any])
Operacao = dict[str, Any]


def criar_extrato(saldo: float = 0.0, /, *, extrato: Iterable[Operacao] = tuple()) -> Extrato:
    extrato_criado = Extrato({"corpo": [], "saldo": "R$ 0.00"})
    atualizar_saldo(extrato_criado, saldo)
    for operacao in extrato:
        adicionar_operacao(extrato_criado, operacao)
    return extrato_criado


def corpo_extrato(extrato: Extrato) -> tuple[str, ...]:
    return tuple(extrato["corpo"])


def saldo_extrato(extrato: Extrato) -> float:
    return extrato["saldo"]


def atualizar_saldo(extrato: Extrato, saldo: float) -> None:
    extrato["saldo"] = f"R$ {saldo:.2f}"


def adicionar_operacao(extrato: Extrato, operacao: Operacao) -> None:
    extrato["corpo"].append(f"{operacao['tipo']}: R$ {operacao['valor']:.2f}")
