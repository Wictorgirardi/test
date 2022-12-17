import socket
import json

"""
Config do socket
"""

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
  config = readConfig('configuracao_sala_02.json')
  server_address = (config['ip_servidor_central'], config['porta_servidor_central'])
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.connect(server_address)

  return server, config