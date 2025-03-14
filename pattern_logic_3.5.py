"""
------------------------------------------------------------------------------------------------------------------------
                        Código hecho por: DIEGO JOSÉ CARRETIÉ SÁNCHEZ-ARJONA
                                Última modificación: 21/06/2023
------------------------------------------------------------------------------------------------------------------------
La finalidad de este programa es la generación de señales con el Digital Discovery (DD) con objeto de enviarlas a un
circuito, recoger la salida y guardarla en un archivo .txt. También representa las señales de salida en caso deseado.
Para ejecutar correctamente el programa deben seguirse los siguientes pasos:
- Las señales personalizadas deben primero pasarse al formato requerido mediante el código "separa_listas.py".
- Importar la lista con los datos de los patrones obtenida mediante "separa_listas.py".
- Importar la variable con los encabezados de las señales si se quieren representar.
- Modificar si es necesario el directorio de guardado de los datos de salida (variable "datafile_path").
- El código preguntará siempre por el trigger. El resto de parámetros pueden modificarse a mano o hacer que el código
  pregunte por ellos activando el modo "manual". Si se pretenden hacer varias pruebas, se recomienda desactivar el modo
  manual y escribir los parámetros relevantes en el propio código.
- Seguir siempre el formato requerido en función del tipo de variable de Python. Por ejemplo, las variables DIO y DIN
  son diccionarios, por lo que si se modifican las entradas deben ingresarse con el formato 'i': j, donde i es un número
  natural empezando por el 1 y j es la etiqueta del pin correspondiente en el DD.
- IMPORTANTE. Ingresar la información de los pins en el mismo orden en el que aparecen las señales correspondientes
  en el documento de texto importado.
- El modo "plot" activa o desactiva la representación de las señales de salida.
- El modo "compare" activa o desactiva la comparación de los patrones de salida frente a un archivo de simulación que
  debe abrirse en una variable aparte en el código.
El programa no funciona si se tiene abierto el software WaveForms. Al ejecutarlo, tras unos segundos aparecerá la
representación de la señal generada. El programa no finalizará hasta que se pare manualmente o se cierre la gráfica.
Si el modo representación está desactivado, el programa finalizará tras generar el documento .txt o comparar.
"""

from WF_SDK import device, logic, pattern, supplies, error   # Instrumentos de la SDK para comunicarse con el DD
from WF_SDK.pattern import idle_state  # Algunas clases relevantes
import matplotlib.pyplot as plt   # Para representar
from time import sleep            # Para los retardos
import numpy as np  # Para guardar la salida con el mismo formato que la entrada
from separa_listas import data  # Lista de listas con los patrones para la entrada en el formato requerido
from separa_listas import lines_hd  # Lista con los nombres de las señales de salida
"""-----------------------------------------------------------------------"""

# Variables del código (NO TOCAR)
inputs = len(data)  # Número de señales de entrada al circuito
ni = 1  # Contador
no = 1  # Contador
buffer_out = []  # Lista de listas que contendrá los datos de salida del circuito
fmt = []  # Lista con el formato de los datos de salida (un valor por señal de salida o columna)

""" PARÁMETROS MODIFICABLES DEL CÓDIGO. 
    Asegurarse especialmente de que los números de los pines DIO/DIN, la tensión, la frecuencia de las señales, la 
    frecuencia de lectura, el buffer y el directorio de guardado son correctos. 
"""
manual = False  # Booleano que controla la entrada de información al programa. True para ingresar la información
# manualmente durante la ejecución del código, False para ingresarla modificando el código antes de ejecutarlo
plot = True  # Booleano que controla la representación de los datos a la salida. False para no hacer la representación.
# Se recomienda representar solo si el número de señales a la salida no es muy grande
compare = True  # Booleano que controla la comparación de los datos de salida con un archivo de simulación del
# circuito. Requiere de un trigger. Dejar en False si no se quiere realizar dicha comparación.
rising_edge_int = 0  # Criterio para comparación (1 subida, 0 bajada)
trigger_signal = 0  # Señal de referencia para comparar en el archivo de salida
sim_trigger_signal = 0  # Señal de referencia para comparar en el archivo de simulación

# Entradas en orden:
# Trigger:
# Números de los pines que mandan las señales
DIO = {}
outputs = 1  # Número de señales de salida
# Salidas en orden:
DIN = {}
# Tensión de la señal. Debe estar entre 1.2 y 3.3 V
voltage = 3.3
# Frecuencia de las señales en Hz (para señales personalizadas marcan la duración de los bits)
# Máxima frecuencia es 100 MHz
frequency = 10000
SF = 0.5 * frequency  # Frecuencia de lectura en Hz. Máximo 800 MHz
wait = 0  # Tiempo de espera en segundos
buffer = int(len(data[0]) * SF / frequency)  # Número de patrones
max_buffer = buffer  # Tamaño máximo del buffer de salida
run_time = "auto"  # Duración de las señales en segundos. "auto" calcula el tiempo necesario para mandar la señal
# completa, 0 es infinito
repeat = 0  # Número de repeticiones. 0 es infinito
# Directorio donde guardar los datos de salida
datafile_path = "/Users/soto/Desktop/DIEGO/DIGILENT DIGITAL/Python/WF/datafile.txt"

# En el siguiente bloque de código se ingresa la información relevante en caso de que manual sea True. NO TOCAR
if manual:
    outputs = int(input("Número de salidas del circuito "))  # Número de señales de salida
    while ni <= inputs:
        x = int(input("Número del DIO "))
        DIO[f"{ni}"] = x
        ni += 1

    while no <= outputs:
        y = int(input("Número del DIN "))
        DIN[f"{no}"] = y
        no += 1

    frequency = int(float(input("Frecuencia de las señales ")))
    SF = int(float(input("Frecuencia de muestreo ")))
    wait = float(input("Tiempo de espera "))
    repeat = int(input("Número de repeticiones (0 para infinito) "))
    buffer = int(float(input("Número de muestras (1 para predeterminado, 0 para el máximo posible) ")))
    if buffer == 1:
        buffer = int(len(data[0]) * SF / frequency)  # Número predeterminado de muestras
        run_time = buffer / SF + wait
    else:
        run_time = int(input("Duración (0 para infinito, 'auto' para duración completa de la señal) "))

enable = bool(int(input("Activar (1) o desactivar (0) el trigger ")))  # Activación del trigger
if enable:
    channel = int(input("Número del DIO/DIN usado como fuente del trigger "))  # Canal de referencia para el trigger
    rising_edge = bool(int(input("Establecer el criterio del trigger. 1 para subida, 0 para bajada ")))  # Condición

# Realización del test. NO TOCAR salvo que se indique lo contrario
try:
    # Conectar al dispositivo.
    device_name = "Digital Discovery"
    device_data = device.open()
    device_data.name = device_name

    """---------------------------------------------"""
    # Establecer la tensión.
    supplies_data = supplies.data()
    supplies_data.master_state = True
    voltage = max(1.2, min(3.3, voltage))
    supplies_data.voltage = voltage
    supplies.switch(device_data, supplies_data)

    """---------------------------------------------"""
    # Inicializar el analizador lógico
    logic.open(device_data, sampling_frequency=SF, buffer_size=buffer)
    """
            initialize the logic analyzer

            parameters: - device data
                        - sampling frequency in Hz, default is 100MHz
                        - buffer size, default is 0 (maximum)
        """

    # Establecer el trigger
    if enable:
        logic.trigger(device_data, enable=enable, channel=channel, rising_edge=rising_edge)

    """
            set up triggering

            parameters: - device data
                        - enable - True or False to enable, or disable triggering
                        - channel - the selected DIO line number to use as trigger source
                        - position - prefill size, the default is 0
                        - timeout - auto trigger time, the default is 0
                        - rising_edge - set True for rising edge, False for falling edge, the default is rising edge
                        - length_min - trigger sequence minimum time in seconds, the default is 0
                        - length_max - trigger sequence maximum time in seconds, the default is 20
                        - count - instance count, the default is 0 (immediate)
        """

    # Generar la señal en canales DIO
    for k in range(1, len(data)+1):
        pattern.generate(device_data, channel=DIO[str(k)], function=pattern.function.custom,
                         frequency=frequency, data=data[k - 1], wait=wait, repeat=repeat,
                         run_time=run_time, idle=idle_state.initial, trigger_enabled=True)

    """
            generate a logic signal

            parameters: - channel - the selected DIO line number
                        - function - possible: pulse, custom, random
                        - frequency in Hz
                        - duty cycle in percentage, used only if function = pulse, default is 50%
                        - data list, used only if function = custom, default is empty
                        - wait time in seconds, default is 0 seconds
                        - repeat count, default is infinite (0)
                        - run_time: in seconds, 0=infinite, "auto"=auto
                        - idle - possible: initial, high, low, high_impedance, default = initial
                        - trigger_enabled - include/exclude trigger from repeat cycle
                        - trigger_source - possible: none, analog, digital, external[1-4]
                        - trigger_edge_rising - True means rising, False means falling, None means either, default is 
                          rising
        """

    sleep(1)    # Esperar 1 segundo

    # Grabar las señales lógicas de la salida
    for k in range(outputs):
        buffer_out.append(logic.record(device_data, channel=DIN[str(k+1)]))
        fmt.append("%d")

    # Limitar el tamaño de los datos mostrados. El límite superior puede modificarse dentro de valores razonables
    # dependiendo del SF
    length = len(buffer_out[0])
    if length > max_buffer:
        length = max_buffer
        for index in range(outputs):
            buffer_out[index] = buffer_out[index][0:length]

    # Guardar los patrones en archivos de texto
    data_out = np.column_stack(buffer_out)
    np.savetxt(datafile_path, data_out, fmt=fmt, delimiter="")

    """ Esta parte del código compara los datos obtenidos en la adquisición con los datos de una simulación del 
    circuito, ambos en archivos de texto. Devuelve un mensaje indicando si los dos archivos de datos coinciden 
    completamente o no a partir de un determinado punto inicial. Pueden modificarse las variables logicdata, sim_data, 
    len_data y los índices a comparar de value_sim y value_data.
    """
    if enable:
        if compare:
            # CARGAR LOS DATOS
            # Abrir los archivos en modo lectura
            logicdata = open("datafile.txt", "r")
            sim_data = open("Test/datos_salidas_led64_ligero_23052023.txt", "r")
            # Leer los archivos
            data = logicdata.read()
            sim_data = sim_data.read()

            # Eliminar los saltos de línea y el último elemento de la lista de datos (línea en blanco)
            data_into_list = data.split("\n")
            data_into_list = data_into_list[0:len(data_into_list) - 1]
            sim_data_into_list = sim_data.split("\n")
            logicdata.close()

            # Búsqueda del comienzo de la comparación
            for j in range(0, len(data_into_list)):  # Buscar el disparo en el archivo de datos de salida
                trigger = False
                value = data_into_list[j]

                if trigger is False and value[trigger_signal] == str(rising_edge_int):
                    trigger = True
                    data_trigger_pos = j
                    print(f"La posición en la que empieza el disparo es {j}")
                    break

            for i in range(0, len(sim_data_into_list)):  # Buscar el comienzo en el archivo de datos de la simulación
                trigger = False
                value = sim_data_into_list[i]

                if trigger is False and value[sim_trigger_signal] == str(rising_edge_int):
                    trigger = True
                    sim_trigger_pos = i
                    break

            len_data = len(sim_data_into_list) - sim_trigger_pos  # Número de datos a comparar
            num_error = 0  # Contador de errores

            for k in range(0, len_data):
                value_sim = sim_data_into_list[sim_trigger_pos + k]
                value_data = data_into_list[data_trigger_pos + k]
                """ La condición del siguiente if debe modificarse según las señales que se quieran comparar en los dos
                archivos. Por ejemplo, si se quieren comparar desde la segunda hasta la cuarta señal del archivo de
                simulación con las mismas del archivo de salida, se escribiría value_sim[1:4] y value_data[1:4]. 
                """
                if value_sim[:] != value_data[:]:  # Comparar los patrones de las señales
                    num_error += 1

            if num_error > 0:
                print(f"\nEl número de fallos es {num_error}")
                print("Las listas no son iguales")
            else:
                print("\nLas listas son iguales! \(^_^)/")

    # Generar buffer para el tiempo
    time = []
    for index in range(length):
        time.append(index*1e06/SF)   # Convertir tiempo a μs

    # Representación
    bufferout_vtg = [[voltage * i for i in inner] for inner in buffer_out]  # Patrones en valores de voltaje
    if plot:
        for index in range(1, outputs + 1):
            plt.subplot(outputs, 1, index)
            plt.plot(time, bufferout_vtg[index - 1])
            plt.ylabel("logic value")
            plt.yticks([0, voltage])
            plt.title(lines_hd[index-1], fontsize=9, y=0.8)  # Puede cambiarse el formato del título y su posición
            if index == outputs:
                plt.xlabel("time (μs)")

        plt.show()

    # Cerrar el suministro de potencia
    supplies_data.master_state = False
    supplies.switch(device_data, supplies_data)
    supplies.close(device_data)

    # Cerrar el analizador lógico
    logic.close(device_data)

    # Cerrar el generador de patrones
    pattern.close(device_data)

    """-----------------------------------"""

    # close the connection
    device.close(device_data)

except error as e:
    print(e)
    # close the connection
    device.close(device.data)
