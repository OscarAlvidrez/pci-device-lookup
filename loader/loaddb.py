import os
import time
import random
import psycopg2
import requests
from datetime import datetime




def load_pci_data(connection):
    cur = connection.cursor()
    response = requests.get("http://pciids.sourceforge.net/v2.2/pci.ids")
    print("Status code {}".format(response.status_code))
    response.raise_for_status()
    content = response.text.split("\n")
    print("\n".join(content[0:5]))
    print("Gor {} more line".format(len(content)))

    cur_vendor = None
    cur_device = None
    last_vendor_id = None

    for i, line in enumerate(content):
        #print("line {} [{}]".format(i, line))
        if not line or line[0] == '#':
            continue
        if line.startswith('\t\t'):
            # process sub device
            clean_line = line.strip()
            sub_vendor, sub_device, device_name = clean_line.split(' ', 2)
            print("v:{} d:{} {} {} {}".format(cur_vendor, cur_device, sub_vendor, sub_device, device_name))

        elif line.startswith('\t'):
            clean_line = line.strip()
            cur_device, device_name = clean_line.split(' ', 1) 
            print("v:{} d:{} {}".format(cur_vendor, cur_device, device_name))
            insert = "INSERT into device (name, code, created_at, vendor_id) VALUES (%s, %s, %s, %s) returning id;"
            cur.execute(insert, (device_name, cur_device, datetime.now(), last_vendor_id))
            connection.commit()

        else:
            # handle vednor
            clean_line = line.strip()
            cur_vendor, vendor_name = clean_line.split(' ', 1)
            print("v:{} {}".format(cur_vendor, vendor_name))
            insert = "INSERT into vendor (name, code, created_at) VALUES (%s, %s, %s) returning id;"
            cur.execute(insert, (vendor_name, cur_vendor, datetime.now()))
            last_vendor_id = cur.fetchone()[0]
            connection.commit()

        if cur_vendor == 'ffff':
            break


if __name__ == "__main__":
    dbname = os.environ.get('USER_DB', None)
    dbuser = os.environ.get('USER_NAME', None)
    dbpass = os.environ.get('USER_PASSWORD', None)
    dbhost = os.environ.get('DB_HOST', None)
    print("Loading database '{}' as user:{}@{}....".format(dbname, dbuser, dbhost))

    for x in range(0, 5):
        try:
            connection = psycopg2.connect(dbname=dbname, user=dbuser, password=dbpass, host=dbhost)
        except Exception:
            print("Connection failed, retry in a second")
            time.sleep(1)

    load_pci_data(connection)
    connection.close()
