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
After=home-assistant@homeasssistant.service
Requires=home-assistant@homeasssistant.service

[Service]
Type=simple
User=%i
ExecStart=/srv/appdaemon/bin/appdaemon -c "/home/%i/.appdaemon/conf/"

[Install]
WantedBy=multi-user.target
```
- Pokračovat dále v části **NEXT STEPS** (místo home-assistant => **app-daemon**)

**Přidání složky do Samby**
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
force user = appdaemon
force create mode = 0777
force directory mode = 0777
```

## LCD I2C
- Postupovat podle: https://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/
- Instalovat do systému:  ```sudo apt-get install i2c-tools ```
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

- Instalace závislostí do systému (kde X.Y je verze PostgreSQL)(možné stéjné jako instalace výše, zjistit rozdíl):
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

## Instalace Mosquitto
- Instalovat do systému: ```sudo apt-get install mosquitto```
- ```cd etc/mosquitto```
- Přidání uživatele:```sudo mosquitto_passwd -c users.passwd <user name-> homeassistant>```
- ```cd etc/mosquitto/conf.d```
- ```sudo nano user.conf```
- - Přidání do souboru:
- - - ```allow_anonymous false```
- - - ```password_file /etc/mosquitto/users.passwd```
- Založit službu/soubor: ```sudo nano -w /etc/systemd/system/mosquitto.service```
- - Vložit:
```
[Unit]
Description=Mosquitto MQTT Broker daemon
ConditionPathExists=/etc/mosquitto/mosquitto.conf
Wants=multi-user.target
After=multi-user.target
Requires=network.target

[Service]
Type=simple
ExecStart=/usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf -d
ExecReload=/bin/kill -HUP $MAINPID
PIDFile=/var/run/mosquitto.pid
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
- - Reload systemd: ```sudo systemctl --system daemon-reload```
- - Povolení služby: ```sudo systemctl enable mosquitto.service```
- Úprava služby Home Assistant (spuštění až za Mosquittem):
```
[Unit]
Description=Home Assistant
After=network-online.target mosquitto.service
Requires=mosquitto.service
[Service]
Type=simple
User=%i
WorkingDirectory=/home/%i/.homeassistant
ExecStart=/srv/homeassistant/bin/hass -c "/home/%i/.homeassistant"

[Install]
WantedBy=multi-user.target
```
- - Reload systemd: ```sudo systemctl --system daemon-reload```
- - Spuštění služby: ```sudo systemctl start mosquitto.service``` 

## Teplotní predikce
- Instalace balíčku **pandas**
- Přepnutí do virtual environment appdaemon:
```
sudo -u appdaemon -H -s
cd /srv/appdaemon
source bin/activate
```
- Instalovat do virtual environment appdaemon: 
  - ```pip3 install pandas```
  - ```pip3.8 install numpy```
  - ```pip3 install psycopg2```
  - ```pip3 install matplotlib```
- sudo apt-get install libatlas-base-dev

- Vytvoření struktury složek:
  - /home/appdaemon/.appdaemon/conf/apps/data/heater/first_floor
  - /home/appdaemon/.appdaemon/conf/apps/data/heater/second_floor
  - /home/appdaemon/.appdaemon/conf/apps/data/temperature_inside/first_floor
  - /home/appdaemon/.appdaemon/conf/apps/data/temperature_inside/second_floor


- Možnost připojení přes uživatel appdaemon do datábaze
- Editovat ```sudo -e /etc/postgresql/X.Y/main/pg_hba.conf``` (X.Y je verze databáze, aktuálně 11)
  - Vložit řádek ``` local    homeassistant   appdaemon   md5``` 
  - Přidání práv pro uživatele do databáze
    - ```sudo -s -u postgres```
    - ```createuser appdaemon``` (vytvoření uživatele)
    - ```psql```
    - ```ALTER USER appdaemon WITH SUPERUSER; ``` (přidání práv pro čtení dat)```
    - ```alter user appdaemon with encrypted password 'VelmiSilneHesloProHomeassistant';```
