from src.sistema_bancario import criar_saque, tipo_operacao, valor_saque

def test_deve_extrair_dados_do_saque() -> None:
    saque = criar_saque(100.00)
    assert tipo_operacao(saque) == "Saque"
    assert valor_saque(saque) == 100.00
