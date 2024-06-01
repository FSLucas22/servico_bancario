from typing import NewType

from .. import contas


ContaModel = NewType("ContaModel", list[contas.Conta])


def criar_conta_model() -> ContaModel:
    return ContaModel([])


def retornar_todas_contas(model: ContaModel) -> list[contas.Conta]:
    return list(model)


def salvar_conta(conta: contas.Conta, model: ContaModel) -> contas.Conta:
    numero = len(model) + 1
    conta = contas.criar_conta(contas.usuario_conta(conta), numero)
    model.append(conta)
    return conta


def retornar_conta_por_numero(
        numero: int, 
        model: ContaModel, *, 
        agencia: str = contas.AGENCIA
) -> contas.Conta | None:
    resultados = list(filter(
        lambda c: (contas.numero_conta(c), contas.agencia_conta(c)) == (numero, agencia), 
        model))
    return None if not resultados else resultados[0]
