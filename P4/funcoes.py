
import math
from os import close, write
import numpy as np


def cria_texto(a):
    f = open("log.txt", "a+")
    f.write(a + "\n")
    f.close()


def divide_pacotes(img):
    p = 114
    lista_payload = []

    for i in range(0, len(img), p):
        payload = img[i:i+p]
        lista_payload.append(payload)

    lista_payload_bytes = []

    for i in range(len(lista_payload)):
        lista_payload_bytes.append([])

        for char in lista_payload[i]:
            lista_payload_bytes[i].append(bytes([char]))

    return lista_payload_bytes


def cria_datagrama(payload, lista_head):
    EOP = [bytes([255]), bytes([170]), bytes([255]), bytes([170])]
    lista_head_bytes = [bytes([i]) for i in lista_head]
    datagrama = lista_head_bytes + payload + EOP

    return np.asarray(datagrama)


def cria_pacotes(lista_payload):
    lista_head = [0]*10

    lista_head[0] = 3
    lista_head[1] = Id_client
    lista_head[2] = Id_server
    lista_head[3] = len(lista_payload)

    lista_pacotes = []
    contador = 0

    for payload in lista_payload:
        lista_head[4] = contador + 1
        contador += 1
        lista_head[5] = len(payload)
        lista_pacotes.append(cria_datagrama(payload, lista_head))

    return lista_pacotes


Id_client = 10
Id_server = 5
Id_pacote = 15


def cria_handshake(numero_de_pacotes):
    lista_head = [0]*10
    lista_head[0] = 1
    lista_head[1] = Id_client
    lista_head[2] = Id_server
    lista_head[3] = numero_de_pacotes
    lista_head[4] = Id_pacote
    payload = []
    datagrama = cria_datagrama(payload, lista_head)

    return datagrama
