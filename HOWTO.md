# How To Install / Setup
1. Copy main.py into the RPi
2. Plug in servo to pin 18 and connect a pi camera

### Setup environment variable for telepot api token
open .bashrc - ```nano ~/.bashrc```  
and add ```export TELEPOT_TOKEN="insert_token_here"``` at the bottom of the file

> **Note:** to generate a new telepot token use the ```/token``` command with the botfather

### To activate run on start up:
```sudo nano  /etc/rc.local```
and then put in a line that runs the  main.py with ```python3```
