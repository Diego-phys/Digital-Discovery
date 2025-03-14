# Digital-Discovery
Project to control Digilent's Digital Discovery device with Python.

The purpose of this program is to generate signals with the Digital Discovery (DD) in order to send them to a circuit, 
collect the output and save it in a .txt file. It also represents the output signals if desired.
To run the program correctly, the following steps must be followed:
- The custom signals must first be converted to the required format using the code ‘separa_listas.py’.
- Import the list with the pattern data obtained via ‘separa_listas.py’.
- Import the variable with the signal headers if you want to represent them.
- Modify if necessary the directory where the output data will be saved (variable ‘datafile_path’).
- The code will always ask for the trigger. The rest of the parameters can be modified manually or have the code ask for
  them by activating the ‘manual’ mode. If you intend to run multiple tests, it is recommended that you disable manual mode
  and write the relevant parameters in the code itself.
- Always follow the required format depending on the type of Python variable. For example, DIO and DIN variables are dictionaries,
  so if the entries are modified they must be entered in the format ‘i’: j, where i is a natural number starting with 1 and j is
  the label of the corresponding pin in the DD.
- IMPORTANT. Enter the pin information in the same order in which the corresponding signals appear in the imported text document.
- The ‘plot’ mode activates or deactivates the representation of the output signals.
- The ‘compare’ mode enables or disables the comparison of the output patterns against a simulation file that must be opened in
  a separate variable in the code.
The program does not work if the WaveForms software is open. When running, the generated signal representation will be displayed
after a few seconds. The program will not terminate until it is manually stopped or the graph is closed.
If the display mode is deactivated, the program will terminate after generating the .txt document or compare.
------------------------------------------------------------------------------------------------------------------------
Proyecto para controlar el dispositivo Digital Discovery de Digilent con Python.

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
