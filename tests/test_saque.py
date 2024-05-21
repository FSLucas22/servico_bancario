import src.sistema_bancario as app

def test_deve_extrair_dados_do_saque() -> None:
    saque = app.saque.criar_saque(100.00)
    assert app.operacao.tipo_operacao(saque) == "Saque"
    assert app.saque.valor_saque(saque) == 100.00
