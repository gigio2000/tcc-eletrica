from matplotlib.animation import FuncAnimation
import csv 
import sys
from datetime import datetime, timedelta
import time 
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
import collections
import RPi.GPIO as GPIO


def acendelamp(r):
    GPIO.setmode(GPIO.BCM)
    #print("oi")
    #GPIO.setup(r, GPIO.IN)
    GPIO.setup(r, GPIO.OUT)
    GPIO.output(r, GPIO.LOW)
    #GPIO.cleanup()

def apagalamp(r):
    GPIO.setmode(GPIO.BCM)
    #print("oi2")
    #GPIO.setup(r, GPIO.IN)
    GPIO.setup(r, GPIO.OUT)
    GPIO.output(r, GPIO.HIGH)
    #GPIO.cleanup()

now = str(time.time())
func = 10
switch = 1
str_switch = "Desligado"
ultimomulti = 0
acendelamp(18)
ultimogeracao = 0
switch_off = 0
switch_on = 0
frame = 0
xplot = 0
yplot = 0
xplot_off_real = []
xplot_off_prev = []
xplot_on_real = []
xplot_on_prev = []

# function to update the data
def my_function(i):
    # get data
    global ultimogeracao
    global ultimomulti
    global func
    global switch
    global switch_off
    global switch_on
    global str_switch
    global frame
    global xplot_real
    global xplot_prev
    global yplot_real
    global xplot2_real
    global yplot2_real
    global yplot_prev
    global xplot2_prev
    global yplot2_prev
    frame += 1
    relay_ch = 18
    temport.pop(0)
    temport.append(tempoplot2[func])
    datetemport = [str(datetime.fromtimestamp(t/1e3)) for t in temport]
    #print(datetemport)
    geracaort.pop(0)
    geracaort.append(invplot[func])
    multirt.pop(0)
    cargart.pop(0)
    if switch == 1:
        apagalamp(relay_ch)
        #print(multiplot[func])
        #print(invplot[func])
        #multirt.append(0)
        multirt.append(multiplot[func])
        #cargart.append(-invplot[func])
        if multirt[-1] + geracaort [-1] < 0:
            cargart.append(0)
        else:
            cargart.append(multirt[-1] + geracaort[-1])
    if switch == 0:
        acendelamp(relay_ch)
        multirt.append(multiplot[func] + 4000)
        if multirt[-1] + geracaort [-1] < 0:
            cargart.append(0)
        else:
            cargart.append(multirt[-1] + geracaort[-1])
    #print("Switch Real " + str(switch))
    
    func += 1
    # clear axis
    """
    ax.cla()
    # plot cpu
    ax.plot(datetemport, geracaort, label = "Geração")
    ax.plot(datetemport, multirt, label = "Multimedidor")
    ax.scatter(len(geracaort)-1, geracaort[-1])
    ax.text(len(geracaort)-1, geracaort[-1], " {}W".format(geracaort[-1]))
    ax.plot(datetemport, cargart, label = "Carga")
    ax.scatter(len(cargart)-1, cargart[-1], color='green')
    ax.text(len(cargart)-1, cargart[-1], " {}W".format(cargart[-1]))
    ax.scatter(len(multirt)-1, multirt[-1], color='orange')
    ax.text(len(multirt)-1, multirt[-1], " {}W".format(multirt[-1]))
    fig.autofmt_xdate()
    ax.legend()
    """
    #global func2
    #temport2.pop(0)
    #temport2.append(tempoplot2[func2])
    #geracaort2.pop(0)
    #geracaort2.append(invplot2[func2])
    #multirt2.pop(0)
    #multirt2.append(multiplot2[func2])
    #cargart2.pop(0)
    #cargart2.append(cargaplot2[func2])
    #func2 += 1
    #print(geracaort[-5:])
    #print(multirt[-5:])
    #print(temport[-1])
    extrapolate_x = temport[-1] + 5 * 60 * 1000
    y_extrap = interp1d(temport[-5:], geracaort[-5:], fill_value='extrapolate')
    res = y_extrap(extrapolate_x)
    multi_extrapolate_x = temport[-1] + 5 * 60 * 1000
    multi_y_extrap = interp1d(temport[-5:], multirt[-5:], fill_value='extrapolate')
    multi_res = multi_y_extrap(multi_extrapolate_x)
    #print(multi_res) 
    geracaort2.pop(0)
    multirt2.pop(0)
    cargart2.pop(0)
    if res < 0:
        geracaort2.append(0)
        multirt2.append(multi_res)
        cargart2.append(0)
    if res >= 70000:
        geracaort2.append(70000)
        multirt2.append(multi_res)
        cargart2.append(multi_res + 70000)
    if res >= 0 and res < 70000: 
        geracaort2.append(res)
        multirt2.append(multi_res)
        cargart2.append(multi_res + res)
    #cargart2.pop(0)
    #cargart2.append(multi_res - res)
    sidx = 2
    datetemport2 = [str(datetime.fromtimestamp(t/1e3)+ timedelta(minutes=5))   for t in temport]
    if multi_res >= geracaort2[-1]:
        switch_off += 1
        switch_on = 0
        if switch_off == sidx:
            xplot_off_real.append(datetemport[-1])
            xplot_off_prev.append(datetemport2[-1])
        if switch_off >= sidx:
            switch = 1
            str_switch = "Desligado"

        #ultimomulti = multi_res
        #ultimogeracao = geracaort2[-1]
    if multi_res < geracaort2[-1]:
        switch_on += 1
        switch_off = 0
        if switch_on == sidx:
            xplot_on_real.append(datetemport[-1])
            xplot_on_prev.append(datetemport2[-1])
        if switch_on >= sidx:
            switch = 0
            str_switch = "Ligado"
        #ultimogeracao = res
    """
    ax2.cla()
    
    ax2.plot(datetemport2, geracaort2, label = "Previsão Geração")
    ax2.scatter(len(geracaort2)-1, geracaort2[-1])
    ax2.text(len(geracaort2)-1, geracaort2[-1], " {}W".format(geracaort2[-1]))
    ax2.plot(datetemport2, multirt2, label = "Previsão Multimedidor")
    ax2.plot(datetemport2, cargart2, label = "Carga Prevista")
    ax2.scatter(len(cargart2)-1, cargart2[-1], color='green')
    ax2.text(len(cargart2)-1, cargart2[-1], " {}W".format(cargart2[-1]))
    ax2.scatter(len(multirt2)-1, multirt2[-1], color='orange')
    ax2.text(len(multirt2)-1, multirt2[-1], " {}W".format(multirt2[-1]))
    fig.autofmt_xdate()
    ax2.legend( )
    """
    temporealplot.append(datetemport[-1])
    geracaorealplot.append(geracaort[-1])
    cargarealplot.append(cargart[-1])
    multirealplot.append(multirt[-1])
    
    tempoprevplot.append(datetemport2[-1])
    geracaoprevplot.append(geracaort2[-1])
    cargaprevplot.append(cargart2[-1])
    multiprevplot.append(multirt2[-1])
    """
    print("===============DEBUG===============")
    print("")
    print("Frame: " + str(frame))
    print("")
    print("Tempo Date Excel: " + str(tempoplot[func -1]))
    print("Tempo Unix Excel: " + str(tempoplot2[func -1]))
    print("Geração Excel: " + str(invplot[func -1]))
    print("Multimedidor Excel: " + str(multiplot[func -1]))
    print("Carga Excel: " + str(cargaplot[func -1]))
    print("")
    print("Tempo Date Plot: " + str(datetemport[-1]))
    print("Tempo Unix Plot: " + str(temport[-1]))
    print("Geração Plot: " + str(geracaort[-1]))
    print("Multimedidor Plot: " + str(multirt[-1]))
    print("Carga Plot: " + str(cargart[-1]))
    print("")
    print("Variaveis_Y Extrap Geração: " + str(geracaort[-5:]))
    print("Variaveis_X Extrap Geração: " + str(temport[-5:]))
    print("Resultado Extrap X+5min Geração: " + str(res))
    print("Variaveis_Y Extrap Multi: " + str(multirt[-5:]))
    print("Variaveis_X Extrap Multi: " + str(temport[-5:]))
    print("Resultado Extrap X+5min Multi: " + str(multi_res))
    print("Calculo Carga: " + str(multi_res) + " - " + str(res) + " = " + str(multi_res - res))
    print("")
    print("Tempo +5min: " + str(datetemport2[-1]))
    print("Geração Previsão: " + str(geracaort2[-1]))
    print("Multimedidor Previsão: " + str(multirt2[-1]))
    print("Carga Previsão: " + str(cargart2[-1]))
    print("")
    #print("Switch ligado quando Previsão de Geração Maior que ultima potência do Multimedidor com Carga Desligada")
    #print("Geração Previsão: " + str(res))
    #print("Ultima Previsão Multimedidor com Carga Desligada: " + str(ultimomulti))
    #print("")
    #print("Switch desligado quando Previsão de Geração Menor que Previsão Multimedidor")
    #print("Ultima Geração Previsão com Carga Ligada: " + str(ultimogeracao))
    #print("Multimedidor Previsão: " + str(multirt2[-1]))
    #print("")
    print("Switch_On index: " + str(switch_on))
    print("Switch_Off index: " + str(switch_off))
    print("Switch: " + str_switch)
    print("Potência Cargas Controláveis: " + str(cargart[-1] - cargaplot[func -1]))
    print("")
    """
    original_stdout = sys.stdout
    with open('log'+ now + '.txt', 'a+') as f:
        sys.stdout = f
        print("===============DEBUG===============")
        print("")
        print("Frame: " + str(frame))
        print("")
        print("Tempo Date Excel: " + str(tempoplot[func -1]))
        print("Tempo Unix Excel: " + str(tempoplot2[func -1]))
        print("Geração Excel: " + str(invplot[func -1]))
        print("Multimedidor Excel: " + str(multiplot[func -1]))
        print("Carga Excel: " + str(cargaplot[func -1]))
        print("")
        print("Tempo Date Plot: " + str(datetemport[-1]))
        print("Tempo Unix Plot: " + str(temport[-1]))
        print("Geração Plot: " + str(geracaort[-1]))
        print("Multimedidor Plot: " + str(multirt[-1]))
        print("Carga Plot: " + str(cargart[-1]))
        print("")
        print("Variaveis_Y Extrap Geração: " + str(geracaort[-5:]))
        print("Variaveis_X Extrap Geração: " + str(temport[-5:]))
        print("Resultado Extrap X+5min Geração: " + str(res))
        print("Variaveis_Y Extrap Multi: " + str(multirt[-5:]))
        print("Variaveis_X Extrap Multi: " + str(temport[-5:]))
        print("Resultado Extrap X+5min Multi: " + str(multi_res))
        print("Calculo Carga: " + str(multi_res) + " - " + str(res) + " = " + str(multi_res - res))
        print("")
        print("Tempo +5min: " + str(datetemport2[-1]))
        print("Geração Previsão: " + str(geracaort2[-1]))
        print("Multimedidor Previsão: " + str(multirt2[-1]))
        print("Carga Previsão: " + str(cargart2[-1]))
        print("")
        """
        print("Switch ligado quando Previsão de Geração Maior que ultima potência do Multimedidor com Carga Desligada")
        print("Geração Previsão: " + str(res))
        print("Ultima Previsão Multimedidor com Carga Desligada: " + str(ultimomulti))
        print("")
        print("Switch desligado quando Previsão de Geração Menor que Previsão Multimedidor")
        print("Ultima Geração Previsão: " + str(ultimogeracao))
        print("Multimedidor Previsão: " + str(multirt2[-1]))
        print("")
        """
        print("Switch_On index: " + str(switch_on))
        print("Switch_Off index: " + str(switch_off))
        print("Switch: " + str_switch)
        print("Potência Cargas Controláveis: " + str(cargart[-1] - cargaplot[func -1]))
        print("")
        
        sys.stdout = original_stdout
    if frame == 42:
        yplot_prev = cargart2[-1]
        xplot_prev = datetemport2[-1]
        yplot_real = cargart[-1]
        xplot_real = datetemport[-1]
    if frame == 164:
        yplot2_prev = cargart2[-1]
        xplot2_prev = datetemport2[-1]
        yplot2_real = cargart[-1]
        xplot2_real = datetemport[-1]


    if frame == 278:

        plt.close()
        
        f1 = plt.figure(1)
        ax3 = plt.axes()
        plt.plot(temporealplot, geracaorealplot, label = "Geração")
        plt.plot(temporealplot, multirealplot, label = "Multimedidor")
        plt.plot(temporealplot, cargarealplot, label = "Carga")
        plt.ylabel('Potência (W)')
        plt.title('Curvas Reais do Sistema Fotovoltaico do DELT com carga controlavel teorica de 4kW')
        ax3.set_xticks(ax3.get_xticks()[::24])
        ax3.annotate("(" + str(xplot_real) + "," + str(yplot_real) + ")", xy=(xplot_real,yplot_real), xytext=(xplot_real,15000 ), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05))
        ax3.annotate("(" + str(xplot2_real) + "," + str(yplot2_real) + ")", xy=(xplot2_real,yplot2_real), xytext=(xplot2_real,15000 ), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05))
        plt.axvspan(xplot_on_real[0], xplot_on_real[0], color='green', alpha=0.5)
        plt.axvspan(xplot_off_real[-2], xplot_off_real[-2], color='red', alpha=0.5)
        plt.gcf().autofmt_xdate()
        plt.legend()
        plt.show()



        f2 = plt.figure(2)
        ax4 = plt.axes()
        #plt.plot(temporealplot, geracaorealplot, label = "Geração")
        #plt.plot(temporealplot, multirealplot, label = "Multimedidor")
        #plt.plot(temporealplot, cargarealplot, label = "Carga")
        plt.plot(tempoprevplot, geracaoprevplot, label = "Geração Prevista")
        plt.plot(tempoprevplot, multiprevplot, label = "Multimedidor Prevista")
        plt.plot(tempoprevplot, cargaprevplot, label = "Carga Prevista")
        for carga in cargaprevplot:
            idx = cargaprevplot.index(carga)
            if carga == 0:
                print(idx)
        print(cargaprevplot)
        plt.ylabel('Potência (W)')
        plt.title('Curvas Previstas 5 minutos no futuro com gerenciamento da carga controláve teorica de 4kW')
        #plt.title('Curvas Reais com carga controlável teórica de 4kW adicionada')
        ax4.set_xticks(ax4.get_xticks()[::24])
        ax4.annotate("(" + str(xplot_prev) + "," + str(yplot_prev) + ")", xy=(xplot_prev,yplot_prev), xytext=(xplot_prev,15000 ), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05))
        ax4.annotate("(" + str(xplot2_prev) + "," + str(yplot2_prev) + ")", xy=(xplot2_prev,yplot2_prev), xytext=(xplot2_prev,15000 ), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05))
        plt.axvspan(xplot_off_prev[-2], xplot_off_prev[-2], color='red', alpha=0.5)
        plt.axvspan(xplot_on_prev[0], xplot_on_prev[0], color='green', alpha=0.5)
        plt.gcf().autofmt_xdate()
        plt.legend()

        plt.show()
        negmultirealplot = []
        for t in multirealplot:
            if t < 0:
                negmultirealplot.append(t)
            else:
                negmultirealplot.append(0)
        
        f3 = plt.figure(3)
        ax5 = plt.axes()
        #plt.plot(temporealplot, geracaorealplot, label = "Geração")
        #plt.plot(temporealplot, multirealplot, label = "Multimedidor")
        #plt.plot(temporealplot, cargarealplot, label = "Carga")
        #plt.plot(tempoprevplot, geracaoprevplot, label = "Geração Prevista")
        #plt.plot(tempoprevplot, multiprevplot, label = "Multimedidor Prevista")
        plt.bar(temporealplot, negmultirealplot, label = "Potência Exportada")
        plt.ylabel('Potência (W)')
        plt.title('Multimedidor com gerenciamento de carga')
        #plt.title('Curvas Reais com carga controlável teórica de 4kW adicionada')
        ax5.set_xticks(ax5.get_xticks()[::24])
        #ax5.annotate("(" + str(xplot_prev) + "," + str(yplot_prev) + ")", xy=(xplot_prev,yplot_prev), xytext=(xplot_prev,5000 ), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05))
        ax5.annotate("(2023-05-14 12:05:00, -42991.87)", xy=("2023-05-14 12:05:00" ,-42991.87), xytext=("2023-05-14 15:00:00", -43000 ), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05))
        #ax5.annotate("(" + str(xplot2_prev) + "," + str(yplot2_prev) + ")", xy=(xplot2_prev,yplot2_prev), xytext=(xplot2_prev,8500 ), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05))
        #plt.axvspan(xplot_off_prev[-2], xplot_off_prev[-2], color='red', alpha=0.5)
        #plt.axvspan(xplot_on_prev[0], xplot_on_prev[0], color='green', alpha=0.5)
        plt.gcf().autofmt_xdate()
        plt.legend()
        energia = 0
        for t in multirealplot:
            if t < 0:
                energia = energia + t*(5/60)
        print(energia)
        plt.show()



        


geracao = "geracao5min2.csv"
multi = "carga5min2.csv"
#prev = "prev_carga5min.csv"

linhas = []
linhas_merge = []

csvfile = open(geracao, 'r')
csvfile2 = open(multi, 'r')

csvreader = csv.reader(csvfile2, quoting=csv.QUOTE_NONNUMERIC)
csvreader2 = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)

for linha in csvreader:
    linhas.append(linha[0])
    linhas_merge.append(linha)

for linha2 in csvreader2:
    if linha2[0] in linhas:
        idx = linhas.index(linha2[0]) 
        linhas_merge[idx].append(linha2[1])

for linha3 in linhas_merge:
    num = len(linha3)
    unix = int(linha3[0])
    linha3[0] = unix
    if num < 3:
        linha3.append(0)
    med = linha3[1]
    inv = linha3[2]
    linha3[1] = inv
    linha3[2] = med

for linha4 in linhas_merge:
    carga = linha4[2] + linha4[1]
    linha4.append(carga)

for linha5 in linhas_merge:
    num = len(linha5)
    if num < 4:
        linha5.append(0)

inv_x = []
inv_y = []
inv_i = 0

for linha5 in linhas_merge:
    if inv_i < 5: 
        inv = linha5[1]
        tempo = linha5[0]
        inv_x.append(tempo)
        inv_y.append(inv)
        inv_i += 1
        tempo_excel = tempo - 5 * 60 * 1000
        if tempo_excel in linhas:
            idx = linhas.index(tempo_excel)
            linhas_merge[idx].append(inv)
    else:
        inv = linha5[1]
        tempo = linha5[0]
        inv_x.append(tempo)
        inv_y.append(inv)
        extrapolate_x = tempo + 5 * 60 * 1000
        y_extrap = interp1d(inv_x[-5:],inv_y[-5:], fill_value='extrapolate')
        res = y_extrap(extrapolate_x)
        tempo_excel = tempo - 5 * 60 * 1000
        if tempo_excel in linhas:
            idx = linhas.index(tempo_excel)
            if res < 0:
                linhas_merge[idx].append(0)
            if res > 70000:
                linhas_merge[idx].append(70000) 
            else:
                linhas_merge[idx].append(res)

for linha5 in linhas_merge:
    num = len(linha5)
    if num < 5:
        linha5.append(0)


multi_x = []
multi_y = []
multi_i = 0

for linha5 in linhas_merge:
    if multi_i < 5: 
        multi = linha5[2]
        tempo = linha5[0]
        multi_x.append(tempo)
        multi_y.append(multi)
        multi_i += 1
        tempo_excel = tempo - 5 * 60 * 1000
        if tempo_excel in linhas:
            idx = linhas.index(tempo_excel)
            linhas_merge[idx].append(multi)
    else:
        inv = linha5[2]
        tempo = linha5[0]
        multi_x.append(tempo)
        multi_y.append(inv)
        extrapolate_x = tempo + 5 * 60 * 1000
        y_extrap = interp1d(multi_x[-5:],multi_y[-5:], fill_value='extrapolate')
        res = y_extrap(extrapolate_x)
        tempo_excel = tempo - 5 * 60 * 1000
        if tempo_excel in linhas:
            idx = linhas.index(tempo_excel)
            linhas_merge[idx].append(res)

for linha5 in linhas_merge:
    num = len(linha5)
    if num < 6:
        linha5.append(0)

for linha4 in linhas_merge:
    print(linha4)
    carga = linha4[5] + linha4[4]
    linha4.append(carga)


tempoplot = []
tempoplot2 = []
invplot = []
invplot2 = []
multiplot = []
multiplot2 = []
cargaplot = []
cargaplot2 = []

for linhaplot in linhas_merge:
    #tempoplot2.append(linhaplot[0])
    tempoplot.append(str(datetime.fromtimestamp(linhaplot[0]/1e3)))
    tempoplot2.append(linhaplot[0])
    invplot.append(linhaplot[1])
    invplot2.append(linhaplot[4])
    multiplot.append(linhaplot[2])
    multiplot2.append(linhaplot[5])
    cargaplot.append(linhaplot[3])
    cargaplot2.append(linhaplot[6])

carga = 0 
temporealplot = [str(datetime.fromtimestamp(1684022400)), str(datetime.fromtimestamp(1684022700)), str(datetime.fromtimestamp(1684023000)), str(datetime.fromtimestamp(1684023300)), str(datetime.fromtimestamp(1684023600)), str(datetime.fromtimestamp(1684023900)), str(datetime.fromtimestamp(1684024200)), str(datetime.fromtimestamp(1684024500)), str(datetime.fromtimestamp(1684024800)), str(datetime.fromtimestamp(1684025100))]
tempoprevplot = [str(datetime.fromtimestamp(1684022700)), str(datetime.fromtimestamp(1684023000)), str(datetime.fromtimestamp(1684023300)), str(datetime.fromtimestamp(1684023600)), str(datetime.fromtimestamp(1684023900)), str(datetime.fromtimestamp(1684024200)), str(datetime.fromtimestamp(1684024500)), str(datetime.fromtimestamp(1684024800)), str(datetime.fromtimestamp(1684025100)), str(datetime.fromtimestamp(1684025400))]
geracaorealplot = invplot[0:10]
geracaoprevplot = [0,0,0,0,0,0,0,0,0,0]
cargarealplot = [cargaplot[0] +carga,cargaplot[1] +carga,cargaplot[2] +carga,cargaplot[3] +carga,cargaplot[4] +carga,cargaplot[5] +carga,cargaplot[6] +carga,cargaplot[7] +carga,cargaplot[8] +carga,cargaplot[9] +carga]
cargaprevplot = [cargaplot2[0] +carga,cargaplot2[1] +carga,cargaplot2[2] +carga,cargaplot2[3] +carga,cargaplot2[4] +carga,cargaplot2[5] +carga,cargaplot2[6] +carga,cargaplot2[7] +carga,cargaplot2[8] +carga,cargaplot2[9] +carga]
#multirealplot = multiplot[0:10]
multirealplot = [multiplot[0] +carga,multiplot[1] +carga,multiplot[2] +carga,multiplot[3] +carga,multiplot[4] +carga,multiplot[5] +carga,multiplot[6] +carga,multiplot[7] +carga,multiplot[8] +carga,multiplot[9] +carga]
multiprevplot = [multiplot2[0] +carga,multiplot2[1] +carga,multiplot2[2] +carga,multiplot2[3] +carga,multiplot2[4] +carga,multiplot2[5] +carga,multiplot2[6] +carga,multiplot2[7] +carga,multiplot2[8] +carga,multiplot2[9] +carga]




"""
f1 = plt.figure(1)
ax = plt.axes()
plt.plot(tempoplot, invplot, label = "Previsão Geração")
plt.plot(tempoplot, multiplot, label = "Previsão Multimedidor")
plt.plot(tempoplot, cargaplot, label = "Carga Prevista")
plt.ylabel('Potência (W)')
ax.set_xticks(ax.get_xticks()[::24])
plt.gcf().autofmt_xdate()
plt.legend()

plt.show()
"""

geracaort2 = invplot2[0:9] 
geracaort = invplot[0:9] 
cargart2 = cargaplot2[0:9]
cargart = cargaplot[0:9]
multirt2 = multiplot2[0:9]
multirt = multiplot[0:9]
#multirt = [4000,4000,4000,4000,4000,4000,4000,4000,4000]
temport2 = tempoplot2[0:9]
temport = tempoplot2[0:9]
datetemport = []
datetemport2 = []


#fig, (ax, ax2) = plt.subplots(2, 1)
fig = plt.figure(1)
ax = plt.subplot(121)
#fig2 = plt.figure(2)
ax2 = plt.subplot(122)

#fig.autofmt_xdate()
#fig.legend()

ani = FuncAnimation(fig, my_function, interval=0)
#ani2 = FuncAnimation(fig2, my_function2, interval=1000)
plt.show()


with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(linhas_merge)
"""
while True:    
    for linha in linhas_merge: 
        data = datetime.fromtimestamp(linha[0]/1e3)
        print(data)
        print("Potência Gerada Inversor Delt: " + str(linha[1]) + " W")
        print("Leitura Multimedidor PK: " + str(linha[2]) + " W")
        print("Carga do PK: " + str(linha[3]) + " W")
        print("Potência Gerada esperada 5 minutos no futuro: " + str(linha[5]) + " W")
        print("Leitura Multimedidor PK esperada 5 minutos no futuro: " + str(linha[4]) + " W")
        print("Carga do PK esperada 5 minutos no futuro: " + str(linha[6]) + " W")
        print("")
        time.sleep(1)
"""
        

