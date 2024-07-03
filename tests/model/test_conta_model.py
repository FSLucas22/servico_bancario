from datetime import datetime

import pytest
import src.sistema_bancario.model as model
import src.sistema_bancario as app


@pytest.fixture
def usuario() -> app.usuarios.Usuario:
    return app.usuarios.criar_usuario(
        "Lucas", 
        datetime(1999, 6, 22), 
        "123456789", 
        "logradouro, 0001 - bairro - cidade/UF")


@pytest.fixture
def conta(usuario) -> app.contas.Conta:
    return app.contas.criar_conta(usuario)


@pytest.fixture
def conta_model() -> model.conta_model.ContaModel:
    return model.conta_model.criar_conta_model()


def test_deve_criar_model_de_conta_vazio(conta_model) -> None:
    assert model.conta_model.retornar_todas_contas(conta_model) == []


def test_deve_salvar_conta(conta_model, conta) -> None:
    conta_salva = model.conta_model.salvar_conta(conta, conta_model)
    usuario = app.contas.usuario_conta(conta_salva)

    assert usuario is not None
    assert app.usuarios.cpf_usuario(usuario) == "123456789"
    assert app.contas.agencia_conta(conta_salva) == app.contas.AGENCIA
    assert app.contas.numero_conta(conta_salva) == 1

    contas_salvas = model.conta_model.retornar_todas_contas(conta_model)
    assert len(contas_salvas) == 1
    
    conta_salva = contas_salvas[0]
    usuario = app.contas.usuario_conta(conta_salva)

    assert usuario is not None
    assert app.contas.agencia_conta(conta_salva) == app.contas.AGENCIA
    assert app.contas.numero_conta(conta_salva) == 1
    assert app.usuarios.cpf_usuario(usuario) == "123456789"


def test_deve_ter_numero_conta_sequencial(conta_model, conta) -> None:
    conta_salva = model.conta_model.salvar_conta(conta, conta_model)
    conta2_salva = model.conta_model.salvar_conta(conta, conta_model)

    assert app.contas.numero_conta(conta_salva) == 1
    assert app.contas.numero_conta(conta2_salva) == 2


def test_deve_retornar_conta_por_numero(conta_model, conta) -> None:
    model.conta_model.salvar_conta(conta, conta_model)
    conta_salva = model.conta_model.retornar_conta_por_numero(1, conta_model)
    assert conta_salva is not None

    usuario = app.contas.usuario_conta(conta_salva)
    
    assert usuario is not None
    assert app.usuarios.cpf_usuario(usuario) == "123456789"
    assert app.contas.numero_conta(conta_salva) == 1


def test_deve_retornar_None_quando_numero_nao_pertence_a_uma_conta(conta_model) -> None:
    conta_salva = model.conta_model.retornar_conta_por_numero(1, conta_model)
    assert conta_salva is None


def test_deve_retornar_todas_as_contas_por_usuario(conta_model, conta) -> None:
    model.conta_model.salvar_conta(conta, conta_model)
    model.conta_model.salvar_conta(conta, conta_model)

    usuario = app.usuarios.criar_usuario("", datetime(1999, 1, 1), "123456789", "")
    contas = model.conta_model.retornar_contas_por_usuario(usuario, conta_model)
    assert len(contas) == 2
    assert app.contas.numero_conta(contas[0]) in [1, 2]
    assert app.contas.numero_conta(contas[1]) in [1, 2]
    assert app.contas.numero_conta(contas[1]) != app.contas.numero_conta(contas[0])


def test_deve_retornar_lista_vazia_quando_usuario_sem_contas(conta_model, usuario) -> None:
    assert len(model.conta_model.retornar_contas_por_usuario(usuario, conta_model)) == 0


def test_deve_adicionar_deposito_na_conta(conta_model, conta) -> None:
    deposito = app.depositos.criar_deposito(100.0)

    conta_salva = model.conta_model.salvar_conta(conta, conta_model)
    model.conta_model.realizar_deposito(conta_salva, deposito, conta_model)
    conta_retornada = model.conta_model.retornar_conta_por_numero(1, conta_model)

    assert conta_retornada is not None
    assert app.contas.saldo_conta(conta_salva) == 100.0
    assert app.contas.quantidade_operacoes(conta_salva) == 1


def test_deve_lancar_erro_quando_conta_nao_existe_ao_realizar_deposito(conta_model, usuario) -> None:
    deposito = app.depositos.criar_deposito(100.0)
    conta = app.contas.criar_conta(usuario, 1, "0001")

    with pytest.raises(app.exceptions.ContaNaoExisteException) as error_info:
        model.conta_model.realizar_deposito(conta, deposito, conta_model)

    assert f"Conta não existe com número 1 e agência 0001" in str(error_info)    


def test_deve_adicionar_saque_na_conta(conta_model, conta) -> None:
    deposito = app.depositos.criar_deposito(100.0)
    saque = app.saques.criar_saque(30.0)
    conta_salva = model.conta_model.salvar_conta(conta, conta_model)
    model.conta_model.realizar_deposito(conta_salva, deposito, conta_model)
    model.conta_model.realizar_saque(conta_salva, saque, conta_model)

    conta_retornada = model.conta_model.retornar_conta_por_numero(1, conta_model)
    
    assert conta_retornada is not None
    assert app.contas.saldo_conta(conta_salva) == 70.0
    assert app.contas.quantidade_operacoes(conta_salva) == 2
    assert app.contas.quantidade_saques_do_dia(conta_salva) == 1


def test_deve_lancar_erro_quando_conta_nao_existe_ao_realizar_saque(conta_model, usuario) -> None:
    saque = app.saques.criar_saque(100.0)
    conta = app.contas.criar_conta(usuario, 1, "0001")

    with pytest.raises(app.exceptions.ContaNaoExisteException) as error_info:
        model.conta_model.realizar_saque(conta, saque, conta_model)

    assert f"Conta não existe com número 1 e agência 0001" in str(error_info)
