from show_devices import connectCentral, showDevices


menu_options = {
    1: 'Acesso salas 1 e 3',
    2: 'Acesso salas 2 e 4',
    3: 'Sair',
}


def print_menu():
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


def option1():
   connectCentral()


def option2():
    showDevices(2)


if __name__ == '__main__':
    while(True):
        print('Bem vindo ao trabalho 1 de Fundamentos de Sistemas Embarcados do Wictor Girardi')
        print_menu()
        option = ''
        try:
            option = int(input('Escolha sua opção: '))
        except:
            print('Formato errado. Entre um número ...')
        # Check what choice was entered and act accordingly
        if option == 1:
            option1()
        elif option == 2:
            option2()
        elif option == 3:
            print('Obrigado por utilizar o projeto!')
            exit()
        else:
            print('Opção invalida, tente novamente!')
