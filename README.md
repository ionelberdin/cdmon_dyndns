# CDmon Dynamic DNS update
If you have domains in CDmon and want to map them to a dynamic IP, then you have to:
- Configure a DynDNS user:
  - user
  - password

Please note that those login details are not the ones to access the customer area.

Then point the domain DNS to the dynamic addresses from CDmon  (more details in the links below).

And then associate the domain with the Dynamic DNS user.

From that point onwards, you can use this script to update the Dynamic DNS service provided by CDmon ([https//cdmon.com](https//cdmon.com)).

Instructions from CDmon about how to trigger Dynamic DNS updates:
- [API de actualización de IP del DNS gratis dinámico](https://ticket.cdmon.com/es/support/solutions/articles/7000005922-api-de-actualizaci%c3%b3n-de-ip-del-dns-gratis-din%c3%a1mico?set_locale=2&_ga=2.261179533.1883837017.1609418615-1272155764.1496775312).
- [FAQs: Gestor DNS gratis dinámico](https://ticket.cdmon.com/es/support/solutions/articles/7000005916-faqs-gestor-dns-gratis-din%C3%A1mico)

## Dependencies:
* ```Python 3.x```
* ```ipgetter2 library```

## Use cases:
### 1. Check if your login details work:
```bash
$ python3 cdmon_dyndns.py -c
``` 
You'll be prompted to enter user name and password.

If you'd rather enter those details directly:
```bash
$ python3 cdmon_dyndns.py -c -u {username} -p {password}
```
Where ```{username}``` and ```{password}``` are placeholders for your actual login details.

### 2. Store your login details in a local file.

Note: password will be only stored in MD5 encrypted manner.
```bash
$ python3 cdmon_dyndns.py -cs [-u {username} -p {password}]
```
```-c``` will prevent the script from requesting an IP address.

The block between backets is optional.

### 3. Update the IP address using your previously stored login details:
```bash
$ python3 cdmon_dyndns.py -lg
```
The IP address will be automatically retrieved.

### 4. Update to an IP address of your choice:
```bash
$ python3 cdmon_dyndns.py -i {IP_address}
```
Where ```{IP_address}``` is a placeholder for the actual IP address to use for the update request.

### 5. Print request URL using verbose mode:
```bash
$ python3 cdmon_dyndns.py -v
```

### 6. Send the request from a different script:
```python
from cdmon_dyndns import send_request
send_request(user, md5pass)  # this will only check if the login succeeds
send_request(user, md5pass, ip)  # this will also try to update the IP
```

Please note that several other option combinations may also be possible.

You may get more information about the available options by either reading
the ```cdmon_dyndns.py``` script, or by invoking its argparse help:
```bash
$ python3 cdmon_dyndns.py -h
```
or:

```bash
$ python3 cdmon_dyndns.py --help
```
