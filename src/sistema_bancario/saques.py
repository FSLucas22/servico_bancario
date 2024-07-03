from . import operacoes
from . import exceptions
from typing import NewType, Any


Saque = NewType('Saque', operacoes.Operacao)


def criar_saque(valor: float) -> Saque:
    if valor < 0:
        raise exceptions.SaqueInvalidoException("Saque não pode ser negativo")

    def conversor() -> dict[str, Any]:
        return {"tipo": "Saque", "valor": valor}
    
    return Saque(operacoes.Operacao({"tipo": "Saque", "valor": valor, "conversor": conversor}))


def valor_saque(saque: Saque) -> float:
    return saque["valor"]
