from telnetlib import Telnet
import time
import requests
import os
import logging
import hashlib
import getpass
import netifaces

### Menu ####


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
        print(f'{c} - {item}')
        c += 1
    print(linha())
    opc = leiaInt('Digite sua opção: ')
    return opc

def telnet_habil():
    header('Habilitando telnet, aguarde...')

def telnet_ok():
    header('Telnet habilitado com sucesso!!!')

def menu_principal():
    answer = menu(['Canal do Wi-Fi 5Ghz', 'Canal do Wi-Fi 2.4Ghz', 'Largura de banda 5Ghz', 'Largura de banda 2.4Ghz', 'SIP ALG', 'Sair'])
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
    header('Canais suportados: 36, 40, 44, 46, 48, 149, 153, 157 e 161')
    canal_5 = leiaInt('Digite o canal desejado: ')
    if (canal_5 == 36) or (canal_5 == 40) or (canal_5 == 44) or (canal_5 == 46) or (canal_5 == 48) or (
            canal_5 == 149) or (canal_5 == 153) or (canal_5 == 157) or (canal_5 == 161):
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
                    tn.write(b'reboot\n')
                    tn.read_until(b"~ # ")
                    OK()
                    time.sleep(3)
                    os.system('cls')
                    exit()
                else:
                    tn.write(b'cfm set wl5g.lock.channel ' + f'{canal_5:"^4}'.encode('ascii') + b'\n')
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

def canais_2():
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

def largura_5G():
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
        print('\033[31mERRO: Você digitou um canal inválido, tente novamente! \033[m')
        time.sleep(3)
        os.system('cls')
        return largura_5G()

def largura_2G():
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
        print('\033[31mERRO: Você digitou um canal inválido, tente novamente! \033[m')
        time.sleep(3)
        os.system('cls')
        return largura_2G()
def sip_alg():
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

#lembrete()
#time.sleep(3)
#os.system('cls')
#header('Projeto Dexter - V1.0')

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
        print(f"Status Code: {r.status_code}, Response: {r.json()}")
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
    
        

### Login telnet ####

#def login(Telnet):

#    with Telnet('192.168.6.1', 23, timeout=3) as tn:
        #tn.set_debuglevel(1)
#        pwd = tn.read_until(b"login:")
#        tn.write(b'root\r\n')
#        tn.read_until(b"Password:")
#        tn.write(pwd[19:25] + b'\r\n')
#        tn.interact()






#



### Habilitar telnet #####

#r = requests.post('http://192.168.6.1/login.html', auth=('', '12345678'))
#print(r.status_code)
#r = requests.get('http://192.168.6.1/goform/get?module_id=guest_pass')
#print(r.status_code)
#r = requests.get('http://192.168.6.1/goform/telnet')
#print(r.status_code)

##
##

###