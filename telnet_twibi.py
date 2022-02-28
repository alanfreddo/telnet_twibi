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
                # os.system('cls')
                continue
            except (KeyboardInterrupt):
                print('\n\033[31mTempo esgotado, sessão encerrada. \033[m')
                time.sleep(2)
                # os.system('cls')
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
                    os.system('cls')
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
                        os.system('cls')
                        print('\033[31mERRO: Senha incorreta, tente novamente! \033[m')
                        time.sleep(3)
                        os.system('cls')
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
                        self.header('\033[31mERRO: SEM CONEXÃO COM O IP ' + f'{self.default_gateway}' + ', VERIFIQUE O IP DIGITADO!\033[m')
                        time.sleep(3)
                        self.enable_telnet()
                    self.senha_admin = getpass.getpass("Digite sua senha de administrador do Twibi: ").encode()
                    os.system('cls')
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
                        os.system('cls')
                        print('\033[31mERRO: Senha incorreta, tente novamente! \033[m')
                        time.sleep(3)
                        os.system('cls')
                        continue
                    else:
                        r = requests.get('http://' + f'{self.default_gateway}' + '/goform/telnet', cookies=cookies1, timeout=10)
                        # print(r.text)

            except Exception:
                logging.debug('Twibi - telnet enabled!')
                time.sleep(1)
                os.system('cls')
                self.telnet_ok()
                time.sleep(2)
                os.system('cls')
                self.menu_principal()

    def ip_modify(self):
        ip_address_modify = input('Digite o IP do seu Twibi: ')
        return ip_address_modify

    def telnet_ok(self):
        self.header('Telnet habilitado com sucesso!!!')

    def OK(self):
        self.header('CONFIGURAÇÃO REALIZADA COM SUCESSO, APLIQUE AS CONFIGURAÇÕES NO MENU PRINCIPAL')

    def apply_ok(self):
        self.header('CONFIGURAÇÕES APLICADAS COM SUCESSO!')

    def menu_principal(self):
        self.header('MENU PRINCIPAL')
        answer = self.menu(['Canal Wi-Fi 5Ghz', 'Canal Wi-Fi 2.4Ghz', 'Largura de banda 5Ghz', 'Largura de banda 2.4Ghz', 'SIP ALG', 'IPv6', 'SSID', 'Aplicar Configurações', 'Sair'])
        if answer == 1:
            os.system('cls')
            self.canais_5()

        elif answer == 2:
            os.system('cls')
            self.canais_2()

        elif answer == 3:
            os.system('cls')
            self.largura_5G()

        elif answer == 4:
            os.system('cls')
            self.largura_2G()

        elif answer == 5:
            os.system('cls')
            self.sip_alg()

        elif answer == 6:
            os.system('cls')
            self.ipv6()

        elif answer == 7:
            os.system('cls')
            self.ssid()

        elif answer ==8:
            os.system('cls')
            self.apply()

        elif answer == 9:
            os.system('cls')
            self.header('INTELBRAS, SEMPRE PRÓXIMA.')
            time.sleep(3)
            exit()

        else:
            print('\033[31mERRO: Digite uma opção válida!\033[m')
            time.sleep(3)
            os.system('cls')
            return self.menu_principal()

    def canais_5(self):
        self.header('CANAL 5Ghz')
        copc5 = self.menu(['Alterar Canal', 'Visualizar Canal', 'Voltar'])
        if copc5 == 1:
            self.header('Canais suportados: 36, 40, 44, 46, 48, 149, 153, 157 e 161')
            self.header('Digite 0 para cancelar')
            canal_5 = self.leiaInt('Digite o canal desejado: ')
            if (canal_5 == 36) or (canal_5 == 40) or (canal_5 == 44) or (canal_5 == 46) or (canal_5 == 48) or (
                    canal_5 == 149) or (canal_5 == 153) or (canal_5 == 157) or (canal_5 == 161):
                with Telnet(self.default_gateway, 23, timeout=3) as tn:  #LOGIN TELNET
                    # tn.set_debuglevel(1)
                    pwd = tn.read_until(b"login:").decode('utf-8')
                    pwd_str = str(pwd)
                    if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                        tn.write(b'root\r\n')
                        tn.read_until(b"Password:")
                        tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                        # tn.interact()
                        tn.read_until(b"~ # ")
                        if (canal_5 == 149) or (canal_5 == 153) or (canal_5 == 157) or (canal_5 == 161):
                            tn.write(b'cfm set wl5g.lock.channel ' + f'{canal_5:"^5}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            tn.write(b'cfm set wl5g.public.channel ' + f'{canal_5:"^5}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            # tn.write(b'cfm post netctrl 19?op=3,wl_rate=5\n')
                            # tn.read_until(b"~ # ")
                            # tn.write(b'reboot\n')
                            self.OK()
                            time.sleep(3)
                            os.system('cls')
                            return self.menu_principal()
                        else:
                            tn.write(b'cfm set wl5g.lock.channel ' + f'{canal_5:"^4}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            tn.write(b'cfm set wl5g.public.channel ' + f'{canal_5:"^4}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            # tn.write(b'reboot\n')
                            # tn.read_until(b"~ # ")
                            # tn.write(b'cfm post netctrl 19?op=3,wl_rate=5\n')
                            # tn.read_until(b"~ # ")
                            self.OK()
                            time.sleep(3)
                            os.system('cls')
                            return self.menu_principal()
                    elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                        tn.write(b'root\r\n')
                        tn.read_until(b"Password:")
                        tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                        # tn.interact()
                        tn.read_until(b"~ # ")
                        if (canal_5 == 149) or (canal_5 == 153) or (canal_5 == 157) or (canal_5 == 161):
                            tn.write(b'cfm set wl5g.lock.channel ' + f'{canal_5:"^5}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            tn.write(b'cfm set wl5g.public.channel ' + f'{canal_5:"^5}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            # tn.write(b'reboot\n')
                            # tn.read_until(b"~ # ")
                            # tn.write(b'cfm post netctrl 19?op=3,wl_rate=5\n')
                            # tn.read_until(b"~ # ")
                            self.OK()
                            time.sleep(3)
                            os.system('cls')
                            return self.menu_principal()
                        else:
                            tn.write(b'cfm set wl5g.lock.channel ' + f'{canal_5:"^4}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            tn.write(b'cfm set wl5g.public.channel ' + f'{canal_5:"^4}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            # tn.write(b'reboot\n')
                            # tn.read_until(b"~ # ")
                            # tn.write(b'cfm post netctrl 19?op=3,wl_rate=5\n')
                            # tn.read_until(b"~ # ")
                            self.OK()
                            time.sleep(3)
                            os.system('cls')
                            return self.menu_principal()

            elif canal_5 == 0:
                return self.canais_5()

            else:
                print('\033[31mERRO: Você digitou um canal inválido, tente novamente! \033[m')
                time.sleep(3)
                os.system('cls')
                return self.canais_5()
        elif copc5 == 2:
            with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd = tn.read_until(b"login:").decode('utf-8')
                pwd_str = str(pwd)
                if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get wl5g.lock.channel'.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    tn.write(b"exit\n")
                    time.sleep(0.5)
                    m_canal5g = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    print('O canal 5Ghz configurado é: ' + m_canal5g.split()[3])
                    time.sleep(5)
                    return self.canais_5()

                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    # tn.set_debuglevel(1)
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get wl5g.lock.channel'.encode('ascii') + b'\n')
                    time.sleep(1)
                    tn.write(b"exit\n")
                    time.sleep(1)
                    m_canal5g = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    print('O canal 5Ghz configurado é: ' + m_canal5g.split()[3])
                    time.sleep(5)
                    return self.canais_5()
        elif copc5 == 3:
            return self.menu_principal()

        else:
            print('\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m')
            time.sleep(3)
            os.system('cls')
            return self.canais_2()

    def canais_2(self):
        self.header('CANAL 2.4Ghz')
        copc2 = self.menu(['Alterar Canal', 'Visualizar canal', 'Voltar'])
        if copc2 == 1:
            self.header('Canais suportados: 1 até 13')
            self.header('Digite 0 para cancelar')
            canal_2 = self.leiaInt('Digite o canal desejado: ')
            if (canal_2 == 1) or (canal_2 == 2) or (canal_2 == 3) or (canal_2 == 4) or (canal_2 == 5) or (canal_2 == 6) or (
                    canal_2 == 7) or (canal_2 == 8) or (canal_2 == 9) or (canal_2 == 10) or (canal_2 == 11) or (
                    canal_2 == 12) or (canal_2 == 13):
                with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                    # tn.set_debuglevel(1)
                    pwd = tn.read_until(b"login:").decode('utf-8')
                    pwd_str = str(pwd)
                    if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                        tn.write(b'root\r\n')
                        tn.read_until(b"Password:")
                        tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                        # tn.interact()
                        tn.read_until(b"~ # ")
                        if (canal_2 == 10) or (canal_2 == 11) or (canal_2 == 12) or (canal_2 == 13):
                            tn.write(b'cfm set auto_channel "0"\n')
                            tn.read_until(b"~ # ")
                            tn.write(b'cfm set wl2g.lock.channel ' + f'{canal_2:"^4}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            tn.write(b'cfm set wl2g.public.channel ' + f'{canal_2:"^4}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            # tn.write(b'cfm post netctrl 19?op=3,wl_rate=24\n')
                            # tn.read_until(b"~ # ")
                            os.system('cls')
                            self.OK()
                            time.sleep(3)
                            return self.menu_principal()
                        else:
                            tn.write(b'cfm set auto_channel "0"\n')
                            tn.read_until(b"~ # ")
                            tn.write(b'cfm set wl2g.lock.channel ' + f'{canal_2:"^3}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            tn.write(b'cfm set wl2g.public.channel ' + f'{canal_2:"^3}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            # tn.write(b'cfm post netctrl 19?op=3,wl_rate=24\n')
                            # tn.read_until(b"~ # ")
                            os.system('cls')
                            self.OK()
                            time.sleep(3)
                            return self.menu_principal()
                    elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                        tn.write(b'root\r\n')
                        tn.read_until(b"Password:")
                        tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                        # tn.interact()
                        tn.read_until(b"~ # ")
                        if (canal_2 == 10) or (canal_2 == 11) or (canal_2 == 12) or (canal_2 == 13):
                            tn.write(b'cfm set auto_channel "0"\n')
                            tn.read_until(b"~ # ")
                            tn.write(b'cfm set wl2g.lock.channel ' + f'{canal_2:"^4}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            tn.write(b'cfm set wl2g.public.channel ' + f'{canal_2:"^4}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            # tn.write(b'cfm post netctrl 19?op=3,wl_rate=24\n')
                            # tn.read_until(b"~ # ")
                            os.system('cls')
                            self.OK()
                            time.sleep(3)
                            return self.menu_principal()
                        else:
                            tn.write(b'cfm set auto_channel "0"\n')
                            tn.read_until(b"~ # ")
                            tn.write(b'cfm set wl2g.lock.channel ' + f'{canal_2:"^3}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            tn.write(b'cfm set wl2g.public.channel ' + f'{canal_2:"^3}'.encode('ascii') + b'\n')
                            tn.read_until(b"~ # ")
                            # tn.write(b'cfm post netctrl 19?op=3,wl_rate=24\n')
                            # tn.read_until(b"~ # ")
                            # tn.write(b'reboot\n')
                            # tn.read_until(b"~ # ")
                            os.system('cls')
                            self.OK()
                            time.sleep(3)
                            return self.menu_principal()

            elif canal_2 == 0:
                return self.canais_2()

            else:
                print('\033[31mERRO: Você digitou um canal inválido, tente novamente! \033[m')
                time.sleep(3)
                os.system('cls')
                return self.canais_2()
        elif copc2 == 2:
            with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd = tn.read_until(b"login:").decode('utf-8')
                pwd_str = str(pwd)
                if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get wl2g.lock.channel'.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    tn.write(b"exit\n")
                    time.sleep(0.5)
                    m_canal2g = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    print('O canal 2.4Ghz configurado é: ' + m_canal2g.split()[3])
                    time.sleep(5)
                    return self.canais_2()

                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get wl2g.lock.channel'.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    tn.write(b"exit\n")
                    time.sleep(0.5)
                    m_canal2g = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    print('O canal 2.4Ghz configurado é: ' + m_canal2g.split()[3])
                    time.sleep(5)
                    return self.canais_2()
        elif copc2 == 3:
            return self.menu_principal()

        else:
            print('\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m')
            time.sleep(3)
            os.system('cls')
            return self.canais_2()

    def largura_5G(self):
        self.header('LARGURA DE BANDA 5Ghz')
        lopc5 = self.menu(['Alterar Largura de Banda', 'Visualizar Largura de Banda', 'Voltar'])
        if lopc5 == 1:
            self.header('Larguras de banda suportadas para 5Ghz: 20, 40 e 80')
            self.header('Digite 0 para cancelar')
            largura_5 = self.leiaInt('Qual a largura de banda 5Ghz você deseja: ')
            if (largura_5 == 20) or (largura_5 == 40) or (largura_5 == 80):
                with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                    # tn.set_debuglevel(1)
                    pwd = tn.read_until(b"login:").decode('utf-8')
                    pwd_str = str(pwd)
                    if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                        tn.write(b'root\r\n')
                        tn.read_until(b"Password:")
                        tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                        # tn.interact()
                        tn.read_until(b"~ # ")
                        tn.write(b'cfm set wl5g.lock.bandwidth ' + f'{largura_5:"^4}'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        # tn.write(b'reboot\n')
                        # tn.read_until(b"~ # ")
                        os.system('cls')
                        self.OK()
                        time.sleep(3)
                        return self.menu_principal()
                    elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                        tn.write(b'root\r\n')
                        tn.read_until(b"Password:")
                        tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                        # tn.interact()
                        tn.read_until(b"~ # ")
                        tn.write(b'cfm set wl5g.lock.bandwidth ' + f'{largura_5:"^4}'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        # tn.write(b'reboot\n')
                        # tn.read_until(b"~ # ")
                        os.system('cls')
                        self.OK()
                        time.sleep(1)
                        return self.menu_principal()

            elif largura_5 == 0:
                return self.largura_5G()

            else:
                print('\033[31mERRO: Você digitou largura de banda inválida, tente novamente! \033[m')
                time.sleep(3)
                os.system('cls')
                return self.largura_5G()
        elif lopc5 == 2:
            with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd = tn.read_until(b"login:").decode('utf-8')
                pwd_str = str(pwd)
                if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get wl5g.lock.bandwidth'.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    tn.write(b"exit\n")
                    time.sleep(0.5)
                    m_largura5g = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    print('A largura de banda configurada em 5Ghz é: ' + m_largura5g.split()[3])
                    time.sleep(5)
                    return self.largura_5G()

                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get wl5g.lock.bandwidth'.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    tn.write(b"exit\n")
                    time.sleep(0.5)
                    m_largura5g = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    print('A largura de banda configurada em 5Ghz é: ' + m_largura5g.split()[3])
                    time.sleep(5)
                    return self.largura_5G()

        elif lopc5 == 3:
            return self.menu_principal()

        else:
            print('\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m')
            time.sleep(3)
            os.system('cls')
            return self.largura_5G()

    def largura_2G(self):
        self.header('LARGURA DE BANDA 2.4Ghz')
        lopc2 = self.menu(['Alterar Largura de Banda', 'Visualizar Largura de Banda', 'Voltar'])
        if lopc2 == 1:
            self.header('Larguras de banda suportadas para 2.4Ghz: 20 e 40')
            self.header('Digite 0 para cancelar')
            largura_2 = self.leiaInt('Qual a largura de banda 2.4Ghz você deseja: ')
            if (largura_2 == 20) or (largura_2 == 40):
                with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                    # tn.set_debuglevel(1)
                    pwd = tn.read_until(b"login:").decode('utf-8')
                    pwd_str = str(pwd)
                    if pwd_str[3:6] == 'Int':  #TWIBI FAST / GIGA
                        tn.write(b'root\r\n')
                        tn.read_until(b"Password:")
                        tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                        # tn.interact()
                        tn.read_until(b"~ # ")
                        tn.write(b'cfm set wl2g.lock.bandwidth ' + f'{largura_2:"^4}'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        # tn.write(b'reboot\n')
                        # tn.read_until(b"~ # ")
                        os.system('cls')
                        self.OK()
                        time.sleep(3)
                        return self.menu_principal()
                    elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                        tn.write(b'root\r\n')
                        tn.read_until(b"Password:")
                        tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                        # tn.interact()
                        tn.read_until(b"~ # ")
                        tn.write(b'cfm set wl2g.lock.bandwidth ' + f'{largura_2:"^4}'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        # tn.write(b'reboot\n')
                        # tn.read_until(b"~ # ")
                        os.system('cls')
                        self.OK()
                        time.sleep(1)
                        return self.menu_principal()

            elif largura_2 == 0:
                return self.largura_2G()

            else:
                print('\033[31mERRO: Você digitou uma largura de banda inválido, tente novamente! \033[m')
                time.sleep(3)
                os.system('cls')
                return self.largura_2G()

        elif lopc2 == 2:
            with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd = tn.read_until(b"login:").decode('utf-8')
                pwd_str = str(pwd)
                if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get wl2g.lock.bandwidth'.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    tn.write(b"exit\n")
                    time.sleep(0.5)
                    m_largura2g = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    print('A largura de banda configurada em 2.4Ghz é: ' + m_largura2g.split()[3])
                    time.sleep(5)
                    return self.largura_2G()

                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get wl2g.lock.bandwidth'.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    tn.write(b"exit\n")
                    time.sleep(0.5)
                    m_largura2g = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    print('A largura de banda configurada em 2.4Ghz é: ' + m_largura2g.split()[3])
                    time.sleep(5)
                    return self.largura_2G()

        elif lopc2 == 3:
            return self.menu_principal()

        else:
            print('\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m')
            time.sleep(3)
            os.system('cls')
            return self.largura_2G()

    def sip_alg(self):
        self.header('SIP ALG')
        alg = self.menu(['Ativar', 'Desativar', 'Status', 'Voltar'])
        if alg == 1:
            with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd = tn.read_until(b"login:").decode('utf-8')
                pwd_str = str(pwd)
                if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write(b'cfm set sip_en 1\n')
                    tn.read_until(b"~ # ")
                    os.system('cls')
                    self.OK()
                    time.sleep(2)
                    # tn.read_until(b"~ # ")
                    # tn.write(b'reboot\n')
                    # tn.read_until(b"~ # ")
                    # os.system('cls')
                    # self.OK()
                    # time.sleep(1)
                    return self.menu_principal()
                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write(b'cfm set sip_en 1\n')
                    tn.read_until(b"~ # ")
                    self.OK()
                    time.sleep(2)
                    os.system('cls')
                    # tn.read_until(b"~ # ")
                    # tn.write(b'reboot\n')
                    # tn.read_until(b"~ # ")
                    # os.system('cls')
                    # self.OK()
                    # time.sleep(1)
                    return self.menu_principal()
        elif alg == 2:
            with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd = tn.read_until(b"login:").decode('utf-8')
                pwd_str = str(pwd)
                if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write(b'cfm set sip_en 0\n')
                    tn.read_until(b"~ # ")
                    os.system('cls')
                    self.OK()
                    time.sleep(2)
                    # tn.read_until(b"~ # ")
                    # tn.write(b'reboot\n')
                    # tn.read_until(b"~ # ")
                    # os.system('cls')
                    # self.OK()
                    # time.sleep(1)
                    return self.menu_principal()
                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write(b'cfm set sip_en 0\n')
                    tn.read_until(b"~ # ")
                    self.OK()
                    time.sleep(2)
                    os.system('cls')
                    # tn.read_until(b"~ # ")
                    # tn.write(b'reboot\n')
                    # tn.read_until(b"~ # ")
                    # os.system('cls')
                    # self.OK()
                    # time.sleep(1)
                    return self.menu_principal()
        elif alg == 3:
            with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd = tn.read_until(b"login:").decode('utf-8')
                pwd_str = str(pwd)
                if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get sip_en'.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    tn.write(b"exit\n")
                    time.sleep(0.5)
                    m_sip = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    if m_sip == 0:
                        self.header('SIP ALG ESTA DESATIVADO ')
                    else:
                        self.header("SIP ALG ESTA ATIVADO")
                    time.sleep(5)
                    return self.sip_alg()

                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get sip_en'.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    tn.write(b"exit\n")
                    time.sleep(0.5)
                    m_sip = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    if m_sip == 0:
                        self.header('SIP ALG ESTA DESATIVADO ')
                    else:
                        self.header("SIP ALG ESTA ATIV0")
                    time.sleep(5)
                    return self.sip_alg()

        elif alg == 4:
            return self.menu_principal()

        else:
            print('\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m')
            time.sleep(3)
            os.system('cls')
            return self.sip_alg()

    def ipv6(self):
        self.header('IPV6')
        opcipv6 = self.menu(['Ativar', 'Desativar', 'Status', 'Voltar'])
        if opcipv6 == 1:
            with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd = tn.read_until(b"login:").decode('utf-8')
                pwd_str = str(pwd)
                if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write(b'cfm set ipv6.enable 1\n')
                    tn.read_until(b"~ # ")
                    # tn.write(b'reboot\n')
                    # tn.read_until(b"~ # ")
                    self.OK()
                    time.sleep(3)
                    os.system('cls')
                    return self.menu_principal()
                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write(b'cfm set ipv6.enable 1\n')
                    tn.read_until(b"~ # ")
                    # tn.write(b'reboot\n')
                    # tn.read_until(b"~ # ")
                    self.OK()
                    time.sleep(3)
                    os.system('cls')
                    return self.menu_principal()
        elif opcipv6 == 2:
            with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd = tn.read_until(b"login:").decode('utf-8')
                pwd_str = str(pwd)
                if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write(b'cfm set ipv6.enable 0\n')
                    tn.read_until(b"~ # ")
                    # tn.write(b'reboot\n')
                    # tn.read_until(b"~ # ")
                    self.OK()
                    time.sleep(3)
                    os.system('cls')
                    return self.menu_principal()
                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write(b'cfm set ipv6.enable 0\n')
                    tn.read_until(b"~ # ")
                    # tn.write(b'reboot\n')
                    # tn.read_until(b"~ # ")
                    self.OK()
                    time.sleep(3)
                    os.system('cls')
                    return self.menu_principal()
        elif opcipv6 == 3:
            with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd = tn.read_until(b"login:").decode('utf-8')
                pwd_str = str(pwd)
                if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get ipv6.enable'.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    tn.write(b"exit\n")
                    time.sleep(0.5)
                    m_ipv6 = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    if m_ipv6 == 0:
                        self.header('IPv6 ESTA DESATIVADO ')
                    else:
                        self.header("IPv6 ESTA ATIVADO")
                    time.sleep(5)
                    return self.ipv6()

                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get ipv6.enable'.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    tn.write(b"exit\n")
                    time.sleep(0.5)
                    m_ipv6 = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    if m_ipv6 == 0:
                        self.header('IPv6 ESTA DESATIVADO ')
                    else:
                        self.header("IPv6 ESTA ATIVADO")
                    time.sleep(5)
                    return self.ipv6()

        elif opcipv6 == 4:
            return self.menu_principal()

        else:
            print('\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m')
            time.sleep(3)
            os.system('cls')
            return self.ipv6()

    def ssid(self):
        self.header('SSID WIFI')
        opcssid = self.menu(['Alterar SSID 2.4Ghz', 'Alterar SSID 5Ghz', 'Status SSID 2.4Ghz', 'Status SSID 5Ghz', 'Voltar'])
        if opcssid == 1:
            self.header('Digite 0 para cancelar')
            ssid_2g = input('Digite o nome do SSID para a rede 2.4Ghz: ')
            if ssid_2g == '0':
                return self.ssid()

            else:
                with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                    # tn.set_debuglevel(1)
                    pwd = tn.read_until(b"login:").decode('utf-8')
                    pwd_str = str(pwd)
                    if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                        tn.write(b'root\r\n')
                        tn.read_until(b"Password:")
                        tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                        # tn.interact()
                        tn.read_until(b"~ # ")
                        tn.write(b'cfm set wl2g.ssid0.ssid ' + f'"{ssid_2g}"'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        # tn.write(b'reboot\n')
                        # tn.read_until(b"~ # ")
                        self.OK()
                        time.sleep(3)
                        os.system('cls')
                        return self.menu_principal()
                    elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                        tn.write(b'root\r\n')
                        tn.read_until(b"Password:")
                        tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                        # tn.interact()
                        tn.read_until(b"~ # ")
                        tn.write(b'cfm set wl2g.ssid0.ssid ' + f'"{ssid_2g}"'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        # tn.write(b'reboot\n')
                        # tn.read_until(b"~ # ")
                        self.OK()
                        time.sleep(3)
                        os.system('cls')
                        return self.menu_principal()
        elif opcssid == 2:
            self.header('Digite 0 para cancelar')
            ssid_5g = input('Digite o nome do SSID para a rede 5Ghz: ')
            self.header('Digite 0 para cancelar')
            if ssid_5g == '0':
                return self.ssid()

            else:
                with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                    # tn.set_debuglevel(1)
                    pwd = tn.read_until(b"login:").decode('utf-8')
                    pwd_str = str(pwd)
                    if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                        tn.write(b'root\r\n')
                        tn.read_until(b"Password:")
                        tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                        # tn.interact()
                        tn.read_until(b"~ # ")
                        tn.write(b'cfm set wl5g.ssid0.ssid ' + f'"{ssid_5g}"'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        # tn.write(b'reboot\n')
                        # tn.read_until(b"~ # ")
                        self.OK()
                        time.sleep(3)
                        os.system('cls')
                        return self.menu_principal()
                    elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                        tn.write(b'root\r\n')
                        tn.read_until(b"Password:")
                        tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                        # tn.interact()
                        tn.read_until(b"~ # ")
                        tn.write(b'cfm set wl5g.ssid0.ssid ' + f'"{ssid_5g}"'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        # tn.write(b'reboot\n')
                        # tn.read_until(b"~ # ")
                        self.OK()
                        time.sleep(3)
                        os.system('cls')
                        return self.menu_principal()
        elif opcssid == 3:
            with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd = tn.read_until(b"login:").decode('utf-8')
                pwd_str = str(pwd)
                if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get wl2g.ssid0.ssid'.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    tn.write(b"exit\n")
                    time.sleep(0.5)
                    m_ssid2 = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    print('SSID atual da rede 2.4Ghz é: '+ m_ssid2.split("\n")[1])
                    time.sleep(5)
                    return self.ssid()

                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get wl2g.ssid0.ssid'.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    tn.write(b"exit\n")
                    time.sleep(0.5)
                    m_ssid2 = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    print('SSID atual da rede 2.4Ghz é: ' + m_ssid2.split("\n")[1])
                    time.sleep(5)
                    return self.ssid()

        elif opcssid == 4:
            with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
                # tn.set_debuglevel(1)
                pwd = tn.read_until(b"login:").decode('utf-8')
                pwd_str = str(pwd)
                if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get wl5g.ssid0.ssid'.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    tn.write(b"exit\n")
                    time.sleep(0.5)
                    m_ssid5 = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    print('SSID atual da rede 5Ghz é: ' + m_ssid5.split("\n")[1])
                    time.sleep(5)
                    return self.ssid()

                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write('cfm get wl5g.ssid0.ssid'.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    tn.write(b"exit\n")
                    time.sleep(0.5)
                    m_ssid5 = str(tn.read_very_eager().decode('ascii'))
                    os.system('cls')
                    print('SSID atual da rede 5Ghz é: ' + m_ssid5.split("\n")[1])
                    time.sleep(5)
                    return self.ssid()
        elif opcssid == 5:
            return self.menu_principal()

        else:
            print('\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m')
            time.sleep(3)
            os.system('cls')
            return self.ssid()

    def apply(self):
        with Telnet(self.default_gateway, 23, timeout=3) as tn:  # LOGIN TELNET
            # tn.set_debuglevel(1)
            pwd = tn.read_until(b"login:").decode('utf-8')
            pwd_str = str(pwd)
            if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                tn.write(b'root\r\n')
                tn.read_until(b"Password:")
                tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                # tn.interact()
                tn.read_until(b"~ # ")
                tn.write(b'reboot\n')
                tn.read_until(b"~ # ")
                os.system('cls')
                self.apply_ok()
                time.sleep(3)
                os.system('cls')
                self.header('INTELBRAS, SEMPRE PRÓXIMA.')
                time.sleep(3)
                exit()

            elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                tn.write(b'root\r\n')
                tn.read_until(b"Password:")
                tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                # tn.interact()
                tn.read_until(b"~ # ")
                tn.write(b'reboot\n')
                tn.read_until(b"~ # ")
                os.system('cls')
                self.apply_ok()
                time.sleep(3)
                os.system('cls')
                self.header('INTELBRAS, SEMPRE PRÓXIMA.')
                time.sleep(3)
                exit()

    def twibi_giga(self, timeout=3, port=9000):
        while True:
            try:
                gateway = netifaces.gateways()
                self.default_gateway = gateway['default'][netifaces.AF_INET][0]
                # print(self.default_gateway)
                if self.default_gateway == '192.168.5.1':
                    self.lembrete()
                    time.sleep(3)
                    os.system('cls')
                    self.menu_principal()

                else:
                    self.default_gateway = input('Digite o endereço IP do seu Twibi: ')
                    try:
                        socket.setdefaulttimeout(timeout)
                        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.default_gateway, port))
                        self.lembrete()
                        time.sleep(3)
                        os.system('cls')
                        self.menu_principal()
                    except socket.error as ex:
                        self.header(
                            '\033[31mERRO: SEM CONEXÃO COM O TWIBI UTILIZANDO O IP DIGITADO ' + f'{self.default_gateway}' + ', CONECTE O TWIBI NO SEU COMPUTADOR E TENTE NOVAMENTE!\033[m')
                        time.sleep(3)
                        self.modelo()
            except Exception:
                logging.debug('Twibi - telnet enabled!')
                time.sleep(1)
                os.system('cls')
                # self.telnet_ok()
                # time.sleep(2)
                # os.system('cls')
                self.menu_principal()

    def modelo(self):
        self.header('MODELO DO PRODUTO')
        print('Qual o modelo do seu Twibi?')
        modelo_id = self.menu(['Twibi Fast / Giga +', 'Twibi Giga'])
        if modelo_id == 1:
            self.enable_telnet()

        elif modelo_id == 2:
            self.twibi_giga()

        else:
            print('\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m')
            time.sleep(3)
            os.system('cls')
            return self.modelo()

t = twibi()
t.modelo()