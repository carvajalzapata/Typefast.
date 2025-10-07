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
    def __init__(self, numero: int, tiempo_limite: float, precision_requerida:float) -> None:
        self.numero: int = numero
        self.tiempo_limite: float = tiempo_limite
        self.precision_requerida: float = precision_requerida
        self.palabras: list = []
        self.indice_actual: int = 0

    def generar_palabra(self):
        pass
    def obtener_palabra(self):
        pass


    def puede_pasar(self, precision:float, velocidad:int):
        pass

    def siguiente_palabra(self):
        pass

    def reducir_tiempo(self):
        pass

    def pasar_nivel(self):
        pass

    def mostrar_informacion(self):
        pass

    def reiniciar(self):
        pass


    