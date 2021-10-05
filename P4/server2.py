from enlace import *
import time
import numpy as np
from funcoes import *
serialName = "COM4"

com2 = enlace(serialName)
com2.enable()

server_id = 5
client_id = 10
pacote_id = 15
lista_payloads_recebidos = []


def recebe_header():
    r_header, len_r_header = com2.getData(10)

    return r_header, len_r_header


def recebe_handshake():
    terminou_handshake = False

    while not terminou_handshake:
        header, tamanho_header = com2.getData(14)
        header = list(header)
        total_pacotes_para_receber = header[3]
        print(f'Header Handshaeke: {header} ')

        if header[2] == server_id:
            if header[0] == 1:
                payload = []
                header = [0]*10
                header[0] = 2
                header[1] = client_id
                header[2] = server_id
                pacote = cria_datagrama(payload, header)
                com2.sendData(pacote)
                terminou_handshake = True
                print(f'Handshake enviado!')
        else:
            print(f'ID errado do hanshake')

    return total_pacotes_para_receber


def recebe_imagem(quantidade_pacotes):  
    numero_pacote_atual = 0

    while numero_pacote_atual < quantidade_pacotes:
        init_timer1 = time.time()
        init_timer2 = time.time()

        while com2.rx.getBufferLen() == 0:
            delta_timer1 = init_timer1 - time.time()
            delta_timer2 = init_timer2 - time.time()

            if delta_timer2 >= 20:
                print(f'passou 20 segundos, desligando...')
                payload = []

                header = [0]*10
                header[0] = 5
                header[1] = Id_client
                header[2] = Id_server
                pacote = cria_datagrama(payload, header)
                com2.sendData(pacote)

            if delta_timer1 >= 5:
                print(
                    f'5 segundos sem resposta, enviando de novo...')
                

        # Header received
        received_head = com2.getData(10)[0]
        received_head = list(received_head)
        print(f'header recebido: {received_head}', end='')
        # Payload and eop
        tamanho_pacote = 4
        msg_type = received_head[0]
        quantidade_pacotes = received_head[3]
        numero_pacote_atual = received_head[4]


        if msg_type == 3:
            payload_size = received_head[5]
            tamanho_pacote += payload_size

        if msg_type == 5:
            print(f'Código 5 - desligar...')

        pacote_recebido, len_pacote_recebido = com2.getData(tamanho_pacote)
        payload_recebido = pacote_recebido[:-4]
        lista_payloads_recebidos.append(payload_recebido)
        eop_recebido = pacote_recebido[-4:]

        # EOP check
        print(
            f'Received package [{numero_pacote_atual} / {quantidade_pacotes}]')

    print(f'Received all packages')
    # Junta e salva imagem
    juntar_imagem(lista_payloads_recebidos)


def juntar_imagem(lista_payloads_recebidos):
    imagem_recebida = b''.join(lista_payloads_recebidos)

    with open('img_recebida.png', 'wb') as file:
        file.write(imagem_recebida)

    print(f'Salvando imagem\n')


def main():
    print('Server Start')

    total_pacotes_receber = recebe_handshake()

    print('Terminou handshake, iniciando recepcao de pacotes')
    recebe_imagem(total_pacotes_receber)

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com2.disable()

if __name__ == "__main__":
    main()
