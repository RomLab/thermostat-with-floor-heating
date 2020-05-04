# Instalace

## Instalace Home Assistant
- Postupovat podle: https://www.home-assistant.io/docs/installation/raspberry-pi/

**Vytvoření služby pro spuštení:**
- Založit službu/soubor: ```sudo nano -w /etc/systemd/system/home-assistant@homeasssistant.service```
- Postupovat podle: https://www.home-assistant.io/docs/autostart/systemd/ (nakopírovat obsah z části **PYTHON VIRTUAL ENVIRONMENT** do služby/souboru viz výše)
- Pokračovat dále v části **NEXT STEPS**

## Instalce Samba
```
sudo apt-get install samba
sudo smbpasswd -a homeassistant
```
- Po výzvě zadat požadované heslo
- Editace konfiguračního souboru:
```
sudo nano /etc/samba/smb.conf
```
- Na konec souboru smb.conf vložit:
```
[homeassistant]
path = /home/homeassistant/.homeassistant/
read only = no
valid users = homeassistant
writable = yes
create mask = 0777
directory mask = 0777
force user = homeassistant
force create mode = 0777
force directory mode = 0777
```
- Restart Samby:
```
sudo service smbd restart
```

## Instalce AppDaemon
- Postupovat podle: https://www.home-assistant.io/docs/installation/raspberry-pi/ (změna homeassistant na appdaemon, **začátek od sudo useradd …**, konec po instalaci Python balíčků)
- Naistalovat místo pip3 install homeassistant => **pip3 install appdaemon**

**Vytvoření služby pro spuštení:**
- Založit službu/soubor: ```sudo nano -w /etc/systemd/system/app-daemon@appdaemon.service```
- Postupovat podle: https://www.home-assistant.io/docs/autostart/systemd/ 
- Nakopírovat obsah níže do služby/souboru viz výše:
```
[Unit]
Description=App Deamon
After=network-online.target

[Service]
Type=simple
User=%i
ExecStart=/srv/appdaemon/bin/appdaemon -c "/home/%i/.appdaemon/conf/"

[Install]
WantedBy=multi-user.target
```
- Pokračovat dále v části **NEXT STEPS** (místo home-assistant => **app-daemon**)

## LCD I2C
- Postupovat podle: https://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/
- Instalovat:  ```sudo apt-get install i2c-tools do systému```
- Přepnutí do virtual environment appdaemon:
```
sudo -u appdaemon -H -s
cd /srv/appdaemon
source bin/activate
```
Instalovat do virtual environment appdaemon: ```pip3 install smbus```


## Instalace PostgreSQL
Instalace: ```sudo apt-get install postgresql```

- Vytvoření databáze:
```
sudo -s -u postgres
createuser homeassistant
createdb -O homeassistant homeassistant
```

- Instalace závislostí do systému (kde X.Y je verze PostgreSQL):
```sudo apt-get install postgresql-server-dev-X.Y```
- Přepnutí do virtual environment homeassistant: 
```
sudo -u homeassistant -H -s
cd /srv/homeassistant
source bin/activate
```

Instalace do virtual environment homeassistant: ```pip3 install psycopg2```


**Definování připojení do databáze (kde X.Y je verze PostgreSQL):**
```
sudo -e /etc/postgresql/X.Y/main/pg_hba.conf
```
- Vložit na nový řádek:
```local homeassistant homeassistant peer```
- Refresh PostgreSQL nastavení:
```sudo -i -u postgres psql -c "SELECT pg_reload_conf();"```

**Přidání služby do Home Assistant služby:**
```sudo nano /etc/systemd/system/home-assistant@homeassistant.service```
- Přidat/upravit na řádku:
```
[Unit]
Description=Home Assistant
After=network-online.target postgresql.service
```
- Refresh:
```sudo systemctl daemon-reload```

## Ostatní instalace
**Práce s GPIO:**
- Doinstalovat do virtual environment appdaemon pro práci s GPIO RPI:
- Přepnutí do virtual environment appdaemon:
```
sudo -u appdaemon -H -s
cd /srv/appdaemon
source bin/activate
```
Instalace do virtual environment appdaemon: ```pip3 install RPi.GPIO```

**Shell command – práva:**
- Upravení práv pro uživatel homeassistant pro spuštení shell_command skrz HA (https://community.home-assistant.io/t/is-adding-the-hass-user-to-sudoers-for-script-a-good-idea/78862)
- Spustit přes: ```sudo visudo```
- Vložit na konec souboru (zjistit, jestli neomezit jen pro jakou složku/soubor): ```homeassistant ALL=NOPASSWD: ALL```
