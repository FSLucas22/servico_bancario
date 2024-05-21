import src.sistema_bancario as app
import pytest


def test_deve_criar_conta_sem_operacoes() -> None:
    conta = app.criar_conta()
    assert app.quantidade_operacoes(conta) == 0
    assert app.saldo_conta(conta) == 0.0


def test_deve_aumentar_o_saldo_com_deposito() -> None:
    conta = app.criar_conta()
    app.realizar_deposito(conta, app.criar_deposito(100.0))
    assert app.quantidade_operacoes(conta) == 1
    assert app.saldo_conta(conta) == 100.0


def test_deve_diminuir_o_saldo_com_saque() -> None:
    conta = app.criar_conta()
    app.realizar_deposito(conta, app.criar_deposito(100.0))
    app.realizar_saque(conta, app.criar_saque(10.0))
    assert app.quantidade_operacoes(conta) == 2
    assert app.saldo_conta(conta) == 90.0

def test_nao_deve_permitir_saque_de_valor_indisponivel() -> None:
    conta = app.criar_conta()
    app.realizar_deposito(conta, app.criar_deposito(50.0))
    
    with pytest.raises(app.exceptions.SaldoInsuficienteException) as error_info:
        app.realizar_saque(conta, app.criar_saque(100.0))
    
    assert "Saldo insuficiente para realizar o saque" in str(error_info.value)
