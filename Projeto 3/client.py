#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
#####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

# Estrutura do head
# 4 bytes para o index do pacote
# 4 bytes para o numero total de pacotes
# 2 bytes para o tamanho do payload sendo enviado


from numpy.testing._private.utils import print_assert_equal
from enlace import *
import time
import numpy as np
import random
from colors import Bcolors

#   python -m serial.tools.list_ports
serialName = "COM3"  

def main():
    head_index_size = 4
    n_of_packets_size = 4
    head_payload_size = 2
    head_size = 10
    eop_size = 4
    handshake = False
    transmission = False
    ending = False
    test_phase_1 = False
    test_phase_2 = True

    try:
        print(f"{Bcolors.OKBLUE}Estabelencendo enlace:")
        com1 = enlace('COM3')
        print(f"{Bcolors.OKGREEN}Done")  
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print(f"{Bcolors.OKGREEN}Estabelecida")
        print(f"{Bcolors.OKGREEN}Preparando envio \n")

        #divide imagem para preparar o payload
        image_path = "imgs/image.png"
        bytes_array = open(image_path, 'rb').read()
        info = [bytes_array[i:i+114] for i in range(0, len(bytes_array), 114)]
        n_total_pacotes = len(info)

        #Handshake
        while handshake == False:
            try:
                print(f"{Bcolors.OKBLUE}Iniciando Handshake com o servidor:")
                handshake_head = int(0).to_bytes(head_size, 'big')
                handshake_eop = int(0).to_bytes(eop_size, 'big')
                com1.sendData(handshake_head  + handshake_eop)

                received_head = com1.getData(10)
                received_eop = com1.getData(4)
                print(f"{Bcolors.OKGREEN}handshake executado com sucesso!")
                print(f"{Bcolors.OKGREEN}Inciando transmissao \n{Bcolors.ENDC}")
                handshake = True

            
            except RuntimeError:
                continuar = input(f"{Bcolors.WARNING}Servidor inativo. Tentar novamente? S/N")
                if continuar == "S":
                    pass
                else:
                    break

        while handshake == True and transmission == False:
            payload_index = 0
            while payload_index < len(info):
                
                #setup head
                head_index = int(payload_index + 1).to_bytes(head_index_size, 'big')
                n_of_packets = (n_total_pacotes).to_bytes(n_of_packets_size, 'big')
                head_payload_len = (len(info[payload_index])).to_bytes(head_payload_size, 'big')

                print("-------------------------")
                print(f"{Bcolors.OKGREEN}Index do pacote a ser enviado: {Bcolors.ENDC}{payload_index + 1}")
                print(f"{Bcolors.OKGREEN}Numero total de pacotes a serem enviados: {Bcolors.ENDC}{n_total_pacotes}")
                print(f"{Bcolors.OKGREEN}Tamanho do payload no pacote a ser enviado: {Bcolors.ENDC}{len(info[payload_index])}")

                #Fim de teste
                if test_phase_1 == True and payload_index == 1:
                    head_index = int(payload_index + 2).to_bytes(head_index_size, 'big')
                    test_phase_1 = False

                head = head_index + n_of_packets + head_payload_len

                # payload
                payload = info[payload_index]

                if test_phase_2 == True and payload_index == 1:
                    payload += b"00FF"
                    test_phase_2 = False

                #eop code 2 is sent with the last package
                if payload_index == len(info) - 1:
                    eop = int(2).to_bytes(eop_size, 'big')
                
                else:
                    eop = int(1).to_bytes(eop_size, 'big')

                com1.sendData(head + payload + eop)

                print(f"{Bcolors.OKGREEN}Payload enviado: {Bcolors.ENDC}{payload}")
                print(f"{Bcolors.OKGREEN}EOP enviado: {Bcolors.ENDC}{int.from_bytes(eop, byteorder='big')}")

                time.sleep(2)
                server_response_head, nRx = com1.getData(10)
                server_response_eop_b, nRx = com1.getData(4)
                server_response_eop = int.from_bytes(server_response_eop_b, byteorder='big')
                print(f"{Bcolors.OKGREEN}EOP recebido: {Bcolors.ENDC}{server_response_eop}")

                #eop code 1 restarts the whole transmission
                if server_response_eop == 1:
                    #limpa o buffer
                    com1.fisica.flush()
                    com1.rx.clearBuffer()

                    print(f"{Bcolors.FAIL}Erro! Reiniciando transmissao.")
                    payload_index = 0

                #eop code 2 restarts transmission of current payload
                elif server_response_eop == 2:
                    com1.fisica.flush()
                    com1.rx.clearBuffer()

                    print(f"{Bcolors.FAIL}Erro! Reenviando do payload.")
                    pass

                else:
                    payload_index += 1

                print("-------------------------")
            
            transmission = True

        while ending == False:
            server_final_response_head, nRx = com1.getData(10)
            server_final_response_eop_b, nRx = com1.getData(4)
            server_final_response_eop = int.from_bytes(server_final_response_eop_b, byteorder='big')

            #eop code 3 transmission successful
            if server_final_response_eop == 3:
                print("Transmissão bem-sucedida!")

            #eop code 4 transmission failed
            elif server_final_response_eop == 4:
                print("Falha na transmissão!")

            ending = True


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