# Define o limite máximo de saque
limite = 1500
# Variável auxiliar para controlar o total de saques realizados
aux_limite = 0
# Saldo inicial da conta
saldo = 0

# Função para realizar depósitos
def op_deposito():
    global saldo
    valor = float(input("Digite o valor para depósito: "))
    # Adiciona o valor depositado ao saldo
    saldo += valor
    print(f"Depósito R${valor:.2f} realizado com sucesso. Saldo atualizado: R${saldo:.2f}.\n")
    pressione_qualquer_tecla()

def op_saque():
    global saldo, limite, aux_limite
    valor = float(input("Digite o valor para saque: "))
    # Verifica se o saldo é suficiente para o saque
    if valor > saldo:
        print("Saldo insuficiente.")
        pressione_qualquer_tecla()
    else:
        # Verifica se o limite de saques foi atingido
        if aux_limite == limite or aux_limite >= limite:
            print(f"Valor excede o limite de saques totais: R${limite:.2f}.\n")
            pressione_qualquer_tecla()
        else:
            # Atualiza o total de saques realizados e o saldo
            aux_limite += valor
            saldo -= valor
            print(f"Saque de R${valor:.2f} realizado com sucesso. Saldo atualizado: R${saldo:.2f}.\n")
            pressione_qualquer_tecla()

# Função para exibir o extrato
def op_extrato():
    global saldo
    print(f"Saldo atual: R${saldo:.2f}.\n")
    pressione_qualquer_tecla()

# Função para pausar até que o usuário pressione uma tecla
def pressione_qualquer_tecla():
    input("Pressione qualquer tecla para continuar...")

# Loop principal do programa
while True:
    # Solicita ao usuário que escolha uma operação
    operacao = input("""
Digite a letra para prosseguir com a operação:
                     
    Digite 'd' para acessar a operação de depósito;
    Digite 's' para acessar a operação de saque;
    Digite 'e' para acessar a operação de extrato;
    Digite 'q' para finalizar a sessão.
                     
>> """)
    
    if operacao == 'd':
        op_deposito()
    elif operacao == 's':
        op_saque()
    elif operacao == 'e':
        op_extrato()
    elif operacao == 'q':
        print("Sessão finalizada.")
        break
    else:
        print("Operação inválida. Tente novamente.")
