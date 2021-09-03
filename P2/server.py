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

def separa_lista_comandos(comandos_b):
    lista_separada = []

    i = 0
    while i < len(comandos_b):
        if comandos_b[i:i+1] == b'b':
            lista_separada.append(comandos_b[i+1:i+5])
            i += 5
        
        else:
            lista_separada.append(comandos_b[i:i+2])
            i += 2

    return lista_separada


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

        # os.system('py client.py')

        print("Recepção começando")

        #PEGANDO O TIMING
        

        #Recebe header
        msg_len_b, nRx = com2.getData(4)
        print("Recebeu header")
        
        tempo=time.time()

        #converte header e obtem tamanho da transmissao
        msg_len = int.from_bytes(msg_len_b, byteorder="big")
        print(f"tamanho da transmissao: {msg_len}")

        #recebe numero de comandos e converte para decimal
        # n_comandos_b, nRx = com2.getData(2)
        # n_comandos = int.from_bytes(n_comandos_b, byteorder="big")
        # print(f"Numero de comandos a serem recebidos: {n_comandos}")


        #recebe mensagem 
        rxBuffer, nRx = com2.getData(msg_len)

        print("recebeu {}" .format(rxBuffer))

        lista_separada = separa_lista_comandos(rxBuffer)
        n_comandos = len(lista_separada)

        print(f"lista de comandos separados: {lista_separada}")
        print(f"comandos recebidos: {n_comandos}")

        ftempo=time.time()
        print("Tempo de recebimento: {}".format(ftempo-tempo))

        com2.sendData(n_comandos.to_bytes(2, 'big'))

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
