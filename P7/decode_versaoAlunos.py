#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from suaBibSignal import signalMeu
import time
import peakutils as pk

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def plot_func(x, y, titulo):
    limites = [0, 3, -1, 1]
    plt.axis(limites)
    plt.plot(x, y)
    plt.title(titulo)
    plt.show()

NUMBER_FREQ_TABLE = {
    0 : (1336, 941),
    1 : (1209, 697),
    2 : (1336, 697),
    3 : (1477, 697),
    4 : (1209, 770),
    5 : (1336, 770),
    6 : (1477, 770),
    7 : (1209, 852),
    8 : (1336, 852),
    9 : (1477, 852)    
}


def main():
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    signal = signalMeu()
    freqDeAmostragem = 44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = 44100 #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = 3 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    print("captacao comeca em 2 segundos")
    time.sleep(2)

   
    #faca um print informando que a gravacao foi inicializada
    print("iniciando gravacao")
   
    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = duration * freqDeAmostragem
   
    sd.default.device = 1
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    dados = np.array([i[0] for i in audio])

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(0,duration,numAmostras)

    # plot do gravico  áudio vs tempo!
    plot_func(t, dados, "Audio vs tempo")
    plt.show()
    
   
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, freqDeAmostragem)
    # plt.figure("F(y)")
    limites = [600, 1600, 0, 10000]
    plt.axis(limites)
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    plt.show()
    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    index = pk.peak.indexes(yf, thres=0.3, min_dist=50,)

    # if len(index) > 2:
        # print("mais que duas frequencias encontradas")
        # return

    #printe os picos encontrados! 
    print(index)

    freqs = []
    h = []
    for i in index:
        foo = int(round(xf[i]))
        h.append(int(yf[i]))
        freqs.append(foo)
        print(f"Frequencias de pico: {foo}, {round(yf[i])}")
    

    largest = max(h)
    largest_index = h.index(largest)
    print(h)
    h_copy = h.copy()
    h_copy.remove(largest)
    print(h_copy)
    second = max(h_copy)
    second_index = h.index(second)

    two_freq = [freqs[largest_index], freqs[second_index]]

    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    tecla = 0

    for key in NUMBER_FREQ_TABLE:
        if two_freq[0] in NUMBER_FREQ_TABLE[key] and two_freq[1] in NUMBER_FREQ_TABLE[key]:
            tecla = key
            break

    #print a tecla.
    print(f"A tecla pressionada foi: {tecla}")
  
    ## Exibe gráficos
    

if __name__ == "__main__":
    main()
