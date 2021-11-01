#importe as bibliotecas
import sys
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from suaBibSignal import signalMeu



def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def plot_func(x, y, titulo):
    limites = [0, 0.01, -1, 1]
    plt.axis(limites)
    plt.plot(x, y)
    plt.title(titulo)
    # plt.show()

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
    print("Inicializando encoder")
    
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    encoder = signalMeu()
    sample_freq = 44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    
    duration = 5 #cinco segundos 
      
    #relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3

    input_num = int(input("Digite o simbolo: "))
    print("Gerando Tons base")

    
    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 
    #use para isso sua biblioteca (cedida)
    #obtenha o vetor tempo tb.
    #deixe tudo como array
    amp = 0.3
    freqs = NUMBER_FREQ_TABLE[input_num]
    sin1_t, sin1_amp = encoder.generateSin(freqs[0], amp, duration, sample_freq)
    sin2_t, sin2_amp = encoder.generateSin(freqs[1], amp, duration, sample_freq)


    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    #nao aceite outro valor de entrada.
    print("Gerando Tom referente ao símbolo : {}".format(input_num))
    
    
    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides
    sum_signal = sin1_amp + sin2_amp
    plot_func(sin1_t, sum_signal, "Frequencias somadas no tempo")

    
    
    

    # reproduz o som
    sd.play(sum_signal, sample_freq)

    # Exibe gráficos
    #printe o grafico no tempo do sinal a ser reproduzido (duas frequências somadas)
    plot_func(sin1_t, sum_signal, "Frequencias somadas no tempo")
    plt.show()

    #printa gráfico no domínio da frequência do sinal emitido (transformada de Fourier)
    encoder.plotFFT(sum_signal, sample_freq)
    plt.show()

    # aguarda fim do audio
    sd.wait()

if __name__ == "__main__":
    main()
