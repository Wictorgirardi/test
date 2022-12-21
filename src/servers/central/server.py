import threading
import json
import socket

listconn = {}
addresses = []

def sendCommand(conn, COMMAND):
  conn.send(COMMAND.encode('ascii'))

def show_devices(conn, showAll):
    status = conn.recv(2048).decode('ascii')
    status = json.loads(status)

    if status['SPres'] == 'ON' or status['SFum'] == 'ON' or status['SJan'] == 'ON' or status['SPor'] == 'ON' :
      status['AL_BZ'] = 'ON'

    if(showAll == 'true'):
      print('\n')
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
      print('\n')
      print('1 - Luz 01: ' +status['L_01'])
      print('2 - Luz 02: ' +status['L_02'])
      print('3 - Ar condicionado: ' +status['AC'])
      print('4 - Projetor: ' +status['PR'])
      print('5 - Alarme: ' +status['AL_BZ'])

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
        sendCommand(listconn[addresses[0]], f'GET_STATUS')
        show_devices(listconn[addresses[0]], "true")
        input('Continuar...')
      if op == 2:
        device = -1
        while device < 1 or device > 7:
          print('Listagem de dispositivos:')
          sendCommand(listconn[addresses[0]], f'GET_STATUS')
          show_devices(listconn[addresses[0]], "false")
          print('OBS: Escolha o digito 6 para acionar todos os dispositivos (ON) e 7 para desativar(OFF)')
          device = int(input('Digite o numero do dispositivo que deseja alternar entre ON/OFF: '))
          if device == 1:
            sendCommand(listconn[addresses[0]], f'ON_OFF_L_01')
          elif device == 2:
            sendCommand(listconn[addresses[0]], f'ON_OFF_L_02')
          elif device == 3:
            sendCommand(listconn[addresses[0]], f'ON_OFF_AC')
          elif device == 4:
            sendCommand(listconn[addresses[0]], f'ON_OFF_PR')
          elif device == 5:
            sendCommand(listconn[addresses[0]], f'ON_OFF_AL_BZ')
          elif device == 6:
            sendCommand(listconn[addresses[0]], f'ON_ALL')
          elif device == 7:
            sendCommand(listconn[addresses[0]], f'OFF_ALL')
          print('Dispositivo alternado com sucesso!') if listconn[addresses[0]].recv(2048).decode('ascii') == 'OK' else print('Ooops! Algo errado aconteceu, tente novamente.')
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
            listconn[addr[0]] = conn
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)