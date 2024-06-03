import pytest
import src.sistema_bancario as app


@pytest.fixture
def secao() -> app.secoes.Secao:
    return app.secoes.criar_secao()


def test_deve_criar_secao_sem_dados(secao) -> None:
    assert app.secoes.parametros_secao(secao) == tuple()


def test_deve_salvar_parametro_na_sessao(secao) -> None:
    app.secoes.salvar_parametro(secao, "parametro", "abcd")
    assert app.secoes.parametros_secao(secao) == ("parametro",)


def test_deve_retornar_valor_salvo_na_sessao(secao) -> None:
    app.secoes.salvar_parametro(secao, "parametro", "abcd")
    assert app.secoes.valor_parametro(secao, "parametro") == "abcd"


def test_deve_retornar_None_quando_parametro_nao_existe(secao) -> None:
    assert app.secoes.valor_parametro(secao, "parametro") is None


def test_deve_excluir_parametro_da_secao(secao) -> None:
    app.secoes.salvar_parametro(secao, "parametro", "abcd")
    app.secoes.deletar_parametro(secao, "parametro")
    assert app.secoes.parametros_secao(secao) == tuple()
    assert app.secoes.valor_parametro(secao, "parametro") == None


def test_nao_deve_acontecer_nada_quando_parametro_excluido_nao_existe(secao) -> None:
    app.secoes.deletar_parametro(secao, "parametro")
    assert app.secoes.parametros_secao(secao) == tuple()
    assert app.secoes.valor_parametro(secao, "parametro") == None
