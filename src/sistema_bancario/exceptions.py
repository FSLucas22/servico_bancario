class DepositoInvalidoException(Exception):
    pass


class SaldoInsuficienteException(Exception):
    pass


class SaqueAcimaDoValorLimiteException(Exception):
    pass


class QuantidadeDeSaquesSuperiorAoLimiteException(Exception):
    pass


class CpfJaExisteException(Exception):
    pass
