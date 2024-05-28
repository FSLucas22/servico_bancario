from typing import Any, Callable
from . import contas, depositos, exceptions, saques, extratos


def realizar_deposito(conta: contas.Conta, deposito: depositos.Deposito) -> None:
    contas.adicionar_operacao(conta, deposito)
    contas.adicionar_saldo(conta, depositos.valor_deposito(deposito))


def realizar_saque(conta: contas.Conta, saque: saques.Saque) -> None:
    if contas.quantidade_saques_do_dia(conta) >= contas.maximo_saques_diarios(conta):
        raise exceptions.QuantidadeDeSaquesSuperiorAoLimiteException(
            "Quantidade de saques realizados superior ao máximo permitido para o dia"
        )
    
    if contas.valor_maximo_saque(conta) < saques.valor_saque(saque):
        raise exceptions.SaqueAcimaDoValorLimiteException(
            "Valor do saque não pode ser superior ao valor limite da conta")
    
    if contas.saldo_conta(conta) - saques.valor_saque(saque) < 0:
        raise exceptions.SaldoInsuficienteException("Saldo insuficiente para realizar o saque")

    contas.adicionar_operacao(conta, saque)
    contas.adicionar_saldo(conta,  (-1) * saques.valor_saque(saque))
    contas.aumentar_quantidade_saques(conta)


def percorrer_operacoes(conta: contas.Conta, recebedor: Callable[[dict[str, Any]], None]):
    for op in contas.operacoes_conta(conta):
        recebedor(op)


def preencher_extrato(conta: contas.Conta, extrato: extratos.Extrato) -> None:
    percorrer_operacoes(conta, lambda op: extratos.adicionar_operacao(extrato, op))
    extratos.atualizar_saldo(extrato, contas.saldo_conta(conta))
