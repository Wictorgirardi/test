# Trabalho 1 FSE 2022.2
Trabalho 1 da disciplina de Fundamentos de Sistemas Embarcados (2022/2)

Autor: Vinícius Vieira de Souza - Matrícula: 17/0115500

## Descrição
A descrição sobre os objetivos e os detalhes de implementação requisitados podem ser encontrados através [deste link](https://gitlab.com/fse_fga/trabalhos-2022_2/trabalho-1-2022-2)

## Uso
### Passo 1:
Configure os arquivos de comunicação entre servidores (central\tcpCentral.py e distribuido\tcpDistr.py) baseados em quais placas Raspberry Pi irão rodar os servidores distribuidos e central. 

Exemplo: em central\tcpCentral.py e distribuido\tcpDistr.py podemos trocar a configuração da sala desejada na função init()
```python
def init():
  config = readConfig('configuracao_sala_02.json') 
  #... resto do codigo ....#
```

OBS: Altere os arquivos de configuracao_sala_0x.json de acordo com sua necessidade. Por padrão o servidor central de todas as configurações foi definido como o mesmo IP enquanto que o distribuido foi definido conforme sua respectiva placa raspberry

## Passo 2:
Coloque o servidor central em execução primeiro com o comando abaixo na raiz do projeto:
```terminal
python central/central_server.py
```

## Passo 3:
Para conectar um servidor distribuido execute em seguida o comando na raiz do projeto:
```terminal
python distribuido/distr_server.py
```
OBS 1: Caso utilize o distribuido em outra placa lembre-se de atualizar o arquivo de configuração lido em tcpDistr como mencionado no passo 1.

OBS 2: Para a placa rasp43 os comandos serão mesmo porem utilizando python3.

Exemplo:
```terminal
python3 distribuido/distr_server.py
```

