import json
import socket


def showDevices(sala):
    print('Bem vindo a sala: ' + str(sala))
    print('lista de dispositivos:\n')
    
    f = open('configs/configuracao_sala_01.json')
    data = json.load(f)
    for i in data['outputs']:
        print(str(data['outputs'].index(i)) + ' - ' + i['tag'])
    f.close()


def showInputs(sala):
    print('Bem vindo a sala: ' + str(sala))
    print('lista de inputs:\n')
    f = open('configs/configuracao_sala_01.json')
    data = json.load(f)
    for i in data['inputs']:
        print(str(data['inputs'].index(i)) + ' - ' + i['tag'])
    f.close()


def connectCentral():
    f = open('configs/configuracao_sala_01.json')
    data = json.load(f)
    print(data['ip_servidor_central'],
          data['porta_servidor_central'])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((data['ip_servidor_central'], data['porta_servidor_central']))
        s.listen()
        conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)


def connectDistribuido():
    f = open('configs/configuracao_sala_01.json')
    data = json.load(f)
    print(data['ip_servidor_distribuido'],
          data['porta_servidor_distribuido'])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((data['ip_servidor_distribuido'],
               data['porta_servidor_distribuido']))
        s.listen()
        conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
