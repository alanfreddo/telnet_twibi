from telnetlib import Telnet
import time
import requests
import os
import logging
import hashlib
import getpass
import netifaces


class twibi:

    def __init__(self):
        pass

    def habilita_telnet(self, senha_admin):
        self.senha_admin = senha_admin
        try:
            # gateway = netifaces.gateways()
            # default_gateway = gateway['default'][netifaces.AF_INET][0]
            os.system('cls')
            hash = hashlib.md5(senha_admin)
            encrypt = hash.hexdigest()
            self.telnet_habil()
            # print(encrypt)
            r = requests.post('http://192.168.5.1/goform/set', json={"login": {"pwd": f'{encrypt}'}})
            # print(f"Status Code: {r.status_code}, Response: {r.json()}")
            if f'{r.json()}' == "{'errcode': '1'}":
                time.sleep(2)
                os.system('cls')
                print('\033[31mERRO: Senha incorreta, tente novamente! \033[m')
                time.sleep(3)
                os.system('cls')
            else:
                r = requests.get('http://192.168.5.1/goform/telnet', timeout=10)
        except Exception:
            logging.debug('Twibi - telnet enabled!')
            time.sleep(1)

    def menu_principal(self):
        self.menu(['Alterar canal do Wi-Fi 5Ghz', 'Alterar canal do Wi-Fi 2.4Ghz', 'Alterar largura de banda 5Ghz',
                       'Alterar largura de banda 2.4Ghz', 'Desabilitar SIP ALG', 'Sair'])

    def leiaInt(self, msg):
        while True:
            try:
                n = int(input(msg))
            except (ValueError, TypeError):
                print('\033[31mERRO: Digite um número inteiro válido! \033[m')
                continue
            except (KeyboardInterrupt):
                print('\n\033[31mTempo esgotado, tente novamente. \033[m')
                return 0
            else:
                return n

    def linha(self, size=50):
        return '-' * size

    def header(self, text):
        print(self.linha())
        print(text.center(50))
        print(self.linha())

    def lembrete(self):
        print(self.linha())
        print('ANTES DE CONTINUAR HABILITE O TELNET DO SEU PRODUTO')
        print(self.linha())

    def menu(self, lista):
        self.header('MENU PRINCIPAL')
        c = 1
        for item in lista:
            print(f'{c} - {item}')
            c += 1
        print(self.linha())
        opc = self.leiaInt('Digite sua opção: ')
        return opc

    def OK(self):
        self.header('CONFIGURACAO APLICADA COM SUCESSO')

    def canais_5(self):
        self.header('Canais suportados: 36, 40, 44, 46, 48, 149, 153, 157 e 161')

    def canais_2(self):
        self.header('Canais suportados: 1 até 13')

    def largura_5(self):
        self.header('Larguras de banda suportadas para 5Ghz: 20, 40 e 80')

    def largura_2(self):
        self.header('Larguras de banda suportadas para 2.4Ghz: 20 e 40')

    def telnet_habil(self):
        self.header('Habilitando telnet, aguarde...')

    def telnet_ok(self):
        self.header('Telnet habilitado com sucesso!!!')

t = twibi()
senha_admin = getpass.getpass("Digite sua senha de administrador do Twibi: ").encode()
t.habilita_telnet(senha_admin)
