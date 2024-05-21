from src.sistema_bancario import criar_conta, quantidade_operacoes

def test_deve_criar_conta_sem_operacoes() -> None:
    conta = criar_conta()
    assert quantidade_operacoes(conta) == 0
