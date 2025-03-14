# El archivo de texto CLK (prueba) contiene dos columnas; la primera con un reloj y la segunda un reset que está activo
# durante 4 bits.
from bitstring import BitArray

clk_in = open('entrada_single.txt', 'r')  # Abre el documento de texto en modo lectura ('r')
CLKA = []  # Definición de las variables tipo lista donde se van a guardar los datos
lines = clk_in.readlines()  # Guardado de las líneas del documento en una variable

# El siguiente bucle for corre a lo largo de dos índices; i selecciona la posición del dígito binario dentro de cada
# fila del documento, mientras que y selecciona cada una de las filas.
for i in range(1):
    for y in lines:
        if i == 0:
            CLKA.append(y[i])  # Se añaden los dígitos binarios de la posición correspondiente del documento

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


data = CLKA
# Finalmente se imprimen las listas resultantes

print(data)
