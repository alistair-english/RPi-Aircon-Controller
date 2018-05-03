# How To Install / Setup
1. Copy main.py into the RPi
2. Plug in servo to pin 18 (using the GPIO naming) and connect a pi camera

### Setup environment variable for telepot api token and run on startup
open /etc/rc.local - ```sudo nano  /etc/rc.local``` and add  

```export TELEPOT_TOKEN="insert_token_here"```  
```python3 /full/path/to/main.py &```  

at the bottom above ```exit 0```

> **Note:** to generate a new telepot token use the ```/token``` command with the botfather
