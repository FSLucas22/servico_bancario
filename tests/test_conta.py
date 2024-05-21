from typing import Any
import src.sistema_bancario as app
import pytest


def test_deve_criar_conta_sem_operacoes() -> None:
    conta = app.criar_conta()
    assert app.quantidade_operacoes(conta) == 0
    assert app.saldo_conta(conta) == 0.0


def test_deve_aumentar_o_saldo_com_deposito() -> None:
    conta = app.criar_conta()
    app.realizar_deposito(conta, app.deposito.criar_deposito(100.0))
    assert app.quantidade_operacoes(conta) == 1
    assert app.saldo_conta(conta) == 100.0


def test_deve_diminuir_o_saldo_com_saque() -> None:
    conta = app.criar_conta()
    app.realizar_deposito(conta, app.deposito.criar_deposito(100.0))
    app.realizar_saque(conta, app.saque.criar_saque(10.0))
    assert app.quantidade_operacoes(conta) == 2
    assert app.saldo_conta(conta) == 90.0


def test_nao_deve_permitir_saque_de_valor_indisponivel() -> None:
    conta = app.criar_conta()
    app.realizar_deposito(conta, app.deposito.criar_deposito(50.0))
    
    with pytest.raises(app.exceptions.SaldoInsuficienteException) as error_info:
        app.realizar_saque(conta, app.saque.criar_saque(100.0))
    
    assert "Saldo insuficiente para realizar o saque" in str(error_info.value)


def test_conta_deve_ter_limite_de_saque_de_500_reais() -> None:
    conta = app.criar_conta()
    assert app.valor_maximo_saque(conta) == 500.0


def test_nao_deve_permitir_saques_acima_do_valor_limite() -> None:
    conta = app.criar_conta()
    saque = app.saque.criar_saque(501.0)
    with pytest.raises(app.exceptions.SaqueAcimaDoValorLimiteException) as error_info:
        app.realizar_saque(conta, saque)
    
    assert "Valor do saque não pode ser superior ao valor limite da conta" in str(error_info.value)


def test_deve_ter_maximo_de_3_saques_diarios() -> None:
    conta = app.criar_conta()
    assert app.maximo_saques_diarios(conta) == 3


def test_deve_contabilizar_a_quantidade_de_saques_do_dia() -> None:
    conta = app.criar_conta()
    assert app.quantidade_saques_do_dia(conta) == 0
    app.realizar_deposito(conta, app.deposito.criar_deposito(100.0))
    app.realizar_saque(conta, app.saque.criar_saque(10.0))
    assert app.quantidade_saques_do_dia(conta) == 1


def test_deve_lancar_error_ao_realizar_mais_saques_que_o_limite_diario() -> None:
    conta = app.criar_conta()
    app.realizar_deposito(conta, app.deposito.criar_deposito(100.0))
    app.realizar_saque(conta, app.saque.criar_saque(10.0))
    app.realizar_saque(conta, app.saque.criar_saque(10.0))
    app.realizar_saque(conta, app.saque.criar_saque(10.0))

    with pytest.raises(app.exceptions.QuantidadeDeSaquesSuperiorAoLimiteException) as error_info:
        app.realizar_saque(conta, app.saque.criar_saque(10.0))
    
    assert "Quantidade de saques realizados superior ao máximo permitido para o dia" in str(error_info)


def test_deve_percorrer_operacoes() -> None:
    conta = app.criar_conta()
    app.realizar_deposito(conta, app.deposito.criar_deposito(100.0))
    app.realizar_saque(conta, app.saque.criar_saque(10.0))

    operacoes = []
    def recebedor(operacao: dict[str, Any]) -> None:
        tipo = operacao["tipo"]
        valor = operacao["valor"]
        operacoes.append(f"{tipo}-{valor}")

    app.percorrer_operacoes(conta, recebedor)

    assert operacoes == ["Depósito-100.0", "Saque-10.0"]
