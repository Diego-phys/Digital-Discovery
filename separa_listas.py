# El archivo de texto CLK (prueba) contiene dos columnas; la primera con un reloj y la segunda un reset que está activo
# durante 4 bits.
from bitstring import BitArray

input = open('entrada.txt', 'r')  # Abre el documento de texto en modo lectura ('r')
headlines = open('Headlines.txt', 'r')  # Abre el documento de texto con los nombres de las salidas en modo lectura
CLKA = []  # Definición de las variables tipo lista donde se van a guardar los datos
CLKA_test = []
ARESET = []
ALOAD = []
BinC1 = []  # MSB
BinC2 = []
BinC3 = []
BinC4 = []  # LSB
lines_input = input.readlines()  # Guardado de las líneas del documento en una variable
lines_hd = headlines.readlines()

# El siguiente bucle for corre a lo largo de dos índices; i selecciona la posición del dígito binario dentro de cada
# fila del documento, mientras que y selecciona cada una de las filas.
for i in range(8):
    for y in lines_input:
        if i == 0:
            ARESET.append(y[i])  # Se añaden los dígitos binarios de la posición correspondiente del documento
        elif i == 1:
            CLKA.append(y[i])
        elif i == 2:
            CLKA_test.append(y[i])
        elif i == 3:
            ALOAD.append(y[i])
        elif i == 4:
            BinC1.append(y[i])
        elif i == 5:
            BinC2.append(y[i])
        elif i == 6:
            BinC3.append(y[i])
        elif i == 7:
            BinC4.append(y[i])

#  for k in range(len(BinC1)):  # Bucle para juntar dos bits en la misma posición de la lista
#      BinC1[k] += BinC2[k]

# BinC = BinC1
# for j in range(len(BinC)):
#     BinC[j] = BitArray(bin=BinC[j])
#     BinC[j] = int(BinC[j].bin)

# Paso de las entradas en formato texto a dígitos binarios en formato número entero
for k in range(len(CLKA)):
    CLKA[k] = BitArray(bin=CLKA[k])
    CLKA[k] = int(CLKA[k].bin)

for k in range(len(CLKA)):
    CLKA_test[k] = BitArray(bin=CLKA_test[k])
    CLKA_test[k] = int(CLKA_test[k].bin)

for k in range(len(CLKA)):
    ARESET[k] = BitArray(bin=ARESET[k])
    ARESET[k] = int(ARESET[k].bin)

for k in range(len(CLKA)):
    ALOAD[k] = BitArray(bin=ALOAD[k])
    ALOAD[k] = int(ALOAD[k].bin)

for k in range(len(BinC1)):
    BinC1[k] = BitArray(bin=BinC1[k])
    BinC1[k] = int(BinC1[k].bin)

for k in range(len(BinC2)):
    BinC2[k] = BitArray(bin=BinC2[k])
    BinC2[k] = int(BinC2[k].bin)

for k in range(len(BinC2)):
    BinC3[k] = BitArray(bin=BinC3[k])
    BinC3[k] = int(BinC3[k].bin)

for k in range(len(BinC2)):
    BinC4[k] = BitArray(bin=BinC4[k])
    BinC4[k] = int(BinC4[k].bin)

data = [ARESET, CLKA, CLKA_test, ALOAD, BinC1, BinC2, BinC3, BinC4]
# Finalmente se imprimen las listas resultantes

print(data)
