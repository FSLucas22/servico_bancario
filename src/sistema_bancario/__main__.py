from datetime import datetime
import sys
from typing import Callable, Final, NoReturn, TypeAlias, cast

from . import depositos
from . import contas
from . import banco
from . import exceptions
from . import extratos
from . import saques
from . import usuarios
from . import secoes

from . import model


Acao: TypeAlias = Callable[[contas.Conta], None]

SECAO: secoes.Secao = secoes.criar_secao()
USUARIO_MODEL: model.usuario_model.UsuarioModel = model.usuario_model.criar_usuario_model()
CONTA_MODEL: model.conta_model.ContaModel = model.conta_model.criar_conta_model()


def get_float(msg: str, 
              error_msg: str | None = None) -> float:
    if error_msg is None:
        error_msg = msg

    try:
        return float(input(msg))
    except ValueError:
        return get_float(error_msg, error_msg)


def get_natural(msg: str, 
            error_msg: str | None = None) -> int:
    if error_msg is None:
        error_msg = msg

    try:
        return int(input(msg))
    except ValueError:
        return get_natural(error_msg, error_msg)


def get_str(msg: str, error_msg: str | None = None) -> str:
    if error_msg is None:
        error_msg = msg
    
    result = input(msg)
    if not result:
        return get_str(error_msg, error_msg)
    return result


def get_date(msg: str, error_msg: str | None = None,
             format: str = "%d/%m/%Y") -> datetime:
    if error_msg is None:
        error_msg = msg
    
    try:
        return datetime.strptime(input(msg), format)
    except ValueError as e:
        print(e)
        return get_date(error_msg, error_msg, format)


def get_cpf(msg: str, error_msg: str | None = None) -> str:
    if error_msg is None:
        error_msg = msg
    
    result = input(msg)
    if not result.isnumeric():
        return get_cpf(error_msg, error_msg)
    return result


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
        banco.realizar_saque(conta=conta, saque=saques.criar_saque(valor))
        print("Saque realizado com sucesso!")
    except (exceptions.SaldoInsuficienteException,
            exceptions.SaqueAcimaDoValorLimiteException,
            exceptions.QuantidadeDeSaquesSuperiorAoLimiteException) as e:
        print(f"Falha ao realizar saque: {str(e)}")


def imprimir_extrato(conta: contas.Conta) -> None:
    saldo = contas.saldo_conta(conta)
    operacoes = contas.operacoes_conta(conta)
    extrato = extratos.criar_extrato(saldo, extrato=operacoes)

    corpo = extratos.corpo_extrato(extrato)

    if not corpo:
        print("Não foram realizadas movimentações.")
        return
    
    print("Movimentações realizadas: ")

    for operacao in corpo:
        print(" - " + operacao)
    print(f'Saldo atual da conta: {extratos.saldo_extrato(extrato)}')


def tela_cadastro_usuario(_) -> None:
    try:
        nome = get_str("Digite seu nome: ")
        data_nascimento = get_date("Digite sua data de nascimento (DD/MM/YYYY): ", 
                                   format="%d/%m/%Y")
        cpf = get_cpf("Digite o seu CPF (Somente números): ")
        logradouro = get_str("Digite o logradouro do endereço: ")
        numero = get_str("Digite o número do endereço: ")
        bairro = get_str("Digite o bairro do endereço: ")
        cidade = get_str("Digite a cidade do endereço: ")
        estado = get_str("Digite a sigla do estado do endereço: ").upper()
        while len(estado) > 2:
            estado = get_str("Digite a sigla do estado do endereço: ").upper()
        
        endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"

        usuario = usuarios.criar_usuario(nome, data_nascimento, cpf, endereco)
        model.usuario_model.salvar_usuario(usuario, USUARIO_MODEL)
    except exceptions.CpfJaExisteException as e:
        print(f"Falha ao cadastrar usuário: {e}.")


def tela_login(_) -> None:
    cpf = get_cpf("Digite o seu CPF (Somente números): ")

    usuario = model.usuario_model.retornar_usuario_por_cpf(cpf, USUARIO_MODEL)

    if usuario is None:
        print("Usuário não cadastrado!")
        return
        
    while True:
        contas_usuario = model.conta_model.retornar_contas_por_usuario(usuario, 
                                                                       CONTA_MODEL)
        ultima_opcao = len(contas_usuario)

        print("Escolha a conta que deseja utilizar: ")
        for i, conta in enumerate(contas_usuario):
            numero = contas.numero_conta(conta)
            agencia = contas.agencia_conta(conta)
            print(f"[{i+1}] - {numero}/{agencia}")
        
        print(f"[{ultima_opcao+1}] - Cadastrar nova conta")

        opcao = get_natural(f"Digite um número de 1 à {ultima_opcao+1}: ") - 1
    
        if opcao == ultima_opcao:
            conta = contas.criar_conta(usuario)
            model.conta_model.salvar_conta(conta, CONTA_MODEL)
            print("Conta criada com sucesso!")
        elif opcao < ultima_opcao:
            secoes.salvar_parametro(SECAO, "conta_ativa", contas_usuario[opcao])
            break


def sair_da_conta(_) -> None:
    secoes.deletar_parametro(SECAO, "conta_ativa")
    print("Logout realizado com sucesso!")


def encerrar_programa(_) -> None:
    sys.exit(0)


Menu: TypeAlias = dict[str, tuple[str, Acao]]

MENU_NAO_LOGADO: Final[Menu] = {
    "U": ("Cadastrar usuário", tela_cadastro_usuario),
    "L": ("Fazer login", tela_login),
    "Q": ("Encerrar programar", encerrar_programa)
}


MENU: Final[Menu] = {
    "D": ("Realizar depósito", tela_de_depositos),
    "S": ("Realizar saque", tela_de_saques),
    "E": ("Consultar extrato", imprimir_extrato),
    "C": ("Sair da conta", sair_da_conta),
    "Q": ("Encerrar programa", encerrar_programa),
}


def mostra_menu(menu: Menu) -> None:
    for opcao, valor in menu.items():
        descricao, _ = valor
        print(f"[{opcao}] - {descricao}")


def recebe_opcao_do_user(menu: Menu) -> Acao:
    opcao = input(": ").upper().strip()
    return menu.get(opcao, ("Ausente", lambda _: print(
        "Opção inválida! Por favor escolha uma das opções apresentadas")))[1]


def tela_geral() -> None:
    usuario = usuarios.criar_usuario("Lucas",
                                        datetime(1999, 6, 22),
                                        "123456789",
                                        "logradouro, 0001 - bairro - cidade/UF")
    conta = contas.criar_conta(usuario)
    
    secoes.salvar_parametro(SECAO, "conta_ativa", conta)
    
    while True:
        conta_ativa = secoes.valor_parametro(SECAO, "conta_ativa")

        if conta_ativa is not None:
            conta_ativa = cast(contas.Conta, conta_ativa)
            nome_usuario = usuarios.nome_usuario(contas.usuario_conta(conta_ativa))
            numero = contas.numero_conta(conta_ativa)
            agencia = contas.agencia_conta(conta_ativa)

            menu = MENU

            cabecalho = f"""Olá {nome_usuario}!
Agência: {agencia}  -  Conta: {numero} 
Escolha a opção que deseja utilizar:"""
            
        else:
            menu = MENU_NAO_LOGADO
            cabecalho = "Bem vindo! Escolha a opção que deseja utilizar:"
        
        print(cabecalho)
        mostra_menu(menu)
        acao = recebe_opcao_do_user(menu)
        acao(conta_ativa)
        print()


def main() -> NoReturn:
    try:
        tela_geral()
        sys.exit(0)
    except Exception as e:
        print("Ocorreu um erro inesperado. Contate o administrador do sistema.")
        print("Informações:")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
