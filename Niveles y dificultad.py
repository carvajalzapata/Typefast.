class PalabraJuego:
    def __init__(self, texto: str, usada: bool = False) -> None:
        self.texto: str = texto
        self.precision: float = 0.0
        self.errores: int = 0
        self.usada: bool = usada


    def calcular_errores(self, entrada: str) -> int:
        error = 0
        i = 0

        while i < len(self.texto) and i < len(entrada):
            if self.texto[i] != entrada[i]:
                error += 1
            i = i + 1

        if len(self.texto) > len(entrada):
            error += (len(self.texto) - len(entrada))
        elif len(entrada) > len(self.texto):
            error += (len(entrada) - len(self.texto))

        self.errores = error
        return error

    def comparar_con(self, entrada: str):
        errores = self.calcular_errores(entrada)
        total = len(entrada)

        if total > 0:
            aciertos = total - errores
            self.precision = aciertos / total
        else:
            self.precision = 0.0

        return self.precision

    def palabra_correcta(self, palabra_correcta: str) -> bool:
        if self.texto.lower().strip() == palabra_correcta.lower().strip():
            return True
        else:
            return False

    def es_correcta(self):
        return self.usada

    def __str__(self) -> str:
        return f"Palabra escrita: {self.texto}, Errores: {self.errores}, Precisión: {round(self.precision * 100, 2)}%"

class RepositorioPalabras:
    def __init__(self) -> None:
        self.palabras: list = []

    def cargar_palabras(self):
        self.palabras = [
            PalabraJuego("gato"),
            PalabraJuego("perro"),
            PalabraJuego("python"),
            PalabraJuego("computador"),
            PalabraJuego("teclado"),
            PalabraJuego("ratón"),
            PalabraJuego("pantalla"),
            PalabraJuego("inteligencia"),
            PalabraJuego("programacion"),
            PalabraJuego("universidad"),
        ]

    def obtener_por_nivel(self, nivel: int, cantidad:int):
        palabras_nivel = []

        for palabra in self.palabras:
            longitud = len(palabra.texto)

            if nivel == 1 and longitud <= 5:
                palabras_nivel.append(palabra)
            elif nivel == 2 and 6 <= longitud <= 8:
                palabras_nivel.append(palabra)
            elif nivel == 3 and longitud > 8:
                palabras_nivel.append(palabra)

        return palabras_nivel


    def __str__(self):
        print("Palabras en el repositorio")
        for palabra in self.palabras:
            print(f"- {palabra.texto}")


class Nivel:
    def __init__(self, numero: int, tiempo_limite: float, precision_requerida:float, repositorio: 'RepositorioPalabras') -> None:
        self.numero: int = numero
        self.tiempo_limite: float = tiempo_limite
        self.precision_requerida: float = precision_requerida
        self.palabras: list = []
        self.indice_actual: int = 0
        self.repositorio: RepositorioPalabras = repositorio

    def generar_palabra(self, repositorio):
        self.palabras = repositorio.obtener_por_nivel(self.numero, 5)

        if len(self.palabras) > 0:
            print("Palabras cargadas para el nivel", self.numero)
            for palabra in self.palabras:
                print("-", palabra.texto)
        else:
            print("No hay palabras disponibles para este nivel.")

    def obtener_palabra(self) -> None:
        if self.indice_actual < len(self.palabras):
            return self.palabras[self.indice_actual]
        else:
            return None

    def siguiente_palabra(self):
        if self.indice_actual < len(self.palabras) - 1:
            self.indice_actual = self.indice_actual + 1
        else:
            print("Ya completaste todas las palabras de este nivel.")

    def puede_pasar(self, precision_jugador:float):
        if precision_jugador >= self.precision_requerida:
            print("¡Nivel superado!")
            return True
        else:
            print("No alcanzaste la precisión requerida.")
            return False

    def reducir_tiempo(self, reduccion: int):
        pass

    def pasar_nivel(self):
        pass

    def mostrar_informacion(self):
        pass

    def reiniciar(self):
        self.indice_actual = 0
        print("Nivel reiniciado.")


    