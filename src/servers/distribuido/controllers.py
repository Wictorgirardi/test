import RPi.GPIO as GPIO
import adafruit_dht
import json
import board
import threading

def countPeople(config,msg):
  try:
    countP = 0
    while True:
      msg['Pessoas'] = str(countP)
      if GPIO.event_detected(config['SC_IN']):
          countP = countP + 1
      if GPIO.event_detected(config['SC_OUT']):
          countP = countP - 1
          if countP < 0:
            countP = 0
  except:
    print('Error counting people')

def temperatura(config,msg):
  try:
      if config['DHT22'] == 4:
        dht_device = adafruit_dht.DHT22(board.D4, False)
      elif config['DHT22'] == 18:
        dht_device = adafruit_dht.DHT22(board.D18, False)
      
      msg['Temperatura'] = round(dht_device.temperature, 2)
      msg['Humidade'] = round(dht_device.humidity, 2)
  except:
    temperatura(config,msg)

def states(config):
  try:
    msg = {
      'L_01': 'OFF',
      'L_02': 'OFF',
      'AC': 'OFF',
      'PR': 'OFF',
      'AL_BZ': 'OFF',
      'SPres': 'OFF',
      'SFum': 'OFF',
      'SJan': 'OFF',
      'SPor': 'OFF',
      'Temperatura': '0',
      'Humidade': '0',
      'Pessoas': 0
    }
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config['L_01'], GPIO.OUT)
    GPIO.setup(config['L_02'], GPIO.OUT)
    GPIO.setup(config['PR'], GPIO.OUT)
    GPIO.setup(config['AC'], GPIO.OUT)
    GPIO.setup(config['AL_BZ'], GPIO.OUT)
    GPIO.setup(config['SPres'], GPIO.IN)
    GPIO.setup(config['SFum'], GPIO.IN)
    GPIO.setup(config['SJan'], GPIO.IN)
    GPIO.setup(config['SPor'], GPIO.IN)
    GPIO.setup(config['SC_IN'], GPIO.IN)
    GPIO.setup(config['SC_OUT'], GPIO.IN)
    GPIO.add_event_detect(config['SC_IN'], GPIO.RISING)
    GPIO.add_event_detect(config['SC_OUT'], GPIO.RISING)
    dhtThread = threading.Thread(target=temperatura, args=(config,msg))
    dhtThread.start()
    countPeopleThread = threading.Thread(target=countPeople, args=(config,msg))
    countPeopleThread.start()

    while(1):
      if GPIO.input(config['L_01']):
        msg['L_01'] = 'ON'
      else:
        msg['L_01'] = 'OFF'

      if GPIO.input(config['L_02']):
         msg['L_02'] = 'ON'
      else:
        msg['L_02'] = 'OFF'

      if GPIO.input(config['AC']):
        msg['AC'] = 'ON'
      else:
        msg['AC'] = 'OFF'

      if GPIO.input(config['PR']):
        msg['PR'] = 'ON'
      else:
        msg['PR'] = 'OFF'

      if GPIO.input(config['AL_BZ']):
        msg['AL_BZ'] = 'ON'
      else:
        msg['AL_BZ'] = 'OFF'

      if GPIO.input(config['SPres']):
        msg['SPres'] = 'ON'
      else:
        msg['SPres'] = 'OFF'

      if GPIO.input(config['SFum']):
        msg['SFum'] = 'ON'
      else:
        msg['SFum'] = 'OFF'
      
      if GPIO.input(config['SJan']):
        msg['SJan'] = 'ON'
      else:
        msg['SJan'] = 'OFF'
      
      if GPIO.input(config['SPor']):
        msg['SPor'] = 'ON'
      else:
        msg['SPor'] = 'OFF'
    
      with open('../../configs/responses.json', 'w') as outfile:
        json.dump(msg,outfile)
  except KeyboardInterrupt: 
    pass

