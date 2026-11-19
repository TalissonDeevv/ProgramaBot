"""Aula 09: classes, objetos, herança e métodos especiais."""


class ContaBancaria:
    banco = "Banco do Estudante"  # atributo de classe (compartilhado)

    def __init__(self, titular: str, saldo: float = 0.0) -> None:
        self.titular = titular  # atributos de instância
        self.saldo = saldo

    def depositar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("Depósito deve ser positivo.")
        self.saldo += valor

    def sacar(self, valor: float) -> None:
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")
        self.saldo -= valor

    @property
    def em_dia(self) -> bool:
        """Usado como atributo: conta.em_dia"""
        return self.saldo >= 0

    def __repr__(self) -> str:
        return f"{type(self).__name__}(titular={self.titular!r}, saldo={self.saldo:.2f})"


class ContaPoupanca(ContaBancaria):  # herança
    def __init__(self, titular: str, saldo: float = 0.0, taxa: float = 0.01) -> None:
        super().__init__(titular, saldo)  # chama o __init__ da classe-mãe
        self.taxa = taxa

    def render(self) -> None:
        self.saldo += self.saldo * self.taxa


conta = ContaBancaria("Ana", 100)
conta.depositar(50)
conta.sacar(30)
print(conta, "| em dia?", conta.em_dia, "|", conta.banco)

poupanca = ContaPoupanca("Bruno", 1000, taxa=0.05)
poupanca.render()
print(poupanca)

try:
    conta.sacar(10_000)
except ValueError as erro:
    print("Erro:", erro)

print("Poupança também é ContaBancaria?", isinstance(poupanca, ContaBancaria))
