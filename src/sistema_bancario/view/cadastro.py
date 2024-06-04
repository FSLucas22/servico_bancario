from datetime import datetime


def mostra_novo_usuario(nome: str, 
                        data_nascimento: datetime, 
                        cpf: str, 
                        endereco: str) -> None:
    print("Usuario cadastrado com sucesso!")
    print("Nome:", nome)
    print("Data de nascimento:", data_nascimento.strftime("%d/%m/%Y"))
    print("CPF:", cpf)
    print("Endereço:", endereco)


def mostra_nova_conta(numero: int, agencia: str) -> None:
    print("Nova conta cadastrada!")
    print(f"Agência: {agencia}   -   Conta: {numero}")
    