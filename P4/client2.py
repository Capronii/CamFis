from enlace import *
import time
from funcoes import *


serialName = "COM3"
path_img = 'img/image.png'

com1 = enlace(serialName)
com1.enable()


def envia_handshake(pacote_hanshake):
    terminou_hs = False

    com1.sendData(pacote_hanshake)
    init_timer1 = time.time()
    init_timer2 = time.time()

    while not terminou_hs:
        while com1.rx.getBufferLen() == 0:
            timer1 = time.time() - init_timer1
            timer2 = time.time() - init_timer2

            if timer2 > 20:
                print(f'passou 20 segundo, desligando tudo')
                # enviar pacote com h0 = 5
                # shutdown
                payload = []
                l_head = [0]*10
                l_head[0] = 5
                pacote = cria_datagrama(payload, l_head)
                com1.sendData(pacote)

            elif timer1 > 5:
                enviar_novamente = input(
                    'No recebi resposta do server, enviar handshake novamente? sim/nao? ')

                if enviar_novamente == 'sim':
                    # enviar handshake novamente
                    com1.sendData(pacote_hanshake)
                    init_timer1 = time.time()
                else:
                    # shutdown
                    print('Try again')

        header, tamanho_header = com1.getData(14)
        header = list(header)

        if header[0] == 2:
            terminou_hs = True
            print(f'Server pode receber os pacotes\n')
        else:
            print(f'Problema no hanshake')


def main():
    try:
        # carrega img
        imagem = open(path_img, 'rb').read()
        # separa os payloads
        lista_payload = divide_pacotes(imagem)

        for i in lista_payload:
            #print(i, "\n")
            # enviar cada pacote
            print('')

        # criando pacotes com head, payload e eop
        lista_pacotes = cria_pacotes(lista_payload)

        # envia handshake
        handshake = cria_handshake(len(lista_payload))
        envia_handshake(handshake)

        # começar a enviar os pacotes

        for i in range(len(lista_pacotes)):
            com1.sendData(lista_pacotes[i])
            print(f'enviou o pacote {i}\n')
            time.sleep(0.2)

        time.sleep(1)
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


main()
