from typing import Any
import src.sistema_bancario as app
import pytest


def test_deve_aumentar_o_saldo_com_deposito() -> None:
    conta = app.contas.criar_conta()
    app.banco.realizar_deposito(conta, app.depositos.criar_deposito(100.0))
    assert app.contas.quantidade_operacoes(conta) == 1
    assert app.contas.saldo_conta(conta) == 100.0


def test_deve_diminuir_o_saldo_com_saque() -> None:
    conta = app.contas.criar_conta()
    app.banco.realizar_deposito(conta, app.depositos.criar_deposito(100.0))
    app.banco.realizar_saque(conta=conta, saque=app.saques.criar_saque(10.0))
    assert app.contas.quantidade_operacoes(conta) == 2
    assert app.contas.saldo_conta(conta) == 90.0


def test_nao_deve_permitir_saque_de_valor_indisponivel() -> None:
    conta = app.contas.criar_conta()
    app.banco.realizar_deposito(conta, app.depositos.criar_deposito(50.0))
    
    with pytest.raises(app.exceptions.SaldoInsuficienteException) as error_info:
        app.banco.realizar_saque(conta=conta, 
                                 saque=app.saques.criar_saque(100.0))
    
    assert "Saldo insuficiente para realizar o saque" in str(error_info.value)


def test_nao_deve_permitir_saques_acima_do_valor_limite() -> None:
    conta = app.contas.criar_conta()
    saque = app.saques.criar_saque(501.0)
    with pytest.raises(app.exceptions.SaqueAcimaDoValorLimiteException) as error_info:
        app.banco.realizar_saque(conta=conta, saque=saque)
    
    assert "Valor do saque não pode ser superior ao valor limite da conta" in str(error_info.value)


def test_deve_contabilizar_a_quantidade_de_saques_do_dia() -> None:
    conta = app.contas.criar_conta()
    assert app.contas.quantidade_saques_do_dia(conta) == 0
    app.banco.realizar_deposito(conta, app.depositos.criar_deposito(100.0))
    app.banco.realizar_saque(conta=conta, saque=app.saques.criar_saque(10.0))
    assert app.contas.quantidade_saques_do_dia(conta) == 1


def test_deve_lancar_error_ao_realizar_mais_saques_que_o_limite_diario() -> None:
    conta = app.contas.criar_conta()
    app.banco.realizar_deposito(conta, app.depositos.criar_deposito(100.0))
    app.banco.realizar_saque(conta=conta, saque=app.saques.criar_saque(10.0))
    app.banco.realizar_saque(conta=conta, saque=app.saques.criar_saque(10.0))
    app.banco.realizar_saque(conta=conta, saque=app.saques.criar_saque(10.0))

    with pytest.raises(app.exceptions.QuantidadeDeSaquesSuperiorAoLimiteException) as error_info:
        app.banco.realizar_saque(conta=conta, saque=app.saques.criar_saque(10.0))
    
    assert "Quantidade de saques realizados superior ao máximo permitido para o dia" in str(error_info)


def test_deve_percorrer_operacoes() -> None:
    conta = app.contas.criar_conta()
    app.banco.realizar_deposito(conta, app.depositos.criar_deposito(100.0))
    app.banco.realizar_saque(conta=conta, saque=app.saques.criar_saque(10.0))

    operacoes = []
    def recebedor(operacao: dict[str, Any]) -> None:
        tipo = operacao["tipo"]
        valor = operacao["valor"]
        operacoes.append(f"{tipo}-{valor}")

    app.banco.percorrer_operacoes(conta, recebedor)

    assert operacoes == ["Depósito-100.0", "Saque-10.0"]


def test_deve_preencher_extrato() -> None:
    conta = app.contas.criar_conta()
    app.banco.realizar_deposito(conta, app.depositos.criar_deposito(100.0))
    app.banco.realizar_saque(conta=conta, saque=app.saques.criar_saque(35.45))
    extrato = app.extratos.criar_extrato()
    app.banco.preencher_extrato(conta, extrato)
    assert app.extratos.corpo_extrato(extrato) == ("Depósito: R$ 100.00", "Saque: R$ 35.45")
    assert app.extratos.saldo_extrato(extrato) == "R$ 64.55"
