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
from colors import Bcolors

#   python -m serial.tools.list_ports
serialName = "COM4" 

def main():
    head_index_size = 4
    head_n_of_packets_size = 4
    head_payload_size = 2
    head_size = 10
    eop_size = 4
    handshake = False
    transmission = False
    ending = False
    received_payload_list = []
    payload_size_problem = False

    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        print(f"{Bcolors.OKBLUE}Estabelencendo enlace:")
        com2 = enlace('COM4')
        print(f"{Bcolors.OKGREEN}Done")
        com2.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print(f"{Bcolors.OKGREEN}Estabelecida")
        # os.system('py client.py')
        print(f"{Bcolors.OKGREEN}Recepção começando \n")

        #Handshake
        while handshake == False:
            try:
                print(f"{Bcolors.OKBLUE}Iniciando Handshake com o cliente:")
                received_head = com2.getData(10)
                received_eop = com2.getData(4)

                handshake_head = int(0).to_bytes(head_size, 'big')
                handshake_eop = int(0).to_bytes(eop_size, 'big')
                com2.sendData(handshake_head  + handshake_eop)
                print(f"{Bcolors.OKGREEN}handshake executado com sucesso!")
                print(f"{Bcolors.OKGREEN}Inciando recepcao \n{Bcolors.ENDC}")
                handshake = True
            
            except RuntimeError:
                pass

        payload_index = 0
        while handshake == True and transmission == False:
            
            client_sent_head, nRx = com2.getData(10)
            packet_index = int.from_bytes(client_sent_head[0:4], 'big')
            n_of_packets = int.from_bytes(client_sent_head[4:8], 'big')
            payload_len = int.from_bytes(client_sent_head[8:10], 'big')

            print("-------------------------")
            print(f"{Bcolors.OKBLUE}Index do pacote esperado: {Bcolors.ENDC}{payload_index + 1}")
        
            if (payload_index + 1) != packet_index:
                print(f"{Bcolors.FAIL}Index do pacote recebido: {Bcolors.ENDC}{packet_index}")
                print(f"{Bcolors.FAIL}Erro na ordem de envio! Reiniciando transmissao.")

                #limpa o buffer
                com2.fisica.flush()
                com2.rx.clearBuffer()

                response_head = int(0).to_bytes(head_size, 'big')
                response_eop = int(1).to_bytes(eop_size, 'big')
                payload_index = 0
                received_payload_list = []
                com2.sendData(response_head + response_eop)

                continue
            
            print(f"{Bcolors.OKGREEN}Index do pacote recebido: {Bcolors.ENDC}{packet_index}")
            print(f"{Bcolors.OKGREEN}Numero total de pacotes a serem recebidos: {Bcolors.ENDC}{n_of_packets}")
            print(f"{Bcolors.OKBLUE}Tamanho do payload informado no head: {Bcolors.ENDC}{payload_len}")
            
            #receive payload
            try:
                payload_and_eop, nRx = com2.getData(payload_len + 4)
                payload = payload_and_eop[:-4]
                eop_b = payload_and_eop[-4:]
                eop = int.from_bytes(eop_b, 'big')

            except RuntimeError:
                payload_size_problem = True

            possible_eops = [0,1,2]

            if len(payload) != payload_len or payload_size_problem or eop not in possible_eops:
                # print(f"{Bcolors.FAIL}Tamanho do payload recebido: {Bcolors.ENDC}{len(payload)}")
                print(f"{Bcolors.FAIL}Tamanho real do payload não corresponde ao informado no head! Solicitando reenvio do payload.")
                
                #limpa o buffer
                com2.fisica.flush()
                com2.rx.clearBuffer()

                response_head = int(0).to_bytes(head_size, 'big')
                response_eop = int(2).to_bytes(eop_size, 'big')
                com2.sendData(response_head + response_eop)

                payload_size_problem = False
                
                continue

            received_payload_list.append(payload)

            print(f"{Bcolors.OKGREEN}Tamanho do payload recebido: {Bcolors.ENDC}{len(payload)}")

            print(f"{Bcolors.OKGREEN}Payload recebido: {Bcolors.ENDC}{payload}")

            print(f"{Bcolors.OKGREEN}EOP recebido: {Bcolors.ENDC}{eop}")
            print("-------------------------")

            #receive eop
            # eop_b, nRx = com2.getData(4)
            # eop = int.from_bytes(eop_b, 'big')

            response_head = int(0).to_bytes(head_size, 'big')
            response_eop = int(0).to_bytes(eop_size, 'big')

            com2.sendData(response_head + response_eop)

            payload_index += 1

            if eop == 2:
                transmission = True

        while ending == False:
            try:
                image_array = b''.join(received_payload_list)
                imageW = "imgs/receivedCopy.png"
                f = open(imageW, 'wb')
                f.write(image_array)
                f.close()

                #final response (transmission and save successful)
                response_head = int(0).to_bytes(head_size, 'big')
                response_eop = int(3).to_bytes(eop_size, 'big')
                com2.sendData(response_head + response_eop)

            except:
                #final response (error)
                response_head = int(0).to_bytes(head_size, 'big')
                response_eop = int(4).to_bytes(eop_size, 'big')
                com2.sendData(response_head + response_eop)

            print("Resposta final enviada")
            ending = True

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