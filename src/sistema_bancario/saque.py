from . import operacao
from typing import NewType, Any


Saque = NewType('Saque', operacao.Operacao)


def criar_saque(valor: float) -> Saque:
    def conversor() -> dict[str, Any]:
        return {"tipo": "Saque", "valor": valor}
    
    return Saque(operacao.Operacao({"tipo": "Saque", "valor": valor, "conversor": conversor}))


def valor_saque(saque: Saque) -> float:
    return saque["valor"]
