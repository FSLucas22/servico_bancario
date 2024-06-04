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
from . import user_inputs
from . import view


Acao: TypeAlias = Callable[[contas.Conta], None]

SECAO: secoes.Secao = secoes.criar_secao()
USUARIO_MODEL: model.usuario_model.UsuarioModel = model.usuario_model.criar_usuario_model()
CONTA_MODEL: model.conta_model.ContaModel = model.conta_model.criar_conta_model()


def tela_de_depositos(conta: contas.Conta) -> None:
    valor = user_inputs.get_float("Por favor digite o valor do depósito: ",
                      "Por favor digite um número válido no formato xxx.xx: ")
    try:
        banco.realizar_deposito(conta, depositos.criar_deposito(valor))
        view.operacoes.novo_deposito(valor)
    except exceptions.DepositoInvalidoException as e:
        view.falha(f"Falha ao realizar depósito: {str(e)}")


def tela_de_saques(conta: contas.Conta) -> None:
    valor = user_inputs.get_float("Por favor digite o valor do saque: ",
                      "Por favor digite um número válido no formato xxx.xx: ")
    try:
        banco.realizar_saque(conta=conta, saque=saques.criar_saque(valor))
        view.operacoes.novo_saque(valor)
    except (exceptions.SaldoInsuficienteException,
            exceptions.SaqueAcimaDoValorLimiteException,
            exceptions.QuantidadeDeSaquesSuperiorAoLimiteException) as e:
        view.falha(f"Falha ao realizar saque: {str(e)}")


def imprimir_extrato(conta: contas.Conta) -> None:
    saldo = contas.saldo_conta(conta)
    operacoes = contas.operacoes_conta(conta)
    extrato = extratos.criar_extrato(saldo, extrato=operacoes)

    view.operacoes.mostra_extrato(extrato)


def tela_cadastro_usuario(_) -> None:
    try:
        nome = user_inputs.get_str("Digite seu nome: ")
        data_nascimento = user_inputs.get_date("Digite sua data de nascimento (DD/MM/YYYY): ", 
                                   format="%d/%m/%Y")
        cpf = user_inputs.get_cpf("Digite o seu CPF (Somente números): ")
        logradouro = user_inputs.get_str("Digite o logradouro do endereço: ")
        numero = user_inputs.get_str("Digite o número do endereço: ")
        bairro = user_inputs.get_str("Digite o bairro do endereço: ")
        cidade = user_inputs.get_str("Digite a cidade do endereço: ")
        estado = user_inputs.get_str("Digite a sigla do estado do endereço: ").upper()
        while len(estado) > 2:
            estado = user_inputs.get_str("Digite a sigla do estado do endereço: ").upper()
        
        endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"

        usuario = usuarios.criar_usuario(nome, data_nascimento, cpf, endereco)
        model.usuario_model.salvar_usuario(usuario, USUARIO_MODEL)

        view.cadastro.mostra_novo_usuario(nome, data_nascimento, cpf, endereco)
    except exceptions.CpfJaExisteException as e:
        view.falha(f"Falha ao cadastrar usuário: {e}.")


def tela_login(_) -> None:
    cpf = user_inputs.get_cpf("Digite o seu CPF (Somente números): ")

    usuario = model.usuario_model.retornar_usuario_por_cpf(cpf, USUARIO_MODEL)

    if usuario is None:
        view.falha("Usuário não cadastrado!")
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

        opcao = user_inputs.get_natural(f"Digite um número de 1 à {ultima_opcao+1}: ") - 1
    
        if opcao == ultima_opcao:
            conta = contas.criar_conta(usuario)
            model.conta_model.salvar_conta(conta, CONTA_MODEL)
            numero = contas.numero_conta(conta)
            agencia = contas.agencia_conta(conta)
            view.cadastro.mostra_nova_conta(numero, agencia)
        elif opcao < ultima_opcao:
            secoes.salvar_parametro(SECAO, "conta_ativa", contas_usuario[opcao])
            break


def sair_da_conta(_) -> None:
    secoes.deletar_parametro(SECAO, "conta_ativa")
    view.sucesso("Logout realizado com sucesso!")


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
        view.falha("""Ocorreu um erro inesperado. Contate o administrador do sistema.
Informações:
{e}""")
        sys.exit(1)


if __name__ == "__main__":
    main()
