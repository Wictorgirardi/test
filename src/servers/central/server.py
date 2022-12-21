import threading
import json
import socket
from datetime import datetime

connection = {}
addresses = []

def log_csv(msg, time):
  with open('log.csv', 'a') as file:
      log = msg + ": " + str(time)
      file.write(log + '\n')

def show_devices(conn, showAll):
    status = conn.recv(2048).decode('ascii')
    status = json.loads(status)

    if status['SPres'] == 'ON' or status['SFum'] == 'ON' or status['SJan'] == 'ON' or status['SPor'] == 'ON' :
      status['AL_BZ'] = 'ON'

    if(showAll == 'true'):
      print('--------------------------')
      print('Luz 01: ' +status['L_01'])
      print('Luz 02: ' +status['L_02'])
      print('Ar condicionado: '+status['AC'])
      print('Projetor: '+status['PR'])
      print('Alarme: '+status['AL_BZ'])
      print('Sensor presença: ' +status['SPres'])
      print('Sensor fumaça: ' +status['SFum'])
      print('Sensor porta: ' +status['SPor'])
      print('Sensor janela: ' +status['SJan'])
      print("Temperatura da sala: " + str(status['Temperatura']) + ' Celsius')
      print("Humidade: " + str(status['Humidade']) + '%')
      print('Total de pessoas: ' +status['Pessoas'])
    else: 
      print('--------------------------')
      print('1 - Luz 01: ' +status['L_01'])
      print('2 - Luz 02: ' +status['L_02'])
      print('3 - Ar condicionado: ' +status['AC'])
      print('4 - Projetor: ' +status['PR'])
      print('5 - Alarme: ' +status['AL_BZ'])
      print('6 - Ligar todos os dispositivos')
      print('7 - Desligar todos os dispositivos')

def menu():
    op = 0
    print('Bem vindo ao trabalho 1 de Fundamentos de Sistemas Embarcados do aluno Wictor Girardi, escolha sua opção abaixo:')
    while op != 3:
      print('1 - Listar todos dispositivos') 
      print('2 - Ativar ou desativar dispositivos disponiveis')
      print('3 - Terminar Execução')
      op = int(input())

      if op not in [1, 2, 3]:
        print('Opção invalida, tente novamente:') 
        menu()
      if op == 1:
        connection[addresses[0]].send((f'GET_ALL').encode('ascii'))
        log_csv(f'GET_ALL', datetime.datetime.now())
        show_devices(connection[addresses[0]], "true")
        print('\n')
      if op == 2:
        device = -1
        while device < 1 or device > 7:
          print('\n')
          print('Listagem de dispositivos:')
          connection[addresses[0]].send((f'GET_ALL').encode('ascii'))
          show_devices(connection[addresses[0]], "false")
          device = int(input('Escolha qual dispositivo deseja alterar: '))
          if device == 1:
            connection[addresses[0]].send(f'CONTROL_L_01'.encode('ascii'))  
            log_csv(f'CONTROL_L_01', datetime.datetime.now())
          elif device == 2:
            connection[addresses[0]].send(f'CONTROL_L_02'.encode('ascii'))          
            log_csv(f'CONTROL_L_02', datetime.datetime.now())
          elif device == 3:
            connection[addresses[0]].send(f'CONTROL_AC'.encode('ascii'))
            log_csv(f'CONTROL_AC', datetime.datetime.now())
          elif device == 4:
            connection[addresses[0]].send(f'CONTROL_PR'.encode('ascii'))  
            log_csv(f'CONTROL_PR', datetime.datetime.now())      
          elif device == 5:
            connection[addresses[0]].send(f'CONTROL_AL_BZ'.encode('ascii'))
            log_csv(f'CONTROL_AL_BZ', datetime.datetime.now())      
          elif device == 6:
            connection[addresses[0]].send(f'ON_ALL'.encode('ascii'))
            log_csv(f'ON_ALL', datetime.datetime.now())      
          elif device == 7:
            connection[addresses[0]].send(f'OFF_ALL'.encode('ascii'))
            log_csv(f'OFF_ALL', datetime.datetime.now())      
          print('\n')
          print('Dispositivo alternado com sucesso!') if connection[addresses[0]].recv(2048).decode('ascii') == 'OK' else print('Ooops! Algo errado aconteceu, tente novamente.')
      if op == 3:
        print('Obrigado por utilizar o projeto!')
        quit()
    
if __name__ == '__main__':
  configfile = open('../../configs/configuracao_sala_02.json')
  file = json.load(configfile)
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((file['ip_servidor_central'], file['porta_servidor_central']))
        server.listen()  
        conn, addr = server.accept()
  with conn:
        print(f"Conectado com o: {addr}")
        while True:
            menuThread = threading.Thread(target=menu, ) 
            menuThread.start() 
            addresses.append(addr[0])
            connection[addr[0]] = conn
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)