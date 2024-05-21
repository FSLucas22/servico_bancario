from src.sistema_bancario import criar_deposito, tipo_operacao, valor_deposito


def test_deve_extrair_dados_do_deposito() -> None:
    deposito = criar_deposito(100.00)
    assert tipo_operacao(deposito) == "Depósito"
    assert valor_deposito(deposito) == 100.00