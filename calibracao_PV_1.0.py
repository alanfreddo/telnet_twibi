import ast
from telnetlib import Telnet
import time
import requests
import os
import logging
import hashlib
import getpass
import socket
import netifaces

class twibi:

    def __init__(self):
        pass

    def leiaInt(self, msg):
        while True:
            try:
                n = int(input(msg))
            except (ValueError, TypeError):
                print('\033[31mERRO: Digite um número inteiro válido! \033[m')
                time.sleep(2)
                # os.system('clear')
                continue
            except (KeyboardInterrupt):
                print('\n\033[31mTempo esgotado, sessão encerrada. \033[m')
                time.sleep(2)
                # os.system('clear')
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
        print('ANTES DE CONTINUAR, HABILITE O TELNET DO SEU PRODUTO')
        print(self.linha())

    def menu(self, lista):
        # self.header('MENU PRINCIPAL')
        c = 1
        for item in lista:
            print(f'[{c}] - {item}')
            c += 1
        print(self.linha())
        opc = self.leiaInt('Digite sua opção: ')
        return opc

    def telnet_habil(self):
        self.header('Habilitando telnet, aguarde...')

    def enable_telnet(self, timeout=5, port=9000):
        while True:
            try:
                gateway = netifaces.gateways()
                self.default_gateway = gateway['default'][netifaces.AF_INET][0]
                # print(self.default_gateway)
                if self.default_gateway == '192.168.5.1':
                    self.senha_admin = getpass.getpass("Digite sua senha de administrador do Twibi: ").encode()
                    os.system('clear')
                    hash = hashlib.md5(self.senha_admin)
                    encrypt = hash.hexdigest()
                    self.telnet_habil()
                    # print(encrypt)
                    r = requests.post('http://' + f'{self.default_gateway}' + '/goform/set', json={"login": {"pwd": f'{encrypt}'}}, timeout=5)
                    cookies1 = dict(r.cookies)
                    # print(cookies1)
                    # print(f"Status Code: {r.status_code}, Response: {r.json()}")
                    if f'{r.json()}' == "{'errcode': '1'}":
                        time.sleep(2)
                        os.system('clear')
                        print('\033[31mERRO: Senha incorreta, tente novamente! \033[m')
                        time.sleep(3)
                        os.system('clear')
                        continue
                    else:
                        r = requests.get('http://' + f'{self.default_gateway}' + '/goform/telnet', cookies=cookies1, timeout=10)
                        # print(r.text)

                else:
                    self.default_gateway = input('Digite o endereço IP do seu Twibi: ')
                    try:
                        socket.setdefaulttimeout(timeout)
                        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.default_gateway, port))
                        pass
                    except socket.error as ex:
                        self.header('\033[31mERRO: SEM CONEXÃO COM O IP ' + f'{self.default_gateway}' + ', VERIFIQUE O IP DIGITADO! \033[m')
                        time.sleep(3)
                        self.enable_telnet()
                    self.senha_admin = getpass.getpass("Digite sua senha de administrador do Twibi: ").encode()
                    os.system('clear')
                    hash = hashlib.md5(self.senha_admin)
                    encrypt = hash.hexdigest()
                    self.telnet_habil()
                    # print(self.default_gateway)
                    r = requests.post('http://' + f'{self.default_gateway}' + '/goform/set', json={"login": {"pwd": f'{encrypt}'}}, timeout=5)
                    cookies1 = dict(r.cookies)
                    # print(cookies1)
                    # print(f"Status Code: {r.status_code}, Response: {r.json()}")
                    if f'{r.json()}' == "{'errcode': '1'}":
                        time.sleep(2)
                        os.system('clear')
                        print('\033[31mERRO: Senha incorreta, tente novamente! \033[m')
                        time.sleep(3)
                        os.system('clear')
                        continue
                    else:
                        r = requests.get('http://' + f'{self.default_gateway}' + '/goform/telnet', cookies=cookies1, timeout=10)
                        # print(r.text)

            except Exception:
                logging.debug('Twibi - telnet enabled!')
                time.sleep(1)
                os.system('clear')
                self.telnet_ok()
                time.sleep(2)
                os.system('clear')
                self.menu_principal()

    def OK(self):
        self.header('CONFIGURAÇÃO REALIZADA COM SUCESSO!!!')

    # def ip_modify(self):
    #     ip_address_modify = input('Digite o IP do seu Twibi: ')
    #     return ip_address_modify

    def telnet_ok(self):
        self.header('Telnet habilitado com sucesso!!!')

    def menu_principal(self):
        self.header('MENU PRINCIPAL')
        answer = self.menu(['Aumentar ajuste' , 'Diminuir ajuste', 'Ajuste atual' , 'MU-MIMO',  'Sair'])
        if answer == 1 :
            os.system( 'clear' )
            self.calibrar_A( )
            # self.calibrar_B()

        elif answer == 2 :
            os.system ( 'clear' )
            self.d_calibrar_A()
            self.d_calibrar_B()

        elif answer == 3 :
            os.system( 'clear' )
            self.status( )

        elif answer == 4 :
            os.system( 'clear' )
            self.mumimo( )

        elif answer == 5 :
            os.system( 'clear' )
            self.header( 'INTELBRAS, SEMPRE PRÓXIMA.' )
            time.sleep( 3 )
            exit( )

        else :
            print( '\033[31mERRO: Digite uma opção válida! \033[m' )
            time.sleep( 3 )
            os.system( 'clear' )
            return self.menu_principal( )

    def timeout(self, timeout=2, port=23):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.default_gateway, 23))
            pass
        except socket.error as ex:
            self.header(
                '\033[31mERRO: SEM CONEXÃO COM TELNET NO IP ' + f'{self.default_gateway}' + ', VERIFIQUE SE VOCÊ ESTA CONECTADO AO TWIBI! \033[m')
            time.sleep(3)
            self.menu_principal()

    def calibrar_A(self) :
        with Telnet( self.default_gateway , 23 , timeout = 3 ) as tn :  # LOGIN TELNET
            pwd=tn.read_until( b"login:" ).decode( 'utf-8' )
            tn.write( b'root\r\n' )
            tn.read_until( b"Password:" )
            tn.write( f'{pwd[15 :21]}'.encode( 'ascii' ) + b'\r\n' )
            # tn.interact()
            tn.read_until( b"~ # " )
            tn.set_debuglevel( 1 )
            tn.write( b'UDPserver $' )
            time.sleep( 2 )
            tn.write( b"exit\n" )
            time.sleep( 0.5 )

            with Telnet ( self.default_gateway , 23 , timeout = 3 ) as tn :  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd = tn.read_until ( b"login:" ).decode ( 'utf-8' )
                tn.write ( b'root\r\n' )
                tn.read_until ( b"Password:" )
                tn.write ( f'{pwd[15 :21]}'.encode ( 'ascii' ) + b'\r\n' )
                # tn.interact()
                tn.read_until( b"~ # " )
                tn.write ( 'flash gethw HW_TX_POWER_5G_HT40_1S_A'.encode ( 'ascii' ) + b'\n' )
                time.sleep ( 0.5 )
                tn.write ( b"exit\n" )
                time.sleep ( 0.5 )
                self.m_calibra = str ( tn.read_very_eager ( ).decode ( 'ascii' ) )
                self.m_calibra_ver = self.m_calibra[417:419]
                self.verificar()

    def calibrar_ver(self):
            ## P1 DA LISTA
            self.m_calibra_p1 = self.m_calibra[63:133]
            self.m_calibra_p1 = " ".join(self.m_calibra_p1[0:2] for i in range(0, len(self.m_calibra_p1), 2))
            # print(self.m_calibra_p1)
            ## P2 DA LISTA
            m_calibra_p2 = self.m_calibra[133:135]
            m_calibra_p2 = '0x' + m_calibra_p2
            m_calibra_p2 = ast.literal_eval(f'{m_calibra_p2}')
            m_calibra_p2 = str(m_calibra_p2 + 4) * 109
            m_calibra_p2 = " ".join(m_calibra_p2[0:2] for i in range(0, len(m_calibra_p2), 2))
            # print(m_calibra_p2)
            ## P3 DA LISTA
            m_calibra_p3 = self.m_calibra[351:353]
            m_calibra_p3 = '0x' + m_calibra_p3
            m_calibra_p3 = ast.literal_eval(f'{m_calibra_p3}')
            m_calibra_p3 = str(m_calibra_p3) * 9
            m_calibra_p3 = " ".join(m_calibra_p3[0:2] for i in range(0, len(m_calibra_p3), 2))
            # print(m_calibra_p3)
            ## P4 DA LISTA
            m_calibra_p4 = self.m_calibra[371:373]
            m_calibra_p4 = '0x' + m_calibra_p4
            m_calibra_p4 = ast.literal_eval(f'{m_calibra_p4}')
            m_calibra_p4 = str(m_calibra_p4) * 24
            m_calibra_p4 = " ".join(m_calibra_p4[0:2] for i in range(0, len(m_calibra_p4), 2))
            # print(m_calibra_p4)
            ## P5 DA LISTA
            # m_calibra_p5 = m_calibra[417:419]
            m_calibra_p5 = str(29)
            m_calibra_p5 = '0x' + m_calibra_p5
            m_calibra_p5 = ast.literal_eval(f'{m_calibra_p5}')
            m_calibra_p5 = str(m_calibra_p5) * 38
            m_calibra_p5 = " ".join(m_calibra_p5[0:2] for i in range(0, len(m_calibra_p5), 2))
            # print(m_calibra_p5)
            espaco = ' '
            UDP_IP = self.default_gateway
            UDP_PORT = 9034
            MESSAGE = b"flash set HW_WLAN0_TX_POWER_5G_HT40_1S_A " + f'{self.m_calibra_p1 + espaco + m_calibra_p2 + espaco + m_calibra_p3 + espaco + m_calibra_p4 + espaco + m_calibra_p5}'.encode(
                'ascii')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            print(MESSAGE)
            time.sleep(1)
            self.calibrar_B()

    def d_calibrar_A(self) :
        with Telnet( self.default_gateway , 23 , timeout = 3 ) as tn :  # LOGIN TELNET
            pwd=tn.read_until( b"login:" ).decode( 'utf-8' )
            tn.write( b'root\r\n' )
            tn.read_until( b"Password:" )
            tn.write( f'{pwd[15 :21]}'.encode( 'ascii' ) + b'\r\n' )
            # tn.interact()
            tn.read_until( b"~ # " )
            tn.set_debuglevel( 1 )
            tn.write( b'UDPserver $' )
            time.sleep( 2 )
            tn.write( b"exit\n" )
            time.sleep( 0.5 )
            with Telnet( self.default_gateway , 23 , timeout = 3 ) as tn :  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd=tn.read_until( b"login:" ).decode( 'utf-8' )
                tn.write( b'root\r\n' )
                tn.read_until( b"Password:" )
                tn.write( f'{pwd[15 :21]}'.encode( 'ascii' ) + b'\r\n' )
                # tn.interact()
                tn.read_until( b"~ # " )
                tn.write( 'flash gethw HW_TX_POWER_5G_HT40_1S_A'.encode( 'ascii' ) + b'\n' )
                time.sleep( 0.5 )
                tn.write( b"exit\n" )
                time.sleep( 0.5 )
                m_calibra=str( tn.read_very_eager( ).decode( 'ascii' ) )
                ## P1 DA LISTA
                m_calibra_p1 = m_calibra[63:133]
                m_calibra_p1 = " ".join(m_calibra_p1[0:2] for i in range(0, len(m_calibra_p1), 2))
                # print(m_calibra_p1)
                ## P2 DA LISTA
                m_calibra_p2 = m_calibra[133:135]
                m_calibra_p2 = '0x' + m_calibra_p2
                m_calibra_p2 = ast.literal_eval(f'{m_calibra_p2}')
                m_calibra_p2 = str(m_calibra_p2 - 4) * 109
                m_calibra_p2 = " ".join(m_calibra_p2[0:2] for i in range(0, len(m_calibra_p2), 2))
                # print(m_calibra_p2)
                ## P3 DA LISTA
                m_calibra_p3 = m_calibra[351:353]
                m_calibra_p3 = '0x' + m_calibra_p3
                m_calibra_p3 = ast.literal_eval(f'{m_calibra_p3}')
                m_calibra_p3 = str(m_calibra_p3) * 9
                m_calibra_p3 = " ".join(m_calibra_p3[0:2] for i in range(0, len(m_calibra_p3), 2))
                # print(m_calibra_p3)
                ## P4 DA LISTA
                m_calibra_p4 = m_calibra[371:373]
                m_calibra_p4 = '0x' + m_calibra_p4
                m_calibra_p4 = ast.literal_eval(f'{m_calibra_p4}')
                m_calibra_p4 = str(m_calibra_p4) * 24
                m_calibra_p4 = " ".join(m_calibra_p4[0:2] for i in range(0, len(m_calibra_p4), 2))
                # print(m_calibra_p4)
                ## P5 DA LISTA
                # m_calibra_p5 = m_calibra[417:419]
                m_calibra_p5 = str(29)
                m_calibra_p5 = '0x' + m_calibra_p5
                m_calibra_p5 = ast.literal_eval(f'{m_calibra_p5}')
                m_calibra_p5 = str(m_calibra_p5) * 38
                m_calibra_p5 = " ".join(m_calibra_p5[0:2] for i in range(0, len(m_calibra_p5), 2))
                # print(m_calibra_p5)
                espaco=' '
                UDP_IP=self.default_gateway
                UDP_PORT=9034
                MESSAGE=b"flash set HW_WLAN0_TX_POWER_5G_HT40_1S_A " + f'{m_calibra_p1 + espaco + m_calibra_p2 + espaco + m_calibra_p3 + espaco + m_calibra_p4 + espaco + m_calibra_p5}'.encode('ascii' )
                sock=socket.socket( socket.AF_INET , socket.SOCK_DGRAM )  # UDP
                sock.sendto( MESSAGE , (UDP_IP , UDP_PORT) )
                print( MESSAGE )
                time.sleep( 1 )
                self.d_calibrar_B( )

    def calibrar_B(self) :
        with Telnet ( self.default_gateway , 23 , timeout = 3 ) as tn :  # LOGIN TELNET
            # tn.set_debuglevel(1)
            pwd = tn.read_until ( b"login:" ).decode ( 'utf-8' )
            tn.write ( b'root\r\n' )
            tn.read_until ( b"Password:" )
            tn.write ( f'{pwd[15 :21]}'.encode ( 'ascii' ) + b'\r\n' )
            # tn.interact()
            tn.read_until ( b"~ # " )
            tn.write ( 'flash gethw HW_TX_POWER_5G_HT40_1S_B'.encode ( 'ascii' ) + b'\n' )
            time.sleep ( 0.5 )
            tn.write ( b"exit\n" )
            time.sleep ( 0.5 )
            m_calibra = str ( tn.read_very_eager ( ).decode ( 'ascii' ) )
            ## P1 DA LISTA
            m_calibra_p1 = m_calibra[63:133]
            m_calibra_p1 = " ".join(m_calibra_p1[0:2] for i in range(0, len(m_calibra_p1), 2))
            # print(m_calibra_p1)
            ## P2 DA LISTA
            m_calibra_p2 = m_calibra[133:135]
            m_calibra_p2 = '0x' + m_calibra_p2
            m_calibra_p2 = ast.literal_eval(f'{m_calibra_p2}')
            m_calibra_p2 = str(m_calibra_p2 + 4) * 109
            m_calibra_p2 = " ".join(m_calibra_p2[0:2] for i in range(0, len(m_calibra_p2), 2))
            # print(m_calibra_p2)
            ## P3 DA LISTA
            m_calibra_p3 = m_calibra[351:353]
            m_calibra_p3 = '0x' + m_calibra_p3
            m_calibra_p3 = ast.literal_eval(f'{m_calibra_p3}')
            m_calibra_p3 = str(m_calibra_p3) * 9
            m_calibra_p3 = " ".join(m_calibra_p3[0:2] for i in range(0, len(m_calibra_p3), 2))
            # print(m_calibra_p3)
            ## P4 DA LISTA
            m_calibra_p4 = m_calibra[371:373]
            m_calibra_p4 = '0x' + m_calibra_p4
            m_calibra_p4 = ast.literal_eval(f'{m_calibra_p4}')
            m_calibra_p4 = str(m_calibra_p4) * 24
            m_calibra_p4 = " ".join(m_calibra_p4[0:2] for i in range(0, len(m_calibra_p4), 2))
            # print(m_calibra_p4)
            ## P5 DA LISTA
            # m_calibra_p5 = m_calibra[417:419]
            m_calibra_p5 = str(29)
            m_calibra_p5 = '0x' + m_calibra_p5
            m_calibra_p5 = ast.literal_eval(f'{m_calibra_p5}')
            m_calibra_p5 = str(m_calibra_p5) * 38
            m_calibra_p5 = " ".join(m_calibra_p5[0:2] for i in range(0, len(m_calibra_p5), 2))
            # print(m_calibra_p5)
            espaco = ' '
            UDP_IP = self.default_gateway
            UDP_PORT = 9034
            MESSAGE = b"flash set HW_WLAN0_TX_POWER_5G_HT40_1S_B " + f'{m_calibra_p1 + espaco + m_calibra_p2 + espaco + m_calibra_p3 + espaco + m_calibra_p4 + espaco + m_calibra_p5}'.encode('ascii')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            print( MESSAGE )
            time.sleep(0.5)
            os.system( 'clear' )
            self.header("Calibrado com sucesso!!!")
            time.sleep(0.5)
            self.reset()

    def d_calibrar_B(self) :
        with Telnet ( self.default_gateway , 23 , timeout = 3 ) as tn :  # LOGIN TELNET
            # tn.set_debuglevel(1)
            pwd = tn.read_until ( b"login:" ).decode ( 'utf-8' )
            tn.write ( b'root\r\n' )
            tn.read_until ( b"Password:" )
            tn.write ( f'{pwd[15 :21]}'.encode ( 'ascii' ) + b'\r\n' )
            # tn.interact()
            tn.read_until ( b"~ # " )
            tn.write ( 'flash gethw HW_TX_POWER_5G_HT40_1S_B'.encode ( 'ascii' ) + b'\n' )
            time.sleep ( 0.5 )
            tn.write ( b"exit\n" )
            time.sleep ( 0.5 )
            m_calibra = str ( tn.read_very_eager ( ).decode ( 'ascii' ) )
            ## P1 DA LISTA
            m_calibra_p1 = m_calibra[63:133]
            m_calibra_p1 = " ".join(m_calibra_p1[0:2] for i in range(0, len(m_calibra_p1), 2))
            # print(m_calibra_p1)
            ## P2 DA LISTA
            m_calibra_p2 = m_calibra[133:135]
            m_calibra_p2 = '0x' + m_calibra_p2
            m_calibra_p2 = ast.literal_eval(f'{m_calibra_p2}')
            m_calibra_p2 = str(m_calibra_p2 - 4) * 109
            m_calibra_p2 = " ".join(m_calibra_p2[0:2] for i in range(0, len(m_calibra_p2), 2))
            # print(m_calibra_p2)
            ## P3 DA LISTA
            m_calibra_p3 = m_calibra[351:353]
            m_calibra_p3 = '0x' + m_calibra_p3
            m_calibra_p3 = ast.literal_eval(f'{m_calibra_p3}')
            m_calibra_p3 = str(m_calibra_p3) * 9
            m_calibra_p3 = " ".join(m_calibra_p3[0:2] for i in range(0, len(m_calibra_p3), 2))
            # print(m_calibra_p3)
            ## P4 DA LISTA
            m_calibra_p4 = m_calibra[371:373]
            m_calibra_p4 = '0x' + m_calibra_p4
            m_calibra_p4 = ast.literal_eval(f'{m_calibra_p4}')
            m_calibra_p4 = str(m_calibra_p4) * 24
            m_calibra_p4 = " ".join(m_calibra_p4[0:2] for i in range(0, len(m_calibra_p4), 2))
            # print(m_calibra_p4)
            ## P5 DA LISTA
            # m_calibra_p5 = m_calibra[417:419]
            m_calibra_p5 = str(29)
            m_calibra_p5 = '0x' + m_calibra_p5
            m_calibra_p5 = ast.literal_eval(f'{m_calibra_p5}')
            m_calibra_p5 = str(m_calibra_p5) * 38
            m_calibra_p5 = " ".join(m_calibra_p5[0:2] for i in range(0, len(m_calibra_p5), 2))
            print(m_calibra_p5)
            espaco = ' '
            UDP_IP = self.default_gateway
            UDP_PORT = 9034
            MESSAGE = b"flash set HW_WLAN0_TX_POWER_5G_HT40_1S_B " + f'{m_calibra_p1 + espaco + m_calibra_p2 + espaco + m_calibra_p3 + espaco + m_calibra_p4 + espaco + m_calibra_p5}'.encode('ascii')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            print(MESSAGE)
            time.sleep(0.5)
            os.system( 'clear' )
            self.header("Calibrado com sucesso!!!")
            time.sleep ( 0.5 )
            self.reset()

    def status(self) :
        self.status_A ( )
        self.status_B ( )

    def status_A(self) :
        with Telnet ( self.default_gateway , 23 , timeout = 3 ) as tn :  # LOGIN TELNET
            # tn.set_debuglevel(1)
            pwd = tn.read_until ( b"login:").decode ( 'utf-8' )
            tn.write ( b'root\r\n' )
            tn.read_until ( b"Password:" )
            tn.write ( f'{pwd[15 :21]}'.encode ( 'ascii' ) + b'\r\n' )
            # tn.interact()
            tn.read_until ( b"~ # " )
            tn.write ( 'flash gethw HW_TX_POWER_5G_HT40_1S_A'.encode ( 'ascii' ) + b'\n' )
            time.sleep ( 0.5 )
            tn.write ( b"exit\n" )
            time.sleep ( 0.5 )
            m_calibra = str ( tn.read_very_eager ( ).decode ( 'ascii' ) )
            print ( "Calibração atual A:" , m_calibra.split ( '=' )[1] )
            self.status_B ( )

    def status_B(self) :
        with Telnet ( self.default_gateway , 23 , timeout = 3 ) as tn :  # LOGIN TELNET
            # tn.set_debuglevel(1)
            pwd = tn.read_until ( b"login:" ).decode ( 'utf-8' )
            tn.write ( b'root\r\n' )
            tn.read_until ( b"Password:" )
            tn.write ( f'{pwd[15 :21]}'.encode ( 'ascii' ) + b'\r\n' )
            # tn.interact()
            tn.read_until ( b"~ # " )
            tn.write ( 'flash gethw HW_TX_POWER_5G_HT40_1S_B'.encode ( 'ascii' ) + b'\n' )
            time.sleep ( 0.5 )
            tn.write ( b"exit\n" )
            time.sleep ( 0.5 )
            m_calibra = str ( tn.read_very_eager ( ).decode ( 'ascii' ) )
            print ( "Calibração atual B:" , m_calibra.split ( '=' )[1] )
            time.sleep ( 2 )
            self.menu_principal ( )

    def reset(self):
        with Telnet ( self.default_gateway , 23 , timeout = 3 ) as tn :  # LOGIN TELNET
            self.header('Realizando reset do Twibi...')
            # tn.set_debuglevel(1)
            pwd = tn.read_until ( b"login:").decode ( 'utf-8' )
            tn.write ( b'root\r\n' )
            tn.read_until ( b"Password:" )
            tn.write ( f'{pwd[15 :21]}'.encode ( 'ascii' ) + b'\r\n' )
            # tn.interact()
            tn.read_until ( b"~ # " )
            tn.write ( b'cfm restore' + b'\n' )
            time.sleep ( 0.5 )
            tn.read_until(b"~ # ")
            tn.write(b'reboot' + b'\n')
            tn.read_until( b"~ # " )
            time.sleep(0.5)
            tn.write ( b"exit\n" )
            exit()

    def verificar(self):
        if self.m_calibra_ver == '29':
            print('\033[31m Este produto ja foi calibrado! \033[m')
            time.sleep(2)
            os.system('clear')
            self.header('Deseja calibrar novamente ?')
            calibra_answer = self.menu(['Sim', 'Não'])
            if calibra_answer == 1:
                self.calibrar_ver()
            elif calibra_answer == 2:
                exit()
            else:
                print('\033[31mERRO: Digite uma opção válida! \033[m')
                time.sleep(3)
                os.system('clear')
                return self.verificar()
        else:
            self.calibrar_ver()

    def mumimo(self):
        self.header( 'MU-MIMO' )
        mimo=self.menu( ['Ativar' , 'Desativar' , 'Status' , 'Voltar'] )
        if mimo == 1 :
            self.timeout( )
            with Telnet( self.default_gateway , 23 , timeout = 3 ) as tn :  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd=tn.read_until( b"login:" ).decode( 'utf-8' )
                pwd_str=str( pwd )
                if pwd_str[3 :6] == 'Int' :  # TWIBI FAST / GIGA
                    tn.write( b'root\r\n' )
                    tn.read_until( b"Password:" )
                    tn.write( f'{pwd[19 :25]}'.encode( 'ascii' ) + b'\r\n' )
                    # tn.interact()
                    tn.read_until( b"~ # " )
                    tn.write( b'cfm set wl5g.public.txbf 1\n' )
                    tn.read_until( b"~ # " )
                    os.system( 'clear' )
                    self.OK( )
                    time.sleep( 2 )
                    return self.mumimo( )
                elif pwd_str[3 :6] == 'Twi' :  # TWIBI GIGA Plus
                    tn.write( b'root\r\n' )
                    tn.read_until( b"Password:" )
                    tn.write( f'{pwd[15 :21]}'.encode( 'ascii' ) + b'\r\n' )
                    # tn.interact()
                    tn.read_until( b"~ # " )
                    tn.write( b'cfm set wl5g.public.txbf 1\n' )
                    tn.read_until( b"~ # " )
                    self.OK( )
                    time.sleep( 2 )
                    os.system( 'clear' )
                    # tn.read_until(b"~ # ")
                    # tn.write(b'reboot\n')
                    # tn.read_until(b"~ # ")
                    # os.system('clear')
                    # self.OK()
                    # time.sleep(1)
                    return self.mumimo( )
        elif mimo == 2 :
            self.timeout( )
            with Telnet( self.default_gateway , 23 , timeout = 3 ) as tn :  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd=tn.read_until( b"login:" ).decode( 'utf-8' )
                pwd_str=str( pwd )
                if pwd_str[3 :6] == 'Int' :  # TWIBI FAST / GIGA
                    tn.write( b'root\r\n' )
                    tn.read_until( b"Password:" )
                    tn.write( f'{pwd[19 :25]}'.encode( 'ascii' ) + b'\r\n' )
                    # tn.interact()
                    tn.read_until( b"~ # " )
                    tn.write( b'cfm set wl5g.public.txbf 0\n' )
                    tn.read_until( b"~ # " )
                    os.system( 'clear' )
                    self.OK( )
                    time.sleep( 2 )
                    # tn.read_until(b"~ # ")
                    # tn.write(b'reboot\n')
                    # tn.read_until(b"~ # ")
                    # os.system('clear')
                    # self.OK()
                    # time.sleep(1)
                    return self.mumimo( )
                elif pwd_str[3 :6] == 'Twi' :  # TWIBI GIGA Plus
                    tn.write( b'root\r\n' )
                    tn.read_until( b"Password:" )
                    tn.write( f'{pwd[15 :21]}'.encode( 'ascii' ) + b'\r\n' )
                    # tn.interact()
                    tn.read_until( b"~ # " )
                    tn.write( b'cfm set wl5g.public.txbf 0\n' )
                    tn.read_until( b"~ # " )
                    self.OK( )
                    time.sleep( 2 )
                    os.system( 'clear' )
                    tn.read_until(b"~ # ")
                    tn.write(b'reboot\n')
                    tn.read_until(b"~ # ")
                    os.system('clear')
                    self.OK()
                    time.sleep(1)
                    return self.mumimo( )
        elif mimo == 3 :
            self.timeout( )
            with Telnet( self.default_gateway , 23 , timeout = 3 ) as tn :  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd=tn.read_until( b"login:" ).decode( 'utf-8' )
                pwd_str=str( pwd )
                if pwd_str[3 :6] == 'Int' :  # TWIBI FAST / GIGA
                    tn.write( b'root\r\n' )
                    tn.read_until( b"Password:" )
                    tn.write( f'{pwd[19 :25]}'.encode( 'ascii' ) + b'\r\n' )
                    # tn.interact()
                    tn.read_until( b"~ # " )
                    tn.write( 'cfm get wl5g.public.txbf'.encode( 'ascii' ) + b'\n' )
                    time.sleep( 0.5 )
                    tn.write( b"exit\n" )
                    time.sleep( 0.5 )
                    m_mimo=str( tn.read_very_eager( ).decode( 'ascii' ) )
                    os.system( 'clear' )
                    if m_mimo == 0 :
                        self.header( 'MU-MIMO ESTA DESATIVADO ' )
                    else :
                        self.header( "MU-MIMO ESTA ATIVADO" )
                    time.sleep( 5 )
                    return self.mumimo( )

                elif pwd_str[3 :6] == 'Twi' :  # TWIBI GIGA Plus
                    tn.write( b'root\r\n' )
                    tn.read_until( b"Password:" )
                    tn.write( f'{pwd[15 :21]}'.encode( 'ascii' ) + b'\r\n' )
                    # tn.interact()
                    tn.read_until( b"~ # " )
                    tn.write( 'cfm get wl5g.public.txbf'.encode( 'ascii' ) + b'\n' )
                    time.sleep( 0.5 )
                    tn.write( b"exit\n" )
                    time.sleep( 0.5 )
                    print(tn.read_very_eager( ).decode( 'ascii' ))
                    m_mimo=str( tn.read_very_eager( ).decode( 'ascii' ) )
                    print("oi")
                    print(m_mimo)
                    os.system( 'clear' )
                    if m_mimo == 0 :
                        self.header( 'MU-MIMO ESTA DESATIVADO ' )
                    else :
                        self.header( "MU-MIMO ESTA ATIVADO" )
                    time.sleep( 5 )
                    return self.mumimo( )

        elif mimo == 4 :
            return self.menu_principal( )

        else :
            print( '\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m' )
            time.sleep( 3 )
            os.system( 'clear' )
            return self.mumimo( )

t = twibi()
t.enable_telnet()