import json

class SaldoInsuficienteError(Exception):
    """Exceção lançada quando o saldo é insuficiente para a operação."""
    pass

class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

    def __repr__(self):
        return f"Cliente({self.nome}, CPF: {self.cpf})"

class Conta:
    def __init__(self, numero, cliente, saldo_inicial=0.0):
        self.numero = numero
        self.cliente = cliente
        self.saldo = saldo_inicial

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print(f"Depósito de R${valor:.2f} realizado com sucesso.")
        else:
            print("Valor de depósito deve ser positivo.")

    def sacar(self, valor):
        if valor > self.saldo:
            raise SaldoInsuficienteError(f"Erro: Saldo insuficiente. Saldo atual: R${self.saldo:.2f}")
        if valor <= 0:
            print("O valor do saque deve ser positivo.")
            return
        
        self.saldo -= valor
        print(f"Saque de R${valor:.2f} realizado.")

    def transferir(self, valor, conta_destino):
        try:
            self.sacar(valor)
            conta_destino.depositar(valor)
            print(f"Transferência de R${valor:.2f} para {conta_destino.cliente.nome} concluída.")
        except SaldoInsuficienteError as e:
            print(f"Falha na transferência: {e}")

class Banco:
    def __init__(self, nome):
        self.nome = nome
        self.contas = {}

    def adicionar_conta(self, conta):
        self.contas[conta.numero] = conta

    def buscar_conta(self, numero):
        return self.contas.get(numero)

# --- Exemplo de Uso ---

# 1. Instanciando o Banco e Clientes
meu_banco = Banco("Python Bank")
cliente1 = Cliente("Alice", "123.456.789-00")
cliente2 = Cliente("Bruno", "987.654.321-11")

# 2. Abrindo Contas
conta_alice = Conta("001", cliente1, 900.0)
conta_bruno = Conta("002", cliente2, 400.0)
meu_banco.adicionar_conta(conta_alice)
meu_banco.adicionar_conta(conta_bruno)

# 3. Operações
print(f"Saldo Inicial Alice: R${conta_alice.saldo}")

conta_alice.depositar(200)
conta_alice.transferir(150, conta_bruno)

# Tentativa de saque maior que o saldo
try:
    print("\nTentando sacar R$1000 da conta da Alice...")
    conta_alice.sacar(1000)
except SaldoInsuficienteError as e:
    print(e)

print(f"\nSaldo Final Alice: R${conta_alice.saldo}")
print(f"Saldo Final Bruno: R${conta_bruno.saldo}")