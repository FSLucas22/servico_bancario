from typing import NewType
from .. import usuarios
from .. import exceptions

UsuarioModel = NewType("UsuarioModel", list[usuarios.Usuario])


def criar_usuario_model() -> UsuarioModel:
    return UsuarioModel([])


def retornar_todos_usuarios(model: UsuarioModel) -> list:
    return list(model)


def salvar_usuario(usuario: usuarios.Usuario, model: UsuarioModel) -> None:
    cpf = usuarios.cpf_usuario(usuario)

    if retornar_usuario_por_cpf(cpf, model) is not None:
        raise exceptions.CpfJaExisteException(f"CPF ({cpf}) já pertence à outro usuário")
    model.append(usuario)


def retornar_usuario_por_cpf(cpf: str, model: UsuarioModel) -> usuarios.Usuario | None:
    resultados = list(filter(lambda u: usuarios.cpf_usuario(u) == cpf, model))
    return None if not resultados else resultados[0]
