#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
#####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from numpy.testing._private.utils import print_assert_equal
from enlace import *
import time
import numpy as np
import random


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)


def main():
    try:
        #Lista de comandos possiveis
        comandos = [b'00FF', b'00', b'0F', b'F0', b'FF00', b'FF']

        #Numeros de comandos a serem enviados
        n_comandos = random.randint(10,30)

        #Lista de a serem enviados
        comandos_a_serem_enviados = []

        #Preenche lista
        for comando in range(n_comandos):
            comando_add = comandos[random.randint(0,5)]
            if len(comando_add) == 4:
                comandos_a_serem_enviados.append(b'b')

            comandos_a_serem_enviados.append(comando_add)

        print(comandos_a_serem_enviados)
        n_comandos_b = n_comandos.to_bytes(2, 'big')

        lista_final = b''.join(comandos_a_serem_enviados)

        print("Estabelencendo enlace:")
        com1 = enlace('COM3')
        print("Done")   
        
        #PEGANDO O TIMING
        tempo=time.time()

        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        print("Ativando comunicação")
        com1.enable()

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Estabelecida")

        # txBuffer = lista_bytes.tobytes()
        txBuffer = lista_final
        message_len = len(txBuffer)
        # numero_comandos_enviados = len(comandos_a_serem_enviados).to_bytes(2,byteorder="big")
        print()


        header_size = 4
        txBuffer_header = message_len.to_bytes(header_size, 'big')
        print(f"tamanho da lista a ser enviada {message_len}")
        print(f'txBuffer header: {txBuffer_header}')

        print(f'numero de comandos a serem enviados: {n_comandos}')

        print(f'txBuffer: {txBuffer}')

        com1.sendData(txBuffer_header  + txBuffer)


        print("Mensagem enviada")
            
        ftempo=time.time()
     

        print("Tempo de envio: {}".format(ftempo-tempo))

        n_comandos_recebidos_b = com1.getData(2)
        n_comandos_recebidos = int.from_bytes(n_comandos_recebidos_b[0], byteorder="big")

        if n_comandos_recebidos == n_comandos:
            print("Sucesso! Servidor recebeu o numero certo de comandos")

        else:
            print("Erro! Servidor nao recebeu o numero certo de comandos")

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

