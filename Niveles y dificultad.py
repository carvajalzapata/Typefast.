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

    def comparar_con(self, entrada: str) ->  float:
        errores = self.calcular_errores(entrada)
        total = len(entrada)

        if total > 0:
            aciertos = total - errores
            self.precision = (aciertos / total) * 100
        else:
            self.precision = 0.0

        return self.precision

    def palabra_correcta(self, palabra_correcta: str) -> bool:
        if self.texto.lower().strip() == palabra_correcta.lower().strip():
            return True
        else:
            return False

    def es_correcta(self) -> bool:
        return self.usada

    def __str__(self) -> str:
        return f"Palabra escrita: {self.texto}, Errores: {self.errores}, Precisión: {round(self.precision ,2)}%"

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
            PalabraJuego("raton"),

            PalabraJuego("teclado"),
            PalabraJuego("pantalla"),
            PalabraJuego("programa"),
            PalabraJuego("circuito"),
            PalabraJuego("robotico"),
            PalabraJuego("sistema"),
            PalabraJuego("ventana"),
            PalabraJuego("botones"),
            PalabraJuego("analisis"),
            PalabraJuego("modular"),

            PalabraJuego("computadora"),
            PalabraJuego("inteligencia"),
            PalabraJuego("programacion"),
            PalabraJuego("parangaricutirimicuaro"),
            PalabraJuego("electromecanico"),
            PalabraJuego("transformacion"),
            PalabraJuego("procesamiento"),
            PalabraJuego("automatizacion"),
            PalabraJuego("esternocleidomastoideo"),
            PalabraJuego("ingenieria"),

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

    def __str__(self) -> str:
        print("Palabras en el repositorio")
        for palabra in self.palabras:
            print(palabra.texto)


class Nivel:
    def __init__(self, numero: int, precision_requerida:float, velocidad_requerida: float, repositorio: 'RepositorioPalabras') -> None:
        self.numero: int = numero
        self.precision_requerida: float = precision_requerida
        self.velocidad_requerida: float = velocidad_requerida
        self.repositorio: RepositorioPalabras = repositorio
        self.palabras: list = []
        self.indice_actual: int = 0
        self.tiempo_limite: float = 40.0
        self.asignar_tiempo_por_nivel()

    def asignar_tiempo_por_nivel(self) -> None:
        self.tiempo_limite = max(10, 40 - (self.numero - 1) * 10)

    def generar_palabras(self) -> list[str]:
        self.palabras = self.repositorio.obtener_por_nivel(self.numero, 10)

        if len(self.palabras) > 0:
            return [p.texto for p in self.palabras]
        else:
            return ["No hay palabras disponibles para este nivel."]

    def obtener_palabra(self) -> PalabraJuego|None:
        if self.indice_actual < len(self.palabras):
            return self.palabras[self.indice_actual]
        else:
            return None

    def siguiente_palabra(self) -> PalabraJuego|None:
        if self.indice_actual < len(self.palabras) - 1:
            self.indice_actual += 1
            return self.palabras[self.indice_actual]

    def calcular_velocidad(self, palabras_correctas: int, tiempo_usado: float) -> float:
        if tiempo_usado > 0:
            velocidad = palabras_correctas / tiempo_usado
        else:
            velocidad = 0
        print(f"Velocidad del jugador: {velocidad:.2f} palabras/segundo")
        return velocidad

    def puede_pasar(self, precision_jugador: float, velocidad_jugador: float) -> bool:
        return (
                precision_jugador >= self.precision_requerida and
                velocidad_jugador >= self.velocidad_requerida
        )

    def reducir_tiempo(self) -> None:
        tiempo_anterior = self.tiempo_limite
        self.asignar_tiempo_por_nivel()
        print(f"Tiempo ajustado de {tiempo_anterior}s a {self.tiempo_limite}s para el nivel {self.numero}.")

    def pasar_nivel(self) -> str|None:
        if self.numero < 4:
            self.numero += 1
            self.precision_requerida = min(1.0, self.precision_requerida + 0.05)
            self.velocidad_requerida = round(self.velocidad_requerida + 0.05, 2)
            self.asignar_tiempo_por_nivel()
            self.indice_actual = 0
            self.generar_palabras()
        else:
            return "🎉 ¡Completaste todos los niveles!"

    def __str__(self) -> str:
        return (f"Nivel {self.numero}\n"
                f"Tiempo límite: {self.tiempo_limite:.0f} s\n"
                f"Precisión requerida: {self.precision_requerida:.2f}\n"
                f"Velocidad requerida: {self.velocidad_requerida:.2f} palabras/segundo\n"
                f"Palabras cargadas: {len(self.palabras)}")

    def reiniciar(self) -> None:
        self.indice_actual = 0
        print("Nivel reiniciado.")




