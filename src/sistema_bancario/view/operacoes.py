from .. import extratos


def novo_deposito(valor: float) -> None:
    print(f"Novo depósito realizado no valor de R${valor:.2f}")


def novo_saque(valor: float) -> None:
    print(f"Novo saque realizado no valor de R${valor:.2f}")


def mostra_extrato(extrato: extratos.Extrato) -> None:
    corpo = extratos.corpo_extrato(extrato)

    if not corpo:
        print("Não foram realizadas movimentações.")
        return
    
    print("Movimentações realizadas: ")

    for operacao in corpo:
        print(" - " + operacao)
    print(f'Saldo atual da conta: {extratos.saldo_extrato(extrato)}')
