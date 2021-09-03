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
import os


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.

        print("Estabelencendo enlace:")
        com2 = enlace('COM4')
        print("Done")

        com2.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Estabelecida")

        os.system('py client.py')

        print("Recepção começando")

        #PEGANDO O TIMING
        tempo=time.time()

        msg_len_b, nRx = com2.getData(4)
        print("Recebeu header")

        msg_len = int.from_bytes(msg_len_b, byteorder="big")

        rxBuffer, nRx = com2.getData(msg_len)

        print("recebeu {}" .format(rxBuffer))

        ftempo=time.time()
        print("Tempo da tranferencia: {}".format(ftempo-tempo))

        response = nRx.to_bytes(4, 'big')
        com2.sendData(response)
        print("resposta enviada")

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com2.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com2.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()