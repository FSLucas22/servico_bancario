import src.sistema_bancario as app

def test_deve_criar_conta_sem_operacoes() -> None:
    conta = app.criar_conta()
    assert app.quantidade_operacoes(conta) == 0

def test_contabilizar_operacoes() -> None:
    conta = app.criar_conta()
    app.realizar_operacao(conta, app.criar_deposito(100.0))
    assert app.quantidade_operacoes(conta) == 1
    app.realizar_operacao(conta, app.criar_saque(50.0))
    assert app.quantidade_operacoes(conta) == 2
    