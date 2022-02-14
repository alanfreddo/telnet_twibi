from telnetlib import Telnet
import time
import requests
import os
import logging
import hashlib
import getpass
import netifaces

def leiaInt(msg):
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

def linha(size=50):
    return '-' * size

def header(text):
    print(linha())
    print(text.center(50))
    print(linha())

def lembrete():
    print(linha())
    print('ANTES DE CONTINUAR HABILITE O TELNET DO SEU PRODUTO')
    print(linha())

def menu(lista):
    header('MENU PRINCIPAL')
    c = 1
    for item in lista:
        print(f'[{c}] - {item}')
        c += 1
    print(linha())
    opc = leiaInt('Digite sua opção: ')
    return opc

def telnet_habil():
    header('Habilitando telnet, aguarde...')

def telnet_ok():
    header('Telnet habilitado com sucesso!!!')

def menu_principal():
    answer = menu(['Canal Wi-Fi 5Ghz', 'Canal Wi-Fi 2.4Ghz', 'Largura de banda 5Ghz', 'Largura de banda 2.4Ghz', 'SIP ALG', 'IPv6', 'SSID', 'Sair'])
    if answer == 1:
        os.system('cls')
        canais_5()

    elif answer == 2:
        os.system('cls')
        canais_2()

    elif answer == 3:
        os.system('cls')
        largura_5G()

    elif answer == 4:
        os.system('cls')
        largura_2G()

    elif answer == 5:
        os.system('cls')
        sip_alg()

    elif answer == 6:
        os.system('cls')
        ipv6()

    elif answer == 7:
        os.system('cls')
        ssid()

    elif answer == 8:
        os.system('cls')
        header('INTELBRAS, SEMPRE PRÓXIMA.')
        time.sleep(3)
        exit()

    else:
        print('\033[31mERRO: Digite uma opoção válida!\033[m')
        time.sleep(3)
        return menu_principal()

def OK():
    header('CONFIGURACAO APLICADA COM SUCESSO')

def canais_5():
    copc5 = menu(['Alterar Canal', 'Visualizar Canal', 'Voltar'])
    if copc5 == 1:
        header('Canais suportados: 36, 40, 44, 46, 48, 149, 153, 157 e 161')
        canal_5 = leiaInt('Digite o canal desejado: ')
        if (canal_5 == 36) or (canal_5 == 40) or (canal_5 == 44) or (canal_5 == 46) or (canal_5 == 48) or (
                canal_5 == 149) or (canal_5 == 153) or (canal_5 == 157) or (canal_5 == 161):
            with Telnet('192.168.5.1', 23, timeout=3) as tn:  #LOGIN TELNET
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
                        tn.write(b'reboot\n')
                        tn.read_until(b"~ # ")
                        OK()
                        time.sleep(3)
                        os.system('cls')
                        exit()
                    else:
                        tn.write(b'cfm set wl5g.lock.channel ' + f'{canal_5:"^4}'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        tn.write(b'cfm set wl5g.public.channel ' + f'{canal_5:"^5}'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        tn.write(b'reboot\n')
                        tn.read_until(b"~ # ")
                        OK()
                        time.sleep(3)
                        os.system('cls')
                        exit()
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
                        tn.write(b'reboot\n')
                        tn.read_until(b"~ # ")
                        OK()
                        time.sleep(3)
                        os.system('cls')
                        exit()
                    else:
                        tn.write(b'cfm set wl5g.lock.channel ' + f'{canal_5:"^4}'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        tn.write(b'cfm set wl5g.public.channel ' + f'{canal_5:"^5}'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        tn.write(b'reboot\n')
                        tn.read_until(b"~ # ")
                        OK()
                        time.sleep(3)
                        os.system('cls')
                        exit()
        else:
            print('\033[31mERRO: Você digitou um canal inválido, tente novamente! \033[m')
            time.sleep(3)
            os.system('cls')
            return canais_5()
    elif copc5 == 2:
        with Telnet('192.168.5.1', 23, timeout=3) as tn:  # LOGIN TELNET
            # tn.set_debuglevel(1)
            pwd = tn.read_until(b"login:").decode('utf-8')
            pwd_str = str(pwd)
            if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                tn.write(b'root\r\n')
                tn.read_until(b"Password:")
                tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                # tn.interact()
                tn.read_until(b"~ # ")
                mostra_canal = tn.write(b'cat proc/wlan0/mib_rf\n')
                tn.read_until(b"~ # ")
                mostra_canal_str = str(mostra_canal)
                print(type(mostra_canal_str))
                time.sleep(5)
                return menu_principal()

            elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                tn.write(b'root\r\n')
                tn.read_until(b"Password:")
                tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                # tn.interact()
                tn.read_until(b"~ # ")
                tn.write(b'cat proc/wlan0/mib_rf\n')
                msg = tn.read_until(b"dot11channel: ")
                msg_str = str(msg)
                print(msg_str)
                tn.read_until(b"~ # ")
                time.sleep(5)
                return menu_principal()
    elif copc5 == 3:
        return menu_principal()

    else:
        print('\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m')
        time.sleep(3)
        os.system('cls')
        return canais_2()

def canais_2():
    copc2 = menu(['Alterar Canal', 'Visualizar canal', 'Voltar'])
    if copc2 == 1:
        header('Canais suportados: 1 até 13')
        canal_2 = leiaInt('Digite o canal desejado: ')
        if (canal_2 == 1) or (canal_2 == 2) or (canal_2 == 3) or (canal_2 == 4) or (canal_2 == 5) or (canal_2 == 6) or (
                canal_2 == 7) or (canal_2 == 8) or (canal_2 == 9) or (canal_2 == 10) or (canal_2 == 11) or (
                canal_2 == 12) or (canal_2 == 13):
            with Telnet('192.168.5.1', 23, timeout=3) as tn:  # LOGIN TELNET
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
                        tn.write(b'reboot\n')
                        tn.read_until(b"~ # ")
                        os.system('cls')
                        OK()
                        time.sleep(3)
                        exit()
                    else:
                        tn.write(b'cfm set auto_channel "0"\n')
                        tn.read_until(b"~ # ")
                        tn.write(b'cfm set wl2g.lock.channel ' + f'{canal_2:"^3}'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        tn.write(b'reboot\n')
                        tn.read_until(b"~ # ")
                        os.system('cls')
                        OK()
                        time.sleep(3)
                        exit()
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
                        tn.write(b'reboot\n')
                        tn.read_until(b"~ # ")
                        os.system('cls')
                        OK()
                        time.sleep(3)
                        exit()
                    else:
                        tn.write(b'cfm set auto_channel "0"\n')
                        tn.read_until(b"~ # ")
                        tn.write(b'cfm set wl2g.lock.channel ' + f'{canal_2:"^3}'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        tn.write(b'reboot\n')
                        tn.read_until(b"~ # ")
                        os.system('cls')
                        OK()
                        time.sleep(3)
                        exit()
        else:
            print('\033[31mERRO: Você digitou um canal inválido, tente novamente! \033[m')
            time.sleep(3)
            os.system('cls')
            return canais_2()
    elif copc2 == 2:
        with Telnet('192.168.5.1', 23, timeout=3) as tn:  # LOGIN TELNET
            # tn.set_debuglevel(1)
            pwd = tn.read_until(b"login:").decode('utf-8')
            pwd_str = str(pwd)
            if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                tn.write(b'root\r\n')
                tn.read_until(b"Password:")
                tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                # tn.interact()
                tn.read_until(b"~ # ")
                mostra_canal = tn.write(b'cat proc/wlan1/mib_rf\n')
                tn.read_until(b"~ # ")
                print(mostra_canal)
                time.sleep(5)
                return menu_principal()

            elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                tn.write(b'root\r\n')
                tn.read_until(b"Password:")
                tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                # tn.interact()
                tn.read_until(b"~ # ")
                mostra_canal = tn.write(b'cat proc/wlan1/mib_rf\n')
                tn.read_until(b"~ # ")
                print(mostra_canal)
                time.sleep(5)
                return menu_principal()
    elif copc2 == 3:
        return menu_principal()

    else:
        print('\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m')
        time.sleep(3)
        os.system('cls')
        return canais_2()

def largura_5G():
    lopc5 = menu(['Alterar Largura de Banda', 'Visualizar Largura de Banda', 'Voltar'])
    if lopc5 == 1:
        header('Larguras de banda suportadas para 5Ghz: 20, 40 e 80')
        largura_5 = leiaInt('Qual a largura de banda 5Ghz você deseja: ')
        if (largura_5 == 20) or (largura_5 == 40) or (largura_5 == 80):
            with Telnet('192.168.5.1', 23, timeout=3) as tn:  # LOGIN TELNET
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
                    tn.write(b'reboot\n')
                    tn.read_until(b"~ # ")
                    os.system('cls')
                    OK()
                    time.sleep(3)
                    exit()
                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write(b'cfm set wl5g.lock.bandwidth ' + f'{largura_5:"^4}'.encode('ascii') + b'\n')
                    tn.read_until(b"~ # ")
                    tn.write(b'reboot\n')
                    tn.read_until(b"~ # ")
                    os.system('cls')
                    OK()
                    time.sleep(1)
                    exit()
        else:
            print('\033[31mERRO: Você digitou largura de banda inválida, tente novamente! \033[m')
            time.sleep(3)
            os.system('cls')
            return largura_5G()
    elif lopc5 == 2:
        pass

    elif lopc5 == 3:
        return menu_principal()

    else:
        print('\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m')
        time.sleep(3)
        os.system('cls')
        return largura_5G()

def largura_2G():
    lopc2 = menu(['Alterar Largura de Banda', 'Visualizar Largura de Banda', 'Voltar'])
    if lopc2 == 1:
        header('Larguras de banda suportadas para 2.4Ghz: 20 e 40')
        largura_2 = leiaInt('Qual a largura de banda 2.4Ghz você deseja: ')
        if (largura_2 == 20) or (largura_2 == 40):
            with Telnet('192.168.5.1', 23, timeout=3) as tn:  # LOGIN TELNET
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
                    tn.write(b'reboot\n')
                    tn.read_until(b"~ # ")
                    os.system('cls')
                    OK()
                    time.sleep(3)
                    exit()
                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write(b'cfm set wl2g.lock.bandwidth ' + f'{largura_2:"^4}'.encode('ascii') + b'\n')
                    tn.read_until(b"~ # ")
                    tn.write(b'reboot\n')
                    tn.read_until(b"~ # ")
                    os.system('cls')
                    OK()
                    time.sleep(1)
                    exit()
        else:
            print('\033[31mERRO: Você digitou uma largura de banda inválido, tente novamente! \033[m')
            time.sleep(3)
            os.system('cls')
            return largura_2G()

    elif lopc2 == 2:
        pass

    elif lopc2 == 3:
        return menu_principal()

    else:
        print('\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m')
        time.sleep(3)
        os.system('cls')
        return largura_2G()

def sip_alg():
    alg = menu(['Ativar', 'Desativar', 'Voltar'])
    if alg == 1:
        with Telnet('192.168.5.1', 23, timeout=3) as tn:  # LOGIN TELNET
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
                OK()
                time.sleep(2)
                tn.read_until(b"~ # ")
                tn.write(b'reboot\n')
                tn.read_until(b"~ # ")
                os.system('cls')
                OK()
                time.sleep(1)
                exit()
            elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                tn.write(b'root\r\n')
                tn.read_until(b"Password:")
                tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                # tn.interact()
                tn.read_until(b"~ # ")
                tn.write(b'cfm set sip_en 1\n')
                tn.read_until(b"~ # ")
                OK()
                time.sleep(2)
                os.system('cls')
                tn.read_until(b"~ # ")
                tn.write(b'reboot\n')
                tn.read_until(b"~ # ")
                os.system('cls')
                OK()
                time.sleep(1)
                exit()
    elif alg == 2:
        with Telnet('192.168.5.1', 23, timeout=3) as tn:  # LOGIN TELNET
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
                OK()
                time.sleep(2)
                tn.read_until(b"~ # ")
                tn.write(b'reboot\n')
                tn.read_until(b"~ # ")
                os.system('cls')
                OK()
                time.sleep(1)
                exit()
            elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                tn.write(b'root\r\n')
                tn.read_until(b"Password:")
                tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                # tn.interact()
                tn.read_until(b"~ # ")
                tn.write(b'cfm set sip_en 0\n')
                tn.read_until(b"~ # ")
                OK()
                time.sleep(2)
                os.system('cls')
                tn.read_until(b"~ # ")
                tn.write(b'reboot\n')
                tn.read_until(b"~ # ")
                os.system('cls')
                OK()
                time.sleep(1)
                exit()

    elif alg == 3:
        return menu_principal()

    else:
        print('\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m')
        time.sleep(3)
        os.system('cls')
        return sip_alg()

def ipv6():
    opcipv6 = menu(['Ativar', 'Desativar', 'Voltar'])
    if opcipv6 == 1:
        with Telnet('192.168.5.1', 23, timeout=3) as tn:  # LOGIN TELNET
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
                tn.write(b'reboot\n')
                tn.read_until(b"~ # ")
                OK()
                time.sleep(3)
                os.system('cls')
                exit()

            elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                tn.write(b'root\r\n')
                tn.read_until(b"Password:")
                tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                # tn.interact()
                tn.read_until(b"~ # ")
                tn.write(b'cfm set ipv6.enable 1\n')
                tn.read_until(b"~ # ")
                tn.write(b'reboot\n')
                tn.read_until(b"~ # ")
                OK()
                time.sleep(3)
                os.system('cls')
                exit()
    elif opcipv6 == 2:
        with Telnet('192.168.5.1', 23, timeout=3) as tn:  # LOGIN TELNET
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
                tn.write(b'reboot\n')
                tn.read_until(b"~ # ")
                OK()
                time.sleep(3)
                os.system('cls')
                exit()

            elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                tn.write(b'root\r\n')
                tn.read_until(b"Password:")
                tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                # tn.interact()
                tn.read_until(b"~ # ")
                tn.write(b'cfm set ipv6.enable 0\n')
                tn.read_until(b"~ # ")
                tn.write(b'reboot\n')
                tn.read_until(b"~ # ")
                OK()
                time.sleep(3)
                os.system('cls')
                exit()
    elif opcipv6 == 3:
        return menu_principal()

    else:
        print('\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m')
        time.sleep(3)
        os.system('cls')
        return ipv6()

def ssid():
    opcssid = menu(['Alterar SSID 2.4Ghz', 'Alterar SSID 5Ghz', 'Voltar'])
    if opcssid == 1:
        ssid_2g = input('Digite o nome do SSID para a rede 2.4Ghz: ')
        with Telnet('192.168.5.1', 23, timeout=3) as tn:  # LOGIN TELNET
            # tn.set_debuglevel(1)
            pwd = tn.read_until(b"login:").decode('utf-8')
            pwd_str = str(pwd)
            if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                tn.write(b'root\r\n')
                tn.read_until(b"Password:")
                tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                # tn.interact()
                tn.read_until(b"~ # ")
                tn.write(b'cfm set wl2g.ssid0.ssid ' + f'{ssid_2g:"^}'.encode('ascii') + b'\n')
                tn.read_until(b"~ # ")
                tn.write(b'reboot\n')
                tn.read_until(b"~ # ")
                OK()
                time.sleep(3)
                os.system('cls')
                exit()

            elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                tn.write(b'root\r\n')
                tn.read_until(b"Password:")
                tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                # tn.interact()
                tn.read_until(b"~ # ")
                tn.write(b'cfm set wl2g.ssid0.ssid ' + f'{ssid_2g:"^}'.encode('ascii') + b'\n')
                tn.read_until(b"~ # ")
                tn.write(b'reboot\n')
                tn.read_until(b"~ # ")
                OK()
                time.sleep(3)
                os.system('cls')
                exit()

    elif opcssid == 2:
        ssid_5g = input('Digite o nome do SSID para a rede 5Ghz: ')
        with Telnet('192.168.5.1', 23, timeout=3) as tn:  # LOGIN TELNET
            # tn.set_debuglevel(1)
            pwd = tn.read_until(b"login:").decode('utf-8')
            pwd_str = str(pwd)
            if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                tn.write(b'root\r\n')
                tn.read_until(b"Password:")
                tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                # tn.interact()
                tn.read_until(b"~ # ")
                tn.write(b'cfm set wl5g.ssid0.ssid ' + f'{ssid_5g:"^}'.encode('ascii') + b'\n')
                tn.read_until(b"~ # ")
                tn.write(b'reboot\n')
                tn.read_until(b"~ # ")
                OK()
                time.sleep(3)
                os.system('cls')
                exit()

            elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                tn.write(b'root\r\n')
                tn.read_until(b"Password:")
                tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                # tn.interact()
                tn.read_until(b"~ # ")
                tn.write(b'cfm set wl5g.ssid0.ssid ' + f'{ssid_5g:"^}'.encode('ascii') + b'\n')
                tn.read_until(b"~ # ")
                tn.write(b'reboot\n')
                tn.read_until(b"~ # ")
                OK()
                time.sleep(3)
                os.system('cls')
                exit()
    elif opcssid == 3:
        return menu_principal()

    else:
        print('\033[31mERRO: Você digitou uma opção inválida, tente novamente! \033[m')
        time.sleep(3)
        os.system('cls')
        return ssid()

while True:

    try:
        # gateway = netifaces.gateways()
        # default_gateway = gateway['default'][netifaces.AF_INET][0]
        senha_admin = getpass.getpass("Digite sua senha de administrador do Twibi: ").encode()
        os.system('cls')
        hash = hashlib.md5(senha_admin)
        encrypt = hash.hexdigest()
        telnet_habil()
        # print(encrypt)
        r = requests.post('http://192.168.5.1/goform/set', json={"login": {"pwd": f'{encrypt}'}}, timeout=5)
        # print(f"Status Code: {r.status_code}, Response: {r.json()}")
        if f'{r.json()}' == "{'errcode': '1'}":
            time.sleep(2)
            os.system('cls')
            print('\033[31mERRO: Senha incorreta, tente novamente! \033[m')
            time.sleep(3)
            os.system('cls')
            continue
        else:
            r = requests.get('http://192.168.5.1/goform/telnet', timeout=10)
            print(r.text)
    except Exception:
        logging.debug('Twibi - telnet enabled!')
        time.sleep(1)
    os.system('cls')
    telnet_ok()
    time.sleep(2)
    os.system('cls')
    menu_principal()
    







#





##
##

###