from telnetlib import Telnet
import time
import requests
import os
import sys
import logging

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

def OK():
    header('CONFIGURACAO APLICADA COM SUCESSO')

def canais_5():
    header('Canais suportados: 36, 40, 44, 46, 48, 149, 153, 157 e 161')

def canais_2():
    header('Canais suportados: 1 até 13')

def largura_5():
    header('Larguras de banda suportadas para 5Ghz: 20, 40 e 80')

def largura_2():
    header('Larguras de banda suportadas para 2.4Ghz: 20 e 40')

def telnet_habil():
    header('Habilitando telnet, aguarde...')

#lembrete()
#time.sleep(3)
#os.system('cls')
#header('Projeto Dexter - V1.0')

try:
    telnet_habil()
    r = requests.post('http://192.168.5.1/goform/set', json={"login":{"pwd":"25d55ad283aa400af464c76d713c07ad"}})
    # print(f"Status Code: {r.status_code}, Response: {r.json()}")
    r = requests.get('http://192.168.5.1/goform/telnet', timeout=10)
    # print(r.text)
except Exception:
    logging.debug('Twibi - telnet enabled!')
    time.sleep(1)

while True:
    answer = menu(['Alterar canal do Wi-Fi 5Ghz', 'Alterar canal do Wi-Fi 2.4Ghz', 'Alterar largura de banda 5Ghz', 'Alterar largura de banda 2.4Ghz', 'Desabilitar SIP ALG', 'Sair'])
    if answer == 1:
        canais_5()
        canal_5 = leiaInt('Digite o canal desejado: ')
        if (canal_5 == 36) or (canal_5 == 40) or (canal_5 == 44) or (canal_5 == 46) or (canal_5 == 48) or (canal_5 == 149) or (canal_5 == 153) or (canal_5 == 157) or (canal_5 == 161):
            with Telnet('192.168.5.1', 23, timeout=3) as tn: #LOGIN TELNET
                #tn.set_debuglevel(1)
                pwd = tn.read_until(b"login:").decode('utf-8')
                pwd_str = str(pwd)
                if pwd_str[3:6] == 'Int': #TWIBI FAST / GIGA
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[19:25]}' .encode('ascii') + b'\r\n')
                    #tn.interact()
                    tn.read_until(b"~ # ")
                    if (canal_5 == 149) or (canal_5 == 153) or (canal_5 == 157) or (canal_5 == 161):
                        tn.write(b'cfm set wl5g.lock.channel ' + f'{canal_5:"^5}'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        tn.write(b'reboot\n')
                        tn.read_until(b"~ # ")
                        OK()
                        time.sleep(3)
                        os.system('cls')
                    else:
                        tn.write(b'cfm set wl5g.lock.channel ' + f'{canal_5:"^4}' .encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        tn.write(b'reboot\n')
                        tn.read_until(b"~ # ")
                        OK()
                        time.sleep(3)
                        os.system('cls')
                elif pwd_str[3:6] == 'Twi': #TWIBI GIGA Plus
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
                    else:
                        tn.write(b'cfm set wl5g.lock.channel ' + f'{canal_5:"^4}' .encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        tn.write(b'reboot\n')
                        tn.read_until(b"~ # ")
                        OK()
                        time.sleep(3)
                        os.system('cls')
        else:
            print('Você digitou um canal inválido, tente novamente.')
            time.sleep(3)
            os.system('cls')

    elif answer == 2:
        canais_2()
        canal_2 = leiaInt('Digite o canal desejado: ')
        if (canal_2 == 1) or (canal_2 == 2) or (canal_2 == 3) or (canal_2 == 4) or (canal_2 == 5) or (canal_2 == 6) or (canal_2 == 7) or(canal_2 == 8) or (canal_2 == 9) or (canal_2 == 10) or (canal_2 == 11) or (canal_2 == 12) or (canal_2 == 13):
            with Telnet('192.168.5.1', 23, timeout=3) as tn:  # LOGIN TELNET
                #tn.set_debuglevel(1)
                pwd = tn.read_until(b"login:").decode('utf-8')
                pwd_str = str(pwd)
                if pwd_str[3:6] == 'Int':  # TWIBI FAST / GIGA
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[19:25]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    if (canal_2 == 10) or (canal_2 == 11) or (canal_2 == 12) or (canal_2 == 13):
                        tn.write(b'cfm set wl2g.lock.channel ' + f'{canal_2:"^4}'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        time.sleep(2)
                        tn.write(b'reboot\n')
                        tn.read_until(b"~ # ")
                        OK()
                        time.sleep(3)
                        os.system('cls')
                        break
                    else:
                        tn.write(b'cfm set wl2g.lock.channel ' + f'{canal_2:"^3}'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        time.sleep(2)
                        tn.write(b'reboot\n')
                        tn.read_until(b"~ # ")
                        OK()
                        time.sleep(3)
                        os.system('cls')
                        break
                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    if (canal_2 == 10) or (canal_2 == 11) or (canal_2 == 12) or (canal_2 == 13):
                        tn.write(b'cfm set wl2g.lock.channel ' + f'{canal_2:"^4}'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        time.sleep(2)
                        tn.write(b'reboot\n')
                        tn.read_until(b"~ # ")
                        OK()
                        time.sleep(3)
                        os.system('cls')
                        break
                    else:
                        tn.write(b'cfm set wl2g.lock.channel ' + f'{canal_2:"^3}'.encode('ascii') + b'\n')
                        tn.read_until(b"~ # ")
                        time.sleep(2)
                        tn.write(b'reboot\n')
                        tn.read_until(b"~ # ")
                        OK()
                        time.sleep(3)
                        os.system('cls')
                        break
        else:
            print('Você digitou um canal inválido, tente novamente.')
            time.sleep(3)
            os.system('cls')
    elif answer == 3:
        largura_5()
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
                    time.sleep(2)
                    tn.write(b'reboot\n')
                    tn.read_until(b"~ # ")
                    OK()
                    time.sleep(3)
                    os.system('cls')
                    break
                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write(b'cfm set wl5g.lock.bandwidth ' + f'{largura_5:"^4}'.encode('ascii') + b'\n')
                    tn.read_until(b"~ # ")
                    time.sleep(2)
                    tn.write(b'reboot\n')
                    tn.read_until(b"~ # ")
                    OK()
                    time.sleep(1)
                    os.system('cls')
                    break
        else:
            print('Você digitou um canal inválido, tente novamente.')
            time.sleep(3)
            os.system('cls')
    elif answer == 4:
        largura_2()
        largura_2 = leiaInt('Qual a largura de banda 2.4Ghz você deseja: ')
        if (largura_2 == 20) or (largura_2 == 40):
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
                    tn.write(b'cfm set wl2g.lock.bandwidth ' + f'{largura_2:"^4}'.encode('ascii') + b'\n')
                    tn.read_until(b"~ # ")
                    time.sleep(2)
                    tn.write(b'reboot\n')
                    tn.read_until(b"~ # ")
                    OK()
                    time.sleep(3)
                    os.system('cls')
                    break
                elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                    tn.write(b'root\r\n')
                    tn.read_until(b"Password:")
                    tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                    # tn.interact()
                    tn.read_until(b"~ # ")
                    tn.write(b'cfm set wl2g.lock.bandwidth ' + f'{largura_2:"^4}'.encode('ascii') + b'\n')
                    tn.read_until(b"~ # ")
                    time.sleep(2)
                    tn.write(b'reboot\n')
                    tn.read_until(b"~ # ")
                    OK()
                    time.sleep(1)
                    os.system('cls')
                    break
        else:
            print('Você digitou um canal inválido, tente novamente.')
            time.sleep(3)
            os.system('cls')
    elif answer == 5:
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
                tn.write(b'echo sip 0 > proc/alg;\n')
                tn.read_until(b"~ # ")
                OK()
                time.sleep(3)
                os.system('cls')
            elif pwd_str[3:6] == 'Twi':  # TWIBI GIGA Plus
                tn.write(b'root\r\n')
                tn.read_until(b"Password:")
                tn.write(f'{pwd[15:21]}'.encode('ascii') + b'\r\n')
                # tn.interact()
                tn.read_until(b"~ # ")
                tn.write(b'echo sip 0 > proc/alg;\n')
                tn.read_until(b"~ # ")
                OK()
                time.sleep(3)
                os.system('cls')
    elif answer == 6:
        header('INTELBRAS, SEMPRE PRÓXIMA.')
        time.sleep(3)
        break
    else:
        print('\033[31mERRO: Digite uma opoção válida!\033[m')
        time.sleep(3)

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

