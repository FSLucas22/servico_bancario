from datetime import datetime
import pytest
import src.sistema_bancario as app


@pytest.fixture
def conta() -> app.contas.Conta:
    usuario = app.usuarios.criar_usuario(
        "Lucas",
        datetime(1999, 6, 22),
        "123456789",
        "logradouro, 0001 - bairro - cidade/UF"
    )
    numero_conta = 1
    return app.contas.criar_conta(usuario, numero_conta)


def test_deve_criar_conta_sem_operacoes(conta) -> None:
    assert app.contas.quantidade_operacoes(conta) == 0
    assert app.contas.saldo_conta(conta) == 0.0


def test_conta_deve_ter_limite_de_saque_de_500_reais(conta) -> None:
    assert app.contas.valor_maximo_saque(conta) == 500.0


def test_deve_ter_maximo_de_3_saques_diarios(conta) -> None:
    assert app.contas.maximo_saques_diarios(conta) == 3


def test_deve_ter_usuario(conta) -> None:
    usuario = app.contas.usuario_conta(conta)
    assert usuario is not None
    assert app.usuarios.cpf_usuario(usuario) == "123456789"


def test_deve_ter_numero_da_conta(conta) -> None:
    assert app.contas.numero_conta(conta) == 1


def test_deve_ter_agencia(conta) -> None:
    assert app.contas.agencia_conta(conta) == "0001"
