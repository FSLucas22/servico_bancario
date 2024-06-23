from typing import Any, Iterable
import src.sistema_bancario as app


def test_deve_extrair_dados_do_extrato() -> None:
    extrato = app.extratos.criar_extrato()
    assert app.extratos.corpo_extrato(extrato) == tuple()
    assert app.extratos.saldo_extrato(extrato) == "R$ 0.00"


def test_atualizar_saldo() -> None:
    extrato = app.extratos.criar_extrato()
    app.extratos.atualizar_saldo(extrato, 100.0)
    assert app.extratos.saldo_extrato(extrato) == "R$ 100.00"


def test_deve_adicionar_operacao() -> None:
    extrato = app.extratos.criar_extrato()
    app.extratos.adicionar_operacao(extrato, {"tipo": "Depósito", "valor": 15.3})
    app.extratos.adicionar_operacao(extrato, {"tipo": "Saque", "valor": 32.95})
    assert app.extratos.corpo_extrato(extrato) == ("Depósito: R$ 15.30", "Saque: R$ 32.95")


def test_deve_criar_extrato_por_saldo_e_iterable_extrato() -> None:
    operacoes: Iterable[dict[str, Any]] = [{"tipo": "Depósito", "valor": 200.0},
                                           {"tipo": "Saque", "valor": 100.0}]
    extrato = app.extratos.criar_extrato(100.0, extrato=operacoes)
    assert app.extratos.corpo_extrato(extrato) == ("Depósito: R$ 200.00", "Saque: R$ 100.00")
    assert app.extratos.saldo_extrato(extrato) == "R$ 100.00"
