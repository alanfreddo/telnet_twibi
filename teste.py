from telnetlib import Telnet
import time
#import requests
import os
import sys

### Menu ####

def leiaInt(msg):
    while True:
        try:
            n = int(input(msg))
        except (ValueError, TypeError):
            print('\033[31mERRO: Digite um número inteiro válido! \033[m')
            continue
        except (KeyboardInterrupt):
            print('\n\033[31mUsuário não digitou. \033[m')
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
    print('ANTES DE CONTINUAR, HABILITE O TELNET DO SEU PRODUTO')
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


#lembrete()
#time.sleep(3)
#os.system('cls')
#header('Projeto Dexter - V1.0')

while True:
    answer = menu(['Alterar canal do Wi-Fi 5Ghz', 'Alterar canal do Wi-Fi 2.4Ghz', 'Alterar largura de banda 5Ghz', 'Alterar largura de banda 2.4Ghz', 'Desabilitar SIP ALG', 'Sair'])
    if answer == 1:
        #canal_5 = leiaInt('Digite o canal desejado: ')
        with Telnet('192.168.5.1', 23, timeout=3) as tn:
            tn.set_debuglevel(1)
            pwd = tn.read_until(b"login:")
            tn.write(b'root\r\n')
            tn.read_until(b"Password:")
            tn.write(pwd[15:21] + b'\r\n')
            tn.read_until(b'~ # ')
            tn.write(b'cfm set wl5g.lock.channel "48"')
            
            #tn.write(b'cfm set wl5g.lock.channel' + f'"{canal_5}"\n')
            #tn.read_until(b'cfm set wl5g.lock.channel' + f'"{canal_5}"\r\n')
            break

    elif answer == 2:
        canal_2 = input('Digite o canal desejado: ')
        with Telnet('192.168.5.1', 23, timeout=3) as tn:
            # tn.set_debuglevel(1)
            pwd = tn.read_until(b"login:")
            tn.write(b'root\r\n')
            tn.read_until(b"Password:")
            tn.write(pwd[19:25] + b'\r\n')
            tn.read_until(b'~ #\n')
            tn.write("reboot\n")
            # tn.write('reboot')
    elif answer == 3:
        largura_5 = input('Qual a largura de banda 5Ghz você deseja: ')
        with Telnet('192.168.5.1', 23, timeout=3) as tn:
            # tn.set_debuglevel(1)
            pwd = tn.read_until(b"login:")
            tn.write(b'root\r\n')
            tn.read_until(b"Password:")
            tn.write(pwd[19:25] + b'\r\n')
            tn.write("ls\n")
            # tn.write('reboot')
            break
    elif answer == 4:
        largura_2 = input('Qual a largura de banda 2.4Ghz você deseja: ')
        with Telnet('192.168.5.1', 23, timeout=3) as tn:
            # tn.set_debuglevel(1)
            pwd = tn.read_until(b"login:")
            tn.write(b'root\r\n')
            tn.read_until(b"Password:")
            tn.write(pwd[19:25] + b'\r\n')
            tn.interact()
            #tn.write("ls\n")
            # tn.write('reboot')
            break
    elif answer == 5:
        #sip_alg = input('Qual a largura de banda 5Ghz você deseja: ')
        with Telnet('192.168.5.1', 23, timeout=3) as tn:
            # tn.set_debuglevel(1)
            pwd = tn.read_until(b"login:")
            tn.write(b'root\r\n')
            tn.read_until(b"Password:")
            tn.write(pwd[19:25] + b'\r\n')
            tn.write("ls\n")
            # tn.write('reboot\n')
            break
    elif answer == 6:
        print('Até logo. Intelbras, sempre próxima')
        break
    else:
        print('\033[31mERRO: Digite uma opoção válida!\033[m')
        time.sleep(3)
### Login telnet ####

#def login(Telnet):

#    with Telnet('192.168.6.1', 23, timeout=3) as tn:
#        tn.set_debuglevel(1)
#        pwd = tn.read_until(b"login:")
#        tn.write(b'root\r\n')
#        tn.read_until(b"Password:")
#        tn.write(pwd[19:25] + b'\r\n')
#        tn.interact()









### Habilitar telnet #####

#r = requests.post('http://192.168.6.1/login.html', auth=('', '12345678'))
#print(r.status_code)
#r = requests.get('http://192.168.6.1/goform/get?module_id=guest_pass')
#print(r.status_code)
#r = requests.get('http://192.168.6.1/goform/telnet')
#print(r.status_code)


