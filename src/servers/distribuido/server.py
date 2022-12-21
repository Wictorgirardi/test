import json
import threading
import controller
import RPi.GPIO as GPIO
import socket

server = 0

def readConfig(sala):
    configfile = open('../../configs/configuracao_sala_01.json') if sala == 1 else open('../../configs/configuracao_sala_02.json')
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

def openSocket(config):
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.connect((config['ip_servidor_central'], config['porta_servidor_central']))
  return server
  
def receive(server, config):
    while True:
      message = server.recv(2048).decode('ascii')
      if 'GET_ALL' in message:
        responseFile = open('../../configs/responses.json')
        file = json.load(responseFile)
        msg_to_send = json.dumps(file).encode('ascii')
        server.send(msg_to_send)

      if 'CONTROL_' in message:
        device = message[8:]
        if GPIO.input(config[device]):
          GPIO.output(config[device], GPIO.LOW)
          server.send('OK'.encode('ascii'))
          continue
        else: 
          GPIO.output(config[device], GPIO.HIGH)
          server.send('OK'.encode('ascii'))
          continue

      if 'ON_ALL' in message:
        try:
          keys = [*config]
          for device in keys[5:10]:
            GPIO.output(config[device], GPIO.HIGH)
          server.send('OK'.encode('ascii'))
          continue
        except: 
          server.send('NOT_OK'.encode('ascii'))

      if 'OFF_ALL' in message:
        try:
          keys = [*config]
          for device in keys[5:10]:
            GPIO.output(config[device], GPIO.LOW)
          server.send('OK'.encode('ascii'))
          continue
        except:
          server.send('NOT_OK'.encode('ascii'))

if __name__ == '__main__':
    print('Escolha a configuração de sala desejada: ')
    print('1 - Sala 1')
    print('2 - Sala 2')
    server = int(input())
    config = readConfig(server)
    server = openSocket(config)

    controlThread = threading.Thread(target=controller.states, args=(config,))
    controlThread.start()
    print('Servidor inicializado, recebendo....')
    receive(server, config) 


