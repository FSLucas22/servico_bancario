import src.sistema_bancario as app


def test_deve_criar_conta_sem_operacoes() -> None:
    conta = app.contas.criar_conta()
    assert app.contas.quantidade_operacoes(conta) == 0
    assert app.contas.saldo_conta(conta) == 0.0


def test_conta_deve_ter_limite_de_saque_de_500_reais() -> None:
    conta = app.contas.criar_conta()
    assert app.contas.valor_maximo_saque(conta) == 500.0


def test_deve_ter_maximo_de_3_saques_diarios() -> None:
    conta = app.contas.criar_conta()
    assert app.contas.maximo_saques_diarios(conta) == 3

