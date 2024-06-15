# Sistema Bancário 1.0

import textwrap

# keyword-only arguments
def withdraw(*, saldo, limite, numero_saques, limite_saques, extrato):
    saque = float(input('How much do you want to withdraw? '))
        
    if saque > saldo:
        print('There is not enough money. ')

    elif saque > limite:
        print('The value exceeds the maximum allowed to withdraw. ')
    
    elif numero_saques > limite_saques:
        print('Maximum number of withdraw exceeded. ')

    elif saque > 0:
        saldo -= saque
        numero_saques += 1
        extrato += f"Withdraw: R$ {saque: .2f} \n"

    else:
        print('Error')

    return saldo, extrato

# positional-only arguments
def deposit(saldo, extrato, /):
    while True:
        deposito = float(input('How much do you want to deposit? '))
        if deposito >= 0:
            saldo += deposito
            extrato += f"Deposit: R$ {deposito: .2f}\n"
            break
        print('Error!')

    return saldo, extrato

# positional and keyword
def extract(saldo, /, *, extrato):
    print(('Bank Statement').center(30, '='))
    if extrato:
        print(extrato)
    else:
        print('Any transactions were made.')
    
    print(f"Account balance: R$ {saldo: .2f}")
    print('='*30)

    return saldo, extrato

def create_user(user_list: list):
    cpf = input('Enter the CPF: \n')
    cpf = cpf.replace('.', '')

    usuario = filter_user(cpf, user_list)

    if usuario: 
        print('User already exists!')
        return

    name = input('Enter the name of the user: \n')
    date_of_birth = input('Enter the date of birth (dd-mm-yyyy): \n')
    adress = input('Enter the adress(logradouro, numero - bairro - cidade/SIGLA_ESTADO): \n')

    '''for key, value in user_list:
        if ((key == 'cpf') and (value == cpf)):
            return 'User already exists! '
    '''  
    user_list.append({"name": name, "date_of_birth": date_of_birth, "cpf": cpf, "adress": adress})

    return user_list

def filter_user(cpf, user_list):
    filtered_users = [user for user in user_list if user["cpf"] == str(cpf)]
    # get all the users with this CPF. Since we'll always find only 1, it's only needed the first (and only) element in the list
    return filtered_users[0] if filtered_users else None

def create_accont(agency, user_list, account_list):
    cpf = input('Enter the CPF of the user: \n') 

    user = filter_user(cpf, user_list)

    if user:
        account_number = len(account_list) + 1
        account_list.append({"agency": agency, "account_number": account_number, "user": user})
        print("Account created! \n")
        
        return account_list
    
    print("User not found! \n")

def list_accounts(account_list):
    for account in account_list:
        line = f"""
        Agency: \t{account['agency']}
        Account Number: \t{account['account_number']}
        Owner: \t{account['user']['name']}
        """
        print("="*100)
        print(textwrap.dedent(line))

menu = """

[d] Deposit
[w] Withdraw
[e] Bank Statement (Extract)
[1] New Account
[2] List accounts
[3] New User 
[q] Quit

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
AGENCIA = "0001"
user_list = []
account_list = []

while True:

    option = input(menu)

    if option == "d":
        saldo, extrato = deposit(saldo, extrato)
        
    elif option == "w":
        saldo, extrato = withdraw(saldo=saldo, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES, extrato=extrato)

    elif option == "e":
        saldo, extrato = extract(saldo, extrato=extrato)

    elif option == "1":
        account_list = create_accont(AGENCIA, user_list, account_list)

    elif option == "2":
        if account_list == []:
            print("There is no account created.")
        else:
            list_accounts(account_list)

    elif option == "3":
        user_list = create_user(user_list)

    elif option == "q":
        break

    else:
        print("Invalid operation. Try again.")
