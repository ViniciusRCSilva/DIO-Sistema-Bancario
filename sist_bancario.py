# IMPORTAÇÕES

from abc import ABC, abstractmethod

from datetime import date, datetime

#----------------------------------------------------------------------------------------------------------------

# CLASSES

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.now()

    def formatar_data(self):
        return self._data.strftime("%H:%M:%S %d/%m/%Y")

    def registrar(self, conta):
        conta._saldo += self._valor
        conta._historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.now()

    def registrar(self, conta):
        if conta._saldo >= self._valor:
            conta._saldo -= self._valor
            conta._historico.adicionar_transacao(self)
            return True
        else:
            return False

class Conta:
    _numero_conta_global = 1000

    def __init__(self, cliente, agencia):
        self._saldo = 0.0
        self._numero = Conta._gerar_numero_conta()
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def _gerar_numero_conta(cls):
        numero = cls._numero_conta_global
        cls._numero_conta_global += 1
        return numero

    def get_saldo(self):
        return self._saldo

    @staticmethod
    def nova_conta(cliente, numero, agencia):
        return Conta(cliente, numero, agencia)

    def sacar(self, valor):
        if self._saldo >= valor:
            self._saldo -= valor
            self._historico.adicionar_transacao(Saque(valor))
            return True
        return False

    def depositar(self, valor):
        self._saldo += valor
        self._historico.adicionar_transacao(Deposito(valor))
        return True
    
    def get_transacoes(self):
        transacoes_formatadas = []
        for transacao in self._historico._transacoes:
            transacoes_formatadas.append(f"{type(transacao).__name__}: R${transacao._valor:.2f} às {transacao._data.strftime("%H:%M:%S - %d/%m/%Y")}")
        return transacoes_formatadas

    def extrato(self):
        print(f"\n--- Extrato da Conta {self._numero} ---")
        print(f"Cliente: {self._cliente._nome}")
        print(f"Agência: {self._agencia}")
        print(f"Saldo: R${self._saldo:.2f}")
        print("Transações:")
        transacoes = self.get_transacoes()
        if not transacoes:
            print("Ainda não houveram transações nessa conta.")
        else:
            for transacao in transacoes:
                print(transacao)

class ContaCorrente(Conta):
    def __init__(self, cliente, agencia, limite, limite_saques):
        super().__init__(cliente, agencia)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_diarios = {} 

    def _registrar_saque(self, valor):
        hoje = date.today()
        if hoje in self._saques_diarios:
            self._saques_diarios[hoje] += valor
        else:
            self._saques_diarios[hoje] = valor

    def _total_sacado_hoje(self):
        hoje = date.today()
        return self._saques_diarios.get(hoje, 0.0)

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

#----------------------------------------------------------------------------------------------------------------

clientes = []
contas = []

#----------------------------------------------------------------------------------------------------------------

# FUNÇÕES DE CRIAÇÃO DE CLIENTE E CONTA

def criar_novo_cliente():
    nome = input("Nome do Cliente: ")
    cpf = input("CPF: ")
    endereco = input("Endereço: ")
    data_nascimento = input("Data de Nascimento (YYYY-MM-DD): ")
    data_nascimento = date.fromisoformat(data_nascimento)
    cliente = PessoaFisica(endereco, cpf, nome, data_nascimento)
    clientes.append(cliente)
    return cliente

def criar_nova_conta(cliente=None):
    if cliente is None:
        cliente_cpf = input("CPF do Cliente existente: ")
        cliente = next((c for c in clientes if c._cpf == cliente_cpf), None)
        if cliente is None:
            print("Cliente não encontrado.")
            return
    agencia = input("Agência: ")
    limite = float(input("Limite da Conta Corrente: "))
    limite_saques = int(input("Limite de Saques Diários: "))
    conta_corrente = ContaCorrente(cliente, agencia, limite, limite_saques)
    cliente.adicionar_conta(conta_corrente)
    contas.append(conta_corrente)
    print(f"Conta criada com sucesso! Número da conta: {conta_corrente._numero}")

def visualizar_contas():
    if not contas:
        print("Nenhuma conta encontrada.")
    else:
        for conta in contas:
            print(f"Número: {conta._numero} | Cliente: {conta._cliente._nome} | Saldo: R${conta.get_saldo():.2f}")
            print("=" * 100)

#----------------------------------------------------------------------------------------------------------------

# Quando o usuário inserir o número da conta, será possível realizar operações daquela conta.
def entrar_na_conta():
    numero_conta = int(input("Insira o número da conta: "))
    conta = next((c for c in contas if c._numero == numero_conta), None)
    if conta is None:
        print("Conta não encontrada.")
        return

    while True:
        print(f"\n--- Menu da Conta {numero_conta} ---")
        print("1. Realizar Depósito")
        print("2. Realizar Saque")
        print("3. Visualizar Extrato")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            valor = float(input("Valor do Depósito: "))
            deposito = Deposito(valor)
            conta.depositar(valor)
            print(f"Depósito de R${valor:.2f} realizado com sucesso!")
            pressione_qualquer_tecla()

        elif opcao == "2":
            valor = float(input("Valor do Saque: "))
            saque = Saque(valor)
            if conta.sacar(valor):
                print(f"Saque de R${valor:.2f} realizado com sucesso!")
                pressione_qualquer_tecla()
            else:
                print("Saldo insuficiente ou limite de saque atingido.")
                pressione_qualquer_tecla()

        elif opcao == "3":
            conta.extrato()
            pressione_qualquer_tecla()

        elif opcao == "4":
            print("Saindo da conta...")
            break

        else:
            print("Opção inválida. Tente novamente.")

#----------------------------------------------------------------------------------------------------------------

# Função para pausar até que o usuário pressione uma tecla
def pressione_qualquer_tecla():
    input("\nPressione qualquer tecla para continuar...")

#----------------------------------------------------------------------------------------------------------------

def teste():
    nome = "Vinicius Silva"
    cpf = "000.000.000-00"
    endereco = "Rua Teste, 123"
    data_nascimento = date(2002, 3, 23)
    
    cliente = PessoaFisica(endereco, cpf, nome, data_nascimento)
    clientes.append(cliente)
    
    agencia = "0001"
    limite = 500.00
    limite_saques = 1500
    conta_corrente = ContaCorrente(cliente, agencia, limite, limite_saques)
    cliente.adicionar_conta(conta_corrente)
    contas.append(conta_corrente)

#----------------------------------------------------------------------------------------------------------------

def menu_principal():
    while True:
        print("\n--- Menu Principal ---")
        print("1. Entrar na Conta")
        print("2. Criar Conta")
        print("3. Visualizar Contas")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            entrar_na_conta()

        elif opcao == "2":
            print("\n--- Criar Conta ---")
            print("1. Criar nova conta para novo cliente")
            print("2. Associar nova conta a um cliente existente")
            sub_opcao = input("Escolha uma opção: ")

            if sub_opcao == "1":
                cliente = criar_novo_cliente()
                criar_nova_conta(cliente)
            elif sub_opcao == "2":
                criar_nova_conta()
            else:
                print("Opção inválida. Tente novamente.")

        elif opcao == "3":
            print("\n--- Contas ---")
            visualizar_contas()
            pressione_qualquer_tecla()

        elif opcao == "4":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

#----------------------------------------------------------------------------------------------------------------

# Chamada para o menu principal
teste()
menu_principal()