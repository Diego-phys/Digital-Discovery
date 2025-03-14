from WF_SDK import device, logic, pattern, error   # Instrumentos de la SDK para comunicarse con el DD
from WF_SDK.pattern import idle_state, trigger_source  # Algunas clases relevantes
import matplotlib.pyplot as plt   # Para representar
from time import sleep            # Para los retardos
from spr_entradasingle import data  # Lista de listas con los patrones para la entrada en el formato requerido
import numpy as np  # Para guardar la salida con el mismo formato que la entrada
"""-----------------------------------------------------------------------"""

# Variables del código (no tocar)
inputs = len(data)  # Número de señales de entrada al circuito
outputs = int(input("Número de salidas del circuito "))  # Número de señales de salida
ni = 1
no = 1
f = 1
buffer_out = []  # Lista de listas que contendrá los datos de salida del circuito
fmt = []  # Lista con el formato de los datos de salida (un valor por señal de salida o columna)

plot = True  # Booleano que controla la representación de los datos a la salida. False para no hacer la representación.
# Se recomienda representar solo si el número de señales a la salida no es muy grande.

# Números de los pines que mandan y reciben las señales
DIO = {'1': 28}
DIN = {'1': 1}
# Frecuencia de las señales (para señales personalizadas marcan la duración de los bits). Máxima frecuencia es 100 MHz.
frequency_list = 20000
SF = 3 * frequency_list  # Frecuencia de lectura
wait = 0  # Tiempo de espera
buffer = 200  # Número de muestras
max_buffer = 500000  # Tamaño máximo del buffer de salida
run_time = 0
repeat = 0
# Directorio donde guardar los datos de salida
datafile_path = "/Users/soto/Desktop/DIEGO/DIGILENT DIGITAL/Python/WF/test/datafile.txt"
# En el siguiente bloque de código se ingresa la información relevante en caso de que manual sea True

enable = bool(int(input("Activar (1) o desactivar (0) el trigger ")))
if enable:
    channel = int(input("Número del DIO/DIN usado como fuente del trigger "))
    rising_edge = bool(int(input("Establecer el criterio del trigger. 1 para subida, 0 para bajada ")))

try:
    # Conectar al dispositivo
    device_data = device.open()

    """-----------------------------------"""

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
    pattern.generate(device_data, channel=DIO['1'], function=pattern.function.custom, frequency=frequency_list,
                     data=data, wait=wait, repeat=repeat, run_time=run_time, trigger_enabled=False)

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
    buffer_out.append(logic.record(device_data, channel=DIN['1']))
    fmt.append("%d")

    # Limitar el tamaño de los datos mostrados. El límite superior puede modificarse dentro de valores razonables
    # dependiendo del SF.
    length = len(buffer_out[0])
    if length > max_buffer:
        length = max_buffer
        for index in range(outputs):
            buffer_out[index] = buffer_out[index][0:length]

    data_out = np.column_stack(buffer_out)
    np.savetxt(datafile_path, data_out, fmt=fmt, delimiter="")
    # Generar buffer para el tiempo
    time = []
    for index in range(length):
        time.append(index*1e06/SF)   # Convertir tiempo a μs

    # Representación
    if plot:
        plt.subplot(outputs, 1, 1)
        plt.plot(time, buffer_out[0])
        plt.ylabel("logic value")
        plt.yticks([0, 1])
        plt.title(f"Output")
        plt.xlabel("time (μs)")

        plt.show()

    # reset the logic analyzer
    logic.close(device_data)

    # reset the pattern generator
    pattern.close(device_data)

    """-----------------------------------"""

    # close the connection
    device.close(device_data)

except error as e:
    print(e)
    # close the connection
    device.close(device.data)
