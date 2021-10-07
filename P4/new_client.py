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


from os import error
from numpy.testing._private.utils import print_assert_equal
from enlace import *
import time
import numpy as np
import random
from colors import Bcolors
from functions import *
import datetime

#   python -m serial.tools.list_ports
serialName = "COM5"  
sensor_id = 12
server_id = 23
max_payload_size = 114

def main():
    global sensor_id
    global server_id
    global max_payload_size
    inicia = False
    etapa_1_completa = False
    teste_ordem_pckgs = False
    type4_test = False
    log_file = []
    log_files_path = ''

    try:
        print(f"{Bcolors.OKBLUE}Estabelencendo enlace:{Bcolors.ENDC}")
        com1 = enlace(serialName)
        print(f"{Bcolors.OKGREEN}Done{Bcolors.ENDC}")  
        
        establish_comm(com1)

        image_path = "imgs/image2.png"
        bytes = open(image_path, 'rb').read()

        #arbitrary for now
        file_id = 166

        payload_list = create_payload_list(bytes, max_payload_size)
        total_pckg_num = len(payload_list)

        handshake_timer = time.time()

        while inicia == False:
            if (time.time() - handshake_timer) > 20:
                log_files_path = 'log_files/Client3.txt'
                break

            try:
                send_t1_msg(com1, sensor_id, server_id, total_pckg_num, file_id)
                now =  str(datetime.datetime.now()) + '/envio/1/14' + '\n'
                log_file.append(now)

                print("t1 enviado")
                time.sleep(5)

                head_list, payload_b, eop_b = receive_msg(com1)

                now =  str(datetime.datetime.now()) + '/receb/' + str(head_list[0]) + '/' \
                + str(14 + head_list[5]) + '\n'
                log_file.append(now)
                
                print("recebeu algo")

                # se cliente n receber msg t2 ha um problema
                if head_list[0] != 2:
                    print(f"{Bcolors.WARNING}Mensagem recebida não é do tipo 2! Encerrando com!")
                    break

                else:
                    inicia = True
                    print(f"{Bcolors.OKGREEN}handshake executado com sucesso!")
                    print(f"{Bcolors.OKGREEN}Inciando transmissao \n{Bcolors.ENDC}")

                # t2_received_client_id = 
                
                # if t2_received_client_id == sensor_id:
                #     inicia = True 

                # else:
                #     continuar = input(f"{Bcolors.WARNING}Id do cliente errado. Tentar novamente? S/N")
                #     if continuar == "S":
                #         pass
                #     else:
                #         break

            except RuntimeError:
                # continuar = input(f"{Bcolors.WARNING}Servidor inativo. Tentar novamente? S/N")
                # if continuar == "S":
                #     pass
                # else:
                #     break
                print('Servidor inativo. Tentando novamente!')
                pass

        cont = 1
        while inicia == True and etapa_1_completa == False:
            if cont > total_pckg_num:
                etapa_1_completa = True
                f"{Bcolors.OKGREEN}Sucesso!"
                continue

            payload = payload_list[cont - 1]

            if type4_test == True and cont == 4:
                time.sleep(25)

            # envia pckg cont - msg t3
            if teste_ordem_pckgs:
                print("enviou msg teste")
                send_t3_msg(com1, total_pckg_num, cont+4, len(payload), payload)

                now =  str(datetime.datetime.now()) + '/envio/3/' + str(len(payload)+14) + '/' \
                + str(cont+4) + '/' + str(total_pckg_num) + '/' + str(crc(payload)) + '\n'
                log_file.append(now)

                teste_ordem_pckgs = False

            else:    
                print("enviou msg certa")
                send_t3_msg(com1, total_pckg_num, cont, len(payload), payload)

                now =  str(datetime.datetime.now()) + '/envio/3/' + str(len(payload)+14) + '/' \
                + str(cont) + '/' + str(total_pckg_num) + '/' + str(crc(payload)) + '\n'
                log_file.append(now)

            #set timer 1
            timer1 = time.time() 

            #set timer 2
            timer2 = time.time()

            received_t4 = False

            while received_t4 == False:
                received_t4, head_list = receive_t4(com1, cont)

                if head_list is not None:
                    now =  str(datetime.datetime.now()) + '/receb/' + str(head_list[0]) + '/' \
                    + str(14 + head_list[5]) + '\n'
                    log_file.append(now)

                # time.sleep(2)
                # head_list, payload_b, eop_b = receive_msg(com1)
                


                # print(received_t4)
                # print(head_list)

                if received_t4:
                    continue 

                # if head_list[0] == 4 and head_list[7] == cont:
                #     received_t4 = True
                #     continue
                

                if (time.time() - timer1) > 5:
                    # envia pckg cont - msg t3
                    send_t3_msg(com1, total_pckg_num, cont, len(payload), payload)

                    now =  str(datetime.datetime.now()) + '/envio/3/' + str(len(payload)+14) + '/' \
                    + str(cont) + '/' + str(total_pckg_num) + '/' + str(crc(payload)) + '\n'
                    log_file.append(now)

                    timer1 = time.time()

                if (time.time() - timer2) > 20:
                    # envia msg t5
                    send_t5_msg(com1)

                    now =  str(datetime.datetime.now()) + '/envio/5/14' + '\n'
                    log_file.append(now)
                    log_files_path = 'log_files/Client4.txt'

                    f = open(log_files_path, 'w')
                    for log in log_file:
                        f.write(log)
                    f.close()

                    #encerra com
                    print(f"{Bcolors.WARNING}Timeout!")
                    raise Exception

                if head_list == None:
                    continue

                #recebeu msg t6
                if head_list[0] == 6:
                    log_files_path = 'log_files/Client2.txt'
                    #corrige cont
                    cont = head_list[6]
                    payload = payload_list[cont - 1]

                    #envia pckg cont - msg t3
                    send_t3_msg(com1, total_pckg_num, cont, len(payload), payload)

                    now =  str(datetime.datetime.now()) + '/envio/3/' + str(len(payload)+14) + '/' \
                    + str(cont) + '/' + str(total_pckg_num) + '/' + str(crc(payload)) + '\n'
                    log_file.append(now)

                    timer1 = time.time()
                    timer2 = time.time()
                    
            cont += 1


        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

        if log_files_path == '':
            log_files_path = 'log_files/Client1.txt'

        f = open(log_files_path, 'w')
        for log in log_file:
            f.write(log)
        f.close()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()