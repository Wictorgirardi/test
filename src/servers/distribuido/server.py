import json
import threading
import control
import RPi.GPIO as GPIO
import socket
import json

def readConfig():
    configfile = open('../../configs/configuracao_sala_02.json')
    obj = json.load(configfile)
    config = {}

    config['ip_servidor_central'] = obj['ip_servidor_central']
    config['porta_servidor_central'] = obj['porta_servidor_central']
    config['ip_servidor_distribuido'] = obj['ip_servidor_distribuido']
    config['porta_servidor_distribuido'] = obj['porta_servidor_distribuido']
    config['nome'] = obj['nome']

    config['L_01'] = obj['outputs'][0]['gpio']
    config['L_02'] = obj['outputs'][1]['gpio']
    config['PR'] = obj['outputs'][2]['gpio']
    config['AC'] = obj['outputs'][3]['gpio']
    config['AL_BZ'] = obj['outputs'][4]['gpio']

    config['SPres'] = obj['inputs'][0]['gpio']
    config['SFum'] = obj['inputs'][1]['gpio']
    config['SJan'] = obj['inputs'][2]['gpio']
    config['SPor'] = obj['inputs'][3]['gpio']
    config['SC_IN'] = obj['inputs'][4]['gpio']
    config['SC_OUT'] = obj['inputs'][5]['gpio']
    config['DHT22'] = obj['sensor_temperatura'][0]['gpio']

    return config

def openSocket():
  configfile = open('../../configs/configuracao_sala_02.json')
  file = json.load(configfile)
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
       server.connect((file['ip_servidor_central'], file['porta_servidor_central']))
  return server
  

def receive(server, config):
    while True:
      message = server.recv(2048).decode('ascii')
      print (message)
      if message.startswith('GET_STATUS'):
        with open('../../configs/responses.json', 'r') as openfile:
          json_object = json.load(openfile)
          msg_to_send = json.dumps(json_object).encode('ascii')
          server.send(msg_to_send)

      if message.startswith('ON_OFF_'):
        device = message[7:]
        if GPIO.input(config[device]):
          GPIO.output(config[device], GPIO.LOW)
          server.send('OK'.encode('ascii'))
          continue
        else: 
          GPIO.output(config[device], GPIO.HIGH)
          server.send('OK'.encode('ascii'))
          continue

      if message.startswith('ON_ALL'):
        try:
          keys = [*config]
          for device in keys[5:10]:
            print(config[device])
            GPIO.output(config[device], GPIO.HIGH)
          server.send('OK'.encode('ascii'))
          continue
        except: 
          server.send('NOT_OK'.encode('ascii'))

      if message.startswith('OFF_ALL'):
        try:
          keys = [*config]
          for device in keys[5:10]:
            GPIO.output(config[device], GPIO.LOW)
          server.send('OK'.encode('ascii'))
          continue
        except:
          server.send('NOT_OK'.encode('ascii'))

if __name__ == '__main__':
  try:
    server = openSocket()
    config = readConfig()
    controlThread = threading.Thread(target=control.states, args=(config,))
    controlThread.start()
    print('Servidor inicializado, recebendo....')
    receive(server, config) 

  except KeyboardInterrupt: 
    exit()
