#!/usr/bin/python

import MySQLdb
import sys
import base64
from Crypto.Cipher import AES

key = open('/etc/psa/private/secret_key', 'rb').read()
outfile = open('./accounts.zmp', 'w')

# decrypt function
def deplesk( password ):
  "password decryption"
  lead, typ, iv, ct = password.split('$')
  iv = base64.b64decode(iv)
  ct = base64.b64decode(ct)
  assert typ == 'AES-128-CBC'
  plain = AES.new(key, mode=AES.MODE_CBC, IV=iv).decrypt(ct).rstrip(b'\0')
  return(plain.decode('utf8'))

connection = MySQLdb.connect (host = "localhost", user = "admin", passwd = 'password', db = "psa")

cursor = connection.cursor ()
cursor.execute ("SELECT mail.mail_name,domains.name,accounts.password FROM mail,domains,accounts WHERE mail.dom_id=domains.id AND mail.account_id=accounts.id and (mail.postbox='true' or mail.redirect='true') ORDER BY domains.name,mail.mail_name;")
data = cursor.fetchall ()
for row in data :
  cpass = deplesk("'"+row[2]+"'")
  outfile.write("createAccount "+ row[0]+'@'+row[1]+" "+cpass+"\n")
outfile.close
cursor.close ()
connection.close ()
sys.exit()
