import os
import threading
import json
import socket
import json

room_status = []
listconn = {}
addresses = []

def readConfig(filename):
  with open(filename,'r') as configfile:
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


def init():
  config = readConfig('../configs/configuracao_sala_02.json')
  server_address = (config['ip_servidor_central'], config['porta_servidor_central'])
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind(server_address)
  server.listen(4)

  return server

def accept_connections():
  server = init()
  while True:
    conn, addr = server.accept()
    print(f"{str(addr)} connected")
  
  
def handle(conn):
  try:
    status = conn.recv(2048).decode('ascii')
    status = json.loads(status)
    print(status)
    room_status = status
    return room_status

  except:
    print('Error handling connection')
def sendCommand(conn, COMMAND):
  conn.send(COMMAND.encode('ascii'))

# Apagar? Desnecessario...
def handle(conn):
  try:
    while True:
      status = conn.recv(2048).decode('ascii')
      status = json.loads(status)
      room_status = status
      print(status)
  except KeyboardInterrupt:
    print('Error handling connections')
    exit()

def get_status(conn):
  try:
    status = conn.recv(2048).decode('ascii')
    status = json.loads(status)

    print('Saidas:')
    print('L_01: '+status['L_01']+' L_02: '+status['L_02'])
    print('AC: '+status['AC'])
    print('PR: '+status['PR'])
    print('AL_BZ: '+status['AL_BZ'])
    print('Sensores:')
    print('SPres: '+status['SPres'])
    print('SFum: '+status['SFum'])
    print('SJan: '+status['SJan']+' SPor: '+status['SPor'])
    print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(status['Temperatura'], status['Humidade']))
    print('Total de pessoas nesta sala: '+status['Pessoas'])
  except:
    print('Error getting status')
    

def receive():
  try:
    while True:
      conn, addr = server.accept()
      addresses.append(addr[0])
      listconn[addr[0]] = conn
      print(f"{str(addr)} connected")

  except KeyboardInterrupt:
    return

def menu():
  try:
    op = 0
    while op != 3:
      print('Bem vindo ao trabalho 1 de Fundamentos de Sistemas Embarcados do Wictor Girardi')
      print('1) Listar estados dos dispositivos das salas') # Por enquanto funciona voltado para uma sala 1
      print('2) Ative um dispositivo') # Em construção...
      print('3) Sair do programa')
      op = input('Digite uma opcao: ')
      if int(op)<1 or int(op)> 3:
        menu()
      
      if int(op) == 1:
        if len(addresses) == 0:
          print('Nenhuma sala conectada')
          input('Aperte enter para continuar...')
          continue

        room = -1
        while room > len(addresses) or room < 0:
          os.system('clear')
          print('----- Listar Estados -------')
          print('Salas conectadas:')
          for i in range(len(addresses)):
            print(f'Sala {i} - IP:{addresses[i]}')
          room = int(input('Digite o numero da sala desejada'))

        sendCommand(listconn[addresses[room]], f'GET_STATUS{addresses[room]}') #Mandar ip? Sala...?
        get_status(listconn[addresses[room]])
        input('Aperte enter para continuar...')
        

      if int(op) == 2:
        pass
      if int(op) == 3:
        quit()

  except KeyboardInterrupt:
    quit()


if __name__ == '__main__':
  server = init() #Configura socket do servidor central
  menuThread = threading.Thread(target=menu, ) #thread pra conversar com user
  menuThread.start()  # inicia a thread
  receive() # Inicia dialogo com distr