from typing import List, Tuple
from numpy.testing._private.utils import print_assert_equal
from enlace import *
import time
import numpy as np
import random
from colors import Bcolors
import binascii

RIGHT_EOP = b'\xff\xaa\xff\xaa'
HEX_0 = b'\x00'

def establish_comm(com: enlace) -> None:
    com.enable()
    #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
    print(f"{Bcolors.OKGREEN}Estabelecida{Bcolors.ENDC}")
    print(f"{Bcolors.OKGREEN}Preparando envio \n{Bcolors.ENDC}")


def create_payload_list(bytes_array: bytes, max_payload_size: int) -> List[bytes]:
    return [bytes_array[i:i+max_payload_size] for i in range(0, len(bytes_array), max_payload_size)]


def send_t1_msg(
        com: enlace, sensor_id: int, server_id: int, 
        total_pckg_num: int, file_id: int) -> None:

    h0 = int(1).to_bytes(1, 'little')
    h1 = int(sensor_id).to_bytes(1, 'little')
    h2 = int(server_id).to_bytes(1, 'little')
    h3 = int(total_pckg_num).to_bytes(1, 'little')
    h5 = int(file_id).to_bytes(1, 'little')
    
    head = h0 + h1 + h2 + h3 + HEX_0 + h5 + HEX_0*4
    com.sendData(head + RIGHT_EOP)


def send_t2_msg(com: enlace, sensor_id: int, server_id:int) -> None:

    h0 = int(2).to_bytes(1, 'little')
    h1 = int(sensor_id).to_bytes(1, 'little')
    h2 = int(server_id).to_bytes(1, 'little')

    head = h0 + h1 + h2 + HEX_0*7
    com.sendData(head + RIGHT_EOP)


def send_t3_msg(
        com: enlace, total_pckg_num: int, pckg_index: int, 
        payload_size: int, payload: bytes) -> None:

    h0 = int(3).to_bytes(1, 'little')
    h3 = int(total_pckg_num).to_bytes(1, 'little')
    h4 = int(pckg_index).to_bytes(1, 'little')
    h5 = int(payload_size).to_bytes(1, 'little')
    h8h9 = (binascii.crc_hqx(payload, 0)).to_bytes(2, 'little')
    
    head = h0 + HEX_0*2 + h3 + h4 + h5 + HEX_0*2 + h8h9
    com.sendData(head + payload + RIGHT_EOP)


def send_t4_msg(com: enlace, last_pckg_index: int) -> None:

    h0 = int(4).to_bytes(1, 'little')
    h7 = int(last_pckg_index).to_bytes(1, 'little')

    head = h0 + HEX_0*6 + h7 + HEX_0*2
    com.sendData(head + RIGHT_EOP)


def send_t5_msg(com: enlace) -> None:

    h0 = int(5).to_bytes(1, 'little')

    head = h0 + HEX_0*9
    com.sendData(head + RIGHT_EOP)


def send_t6_msg(com: enlace, last_pckg_index: int) -> None:
    print(time.time())
    h0 = int(6).to_bytes(1, 'little')
    h6 = int(last_pckg_index).to_bytes(1, 'little')

    head = h0 + HEX_0*5 + h6 + HEX_0*3
    com.sendData(head + RIGHT_EOP)

def receive_msg(com: enlace) -> Tuple[List[int], bytes, bytes]:
    head_b, nRx = com.getData(10)
    head_list = []

    for i in range(8):
        head_list.append(int.from_bytes(head_b[i:i+1], "little"))
    head_list.append(int.from_bytes(head_b[8:10], "little"))

    if head_list[0] == 1:
        eop_b, nRx = com.getData(4)
        verify_eop(eop_b)

        print(f'msg tipo {head_list[0]} recebida\n')
        return head_list, None, eop_b

    payload_size = head_list[5]
    payload_b, nRx = com.getData(payload_size)
    eop_b, nRx = com.getData(4)

    verify_eop(eop_b)

    print(f'msg tipo {head_list[0]} recebida\n')

    return head_list, payload_b, eop_b

def receive_t3(com: enlace) -> Tuple[bool, bytes, List[int]]:
    head_list = None
    payload_b = None
    try:
        head_list, payload_b, eop_b = receive_msg(com)

        if head_list[0] == 3:
            verify_eop(eop_b)
            return True, head_list, payload_b

        else:
            return False, head_list, payload_b

    except RuntimeError:
        return False, head_list, payload_b


def receive_t4(com: enlace, last_pckg_index: int) -> Tuple[bool, List[int]]:
    head_list = None
    while True:
        try:
            head_list, payload_b, eop_b = receive_msg(com)

            if head_list[0] == 4 and head_list[7] == last_pckg_index:
                return True, head_list

            else:
                return False, head_list

        except RuntimeError:
            print("erro tempo T4")
            return False, head_list


def verify_eop(eop: bytes) -> None:
    if eop != RIGHT_EOP:
        print("Erro EOP")
        raise EOPError

def crc(data) -> bytes:
    return (binascii.crc_hqx(data, 0)).to_bytes(2, 'little')


class EOPError(Exception):
    pass

