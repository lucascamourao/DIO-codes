"""
Useful extensions: 
Black formatter
isort 
"""

import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
from pathlib import Path

# pega(dinamicamente) a pasta  deste arquivo
ROOT_PATH = Path(__file__).parent


class ContasIterador:
    def __init__(self, contas):
        # elemento de contas: list
        self.contas = contas
        self._contador = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._contador]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._contador += 1


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.index_conta = 0

    def realizar_transacao(self, conta, transacao):
        limite_transacoes = 10
        if len(conta.historico.transacoes_do_dia()) >= limite_transacoes:
            print(f"Atingiu o numero limite de {limite_transacoes}trasações diárias!\n")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


# done (ordem diferente dos argumentos)
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: CPF({self.cpf})>"


# adicionei
class PessoaJuridica(Cliente):
    # antes (02/07/2024): def __init__(self, endereco, cnpj, nome):
    def __init__(self, nome, cnpj, endereco):
        super().__init__(endereco)
        self.cnpj = cnpj
        self.nome = nome

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: CNPJ({self.cpf})>"


# done
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self._saldo

        if valor > saldo:
            print("There is not enough money. ")

        elif valor > 0:
            self._saldo -= valor
            print("Money successfully withdrawn!")
            return True

        else:
            print("Error")

        return False

    def depositar(self, valor):
        if valor >= 0:
            self._saldo += valor
            print("Money successfully deposited!")
            return True

        print("Error!")

        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @classmethod
    def nova_conta(cls, cliente, numero, limite, limite_saques):
        return cls(numero, cliente, limite, limite_saques)

    def sacar(self, valor):
        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == Saque.__name__
            ]
        )

        if valor > self._limite:
            print("The value exceeds the maximum allowed to withdraw. ")

        elif numero_saques > self._limite_saques:
            print("Maximum number of withdraw exceeded. ")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.agencia}', '{self.numero}', '{self.cliente.nome}')>"


# done
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        if not tipo_transacao:  # listar tudo
            for transacao in self._transacoes:
                yield transacao
        else:
            for transacao in self._transacoes:
                if transacao["tipo"].lower() == tipo_transacao.lower():
                    yield transacao

    # done
    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []

        for transacao in self._transacoes:
            data = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if data == data_atual:
                transacoes.append(transacao)
        return transacoes


# done
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


# done
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# done
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
        try:
            with open(ROOT_PATH / "log.txt", "a") as arquivo_log:
                registro = f"[{data_hora}] Função '{func.__name__}' executada com argumentos {args} e {kwargs}. Retornou {resultado}\n"
                arquivo_log.write(registro)
        except Exception as e:
            print(f"Houve um erro: {e}")
            print("erro")
            """
            testar: 
            [3] Novo usuário
            cnpj: 123
            lucas20 gamer
            adress

            error: 'PessoaJuridica' object has no attribute 'cpf'
            """

        # print(f"{data_hora}: {func.__name__.upper()}")
        return resultado

    return envelope


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [1]\tNova conta
    [2]\tListar contas
    [3]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente_cpf(cpf, user_list):
    filtered_users = [cliente for cliente in user_list if cliente.cpf == cpf]
    # get all the users with this CPF. Since we'll always find only 1, it's only needed the first (and only) element in the list
    return filtered_users[0] if filtered_users else None


def filtrar_cliente_cnpj(cnpj, user_list):
    filtered_users = [cliente for cliente in user_list if cliente.cnpj == cnpj]
    # get all the users with this CNPJ. Since we'll always find only 1, it's only needed the first (and only) element in the list
    return filtered_users[0] if filtered_users else None


# done (fixed)
def recuperar_conta_cliente(cliente: Cliente):
    if cliente.contas == []:
        print("O cliente não possui conta. ")
        return
    num_de_contas = len(cliente.contas)
    if num_de_contas == 1:
        return cliente.contas[0]

    while True:
        escolha = int(
            input(
                f"""Você tem {num_de_contas}.
                            Qual conta você escolhe? """
            )
        )
        if escolha >= 1 and escolha <= num_de_contas:
            break
        print(f"Invalído. Escolha um número entre 1 e {num_de_contas}")

    return cliente.contas[escolha]


@log_transacao
def depositar(clientes: list, pessoaFisica: bool):
    if pessoaFisica:
        cpf = input("Digite o CPF da pessoa: ")
        cliente = filtrar_cliente_cpf(cpf, clientes)
    else:
        cnpj = input("Digite o CNPJ: ")
        cliente = filtrar_cliente_cnpj(cnpj, clientes)

    if not cliente:
        print("Client not found! ")
        return

    valor = float(input("Digite o valor do depósito: \n"))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


# adicionei o parametro pessoaFisica (bool)
@log_transacao
def sacar(clientes: list, pessoaFisica: bool):
    if pessoaFisica:
        cpf = input("Digite o CPF da pessoa: ")
        cliente = filtrar_cliente_cpf(cpf, clientes)
    else:
        cnpj = input("Digite o CNPJ: ")
        cliente = filtrar_cliente_cnpj(cnpj, clientes)

    if not cliente:
        print("Client not found! ")
        return

    valor = float(input("Digite o valor do saque: \n"))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


@log_transacao
def exibir_extrato(clientes: list, pessoaFisica: bool):
    if pessoaFisica:
        cpf = input("Digite o CPF da pessoa: ")
        cliente = filtrar_cliente_cpf(cpf, clientes)
    else:
        cnpj = input("Digite o CNPJ: ")
        cliente = filtrar_cliente_cnpj(cnpj, clientes)

    if not cliente:
        print("Client not found! ")
        return

    conta = recuperar_conta_cliente(cliente)

    transacoes = conta.historico.trasacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações. "
    else:
        # for transacao in conta.historico.gerar_relatorio(tipo_transacao="saque")
        for transacao in transacoes:
            extrato += f"\n{transacao['data']} \n{transacao['tipo']}:\n\t R${transacao['valor']:.2f} "
            # extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"Saldo: R${conta.saldo: .2f}")


@log_transacao
def criar_cliente(clientes: list, pessoaFisica: bool):
    if pessoaFisica:
        cpf = input("Digite o CPF da pessoa: ")
        cliente = filtrar_cliente_cpf(cpf, clientes)
    else:
        cnpj = input("Digite o CNPJ: ")
        cliente = filtrar_cliente_cnpj(cnpj, clientes)

    if cliente:
        print("Já existe esse cliente! ")
        return

    if pessoaFisica:
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input(
            "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): "
        )

        cliente = PessoaFisica(
            nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco
        )
    else:
        nome = input("Informe o nome da empresa: ")
        endereco = input(
            "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): "
        )

        cliente = PessoaJuridica(nome=nome, cnpj=cnpj, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


@log_transacao
def criar_conta(numero_conta, clientes: list, contas, pessoaFisica: bool):
    if pessoaFisica:
        cpf = input("Digite o CPF da pessoa: ")
        cliente = filtrar_cliente_cpf(cpf, clientes)
    else:
        cnpj = input("Digite o CNPJ: ")
        cliente = filtrar_cliente_cnpj(cnpj, clientes)

    if not cliente:
        print("Client not found! ")
        return

    conta = ContaCorrente.nova_conta(
        cliente=cliente, numero=numero_conta, limite=500, limite_saques=50
    )
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    if contas == []:
        print("No accounts created! \n")
        return

    for conta in ContasIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes_cpf = []
    cliente_cnpj = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            while True:
                res = input(
                    """Pessoa física ou jurídica? \n
                                    1 - Pessoa física
                                    2 - Pessoa jurídica """
                )
                if res == "1" or res == "2":
                    break
                print("Invalido")

            if res == "1":
                depositar(clientes_cpf, True)
            elif res == "2":
                depositar(cliente_cnpj, False)

        elif opcao == "s":
            while True:
                res = input(
                    """Pessoa física ou jurídica? \n
                                    1 - Pessoa física
                                    2 - Pessoa jurídica """
                )
                if res == "1" or res == "2":
                    break
                print("Invalido")

            if res == "1":
                sacar(clientes_cpf, True)
            elif res == "2":
                sacar(clientes_cpf, False)

        elif opcao == "e":
            while True:
                res = input(
                    """Pessoa física ou jurídica? \n
                                    1 - Pessoa física
                                    2 - Pessoa jurídica """
                )
                if res == "1" or res == "2":
                    break
                print("Invalido")

            if res == "1":
                exibir_extrato(clientes_cpf, True)
            elif res == "2":
                exibir_extrato(cliente_cnpj, False)

        # criar conta
        elif opcao == "1":
            while True:
                res = input(
                    """Pessoa física ou jurídica? \n
                                    1 - Pessoa física
                                    2 - Pessoa jurídica """
                )
                if res == "1" or res == "2":
                    break
                print("Invalido")

            numero_conta = len(contas) + 1

            if res == "1":
                criar_conta(numero_conta, clientes_cpf, contas, True)
            elif res == "2":
                criar_conta(numero_conta, cliente_cnpj, contas, False)

        # listar contas
        elif opcao == "2":
            listar_contas(contas)

        # criar cliente
        elif opcao == "3":
            while True:
                res = input(
                    """Pessoa física ou jurídica? \n
                                    1 - Pessoa física
                                    2 - Pessoa jurídica """
                )
                if res == "1" or res == "2":
                    break
                print("Invalido")

            if res == "1":
                criar_cliente(clientes_cpf, True)
            elif res == "2":
                criar_cliente(cliente_cnpj, False)

        elif opcao == "q":
            break

        else:
            print("Invalid operation. Try again.")


main()
