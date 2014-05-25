ziplesk
=======


Plesk Panel integration with Zimbra

My aim is to make Zimbra's free version an option as an email server to Plesk Panel.

How to use..

Install pycrypt to your Plesk Panel server, run ziplesk.py and copy the .zmp files to zimbra server.

then..

su - zimbra
zmprov -f domains.zmp
zmprov -f accounts.zmp
zmprov -f aliases.zmp

.. and wait for each of these to complete before proceeding to next one. I still have some problems with aliases.

Ideas and contributions are always welcome.

TODO:

from Plesk:

- When an email account gets deleted from plesk, it also disappears from Zimbra.
- Changing email passwords (by customer's admin user)
- mailing lists
- mailbox redirects
- email aliases
- .. and much more


Excellent sources for some more info..

http://wiki.zimbra.com/wiki/Zmprov

http://wiki.zimbra.com/wiki/Bulk_Provisioning

https://www.rackerbox.com/wiki/index.php/Plesk_MySQL_queries

