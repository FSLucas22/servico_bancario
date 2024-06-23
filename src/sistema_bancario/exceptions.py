class DepositoInvalidoException(Exception):
    pass


class SaldoInsuficienteException(Exception):
    pass


class SaqueInvalidoException(Exception):
    pass


class SaqueAcimaDoValorLimiteException(Exception):
    pass


class QuantidadeDeSaquesSuperiorAoLimiteException(Exception):
    pass


class CpfJaExisteException(Exception):
    pass


class ContaNaoExisteException(Exception):
    pass
