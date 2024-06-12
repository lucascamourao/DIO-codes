# Sistema Bancário 1.0

menu = """

[d] Deposit
[w] Withdraw
[e] Bank Statement (Extract)
[q] Quit

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    option = input(menu)

    if option == "d":
        while True:
            deposito = float(input('How much do you want to deposit? '))
            if deposito >= 0:
                saldo += deposito
                extrato += f"Deposit: R$ {deposito: .2f}\n"
                break
            print('Error!')
        
    elif option == "w":
        saque = float(input('How much do you want to withdraw? '))
        
        if saque > saldo:
            print('There is not enough money. ')

        elif saque > limite:
            print('The value exceeds the maximum allowed to withdraw. ')
        
        elif numero_saques > LIMITE_SAQUES:
            print('Maximum number of withdraw exceeded. ')

        elif saque > 0:
            saldo -= saque
            numero_saques += 1
            extrato += f"Withdraw: R$ {saque: .2f} \n"

        else:
            print('Error')

    elif option == "e":
        print(('Bank Statement').center(30, '='))
        if extrato:
            print(extrato)
        else:
            print('Any transactions were made.')
        
        print(f"Account balance: R$ {saldo: .2f}")
        print('='*30)

    elif option == "q":
        break

    else:
        print("Invalid operation. Try again.")
