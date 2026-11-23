# Proyecto de Arreglos - Resistencia eléctrica
# Estructuras de Datos y Algoritmos
#
# Aquí está la lógica del proyecto:
#   - Los arreglos con la tabla de colores.
#   - La clase Resistencia (R1: colores a partir del valor).
#   - La clase Circuito (R2: serie y R3: paralelo).

import random

# Arreglo de colores. La posición de cada color es el número que vale.
# Ejemplo: COLORES[6] es "Azul" porque el azul vale 6.
COLORES = ["Negro", "Marrón", "Rojo", "Naranja", "Amarillo",
           "Verde", "Azul", "Violeta", "Gris", "Blanco"]

# Arreglo de multiplicadores. Usa las mismas posiciones que COLORES.
# Ejemplo: MULTIPLICADORES[2] es 100 y le toca el color Rojo.
MULTIPLICADORES = [1, 10, 100, 1000, 10000, 100000, 1000000,
                   10000000, 100000000, 1000000000]

# Multiplicadores para valores menores que 10 ohmios (también son de la tabla).
# Dorado multiplica por 0.1 y Plateado por 0.01.
COLORES_ESPECIALES = ["Dorado", "Plateado"]
MULTIPLICADORES_ESPECIALES = [0.1, 0.01]

MINIMO_RESISTOR = 10
MAXIMO_RESISTOR = 1000000000
MAXIMO_N = 1000


class Resistencia:
    # Guarda el valor de la resistencia y un arreglo con los colores de sus bandas.

    def __init__(self, valor):
        self.valor = valor
        self.bandas = []
        self.multiplicador = 1
        self.error = ""

    def calcular_colores(self):
        # Llena el arreglo bandas con 3 colores:
        #   banda 1 = primer dígito, banda 2 = segundo dígito, banda 3 = multiplicador.
        # Ejemplos:
        #   5800 -> 58 x 100  -> Verde, Gris, Rojo
        #   4.7  -> 47 x 0.1  -> Amarillo, Violeta, Dorado
        #   0.47 -> 47 x 0.01 -> Amarillo, Violeta, Plateado
        # Regresa True si se pudo y False si el valor no es válido.
        self.bandas = []

        if self.valor >= 10:
            return self.colores_valor_grande()
        if self.valor >= 1:
            return self.colores_valor_chico(0)   # posición 0 = Dorado (x 0.1)
        if self.valor >= 0.1:
            return self.colores_valor_chico(1)   # posición 1 = Plateado (x 0.01)

        self.error = "El valor debe ser de 0.1 ohmios o más."
        return False

    def colores_valor_grande(self):
        # Para valores de 10 o más: dos dígitos y después solo ceros.
        if self.valor != int(self.valor):
            self.error = "Los valores de 10 ohmios o más deben ser enteros."
            return False

        texto = str(int(self.valor))

        # Después de los dos primeros dígitos solo puede haber ceros.
        for i in range(2, len(texto)):
            if texto[i] != "0":
                self.error = "El valor " + texto + " no se puede representar con 3 bandas."
                return False

        ceros = len(texto) - 2
        if ceros > 9:
            self.error = "El valor es demasiado grande para la tabla de colores."
            return False

        self.bandas.append(COLORES[int(texto[0])])
        self.bandas.append(COLORES[int(texto[1])])
        self.bandas.append(COLORES[ceros])
        self.multiplicador = MULTIPLICADORES[ceros]
        return True

    def colores_valor_chico(self, posicion):
        # Para valores menores que 10: se busca el número de dos dígitos que,
        # multiplicado por 0.1 (Dorado) o 0.01 (Plateado), da el valor.
        # Ejemplo: 4.7 / 0.1 = 47
        multiplicador = MULTIPLICADORES_ESPECIALES[posicion]
        dos_digitos = round(self.valor / multiplicador)

        # Si la división no da un número entero, el valor tiene demasiados decimales.
        if abs(self.valor / multiplicador - dos_digitos) > 0.001:
            self.error = "El valor " + str(self.valor) + " tiene demasiados decimales para 3 bandas."
            return False

        primer_digito = dos_digitos // 10
        segundo_digito = dos_digitos % 10
        self.bandas.append(COLORES[primer_digito])
        self.bandas.append(COLORES[segundo_digito])
        self.bandas.append(COLORES_ESPECIALES[posicion])
        self.multiplicador = multiplicador
        return True

    def texto_colores(self):
        # Regresa los colores separados por comas, por ejemplo "Verde, Gris, Rojo".
        texto = self.bandas[0]
        for i in range(1, len(self.bandas)):
            texto = texto + ", " + self.bandas[i]
        return texto


class Circuito:
    # Guarda n resistencias aleatorias en un arreglo y calcula serie y paralelo.

    def __init__(self, n):
        self.n = n
        self.resistores = []
        for i in range(n):
            self.resistores.append(0)

    def generar_resistores(self):
        # Llena el arreglo con números enteros aleatorios entre 10 y 1,000,000,000.
        for i in range(self.n):
            self.resistores[i] = random.randint(MINIMO_RESISTOR, MAXIMO_RESISTOR)

    def total_serie(self):
        # Rts = R1 + R2 + R3 + ... + Rn
        suma = 0
        for i in range(self.n):
            suma = suma + self.resistores[i]
        return suma

    def suma_inversos(self):
        # 1/R1 + 1/R2 + 1/R3 + ... + 1/Rn
        # Esta es la suma que escribe el PDF. Es un resultado intermedio
        # (se mide en siemens), todavía no es la resistencia en ohmios.
        suma = 0
        for i in range(self.n):
            suma = suma + 1 / self.resistores[i]
        return suma

    def total_paralelo(self):
        # Rtp = 1 / (1/R1 + 1/R2 + ... + 1/Rn)
        # Se divide 1 entre la suma de inversos para tener la resistencia en ohmios.
        return 1 / self.suma_inversos()
