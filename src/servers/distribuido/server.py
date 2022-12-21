import json
import threading
import control
import RPi.GPIO as GPIO
import socket
import json

def openSocket():
  configfile = open('../../configs/configuracao_sala_02.json')
  file = json.load(configfile)
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((file['ip_servidor_central'], file['porta_servidor_central']))
  return server
  
def receive(server):
    configfile = open('../../configs/configuracao_sala_02.json')
    file = json.load(configfile)
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
        if GPIO.input(file[device]):
          GPIO.output(file[device], GPIO.LOW)
          server.send('OK'.encode('ascii'))
          continue
        else: 
          GPIO.output(file[device], GPIO.HIGH)
          server.send('OK'.encode('ascii'))
          continue

      if message.startswith('ON_ALL'):
        try:
          keys = [*file]
          for device in keys[5:10]:
            print(file[device])
            GPIO.output(file[device], GPIO.HIGH)
          server.send('OK'.encode('ascii'))
          continue
        except: 
          server.send('NOT_OK'.encode('ascii'))

      if message.startswith('OFF_ALL'):
        try:
          keys = [*file]
          for device in keys[5:10]:
            GPIO.output(file[device], GPIO.LOW)
          server.send('OK'.encode('ascii'))
          continue
        except:
          server.send('NOT_OK'.encode('ascii'))

if __name__ == '__main__':
  try:
    server = openSocket()
    controlThread = threading.Thread(target=control.states)
    controlThread.start()
    print('Servidor inicializado, recebendo....')
    receive(server) 

  except KeyboardInterrupt: 
    exit()
