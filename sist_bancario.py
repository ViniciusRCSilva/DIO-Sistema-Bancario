# IMPORTAÇÕES

import re

from datetime import datetime, timedelta

#----------------------------------------------------------------------------------------------------------------

# FUNÇÕES GLOBAIS

clientes = []

contas_correntes = []

transacoes = []

limite_saque = 1500

#----------------------------------------------------------------------------------------------------------------

# FUNÇÕES DE CRIAR CLIENTE E CONTA CORRENTE

def create_cliente(cpf, nome, data_nascimento, endereco):
    cliente = {
        "cpf": cpf, 
        "nome": nome, 
        "data de nascimento": data_nascimento, 
        "endereco": endereco
    }
    clientes.append(cliente)

def create_conta_corrente(cpf):
    conta_corrente = {
        "agencia": "0001",
        "numero_conta": len(contas_correntes) + 1,
        "cpf": cpf,
        "saldo": 0.0
    }
    contas_correntes.append(conta_corrente)
    return conta_corrente["numero_conta"]

#----------------------------------------------------------------------------------------------------------------

# FUNÇÕES DE BUSCA

def get_cliente(cpf):
    for cliente in clientes:
        if cpf == cliente["cpf"]:
            return cliente
    return None

def get_conta_corrente(conta_num):
    for conta in contas_correntes:
        if conta_num == conta["numero_conta"]:
            return conta
    return None

def get_transacoes_saque_dia(conta_num, data):
    saques_dia = 0.0
    for transacao in transacoes:
        if conta_num == transacao["conta_num"]:
            if transacao["tipo"] == "saque" and data in transacao["data_hora"]:
                saques_dia += transacao["valor"]
    return saques_dia

#----------------------------------------------------------------------------------------------------------------

def list_info_conta_corrente(conta_num):
    conta = get_conta_corrente(conta_num)
    if conta is None:
        print(f"Conta {conta_num} inexistente.")
    else:
        cliente = get_cliente(conta["cpf"])
        print(f"Titular da conta: {cliente["nome"]} - CPF: {cliente["cpf"]}\nSaldo: R${conta["saldo"]}")

#----------------------------------------------------------------------------------------------------------------

# FUNÇÕES DE USO BANCÁRIO

# Função para realizar depósitos
def op_deposito(conta_num, valor_deposito):
    conta = get_conta_corrente(conta_num)
    if conta is not None:
        conta["saldo"] += valor_deposito
        transacoes.append({
            "conta_num": conta_num,
            "data_hora": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "tipo": "deposito",
            "valor": valor_deposito
        })
        msg = f"\nDepósito de R${valor_deposito:.2f} realizado com sucesso. Saldo atualizado: R${conta["saldo"]:.2f}.\n"
        print(msg)
        print("=" * len(msg))
    else:
        print("\nConta inexistente.")
        return None

# Função para realizar saques
def op_saque(conta_num, valor_saque):
    conta = get_conta_corrente(conta_num)
    if conta is not None:
        if conta["saldo"] >= valor_saque:
            if (get_transacoes_saque_dia(conta_num, datetime.now().strftime("%d-%m-%Y")) + valor_saque) <= limite_saque:
                conta["saldo"] -= valor_saque
                transacoes.append({
                        "conta_num": conta_num,
                        "data_hora": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                        "tipo": "saque",
                        "valor": valor_saque
                    })
                msg = f"Saque de R${valor_saque:.2f} realizado com sucesso. Saldo atualizado: R${conta["saldo"]:.2f}.\n"
                print(msg)
                print("=" * len(msg))
            else:
                print(f"\nValor excede o limite de saques totais: R${limite_saque:.2f}.")
                return False
        else:
            print("\nSaldo insuficiente.")
            return False
    else:
        print("\nConta inexistente.")
        return None


# Função para exibir o extrato dentro do intervalo das datas
def op_extrato(conta_num, data_final = None, num_dias = 7):
    conta = get_conta_corrente(conta_num)

    if data_final is None:
        data_final = datetime.now()
    else:
        data_final = datetime.strptime(data_final, "%d-%m-%Y %H:%M:%S")

    data_inicial = (data_final - timedelta(days=num_dias))

    if conta is None:
        print(f"\nConta {conta_num} inexistente.")
    else:
        cabecalho = f"\nSaldo da conta {conta_num}: R${conta["saldo"]} em {datetime.strftime(data_final, "%d-%m-%Y %H:%M:%S")}"
        print(cabecalho)
        print("=" * len(cabecalho))
        if len(transacoes) == 0:
            print("\nNenhuma transação registrada.")
        else:
            for transacao in transacoes:
                data_transacao = datetime.strptime(transacao["data_hora"], "%d-%m-%Y %H:%M:%S")
                if data_inicial <= data_transacao <= data_final:
                    print(f"Transação realizada no dia {transacao['data_hora']} - {str(transacao['tipo']).capitalize()}: R${transacao['valor']:.2f}")

#----------------------------------------------------------------------------------------------------------------

def teste():
    create_cliente("123.456.789-10", "Fulano", "10/10/2000", "Rua Aurora, 135")
    create_conta_corrente("123.456.789-10")
    create_cliente("456.123.789-50", "Ciclano", "11/01/2002", "Rua Piedade, 89")
    create_conta_corrente("456.123.789-50")
    create_conta_corrente("123.456.789-10")

#----------------------------------------------------------------------------------------------------------------

# Função para pausar até que o usuário pressione uma tecla
def pressione_qualquer_tecla():
    input("\nPressione qualquer tecla para continuar...")

#----------------------------------------------------------------------------------------------------------------

def get_conta_corrente_cpf(cpf):
    for conta in contas_correntes:
        if cpf == conta["cpf"]:
            return True

def menu_inicial():
    while True:
        print("\nMENU\n")
        print("[1] Acessar conta")
        print("[2] Criar conta")
        print("[3] Listar contas")
        print("[4] Sair\n")
        opcao = input(">> ")

        if opcao == "1":
            conta_num = int(input("\nInsira o número da conta: "))
            if get_conta_corrente(conta_num) is not None:
                menu_conta(conta_num)
            else:
                print("Conta inexistente.")
                pressione_qualquer_tecla()
        elif opcao == "2":
            cpf = input("\nInsira o CPF: ")
            if get_conta_corrente_cpf(cpf):
                numero_conta = create_conta_corrente(cpf)
                print(f"\nNova conta corrente associada para o CPF: {cpf}")
                print(f"Número da conta: {numero_conta}")
                pressione_qualquer_tecla()
            else:
                menu_form_cliente(cpf)
        elif opcao == "3":
            print("\nCONTAS")
            for conta in contas_correntes:
                print("=" * 30)
                print(f"Agência: {conta["agencia"]}")
                print(f"Número da conta: {conta["numero_conta"]}")
                print(f"CPF da conta: {conta["cpf"]}")
                print(f"Saldo da conta: {conta["saldo"]}")
            pressione_qualquer_tecla()
        elif opcao == "4":
            print("\nEncerrando sistema...")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

def menu_form_cliente(cpf):
    cabecalho = f"\nPreencha as informações do cliente"
    print(cabecalho)
    print("=" * len(cabecalho))
    nome = input("\nNome: ").capitalize()
    data_nascimento = input("Data de Nascimento: ")
    endereco = input("Endereço: ").capitalize()
    print("=" * len(cabecalho))
    create_cliente(cpf, nome, data_nascimento, endereco)
    numero_conta = create_conta_corrente(cpf)
    print(f"\nCliente {nome} - {cpf} criada com sucesso.")
    print(f"Conta {numero_conta} criada com sucesso.")
    pressione_qualquer_tecla()

def menu_conta(conta_num):
    conta_numero = conta_num

    while True:
        cabecalho = f"\nOPERAÇÕES CONTA {conta_numero}"
        print(cabecalho)
        print("=" * len(cabecalho))
        list_info_conta_corrente(conta_numero)
        print("\n[1] Depositar")
        print("[2] Sacar")
        print("[3] Extrato")
        print("[4] Sair da conta\n")
        opcao = input(">> ")

        if opcao == "1":
            valor_deposito = float(input("\nInsira o valor para depósito: "))
            op_deposito(conta_numero, valor_deposito)
            pressione_qualquer_tecla()
        elif opcao == "2":
            valor_saque = float(input("\nInsira o valor para saque: "))
            op_saque(conta_numero, valor_saque)
            pressione_qualquer_tecla()
        elif opcao == "3":
            op_extrato(conta_numero)
            pressione_qualquer_tecla()
        elif opcao == "4":
            print("\nSaindo da conta...")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

#----------------------------------------------------------------------------------------------------------------

# Inicia o programa
if __name__ == "__main__":
    teste()
    menu_inicial()