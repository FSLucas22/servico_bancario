from typing import Any, Callable, NewType
from . import contas, depositos, exceptions, saques, extratos
from . import model as models

Banco = NewType('Banco', tuple[Any])


def criar_banco(conta_model: models.conta_model.ContaModel) -> Banco:
    return Banco((conta_model,))


def conta_model(banco: Banco) -> models.conta_model.ContaModel:
    return banco[0]


def realizar_deposito(banco: Banco, 
                      conta: contas.Conta, 
                      deposito: depositos.Deposito, /) -> None:
    model = conta_model(banco)
    models.conta_model.realizar_deposito(conta, deposito, model)


def realizar_saque(banco: Banco, *, conta: contas.Conta, saque: saques.Saque) -> None:
    model = conta_model(banco)
    
    if contas.quantidade_saques_do_dia(conta) >= contas.maximo_saques_diarios(conta):
        raise exceptions.QuantidadeDeSaquesSuperiorAoLimiteException(
            "Quantidade de saques realizados superior ao máximo permitido para o dia"
        )
    
    if contas.valor_maximo_saque(conta) < saques.valor_saque(saque):
        raise exceptions.SaqueAcimaDoValorLimiteException(
            "Valor do saque não pode ser superior ao valor limite da conta")
    
    if contas.saldo_conta(conta) - saques.valor_saque(saque) < 0:
        raise exceptions.SaldoInsuficienteException("Saldo insuficiente para realizar o saque")

    models.conta_model.realizar_saque(conta, saque, model)


def percorrer_operacoes(conta: contas.Conta, recebedor: Callable[[dict[str, Any]], None]):
    for op in contas.operacoes_conta(conta):
        recebedor(op)


def preencher_extrato(conta: contas.Conta, extrato: extratos.Extrato) -> None:
    percorrer_operacoes(conta, lambda op: extratos.adicionar_operacao(extrato, op))
    extratos.atualizar_saldo(extrato, contas.saldo_conta(conta))
