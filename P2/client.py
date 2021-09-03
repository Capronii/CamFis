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
        # comandos = ['00FF', '00', '0F', 'F0', 'FF00', 'FF']
        comandos = [b'00FF', b'00', b'0F', b'F0', b'FF00', b'FF']

        #Numeros de comandos a serem enviados
        n_comandos = random.randint(10,30)

        #Lista de a serem enviados
        comandos_a_serem_enviados = []

        #Preenche lista
        for comando in range(n_comandos):
            comandos_a_serem_enviados.append(comandos[random.randint(0,5)])

        print(comandos_a_serem_enviados)
        n_comandos = len(comandos_a_serem_enviados).to_bytes(2, 'big')
        # comandos_a_serem_enviados = ['F0', '0F', 'FF', '00', 'FF00', '00FF', '00', 'FF', '00', '00FF', '0F', '00FF', '00', 'F0', '00FF', '00FF']

        # comandos_a_serem_enviados = " ".join(comandos_a_serem_enviados)
        lista_final=b''.join(comandos_a_serem_enviados)
        # txBuffer = bytearray.fromhex(comandos_a_serem_enviados)
        # txBuffer =  b'\xff\x00\xff\xf0'

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

        com1.sendData(txBuffer_header + n_comandos + txBuffer)

        # print(np.asarray(txBuffer_header))
        # com1.sendData(np.asarray(txBuffer_header))
        # print("Header enviado")

        # rxBufferResponse,nRxResponse = com1.getData(header_size)

        # if rxBufferResponse != txBuffer_header:    
            # print("Problema na conferencia")

        # print("Conferencia realizada")

        print(txBuffer)
        # com1.sendData(np.asarray(txBuffer))
        # com1.sendData(txBuffer)
        print("Mensagem enviada")
            
        ftempo=time.time()

        # rxBufferResponse, nRxAns = com1.getData(header_size)

        # ans = int.from_bytes(rxBufferResponse, 'big')

        # if ans == messsage_len:
        #     print("transferencia realizada com sucesso")

        # else:
        #     print("problema na transferencia")        

        print("Tempo de envio: {}".format(ftempo-tempo))

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

