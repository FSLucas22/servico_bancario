from typing import Any, NewType


Extrato = NewType("Extrato", dict[str, Any])


def criar_extrato() -> Extrato:
    return Extrato({"corpo": [], "saldo": "R$ 0.00"})


def corpo_extrato(extrato: Extrato) -> tuple[str, ...]:
    return tuple(extrato["corpo"])


def saldo_extrato(extrato: Extrato) -> float:
    return extrato["saldo"]


def atualizar_saldo(extrato: Extrato, saldo: float) -> None:
    extrato["saldo"] = f"R$ {saldo:.2f}"


def adicionar_operacao(extrato: Extrato, operacao: dict[str, Any]) -> None:
    extrato["corpo"].append(f"{operacao['tipo']}: R$ {operacao['valor']:.2f}")
