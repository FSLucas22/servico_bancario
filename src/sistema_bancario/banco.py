from typing import Any, Callable, NewType
from . import contas, depositos, exceptions, saques, extratos
from . import model as models

Banco = NewType('Banco', tuple[models.conta_model.ContaModel])


def criar_banco(conta_model: models.conta_model.ContaModel) -> Banco:
    return Banco((conta_model,))


def conta_model(banco: Banco) -> models.conta_model.ContaModel:
    return banco[0]


def retornar_conta_salva(banco: Banco, conta: contas.Conta) -> contas.Conta:
    model = conta_model(banco)
    numero = contas.numero_conta(conta)
    agencia = contas.agencia_conta(conta)

    conta_salva = models.conta_model.retornar_conta_por_numero(numero, 
                                                               model, 
                                                               agencia=agencia)
    if conta_salva is None:
        raise exceptions.ContaNaoExisteException(
            f"Conta não existe com número {numero} e agência {agencia}")
    return conta_salva


def realizar_deposito(banco: Banco, 
                      conta: contas.Conta, 
                      deposito: depositos.Deposito, /) -> None:
    model = conta_model(banco)
    models.conta_model.realizar_deposito(conta, deposito, model)


def realizar_saque(banco: Banco, *, conta: contas.Conta, saque: saques.Saque) -> None:
    model = conta_model(banco)
    conta_salva = retornar_conta_salva(banco, conta)

    if contas.quantidade_saques_do_dia(conta_salva) >= contas.maximo_saques_diarios(conta_salva):
        raise exceptions.QuantidadeDeSaquesSuperiorAoLimiteException(
            "Quantidade de saques realizados superior ao máximo permitido para o dia"
        )
    
    if contas.valor_maximo_saque(conta_salva) < saques.valor_saque(saque):
        raise exceptions.SaqueAcimaDoValorLimiteException(
            "Valor do saque não pode ser superior ao valor limite da conta")
    
    if contas.saldo_conta(conta_salva) - saques.valor_saque(saque) < 0:
        raise exceptions.SaldoInsuficienteException("Saldo insuficiente para realizar o saque")

    models.conta_model.realizar_saque(conta_salva, saque, model)


def percorrer_operacoes(banco,
                        conta: contas.Conta, 
                        recebedor: Callable[[dict[str, Any]], None]) -> None:
    conta_salva = retornar_conta_salva(banco, conta)
    for op in contas.operacoes_conta(conta_salva):
        recebedor(op)


def preencher_extrato(banco, conta: contas.Conta, extrato: extratos.Extrato) -> None:
    conta_salva = retornar_conta_salva(banco, conta)
    percorrer_operacoes(banco, conta_salva, lambda op: extratos.adicionar_operacao(extrato, op))
    extratos.atualizar_saldo(extrato, contas.saldo_conta(conta_salva))
