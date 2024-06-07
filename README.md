# raspberry-gpio-python
### A Python module to control the GPIO on a Raspberry Pi


### Документация по API:

[http://rpi0.kknd.gm.corp:8000/docs](http://rpi0.kknd.gm.corp:8000/docs)

[http://rpi0.kknd.gm.corp:8000/redoc/](http://rpi0.kknd.gm.corp:8000/redoc/) 

## Подключение к устройству:
```
1. ssh-keygen -t ed25519 (если нет ssh ключа на вашей машине) 
2. ssh-copy-id pi@rpi0.kknd.gm.corp 
3. Ведите стандартный пароль. В дальнейшем "стандартный пароль" не понадобится.
4. ssh pi@rpi0.kknd.gm.corp
```
## Папка проекта с кодом на устройстве:

```bash
pi@raspberrypi:/home/pi/tolik/
```

### Запуск сервера на устройстве:
```bash
pi@raspberrypi:/tmp/tolik $ tolik-bot --help
usage: tolik-bot [-h] [--host HOST] [-l LOGLEVEL] [-p PORT] [-r]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           Bind host
  -l LOGLEVEL, --loglevel LOGLEVEL
                        Logging level
  -p PORT, --port PORT  Bind port
  -r, --reload          Reload when files change
```

#### Для установки и запуска стабильной версии X.Y.Z

Один раз (если устанавливается первый раз):
```bash
# Взять pip.conf: https://confluence.getmobit.ru/pages/viewpage.action?pageId=468848665
# Скопировать на raspberry pi в /tmp/pip.conf, затем:
sudo cp /tmp/pip.conf /usr/pip.conf
sudo cp ~/tolik/configs/tolik-bot.service /lib/systemd/system/
sudo systemctl enable --now tolik-bot.service
```

Каждый раз для обновления до версии X.Y.Z
```bash
sudo pip3 install tolik-bot==X.Y.Z
sudo systemctl restart tolik-bot
```

#### Для запуска в режиме разработки:
```bash
python3 -u -m uvicorn tolik_bot.main:app --host 0.0.0.0 --port 5000 --reload
```

### Команды USB портов GPIO на Raspberry Pi:
```python
import RPi.GPIO as GPIO

# Config
USB1_PIN = 23
USB2_PIN = 17
# Init
GPIO.setmode(GPIO.BCM)
GPIO.setup(USB1_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(USB2_PIN, GPIO.OUT, initial=GPIO.LOW)
# Control
GPIO.output(USB1_PIN, GPIO.HIGH)  # USB1 connect
GPIO.output(USB2_PIN, GPIO.HIGH)  # USB2 connect
time.sleep(2) # Provide time to move servo to the right position
# Deinit
GPIO.output(USB1_PIN, GPIO.LOW)  # USB1 disconnect
GPIO.output(USB2_PIN, GPIO.LOW)  # USB2 disconnect
GPIO.cleanup()  # Deinit GPIO
```