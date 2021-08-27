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
            comandos_a_serem_enviados.append(comandos[random.randint(0,5)])

        lista_bytes = np.array(comandos_a_serem_enviados)
        

        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.

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

        txBuffer = lista_bytes.tobytes()
        print(len(txBuffer))
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.

        #txBuffer = imagem em bytes!

        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.

            
        #finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!
        com1.sendData(np.asarray(txBuffer))
        
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        #txSize = com1.tx.getStatus()
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        

        ftempo=time.time()

        print("Tempo da tranferencia: {}".format(ftempo-tempo))

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
