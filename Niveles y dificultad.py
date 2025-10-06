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

class PalabraJuego:
    def __init__(self, texto: str, dificultad: int, usada: bool) -> None:
        self.texto: str = texto
        self.dificultad: int = dificultad
        self.usada: bool = usada

    def comparar(self, entrada:str):
        pass

    def calcular_errores(self, entrada: str):
        pass

    def palabra_correcta(self, entrada: str):
        pass

    def es_correcta(self):
        pass