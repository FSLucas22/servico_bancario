from datetime import datetime
import src.sistema_bancario.model as model
import src.sistema_bancario as app
import pytest


@pytest.fixture
def usuario() -> app.usuarios.Usuario:
    return app.usuarios.criar_usuario(
        "Lucas",
        datetime(1999, 6, 22),
        "123456789",
        "logradouro, 0001 - bairro - cidade/UF"
    )


@pytest.fixture
def usuario_model() -> model.usuario_model.UsuarioModel:
    return model.usuario_model.criar_usuario_model()


def assert_usuarios_iguais(usuario1: app.usuarios.Usuario, 
                           usuario2: app.usuarios.Usuario) -> None:
    assert app.usuarios.nome_usuario(usuario1) == app.usuarios.nome_usuario(usuario2) 
    assert app.usuarios.data_nascimento_usuario(usuario1) == \
        app.usuarios.data_nascimento_usuario(usuario2)
    assert app.usuarios.cpf_usuario(usuario1) == app.usuarios.cpf_usuario(usuario2)
    assert app.usuarios.endereco_usuario(usuario1) == app.usuarios.endereco_usuario(usuario2)


def test_deve_criar_model_de_usuario(usuario_model) -> None:
    assert model.usuario_model.retornar_todos_usuarios(usuario_model) == []


def test_deve_salvar_usuario(usuario_model, usuario) -> None:
    model.usuario_model.salvar_usuario(usuario, usuario_model)
    usuarios = model.usuario_model.retornar_todos_usuarios(usuario_model)

    assert len(usuarios) == 1
    
    usuario_salvo = usuarios[0]
    
    assert_usuarios_iguais(usuario, usuario_salvo)


def test_deve_retornar_None_quando_cpf_nao_esta_salvo(usuario_model) -> None:
    assert model.usuario_model.retorna_usuario_por_cpf("123456789", usuario_model) is None


def test_deve_retornar_usuario_por_cpf(usuario_model, usuario) -> None:
    model.usuario_model.salvar_usuario(usuario, usuario_model)
    usuario_salvo = model.usuario_model.retorna_usuario_por_cpf("123456789", usuario_model)
    
    assert usuario_salvo is not None
    assert_usuarios_iguais(usuario, usuario_salvo)


def test_nao_deve_salvar_usuario_com_cpf_duplicado(usuario_model, usuario) -> None:
    model.usuario_model.salvar_usuario(usuario, usuario_model)
    usuario2 = app.usuarios.criar_usuario("", datetime.now(), "123456789", "")
    
    with pytest.raises(app.exceptions.CpfJaExisteException) as error_info:
        model.usuario_model.salvar_usuario(usuario2, usuario_model)
    
    assert "CPF (123456789) já pertence à outro usuário" in str(error_info)
