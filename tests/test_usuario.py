from datetime import datetime
import src.sistema_bancario as app
import src.sistema_bancario.model as model


def test_deve_criar_usuario() -> None:
    usuario: app.usuarios.Usuario = app.usuarios.criar_usuario(
        "Lucas",
        datetime(1999, 6, 22),
        "10978742907",
        "logradouro, 001 - bairro - cidade/UF")
    
    assert app.usuarios.nome_usuario(usuario) == "Lucas"
    assert app.usuarios.data_nascimento_usuario(usuario) == datetime(1999, 6, 22)
    assert app.usuarios.cpf_usuario(usuario) == "10978742907"
    assert app.usuarios.endereco_usuario(usuario) == "logradouro, 001 - bairro - cidade/UF"
