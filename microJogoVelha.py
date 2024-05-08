import machine
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
import utime

def desenha_grid(tileWidth, tileHeight, screenWidth, screenHeight, display):
    display.vline(tileWidth + 1, 1, screenHeight-2, 1) # desenha uma linha vertical x = 9 , y = 8, altura = 22, cor = 1
    display.vline(tileWidth*2 + 2, 1, screenHeight-2, 1)
    display.hline(0, tileHeight*2 + 2, screenWidth, 1)
    display.hline(0, tileHeight + 1, screenWidth, 1)
   
def desenha_x(tile_x, tile_y, tileWidth, tileHeight): # tile_x e tile_y de 0 a 2
   
    x_off = tile_x * tileWidth + tile_x
    y_off = tile_y * tileHeight + tile_y
   
    x0 = 4 + x_off
    y0 = 2 + y_off
   
    x1 = tileWidth - 5 + x_off
    y1 = tileHeight - 2 + y_off
   
    display.line(x0,y0,x1,y1,1)
    display.line(x0,y1,x1,y0,1)
    

    
   
   
def desenha_o(tile_x, tile_y, tileWidth, tileHeight): # tile_x e tile_y de 0 a 2
    x_off = tile_x * tileWidth + tile_x
    y_off = tile_y * tileHeight + tile_y
   
    x0 = 4 + x_off
    y0 = 2 + y_off
    x1 = tileWidth - 5 + x_off
    y1 = tileHeight - 2 + y_off
    xm = int((x0+x1)/2)
    ym = int((y0+y1)/2)
   
    r = int((tileHeight - 4)/2)
   
    display.ellipse(xm,ym,r,r,1)
    
def desenha_quadrado(tile_x, tile_y, tileWidth, tileHeight):
    x_off = tile_x * tileWidth + tile_x
    y_off = tile_y * tileHeight + tile_y
    
    x0 = 4 + x_off
    y0 = 2 + y_off
   
    x1 = tileWidth + x_off
    y1 = tileHeight + y_off
    
    display.rect(x0,y0,tileWidth-6,tileHeight-4,1)
   

# Define os pinos do Raspberry Pi Pico conectados ao barramento I2C 0
i2c0_slc_pin = 5
i2c0_sda_pin = 4
botao_up_pin = 6
botao_down_pin =7
botao_left_pin =8
botao_right_pin = 9
botao2_pin = 12

vol_max = 65535
buzzer = PWM(Pin(16))
buzzer.freq(1500)
#buzzer.duty_u16(vol_max//10)

tones = {
    'C0':16,
    'C#0':17,
    'D0':18,
    'D#0':19,
    'E0':21,
    'F0':22,
    'F#0':23,
    'G0':24,
    'G#0':26,
    'A0':28,
    'A#0':29,
    'B0':31,
    'C1':33,
    'C#1':35,
    'D1':37,
    'D#1':39,
    'E1':41,
    'F1':44,
    'F#1':46,
    'G1':49,
    'G#1':52,
    'A1':55,
    'A#1':58,
    'B1':62,
    'C2':65,
    'C#2':69,
    'D2':73,
    'D#2':78,
    'E2':82,
    'F2':87,
    'F#2':92,
    'G2':98,
    'G#2':104,
    'A2':110,
    'A#2':117,
    'B2':123,
    'C3':131,
    'C#3':139,
    'D3':147,
    'D#3':156,
    'E3':165,
    'F3':175,
    'F#3':185,
    'G3':196,
    'G#3':208,
    'A3':220,
    'A#3':233,
    'B3':247,
    'C4':262,
    'C#4':277,
    'D4':294,
    'D#4':311,
    'E4':330,
    'F4':349,
    'F#4':370,
    'G4':392,
    'G#4':415,
    'A4':440,
    'A#4':466,
    'B4':494,
    'C5':523,
    'C#5':554,
    'D5':587,
    'D#5':622,
    'E5':659,
    'F5':698,
    'F#5':740,
    'G5':784,
    'G#5':831,
    'A5':880,
    'A#5':932,
    'B5':988,
    'C6':1047,
    'C#6':1109,
    'D6':1175,
    'D#6':1245,
    'E6':1319,
    'F6':1397,
    'F#6':1480,
    'G6':1568,
    'G#6':1661,
    'A6':1760,
    'A#6':1865,
    'B6':1976,
    'C7':2093,
    'C#7':2217,
    'D7':2349,
    'D#7':2489,
    'E7':2637,
    'F7':2794,
    'F#7':2960,
    'G7':3136,
    'G#7':3322,
    'A7':3520,
    'A#7':3729,
    'B7':3951,
    'C8':4186,
    'C#8':4435,
    'D8':4699,
    'D#8':4978,
    'E8':5274,
    'F8':5588,
    'F#8':5920,
    'G8':6272,
    'G#8':6645,
    'A8':7040,
    'A#8':7459,
    'B8':7902,
    'C9':8372,
    'C#9':8870,
    'D9':9397,
    'D#9':9956,
    'E9':10548,
    'F9':11175,
    'F#9':11840,
    'G9':12544,
    'G#9':13290,
    'A9':14080,
    'A#9':14917,
    'B9':15804,
    'P':0
}
# song = ["D6", "P", "A5", "G5", "P", "F#5", "D5", "P", "A5", "C#6", "A5", "D6", "P", "D6"]
somVitoria = ["C7", "C6", "D6", "A6"]
somEmpate = ["D#5", "P", "D#4"]
tempo = 85
notes = 4

debounce_time_ms = 10
obstacle_state = 0
# Variável global para armazenar o estado anterior do sensor
obstacle_last_state = 0

# Habilita o uso de interrupção para o sensor
enable_irq = False

# Configura o pino da saída digital do sensor
botao_up = Pin(botao_up_pin, Pin.IN, Pin.PULL_UP)
botao_down = Pin(botao_down_pin, Pin.IN, Pin.PULL_UP)
botao_right = Pin(botao_right_pin, Pin.IN, Pin.PULL_UP)
botao_left = Pin(botao_left_pin, Pin.IN, Pin.PULL_UP)
botao2 = Pin(botao2_pin, Pin.IN, Pin.PULL_UP)

screenWidth = 128
screenHeight = 64

tileWidth = int((screenWidth - 2)/3)    # 42
tileHeight = int((screenHeight - 4)/3)  # 20

# Inicializa o I2C0 com os pinos GPIO9 (SCL) e GPIO8 (SDA)
i2c0 = I2C(0, scl=Pin(i2c0_slc_pin), sda=Pin(i2c0_sda_pin), freq=400000)

# Inicializa o display OLED I2C de 128x64
display = SSD1306_I2C(screenWidth, screenHeight, i2c0)

# Limpa o display
display.fill(0)   # preenche toda a tela com cor = 

#desenha_x(2, 1, tileWidth, tileHeight)
#desenha_x(1, 0, tileWidth, tileHeight)
#desenha_x(2, 2, tileWidth, tileHeight)

#desenha_o(0, 0, tileWidth, tileHeight)
#desenha_o(1, 1, tileWidth, tileHeight)
#desenha_o(2, 0, tileWidth, tileHeight)

#display.show()                         # escreve o conteúdo do FrameBuffer na memória do display

botao_up_anterior = 0
botao_down_anterior = 0
botao_left_anterior = 0
botao_right_anterior = 0
botao2_anterior = 0

jogador1 = True

def playtone(frequency):
    buzzer.duty_u16(vol_max // 4)
    buzzer.freq(frequency)

def playsong(mysong):
    for i in range(len(mysong)):
        if (mysong[i] == "P"):
            buzzer.duty_u16(0)
        else:
            playtone(tones[mysong[i]])
        utime.sleep(0.15)
    buzzer.duty_u16(0)

def clear_display():
    display.fill(0)
    desenha_grid(tileWidth, tileHeight, screenWidth, screenHeight, display)
    ler_jogadas()
    desenha_quadrado(x, y, tileWidth, tileHeight)
    display.show()
# Loop infinito
x=0
tempo =1500
y=0
#desenha_quadrado(x, y, tileWidth, tileHeight)
#display.show()
jogadas = [[0,0,0],[0,0,0],[0,0,0]]
contar_jogadas =0
def ler_jogadas():
    cont = 0
    for i in range (len(jogadas)):
        for j in range (len(jogadas[i])):
            if jogadas[i][j] == 1:
                desenha_x(j, i, tileWidth, tileHeight)
            elif jogadas[i][j] == 2:
                desenha_o(j, i, tileWidth, tileHeight)
    display.show()
def checar_linhas():
    for i in range(len(jogadas)):
        if jogadas[i][0] == jogadas[i][1] == jogadas[i][2] != 0:
            display.line(0,tileHeight//2 +tileHeight*i,screenWidth,tileHeight//2 +tileHeight*i,1)
            display.show()
            return jogadas[i][0]
    return 0
def checar_colunas():
    for i in range(len(jogadas)):
        if jogadas[0][i] == jogadas[1][i] == jogadas[2][i] != 0:
            display.line(tileWidth//2 +tileWidth*i ,0,tileWidth//2 +tileWidth*i,screenHeight,1)
            display.show()
            return jogadas[0][i]
    return 0
def checar_diagonais():
    if jogadas[0][0] == jogadas[2][2] == jogadas[1][1] != 0:
        display.line(0,0,screenWidth,screenHeight,1)
        display.show()
        return jogadas[0][0]
    elif jogadas[0][2] == jogadas[1][1] == jogadas[2][0] != 0:
        display.line(screenWidth,0,0,screenHeight,1)
        display.show()
        return jogadas[1][1]
    return 0

def resetar():
    utime.sleep_ms(tempo//2)
    display.fill(0)
    zeros = [[0,0,0],[0,0,0],[0,0,0]]
    global jogadas,x,y,contar_jogadas,jogador1
    jogadas = zeros
    x=0
    y=0
    contar_jogadas = 0
    jogador1 = True
    clear_display()

def ganhador():
    diag = checar_diagonais()
    lin = checar_linhas()
    col = checar_colunas()
    if lin > 0:
        utime.sleep_ms(tempo)
#         print("linhas")
        display.fill(0)
        if lin==1:
            display.text("Ganhou o X!", 16, 32)
        else:
            display.text("Ganhou o O!", 16, 32)
        display.show()
        playsong(somVitoria)
        resetar()
    
        
    elif col > 0:
        utime.sleep_ms(tempo)
        display.fill(0)
#         print("colunas")
        if col==1:
            display.text("Ganhou o X!", 16, 32)
        else:
            display.text("Ganhou o O!", 16, 32)
        display.show()
        playsong(somVitoria)
        resetar()
    
    elif diag > 0:
        utime.sleep_ms(tempo)
        display.fill(0)
#         print("diagonais")
        if diag ==1:
            display.text("Ganhou o X!", 16, 32)
        else:
            display.text("Ganhou o O!", 16, 32)
        display.show()
        playsong(somVitoria)
        resetar()
    
    elif contar_jogadas >= 9:
#         print("empate")
        display.fill(0)
        display.text("Empatou!", 16, 32)
        display.show()
        playsong(somEmpate)
        resetar()
        
#desenha_quadrado(x, y, tileWidth, tileHeight)     
clear_display()
#display.show()

while True:
    if botao_up.value() == 0 and botao_up_anterior == 1:
        
        y = y - 1
        if y < 0:
            y = 2      
        clear_display()
        
    if botao_down.value() == 0 and botao_down_anterior == 1:
# y cresce ao descer a tela
        y = y + 1
        if y > 2:
            y = 0

        clear_display()       
    if botao_left.value() == 0 and botao_left_anterior == 1:
        x = x - 1
        if x < 0:
            x = 2      
        clear_display()
        
    if botao_right.value() == 0 and botao_right_anterior == 1:
        
        x = x + 1
        if x > 2:
            x = 0
   
        clear_display()
        
    if botao2.value() == 0 and botao2_anterior == 1:    
        if jogador1 and jogadas[y][x] == 0:
            desenha_x(x,y,tileWidth,tileHeight)
            jogadas[y][x] = 1
            jogador1 = False
            contar_jogadas = contar_jogadas+1
            display.show()
            ganhador()
        elif not jogador1 and jogadas[y][x] == 0:
            desenha_o(x,y,tileWidth,tileHeight)
            jogadas[y][x] = 2
            jogador1 = True
            contar_jogadas = contar_jogadas+1
            display.show()
            ganhador()
        
        
   
        #print(jogadas)
    
    botao_up_anterior = botao_up.value()
    botao_down_anterior = botao_down.value()
    botao_left_anterior = botao_left.value()
    botao_right_anterior = botao_right.value()
    
    botao2_anterior = botao2.value()
    utime.sleep_ms(20)
    
    
