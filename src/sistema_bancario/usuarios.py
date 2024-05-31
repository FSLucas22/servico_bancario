from datetime import datetime
from typing import NewType


Usuario = NewType("Usuario", tuple[str, datetime, str, str])


def criar_usuario(nome: str, data_nascimento: datetime, cpf: str, endereco: str) -> Usuario:
    return Usuario((nome, data_nascimento, cpf, endereco))


def nome_usuario(usuario: Usuario) -> str:
    return usuario[0]


def data_nascimento_usuario(usuario: Usuario) -> datetime:
    return usuario[1]


def cpf_usuario(usuario: Usuario) -> str:
    return usuario[2]


def endereco_usuario(usuario: Usuario) -> str:
    return usuario[3]
