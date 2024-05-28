import src.sistema_bancario as app


def test_deve_extrair_dados_do_saque() -> None:
    saque = app.saques.criar_saque(100.00)
    assert app.operacoes.tipo_operacao(saque) == "Saque"
    assert app.saques.valor_saque(saque) == 100.00


def test_deve_converter_para_dict() -> None:
    saque = app.saques.criar_saque(100.00)
    dict_infos = app.operacoes.converter_para_dict(saque)
    assert dict_infos["tipo"] == "Saque"
    assert dict_infos["valor"] == 100.0
