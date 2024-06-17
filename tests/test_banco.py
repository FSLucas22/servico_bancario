from datetime import datetime
from typing import Any
import src.sistema_bancario as app
import src.sistema_bancario.model as model
import pytest



@pytest.fixture
def conta_model() -> model.conta_model.ContaModel:
    return model.conta_model.criar_conta_model()


@pytest.fixture
def usuario() -> app.usuarios.Usuario:
    return app.usuarios.criar_usuario(
        "Lucas", 
        datetime(1999, 6, 22), 
        "123456789", 
        "logradouro, 0001 - bairro - cidade/UF")


@pytest.fixture
def conta(conta_model, usuario) -> app.contas.Conta:
    c = app.contas.criar_conta(usuario)
    model.conta_model.salvar_conta(c, conta_model)

    return app.contas.criar_conta(usuario, 1)



@pytest.fixture
def banco(conta_model) -> app.banco.Banco:
    return app.banco.criar_banco(conta_model)


def test_deve_aumentar_o_saldo_com_deposito(banco, conta_model, conta) -> None:
    app.banco.realizar_deposito(banco, conta, app.depositos.criar_deposito(100.0))
    conta_salva = model.conta_model.retornar_conta_por_numero(1, conta_model)

    assert conta_salva is not None
    assert app.contas.quantidade_operacoes(conta_salva) == 1
    assert app.contas.saldo_conta(conta_salva) == 100.0


def test_deve_diminuir_o_saldo_com_saque(banco, conta_model, conta) -> None:

    app.banco.realizar_deposito(banco, conta, app.depositos.criar_deposito(100.0))
    app.banco.realizar_saque(banco, conta=conta, saque=app.saques.criar_saque(10.0))
    
    conta_salva = model.conta_model.retornar_conta_por_numero(1, conta_model)

    assert conta_salva is not None
    assert app.contas.quantidade_operacoes(conta_salva) == 2
    assert app.contas.saldo_conta(conta_salva) == 90.0


def test_nao_deve_permitir_saque_de_valor_indisponivel(banco, conta) -> None:
    app.banco.realizar_deposito(banco, conta, app.depositos.criar_deposito(50.0))
    
    with pytest.raises(app.exceptions.SaldoInsuficienteException) as error_info:
        app.banco.realizar_saque(banco, conta=conta, 
                                 saque=app.saques.criar_saque(100.0))
    
    assert "Saldo insuficiente para realizar o saque" in str(error_info.value)


def test_nao_deve_permitir_saques_acima_do_valor_limite(banco, conta) -> None:
    saque = app.saques.criar_saque(501.0)
    with pytest.raises(app.exceptions.SaqueAcimaDoValorLimiteException) as error_info:
        app.banco.realizar_saque(banco, conta=conta, saque=saque)
    
    assert "Valor do saque não pode ser superior ao valor limite da conta" in str(error_info.value)


def test_deve_contabilizar_a_quantidade_de_saques_do_dia(banco, conta_model, conta) -> None:
    conta_salva = model.conta_model.retornar_conta_por_numero(1, conta_model)
    
    assert app.contas.quantidade_saques_do_dia(conta_salva) == 0
    app.banco.realizar_deposito(banco, conta_salva, app.depositos.criar_deposito(100.0))
    app.banco.realizar_saque(banco, conta=conta_salva, saque=app.saques.criar_saque(10.0))
    assert app.contas.quantidade_saques_do_dia(conta_salva) == 1


def test_deve_lancar_error_ao_realizar_mais_saques_que_o_limite_diario(banco, conta) -> None:
    app.banco.realizar_deposito(banco, conta, app.depositos.criar_deposito(100.0))
    app.banco.realizar_saque(banco, conta=conta, saque=app.saques.criar_saque(10.0))
    app.banco.realizar_saque(banco, conta=conta, saque=app.saques.criar_saque(10.0))
    app.banco.realizar_saque(banco, conta=conta, saque=app.saques.criar_saque(10.0))

    with pytest.raises(app.exceptions.QuantidadeDeSaquesSuperiorAoLimiteException) as error_info:
        app.banco.realizar_saque(banco, conta=conta, saque=app.saques.criar_saque(10.0))
    
    assert "Quantidade de saques realizados superior ao máximo permitido para o dia" in str(error_info)


def test_deve_percorrer_operacoes(banco, conta) -> None:
    app.banco.realizar_deposito(banco, conta, app.depositos.criar_deposito(100.0))
    app.banco.realizar_saque(banco, conta=conta, saque=app.saques.criar_saque(10.0))

    operacoes = []
    def recebedor(operacao: dict[str, Any]) -> None:
        tipo = operacao["tipo"]
        valor = operacao["valor"]
        operacoes.append(f"{tipo}-{valor}")

    app.banco.percorrer_operacoes(banco, conta, recebedor)

    assert operacoes == ["Depósito-100.0", "Saque-10.0"]


def test_deve_preencher_extrato(banco, conta) -> None:
    app.banco.realizar_deposito(banco, conta, app.depositos.criar_deposito(100.0))
    app.banco.realizar_saque(banco, conta=conta, saque=app.saques.criar_saque(35.45))
    extrato = app.extratos.criar_extrato()
    app.banco.preencher_extrato(banco, conta, extrato)
    assert app.extratos.corpo_extrato(extrato) == ("Depósito: R$ 100.00", "Saque: R$ 35.45")
    assert app.extratos.saldo_extrato(extrato) == "R$ 64.55"
