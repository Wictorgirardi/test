import time
import os
import json
import threading
import tcpDistr
import control
import RPi.GPIO as GPIO
import socket

def receive(server, config):
  try:
    while True:
      message = server.recv(2048).decode('ascii')
      print (message)
      if message.startswith('GET_STATUS'):
        with open('states/states.json', 'r') as openfile:
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

  except RuntimeError as error:
        return error.args[0]

if __name__ == '__main__':
  try:
    print('Conectando com o servidor central. Aguarde...')
    server, config = tcpDistr.init()
    controlThread = threading.Thread(target=control.states, args=(config,)) # thread pra atualizar controle de estados
    controlThread.start()  # inicia a thread
    os.system('clear')
    print('Conversando com servidor central...')
    receive(server, config) # Inicia dialogo com central

  except KeyboardInterrupt: # if ctrl + c is pressed, exit cleanly
    exit()
