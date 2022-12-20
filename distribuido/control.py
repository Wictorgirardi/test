import RPi.GPIO as GPIO
import adafruit_dht
import time
import os
import json
import board
import threading

temp = 0
hum = 0

def setupPins(config):
  # rasp pin mode setup
  GPIO.setmode(GPIO.BCM)
  # rasp in setup
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

def countPeople(config,msg):
  try:
    countP = 0
    while True:
      msg['Pessoas'] = str(countP)
      time.sleep(0.0001)
      if GPIO.event_detected(config['SC_IN']):
          countP = countP + 1
      if GPIO.event_detected(config['SC_OUT']):
          countP = countP - 1
          if countP < 0:
            countP = 0
  except:
    print('Error counting people')

def getHumidity(config,msg):
  try:
    while True:
      time.sleep(0.002)
      if config['DHT22'] == 4:
        dht_device = adafruit_dht.DHT22(board.D4, False)
      elif config['DHT22'] == 18:
        dht_device = adafruit_dht.DHT22(board.D18, False)
      
      temperature = dht_device.temperature
      humidity = dht_device.humidity
      if humidity is not None and temperature is not None:
        msg['Temperatura'] = temperature
        msg['Humidade'] = humidity
      else:
        print("Failed to retrieve data from humidity sensor")
  except:
    getHumidity(config,msg)

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
    setupPins(config)

    GPIO.add_event_detect(config['SC_IN'], GPIO.RISING)
    GPIO.add_event_detect(config['SC_OUT'], GPIO.RISING)
    dhtThread = threading.Thread(target=getHumidity, args=(config,msg))
    dhtThread.start()
    countPeopleThread = threading.Thread(target=countPeople, args=(config,msg))
    countPeopleThread.start()


    while(1):
      time.sleep(0.05)
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

      # Armazenando dados em um json de estados
      with open('states/states.json', 'w') as outfile:
        json.dump(msg,outfile)
  except KeyboardInterrupt: # if ctrl + c is pressed, exit cleanly
    pass