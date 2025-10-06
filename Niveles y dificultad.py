class PalabraJuego:
    def __init__(self, texto: str, usada: bool) -> None:
        self.texto: str = texto
        self.precision: float = 0.0
        self.errores: int = 0
        self.usada: bool = usada

    def calcular_errores(self, entrada: str) -> int:
        errores = 0
        i = 0

        while i < len(self.texto) and i < len(entrada):
            if self.texto[i] != entrada[i]:
                errores += 1
            i = i + 1

        if len(self.texto) > len(entrada):
            errores = errores + (len(self.texto) - len(entrada))
        elif len(entrada) > len(self.texto):
            errores = errores + (len(entrada) - len(self.texto))

        self.errores = errores
        return errores

    def comparar_con(self, palabra_correcta: str) -> None:
        errores = self.calcular_errores(palabra_correcta)
        total = len(palabra_correcta)

        if total > 0:
            aciertos = total - errores
            self.precision = aciertos / total
        else:
            self.precision = 0.0

    def es_correcta(self, palabra_correcta: str) -> bool:
        if self.texto.lower().strip() == palabra_correcta.lower().strip():
            self.usada = True
        else:
            self.usada = False

        return self.usada

    def __str__(self) -> str:
        return f"Palabra escrita: {self.texto}, Errores: {self.errores}, Precisión: {round(self.precision * 100, 2)}%"


class RepositorioPalabras:
    pass

class Nivel:
    def __init__(self, numero: int, tiempo_limite: float, precision_requerida:float) -> None:
        self.numero: int = numero
        self.tiempo_limite: float = tiempo_limite
        self.precision_requerida: float = precision_requerida
        self.palabras: list = []

    def obtener_palabra(self):
        pass
    
    def generar_palabra(self):
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


    