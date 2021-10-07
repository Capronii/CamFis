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
import os
from colors import Bcolors
from functions import *
import datetime

#   python -m serial.tools.list_ports
serialName = "COM6" 
server_id = 23
max_payload_size = 114

def main():
    global server_id
    global max_payload_size
    ocioso = True
    etapa_1_completa = False
    received_payload_list = []
    log_file = []
    log_files_path = ''
    crc_test = ''
    type4_test = False

    try:
        print(f"{Bcolors.OKBLUE}Estabelencendo enlace:{Bcolors.ENDC}")
        com2 = enlace(serialName)
        print(f"{Bcolors.OKGREEN}Done{Bcolors.ENDC}")

        establish_comm(com2)

        while ocioso:
            try:
                head_list, foo, eop_b = receive_msg(com2)
                now =  str(datetime.datetime.now()) + '/receb/' + str(head_list[0]) + '/' + '\n'
                log_file.append(now)

                # se msg n for do tipo 1 servidor permanece ocioso
                if head_list[0] == 1 and head_list[2] == server_id:
                    print("recebeu msg T1 para servidor certo")
                    ocioso = False
                    total_pckg_num = head_list[3]
                    file_id = head_list[5]

                    send_t2_msg(com2, head_list[1], server_id)
                    now =  str(datetime.datetime.now()) + '/envio/2/14' + '\n'
                    log_file.append(now)

                    print("Enviada msg tipo: 2\n")

                time.sleep(1)
            
            except RuntimeError:
                # continuar = input(f"{Bcolors.WARNING}Nenhuma mensagem recebida. Tentar novamente? S/N")
                # if continuar == "S":
                #     pass
                # else:
                #     break
                print("Servidor ocioso")
                time.sleep(1)
        
        cont = 1
        while etapa_1_completa == False and ocioso == False:

            print(f"Esperando pacote: {cont}")
            
            if cont > total_pckg_num:
                etapa_1_completa = True
                f"{Bcolors.OKGREEN}Sucesso!"
                continue

            #set timer 1
            timer1 = time.time() 
            #set timer 2
            timer2 = time.time()

            received_t3 = False

            if type4_test == True and cont == 4:
                time.sleep(25)

            while received_t3 == False:
                received_t3, head_list_t3, payload_b = receive_t3(com2)

                if head_list_t3 != None:
                    now =  str(datetime.datetime.now()) + '/receb/' + str(head_list_t3[0]) + '/' \
                    + str(14 + head_list_t3[5]) + '/' + str(head_list_t3[4]) + '/' +  str(head_list_t3[3]) \
                    + '/' + str(crc(payload_b)) + '\n'
                    log_file.append(now)

                    if payload_b != None:
                        crc_test = binascii.crc_hqx(payload_b, 0)
                        if crc_test != head_list_t3[8:10][0]:
                            print(crc_test)
                            print(head_list_t3[8:10])
                            print('aqui')
                            send_t6_msg(com2, cont)
                            log_files_path = 'log_files/Server2.txt'

                            now =  str(datetime.datetime.now()) + '/envio/6/14' + '\n'
                            log_file.append(now)

                            continue
                
                if received_t3 == True:
                    continue        
                time.sleep(1)

                if (time.time() - timer2) > 20:
                    ocioso = True
                    # envia msg t5
                    send_t5_msg(com2)
                    log_files_path = 'log_files/Server4.txt'

                    now =  str(datetime.datetime.now()) + '/envio/5/14' + '\n'
                    log_file.append(now)

                    f = open(log_files_path, 'w')
                    for log in log_file:
                        f.write(log)
                    f.close()

                    print("Enviada msg tipo: 5\n")

                    #encerra com
                    print(f"{Bcolors.WARNING}Timeout!")
                    raise Exception

                if (time.time() - timer1) <= 2:
                    print("t<2")
                    continue

                else:
                    send_t4_msg(com2, cont)
                    
                    now =  str(datetime.datetime.now()) + '/envio/4/14' + '\n'
                    log_file.append(now)

                    print("Enviada msg tipo: 4 sem verificar\n")
                    timer1 = time.time() 
                    continue

            # verificar payload
            # verificar n do pacote
            if head_list_t3[4] == cont:
                send_t4_msg(com2, cont)

                now =  str(datetime.datetime.now()) + '/envio/4/14' + '\n'
                log_file.append(now)

                print("Enviada msg tipo: 4 depois de verificado pacotes\n")
                received_payload_list.append(payload_b)
                cont += 1

            else:
                send_t6_msg(com2, cont)
                log_files_path = 'log_files/Server2.txt'

                now =  str(datetime.datetime.now()) + '/envio/6/14' + '\n'
                log_file.append(now)

                time.sleep(3)
                print("Enviada msg tipo: 6\n")

        image_array = b''.join(received_payload_list)
        imageW = "imgs/receivedCopy.png"
        f = open(imageW, 'wb')
        f.write(image_array)
        f.close()
              
        # print(received_payload_list)
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com2.disable()

        if log_files_path == '':
            log_files_path = 'log_files/Server1.txt'

        f = open(log_files_path, 'w')
        for log in log_file:
            f.write(log)
        f.close()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com2.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()