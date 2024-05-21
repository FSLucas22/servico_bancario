import src.sistema_bancario as app

def test_deve_criar_conta_sem_operacoes() -> None:
    conta = app.criar_conta()
    assert app.quantidade_operacoes(conta) == 0
    assert app.saldo_conta(conta) == 0.0


def test_deve_aumentar_o_saldo_com_deposito() -> None:
    conta = app.criar_conta()
    app.realizar_deposito(conta, app.criar_deposito(100.0))
    assert app.quantidade_operacoes(conta) == 1
    assert app.saldo_conta(conta) == 100.0
