import time
import os
import json
import threading
import tcpDistr
import control
import socket

def receive(server):
  try:
    while True:
      message = server.recv(2048).decode('ascii')
      print (message)
      if message.startswith('GET_STATUS'):
        with open('states/states.json', 'r') as openfile:
          json_object = json.load(openfile)
          msg_to_send = json.dumps(json_object).encode('ascii')
          server.send(msg_to_send)
      if str(message) == 'ON':
        print('Tentei')
        GPIO.output(L_01[room], GPIO.LOW)
  except:
    print('Error receiving and handling message')
    pass

if __name__ == '__main__':
  try:
    server, config = tcpDistr.init()
    controlThread = threading.Thread(target=control.states, args=(config,)) # thread pra atualizar controle de estados
    controlThread.start()  # inicia a thread
    print('Conversando com servidor central...')
    receive(server) # Inicia dialogo com central

  except KeyboardInterrupt: # if ctrl + c is pressed, exit cleanly
    exit()

# A Fazer...
# Adicionar sensores no envio e temperatura e humidade
# conectar com o server central [OK]
# instancias conectadas conforme json
# fazer as threads pra distr e central
# Atualizar temp e humidity a cada 2s separadamente
# comunicar com o server pra acionar conforme pedido lampadas, sensores e projetores e retornar sobre sucess
# Informar server central do acionamento do sensor de presença, e janelas e portas
# informar acionamento do sensor de fumaça

# ideias...
# pra comunicar sobre estados enviar sinais pro server central ...