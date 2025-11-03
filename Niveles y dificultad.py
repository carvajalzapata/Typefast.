import random

class PalabraJuego:
    def __init__(self, texto: str):
        self.texto = texto
        self.precision = 0.0

    def comparar_con(self, entrada: str) -> float:
        errores = sum(1 for a, b in zip(self.texto, entrada) if a != b) + abs(len(self.texto) - len(entrada))
        total = max(len(self.texto), 1)
        self.precision = ((len(self.texto) - errores) / total) * 100
        return self.precision

class RepositorioPalabras:

    def __init__(self) -> None:
        self.palabras: list = []

    def cargar_palabras(self) -> None:
        self.palabras = [
            PalabraJuego("sol"),
            PalabraJuego("luz"),
            PalabraJuego("mar"),
            PalabraJuego("casa"),
            PalabraJuego("gato"),
            PalabraJuego("perro"),
            PalabraJuego("flor"),
            PalabraJuego("nube"),
            PalabraJuego("auto"),
            PalabraJuego("piso"),
            PalabraJuego("ratón"),

            PalabraJuego("teclado"),
            PalabraJuego("pantalla"),
            PalabraJuego("programa"),
            PalabraJuego("circuito"),
            PalabraJuego("robótico"),
            PalabraJuego("sistema"),
            PalabraJuego("ventana"),
            PalabraJuego("botones"),
            PalabraJuego("analisis"),
            PalabraJuego("modular"),

            PalabraJuego("computadora"),
            PalabraJuego("inteligencia"),
            PalabraJuego("programación"),
            PalabraJuego("parangaricutirimícuaro"),
            PalabraJuego("electromecánico"),
            PalabraJuego("transformación"),
            PalabraJuego("procesamiento"),
            PalabraJuego("automatización"),
            PalabraJuego("esternocleidomastoideo"),
            PalabraJuego("ingeniería"),

        ]

    def obtener_por_nivel(self, nivel: int, cantidad:int) -> list:
        palabras_nivel = []

        for palabra in self.palabras:
            longitud = len(palabra.texto)

            if nivel == 1 and longitud <= 5:
                palabras_nivel.append(palabra)
            elif nivel == 2 and 6 <= longitud <= 8:
                palabras_nivel.append(palabra)
            elif nivel == 3 and longitud > 8:
                palabras_nivel.append(palabra)
        return palabras_nivel[:cantidad]

class Nivel:
    def __init__(self, numero: int, repositorio: RepositorioPalabras):
        self.numero = numero
        self.repositorio = repositorio
        self.palabras = []
        self.indice_actual = 0
        self.intentos_precision = []
        self.intentos_velocidad = []
        self.puntaje_nivel = 0

        # Requisitos mínimos para pasar
        if numero == 1:
            self.precision_requerida = 80
            self.velocidad_requerida = 5
        elif numero == 2:
            self.precision_requerida = 90
            self.velocidad_requerida = 10
        else:
            self.precision_requerida = 100
            self.velocidad_requerida = 150

    def generar_palabras(self):
        todas = self.repositorio.obtener_por_nivel(self.numero, 999)
        self.palabras = random.sample(todas, 5)
        self.indice_actual = 0
        self.intentos_precision.clear()
        self.intentos_velocidad.clear()
        self.puntaje_nivel = 0

    def obtener_palabra(self):
        if self.indice_actual < len(self.palabras):
            return self.palabras[self.indice_actual]
        return None

    def siguiente_palabra(self):
        if self.indice_actual < len(self.palabras) - 1:
            self.indice_actual += 1
            return True
        return False

    def registrar_intento(self, precision: float, velocidad: float):
        self.intentos_precision.append(precision)
        self.intentos_velocidad.append(velocidad)
        self.puntaje_nivel += int((precision * velocidad) / 10)  # Puntaje por palabra

    def prom_totales(self):
        if not self.intentos_precision:
            return 0, 0
        prom_p = sum(self.intentos_precision) / len(self.intentos_precision)
        prom_v = sum(self.intentos_velocidad) / len(self.intentos_velocidad)
        return prom_p, prom_v

    def puede_pasar(self):
        prom_p, prom_v = self.prom_totales()
        return prom_p >= self.precision_requerida and prom_v >= self.velocidad_requerida





