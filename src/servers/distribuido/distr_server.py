import json
import threading
import tcpDistr
import control
import RPi.GPIO as GPIO

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
    server, config = tcpDistr.init()
    controlThread = threading.Thread(target=control.states, args=(config,))
    controlThread.start()
    print('Servidor inicializado, recebendo....')
    receive(server, config) 

  except KeyboardInterrupt: 
    exit()
