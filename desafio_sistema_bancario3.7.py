from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
    
class Interface:

    def __init__(self):
        self.opcao = input(
''' \n
ENTRE COM UMA DAS OPÇÕES ABAIXO PARA ACESSAR O SITE DO BANCO:
=> Digite 1 para pessoa fÍsica
=> Digite 2 para pessoa jurÍdica
=> Digite 3 para sair
Digite aqui:''')
        if int(self.opcao) < 1 or int(self.opcao) > 3:
            print('! Opcao inexistente. !\n')
            return
        if self.opcao == '1':
            self._cpf = input('=> Digite seu CPF (11 digitos, somente números): ')
        if self.opcao == '2':
            print('! Opcao em construção. Favor escolher outra opção. !')
            return
            self._cnpj = input('Digite seu CNPJ (xxx digitos, somente números): ')

    def verificacao_cadastro_cpf(self,cpf):
        with open('Clientes_Cadastrados.txt','r') as file:
            for line in file:
                if cpf in line:
                    return True

    def login(self,cpf):
        with open('Clientes_Cadastrados.txt','r') as file:
            for line in file:
                if self._cpf in line:
                    usuario=line.split(',')
                    self._usuario_nome=usuario[1]
                    self._senha=input('=> Digite sua senha:')
                    if self._senha == usuario[2]: #confirmaçao da senha
                        if usuario[5]=='fim\n': # exibicao do nome e contas atreladas
                            print(f'\nBem vindo(a) {usuario[1]}: Agencia: {usuario[3]}, Conta: {usuario[4]}')
                        else:
                            print(f'\nBem vindo(a) {usuario[1]}: Agencia: {usuario[3]}, Contas: {usuario[4]} e {usuario[5]}') 
                        self._conta=input('=> Digite o numero da sua conta:')
                        if self._conta == usuario[4] or self._conta == usuario[5]:
                            self._agencia=usuario[3]
                            return self._cpf,self._senha,self._agencia,self._conta,self._usuario_nome
                        else:
                            print('! Conta inválida. !')
                            return self._cpf,self._senha,None,None,self._usuario_nome
                    else: 
                        print('! Senha inválida. !')
                        return self._cpf,None,None,None,self._usuario_nome
                        
    @property
    def cpf(self):
        return self._cpf

    @property
    def senha(self):
        return self._senha
    
    @property
    def agencia(self):
        return self._agencia

    @property
    def conta(self):
        return self._conta

    @property
    def usuario_nome(self):
        return self._usuario_nome

    def verificacao_cadastro_cnpj(self): # EM DESENVOLVIMENTO
        return
        with open('Empresas_Cadastradas.txt','r') as file:
            for line in file:
                if self.cnpj in line:
                    return True


class Pessoa():
    def __init__(self):
        self._nome = input(f'=> Digite {self.texto}:')  
        self._senha = input('=> Crie uma senha de 4 numeros:')

    @property
    def nome(self):
        return self._nome

    @property
    def senha(self):
        return self._senha


class PessoaFisica(Pessoa):
    def __init__(self,cpf):
        print('\n#### CADASTRO DE PESSOA FISICA ####')
        self._cpf = cpf
        self.texto = 'seu nome completo'
        super().__init__()
        
    @property
    def cpf(self):
        return self._cpf
    

class PessoaJuridica(Pessoa): # EM DESENVOLVIMENTO
    def __init__(self):
        self._cnpj = input('=> Digite o CNPJ (somente numeros):')
        self.texto = 'nome do estabelecimento'
        self.texto2 = 'telefone do estabelecimento'
        super().__init__()

    @property
    def cnpj(self):
        return self._cnpj


class RegistroDadosPessoaFisica:
    
    def __init__(self,cpf,nome,senha,agencia,conta):
        impressao=(f'{cpf},{nome},{senha},{agencia},{conta},fim\n')
        with open('Clientes_Cadastrados.txt','a') as file:
            file.write(impressao)  


class Agencia:
    def __init__(self):
        self._id = '0001'

    @property
    def id(self):
        return self._id


class Conta(ABC):
    @abstractmethod
    def criar_conta(self):
        pass

    @abstractmethod
    def ler_saldo(self):
        pass

    @abstractmethod
    def verificacao_quantidade(self):
        pass

    @abstractmethod
    def registro_nova_conta(self):
        pass


class ContaCorrente(Conta):

    def __init__(self):
        self._saldo = '0.00'

    def criar_conta(self,cpf,agencia):
        with open('Contas.txt','r') as file:
            for line in file:
                conta=line
        file = open(f'{cpf}_{agencia}_{conta}.txt','w')
        data,dia = FuncoesAuxiliares.data_time()
        file.write(f'Saldo    - Data e hora: {data},  Valor: R${self._saldo}\n')
        conta=int(conta)
        conta+=1 # atualização da numeração da conta sequencial
        with open('Contas.txt','w') as file:
            file.write(f'{conta}')
        return conta-1 # numero da nova conta

    def ler_saldo(cpf,agencia,conta): # static method
        with open(f'{cpf}_{agencia}_{conta}.txt','r') as file:
                for line in file:
                    if 'Saldo' in line:
                        dividir_linha=line.split(' ')
                        saldo=dividir_linha[-1]
                        saldo_formatado=saldo
                        saldo=float(saldo.replace('R$',''))
                print('### Saldo atual:',saldo_formatado)
                return saldo

    def verificacao_quantidade(self,cpf):
        with open('Clientes_Cadastrados.txt','r') as file:
            for line in file: # obtençao do nome do usuario
                if cpf in line:
                    usuario=line.split(',')
            if len(usuario) == 7:
                print('! Cada usuário pode ter no máximo duas contas corrente distintas. !')
                return True
    
    def registro_nova_conta(self,conta,nova_conta):
        with open('Clientes_Cadastrados.txt','r') as file: # leitura do arquivo dos clientes cadastrados e carregamento dos dados numa variavel temporaria (arquivo)
            arquivo=file.read()
        novo_arquivo=arquivo.replace(f'{conta},fim',f'{conta},{nova_conta},fim') # inclusao dos dados alterados no arquivo dos clientes cadastrados
        with open('Clientes_Cadastrados.txt','w') as file:
            file.write(novo_arquivo)
        print (f'Conta de numero {nova_conta} foi cadastrada com sucesso.')


class ContaPoupanca(Conta):
    pass


class ContaInvestimento(Conta):
    pass


class Extrato():

    def registro(opcao,valor,saldo,cpf,agencia,conta):
        data,dia=FuncoesAuxiliares.data_time()
        if opcao == '1':
            impressao= (f'Deposito - Data e hora: {data},  Valor: +R${valor:.2f},  Saldo: R${saldo:.2f}\n')
        if opcao == '2':
            impressao= (f'Saque    - Data e hora: {data},  Valor: -R${valor:.2f},  Saldo: R${saldo:.2f}\n')
        with open(f'{cpf}_{agencia}_{conta}.txt','a') as file:
            file.write(impressao)  
    
    def exibir_extrato(cpf,agencia,conta):
        with open(f'{cpf}_{agencia}_{conta}.txt','r') as file:
            print('\n####################################### EXTRATO #######################################\n')
            print(f'                    CPF: {cpf}, AGENCIA: {agencia}, CONTA CORRENTE: {conta}\n')
            for line in file:
                print(line,end='')
            print('\n#######################################################################################\n')


class Transacao(ABC):

    @abstractmethod
    def executar_ordem(self):
        pass

    @property
    @abstractproperty
    def valor(self):
        pass

    
class Deposito(Transacao):
    def __init__(self):
        self._valor = float(input('=> Digite o valor desejado para o deposito:'))

    def executar_ordem(self,valor,saldo):
        if valor > 0:
            saldo += valor # incremento do saldo
        else:
            print('! Valor invalido !')
        return valor,saldo

    @property
    def valor(self):
        return self._valor


class Saque(Transacao):

    def __init__(self):
        self.LIMITE_QUANTIDADE_SAQUES = 3
        self.LIMITE_VALOR_SAQUE = 500.00
        self._valor = float(input('=> Digite o valor desejado para o saque:'))

    def limites_saque(self,valor,saldo,cpf,agencia,conta):
        numero_saques=0
        data,dia=FuncoesAuxiliares.data_time()
        with open(f'{cpf}_{agencia}_{conta}.txt','r') as file:
            for line in file:
                if f'Saque    - Data e hora: {dia}' in line:
                    numero_saques +=1
        if numero_saques >= self.LIMITE_QUANTIDADE_SAQUES:
            print('! Limite de saques (3 saques por dia) excedido. !')
            return True
        elif valor > self.LIMITE_VALOR_SAQUE:
            print(f'! Limite de valor (R${self.LIMITE_VALOR_SAQUE: .2f}) excedido. !')
            return True
        elif valor > saldo:
            print('! Saldo insuficiente. !') 
            return True
        elif valor < 0:
            print('! Valor inválido, tente novamente. !')
            return True
        return False

    def executar_ordem(self,valor,saldo):
        if valor > 0:
            saldo -= valor # decremento do saldo
        else:
            print('! Valor invalido !')
        return valor,saldo
    
    @property
    def valor(self):
        return self._valor


class FuncoesAuxiliares():

    def data_time():
        now = datetime.now()
        data = now.strftime("%d/%m/%Y %H:%M:%S")
        dia = now.strftime("%d/%m/%Y")
        return data,dia

    def menu():
        print( """

        [1] Depositar
        [2] Sacar
        [3] Extrato
        [4] Cadastro de nova conta
        [5] Sair

        """)
        opcao = input('=> Digite uma das opcões acima:')
        return opcao


class CarlosFalconeBank:

    def __init__(self):
        print('''\n
          ####################################
            BEM VINDO AO CARLOS FALCONE BANK
          ####################################
           ''')

    def acionamento_menu(self,cpf,senha,agencia,conta,saldo):

        while True:
            
            opcao=FuncoesAuxiliares.menu()

            if opcao =='1': # deposito
                deposito=Deposito()
                valor=deposito.valor
                valor,saldo = deposito.executar_ordem(valor,saldo)
                Extrato.registro(opcao,valor,saldo,cpf,agencia,conta)

            elif opcao =='2': # saque
                saque=Saque()
                valor=saque.valor
                resultado_limites = saque.limites_saque(valor,saldo,cpf,agencia,conta)
                if resultado_limites is False:
                    valor,saldo = saque.executar_ordem(valor,saldo)
                    Extrato.registro(opcao,valor,saldo,cpf,agencia,conta)

            elif opcao == '3': # extrato
                Extrato.exibir_extrato(cpf,agencia,conta)
                
            elif opcao == '4': # cadastro de nova conta corrente
                nova_conta_corrente = ContaCorrente()
                if nova_conta_corrente.verificacao_quantidade(cpf):
                    return
                nova_conta = nova_conta_corrente.criar_conta(cpf,agencia)
                nova_conta_corrente.registro_nova_conta(conta,nova_conta)
            
            elif opcao == '5': # sair
                print(
'''\n
CARLOS FALCONE BANK AGRADECE A PREFERENCIA.

=> Aperte a tecla F5 para iniciar.\n ''')
                break

            else:
                print('! Digite uma opçao válida. !')

    def principal(self):
        interface = Interface() # entradas: tipo pessoa e cpf
        if interface.opcao == '1':
            cpf = interface.cpf
            if len(cpf) < 11:
                print('CPF inválido.')
                return
            if interface.verificacao_cadastro_cpf(cpf): # verificacao de CPF cadastrado
                cpf,senha,agencia,conta,usuario_nome = interface.login(cpf) # login com cpf e senha
                if senha == None or agencia == None:
                    return
                saldo = ContaCorrente.ler_saldo(cpf,agencia,conta)
                self.acionamento_menu(cpf,senha,agencia,conta,saldo)
            else:
                pessoa_fisica = PessoaFisica(cpf) # realizar cadastro do cliente (cpf, nome, senha)
                agencia = Agencia() 
                conta_corrente = ContaCorrente()
                conta = conta_corrente.criar_conta(pessoa_fisica.cpf,agencia.id)
                RegistroDadosPessoaFisica(pessoa_fisica.cpf,pessoa_fisica.nome,pessoa_fisica.senha,agencia.id,conta) # salva os dados do cliente num arquivo .txt (cpf, nome, senha, conta)
                print('Cadastro Pessoa Física realizado com sucesso.')
                self.principal()
        
        elif interface.opcao == '2': # EM DESENVOLVIMENTO
            return


bank=CarlosFalconeBank() # Chamada da classe principal
bank.principal()
