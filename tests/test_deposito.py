import src.sistema_bancario as app
import pytest

def test_deve_extrair_dados_do_deposito() -> None:
    deposito = app.criar_deposito(100.00)
    assert app.tipo_operacao(deposito) == "Depósito"
    assert app.valor_deposito(deposito) == 100.00


def test_nao_deve_aceitar_deposito_negativo() -> None:
    with pytest.raises(app.exceptions.DepositoInvalidoException) as error_info:
        app.criar_deposito(0)
    
    assert "Depósito deve ter valor positivo" in str(error_info.value)
