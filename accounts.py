#!/usr/bin/python

import MySQLdb
import sys
import base64
from Crypto.Cipher import AES

key = open('/etc/psa/private/secret_key', 'rb').read()
outfile = open('./accounts.zmp', 'w')
query = "SELECT mail.mail_name,domains.name,accounts.password FROM mail,domains,accounts WHERE mail.dom_id=domains.id AND mail.account_id=accounts.id and (mail.postbox='true' or mail.redirect='true') ORDER BY domains.name,mail.mail_name;"
queryAliases="select mail.mail_name, domains.name, mail_aliases.alias from mail, domains, mail_aliases where mail.dom_id=domains.id and mail.id=mail_aliases.mn_id;"
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
cursor.execute (query)
data = cursor.fetchall ()
for row in data :
  cpass = deplesk("'"+row[2]+"'")
  outfile.write("createDomain "+row[1]+"\n"
  outfile.write("createAccount "+ row[0]+'@'+row[1]+" "+cpass+"\n")
cursor.close ()
connection.close ()

# aliases

connection = MySQLdb.connect (host = "localhost", user = "admin", passwd = 'password', db = "psa")
cursor = connection.cursor ()
cursor.execute (queryAliases)
data = cursor.fetchall ()
for row in data :
  outfile.write("aaa" +  row[0] + '@' + row[1] + " " + row[2] + '@' + row[1]
outfile.write("exit\n")
outfile.close
cursor.close ()
connection.close ()

sys.exit()
