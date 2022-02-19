import requests
import getpass
import hashlib
import os
import time
import logging

while True:
    try:
        # gateway = netifaces.gateways()
        # default_gateway = gateway['default'][netifaces.AF_INET][0]
        senha_admin = getpass.getpass("Digite sua senha de administrador do Twibi: ").encode()
        os.system('cls')
        hash = hashlib.md5(senha_admin)
        encrypt = hash.hexdigest()
        # print(encrypt)
        r = requests.post('http://192.168.5.1/goform/set', json={"login": {"pwd": f'{encrypt}'}}, timeout=5)
        cookies1 = dict(r.cookies)
        print(cookies1)

        if f'{r.json()}' == "{'errcode': '1'}":
            time.sleep(2)
            os.system('cls')
            print('\033[31mERRO: Senha incorreta, tente novamente! \033[m')
            time.sleep(3)
            os.system('cls')
            continue
        else:
            r = requests.get('http://192.168.5.1/goform/telnet', cookies=cookies1, timeout=10)
            print(r.text)

    except Exception:
        logging.debug('Twibi - telnet enabled!')
        time.sleep(1)