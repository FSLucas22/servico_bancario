import src.sistema_bancario as app
import pytest


def test_deve_extrair_dados_do_deposito() -> None:
    deposito = app.depositos.criar_deposito(100.00)
    assert app.operacoes.tipo_operacao(deposito) == "Depósito"
    assert app.depositos.valor_deposito(deposito) == 100.00


def test_nao_deve_aceitar_deposito_negativo() -> None:
    with pytest.raises(app.exceptions.DepositoInvalidoException) as error_info:
        app.depositos.criar_deposito(0)
    
    assert "Depósito deve ter valor positivo" in str(error_info.value)


def test_deve_converter_para_dict() -> None:
    deposito = app.depositos.criar_deposito(100.0)
    dict_infos = app.operacoes.converter_para_dict(deposito)
    assert dict_infos["tipo"] == "Depósito"
    assert dict_infos["valor"] == 100.0
