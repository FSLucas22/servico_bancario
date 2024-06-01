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