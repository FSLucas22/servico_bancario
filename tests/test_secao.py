import src.sistema_bancario as app


def test_deve_criar_secao_sem_dados() -> None:
    secao = app.secoes.criar_secao()
    assert app.secoes.parametros_secao(secao) == tuple()


def test_deve_salvar_parametro_na_sessao() -> None:
    secao = app.secoes.criar_secao()
    app.secoes.salvar_parametro(secao, "parametro", "abcd")
    assert app.secoes.parametros_secao(secao) == ("parametro",)


def test_deve_retornar_valor_salvo_na_sessao() -> None:
    secao = app.secoes.criar_secao()
    app.secoes.salvar_parametro(secao, "parametro", "abcd")
    assert app.secoes.valor_parametro(secao, "parametro") == "abcd"


def test_deve_retornar_None_quando_parametro_nao_existe() -> None:
    secao = app.secoes.criar_secao()
    assert app.secoes.valor_parametro(secao, "parametro") is None
