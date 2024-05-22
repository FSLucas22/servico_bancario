import sys
from typing import Callable, Final, NoReturn

from . import depositos
from . import contas
from . import banco
from . import exceptions
from . import extratos
from . import saques


def get_float(msg: str, 
              error_msg: str | None = None) -> float:
    if error_msg is None:
        error_msg = msg

    try:
        return float(input(msg))
    except ValueError:
        return get_float(error_msg, error_msg)


def tela_de_depositos(conta: contas.Conta) -> None:
    valor = get_float("Por favor digite o valor do depósito: ",
                      "Por favor digite um número válido no formato xxx.xx: ")
    try:
        banco.realizar_deposito(conta, depositos.criar_deposito(valor))
        print("Depósito realizado com sucesso!")
    except exceptions.DepositoInvalidoException as e:
        print(f"Falha ao realizar depósito: {str(e)}")


def tela_de_saques(conta: contas.Conta) -> None:
    valor = get_float("Por favor digite o valor do saque: ",
                      "Por favor digite um número válido no formato xxx.xx: ")
    try:
        banco.realizar_saque(conta, saques.criar_saque(valor))
        print("Depósito realizado com sucesso!")
    except (exceptions.SaldoInsuficienteException,
            exceptions.SaqueAcimaDoValorLimiteException,
            exceptions.QuantidadeDeSaquesSuperiorAoLimiteException) as e:
        print(f"Falha ao realizar saque: {str(e)}")


def imprimir_extrato(conta: contas.Conta) -> None:
    extrato = extratos.criar_extrato()
    banco.preencher_extrato(conta, extrato)
    operacoes = extratos.corpo_extrato(extrato)

    if not operacoes:
        print("Não foram realizadas movimentações.")
        return
    
    print("Movimentações realizadas: ")
    print('\n'.join(extratos.corpo_extrato(extrato)))
    print(f'Saldo atual da conta: {extratos.saldo_extrato(extrato)}')


MENU: Final[dict[str, tuple[str, Callable[[contas.Conta], None]]]] = {
    "D": ("Realizar depósito", tela_de_depositos),
    "S": ("Realizar saque", tela_de_saques),
    "E": ("Consultar extrato", imprimir_extrato),
    "Q": ("Encerrar programa", lambda _: sys.exit(0)),
}


def mostra_menu() -> None:
    print("""Bem vindo usuário!
Escolha a opção que deseja utilizar:""")
    for opcao, valor in MENU.items():
        descricao, _ = valor
        print(f"[{opcao}] - {descricao}")


def recebe_opcao_do_user() -> Callable[[], None]:
    opcao = input(": ").upper().strip()
    return MENU.get(opcao, ("Ausente", lambda _: print(
        "Opção inválida! Por favor escolha uma das opções apresentadas")))[1]


def main() -> NoReturn:
    try:
        conta = contas.criar_conta()
        while True:
            mostra_menu()
            acao = recebe_opcao_do_user()
            acao(conta)
            print()
    except Exception as e:
        print("Ocorreu um erro inesperado. Contate o administrador do sistema.")
        print("Informações:")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
