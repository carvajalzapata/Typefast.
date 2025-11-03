import random

class Jugador:
    def __init__(self, nombre: str):
        self.nombre: str = nombre
        self.puntaje_total = 0
        self.promedios_por_nivel = {}
        self.puntaje_por_nivel = {}


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
import time

class Partida:
    def __init__(self, jugador: Jugador, repositorio: RepositorioPalabras):
        self.jugador = jugador
        self.repositorio = repositorio
        self.numero_nivel = 1
        self.nivel_actual = Nivel(self.numero_nivel, self.repositorio)
        self.en_curso = False

    def iniciar(self):
        print(f"\n=== Iniciando partida para {self.jugador.nombre} ===")
        self.en_curso = True
        self.nivel_actual.generar_palabras()

    def registrar_entrada(self, entrada: str) -> float:
        palabra = self.nivel_actual.obtener_palabra()
        if not palabra:
            return 0.0
        precision = palabra.comparar_con(entrada)
        return precision

    def asignar_puntaje(self, precision: float, velocidad: float):
        self.nivel_actual.registrar_intento(precision, velocidad)
        self.jugador.puntaje_total += int((precision * velocidad) / 10)

    def aumentar_nivel(self):
        self.numero_nivel += 1
        if self.numero_nivel > 3:
            print("\n¡Has completado todos los niveles!")
            self.en_curso = False
            return
        print(f"\n--- Pasando al NIVEL {self.numero_nivel} ---")
        self.nivel_actual = Nivel(self.numero_nivel, self.repositorio)
        self.nivel_actual.generar_palabras()

    def finalizar(self):
        print("\n=== FIN DE LA PARTIDA ===")
        self.en_curso = False


def jugar():
    print("=== BIENVENIDO A TYPEFAST ===")
    nombre = input("Ingrese su nombre: ")
    jugador = Jugador(nombre)
    repo = RepositorioPalabras()
    repo.cargar_palabras()
    partida = Partida(jugador, repo)
    partida.iniciar()

    while partida.en_curso:
        nivel = partida.nivel_actual
        print(f"\n NIVEL {nivel.numero} | Palabras: {len(nivel.palabras)}")
        for palabra_obj in nivel.palabras:
            print(f"\nEscriba la palabra: {palabra_obj.texto}")
            inicio_palabra = time.time()
            entrada = input(" Ingrese la palabra: ")
            fin_palabra = time.time()

            tiempo_segundos = fin_palabra - inicio_palabra
            tiempo_min = tiempo_segundos / 60
            velocidad = 1 / tiempo_min if tiempo_min > 0 else 0

            precision = partida.registrar_entrada(entrada)
            partida.asignar_puntaje(precision, velocidad)
            print(f" {tiempo_segundos:.2f}s |  {velocidad:.2f} WPM |  {precision:.2f}%")

            nivel.siguiente_palabra()

        prom_p, prom_v = nivel.prom_totales()
        print("\n=== RESULTADOS DEL NIVEL ===")
        print(f" Precisión promedio: {prom_p:.2f}%")
        print(f" Velocidad promedio: {prom_v:.2f} WPM")
        print(f" Puntaje total acumulado: {jugador.puntaje_total}")

        if nivel.puede_pasar():
            print("\n Cumples con los requisitos para avanzar al siguiente nivel.")
            decision = input("¿Deseas pasar al siguiente nivel? (S/N): ").strip().lower()
            if decision == "s":
                partida.aumentar_nivel()
            else:
                print("\nTe has retirado voluntariamente. Fin del juego.")
                partida.finalizar()
        else:
            print("\n No cumples los requisitos para pasar. Debes repetir el nivel.")
            repetir = input("¿Deseas intentarlo de nuevo? (S/N): ").strip().lower()
            if repetir == "s":
                nivel.generar_palabras()
            else:
                print("\nTe has retirado del juego.")
                partida.finalizar()

    print("\n=== RESULTADOS FINALES ===")
    print(f"Jugador: {jugador.nombre}")
    print(f"Puntaje total: {jugador.puntaje_total}")
    print("¡Gracias por jugar TYPEFAST!")


import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk, ImageSequence
import time

# =====================================================
#  INTENTO DE IMPORTAR MÓDULOS PRINCIPALES
# =====================================================
try:
    from typefast_core import Jugador, RepositorioPalabras, Partida
except ImportError:
    messagebox.showerror("Error", "No se encontró el archivo 'typefast_core.py'.")
    exit()

# =====================================================
#  CLASE PRINCIPAL DE LA INTERFAZ
# =====================================================
class InterfazTypeFast:
    def __init__(self, root):
        self.root = root
        self.root.title("TypeFast - Juego de Mecanografía")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # --- Fondos por nivel ---
        self.fondos = {
            1: "fondo_nivel1.png",
            2: "fondo_nivel2.png",
            3: "fondo_nivel3.png"
        }

        # --- Variables del juego ---
        self.partida = None
        self.jugador = None
        self.repo = None
        self.inicio_palabra = 0
        self.palabra_actual = None

        # --- Fondo base ---
        self.label_fondo = tk.Label(root)
        self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        # --- Fondo animado principal (GIF) ---
        self.cargar_fondo_gif_principal("fondo_principal.gif")

        # --- Widgets principales ---
        self.label_titulo = tk.Label(root, text="TYPEFAST", font=("Arial", 32, "bold"),
                                     fg="white", bg="black")
        self.label_titulo.pack(pady=20)

        self.label_palabra = tk.Label(root, text="", font=("Arial", 28, "bold"),
                                      fg="yellow", bg="black")
        self.label_palabra.pack(pady=20)

        self.entry_palabra = tk.Entry(root, font=("Arial", 20))
        self.entry_palabra.pack()
        self.entry_palabra.bind("<Return>", self.verificar_palabra)

        self.label_promedios = tk.Label(root,
            text="Promedios: Precisión 0.00% | Velocidad 0.00 WPM",
            font=("Arial", 14), fg="white", bg="black"
        )
        self.label_promedios.pack(pady=10)

        self.label_puntaje = tk.Label(root,
            text="Puntaje total: 0", font=("Arial", 14),
            fg="white", bg="black"
        )
        self.label_puntaje.pack(pady=10)

        self.boton_iniciar = tk.Button(root, text="Iniciar Partida",
                                       font=("Arial", 14), command=self.iniciar_partida)
        self.boton_iniciar.pack(pady=20)

    # =====================================================
    #  FONDO ANIMADO PRINCIPAL (GIF)
    # =====================================================
    def cargar_fondo_gif_principal(self, archivo_gif):
        """Carga y anima un GIF en la pantalla principal."""
        try:
            gif = Image.open(archivo_gif)
            self.frames_gif = [ImageTk.PhotoImage(img.resize((900, 600)))
                               for img in ImageSequence.Iterator(gif)]
            self.frame_index_gif = 0
            self.animar_gif_principal()
        except Exception as e:
            print(f"Error al cargar GIF: {e}")
            self.label_fondo.config(bg="black")

    def animar_gif_principal(self):
        """Reproduce el GIF de fondo de la pantalla principal."""
        if hasattr(self, 'frames_gif') and self.frames_gif:
            frame = self.frames_gif[self.frame_index_gif]
            self.label_fondo.config(image=frame)
            self.frame_index_gif = (self.frame_index_gif + 1) % len(self.frames_gif)
            self.animacion_gif = self.root.after(100, self.animar_gif_principal)

    def detener_gif_principal(self):
        """Detiene la animación del GIF."""
        if hasattr(self, 'animacion_gif'):
            self.root.after_cancel(self.animacion_gif)

    # =====================================================
    #  CAMBIAR FONDO SEGÚN NIVEL
    # =====================================================
    def cambiar_fondo(self, nivel):
        """Carga una imagen de fondo distinta por nivel."""
        if nivel in self.fondos:
            try:
                self.detener_gif_principal()  # Detener GIF antes de cambiar fondo
                imagen = Image.open(self.fondos[nivel])
                imagen = imagen.resize((900, 600))
                self.img_fondo = ImageTk.PhotoImage(imagen)
                self.label_fondo.config(image=self.img_fondo)
            except Exception as e:
                print(f"No se pudo cargar fondo del nivel {nivel}: {e}")
                self.label_fondo.config(bg="black")

    # =====================================================
    #  INICIAR PARTIDA
    # =====================================================
    def iniciar_partida(self):
        nombre = simpledialog.askstring("Nombre del jugador", "Ingrese su nombre:")
        if not nombre:
            return

        self.jugador = Jugador(nombre)
        self.repo = RepositorioPalabras()
        self.repo.cargar_palabras()
        self.partida = Partida(self.jugador, self.repo)
        self.partida.iniciar()
        self.mostrar_palabra_actual()

    # =====================================================
    #  MOSTRAR PALABRA ACTUAL
    # =====================================================
    def mostrar_palabra_actual(self):
        nivel = self.partida.nivel_actual
        self.cambiar_fondo(nivel.numero)
        palabra = nivel.obtener_palabra()
        if palabra:
            self.palabra_actual = palabra
            self.label_palabra.config(text=palabra.texto)
            self.entry_palabra.delete(0, tk.END)
            self.entry_palabra.focus()
            self.inicio_palabra = time.time()
        else:
            self.finalizar_nivel()

    # =====================================================
    #  VERIFICAR PALABRA
    # =====================================================
    def verificar_palabra(self, event=None):
        if not self.palabra_actual:
            return

        entrada = self.entry_palabra.get()
        fin_palabra = time.time()
        tiempo_seg = fin_palabra - self.inicio_palabra
        tiempo_min = tiempo_seg / 60
        velocidad = 1 / tiempo_min if tiempo_min > 0 else 0

        precision = self.partida.registrar_entrada(entrada)
        self.partida.asignar_puntaje(precision, velocidad)

        prom_p, prom_v = self.partida.nivel_actual.prom_totales()
        self.label_promedios.config(
            text=f"Promedios: Precisión {prom_p:.2f}% | Velocidad {prom_v:.2f} WPM"
        )
        self.label_puntaje.config(text=f"Puntaje total: {self.jugador.puntaje_total}")

        if not self.partida.nivel_actual.siguiente_palabra():
            self.finalizar_nivel()
        else:
            self.mostrar_palabra_actual()

    # =====================================================
    #  FINALIZAR NIVEL
    # =====================================================
    def finalizar_nivel(self):
        nivel = self.partida.nivel_actual
        prom_p, prom_v = nivel.prom_totales()
        resumen = (
            f"Nivel {nivel.numero} completado.\n\n"
            f"Precisión promedio: {prom_p:.2f}%\n"
            f"Velocidad promedio: {prom_v:.2f} WPM\n"
            f"Puntaje total acumulado: {self.jugador.puntaje_total}"
        )
        messagebox.showinfo("Estadísticas del nivel", resumen)

        if nivel.puede_pasar():
            if messagebox.askyesno("Avanzar", "¿Deseas pasar al siguiente nivel?"):
                self.partida.aumentar_nivel()
                self.mostrar_palabra_actual()
            else:
                self.partida.finalizar()
                messagebox.showinfo("Fin del juego", "Te has retirado del juego.")
        else:
            if messagebox.askyesno("Reintentar", "No cumples los requisitos. ¿Reintentar el nivel?"):
                nivel.generar_palabras()
                self.mostrar_palabra_actual()
            else:
                self.partida.finalizar()
                messagebox.showinfo("Fin del juego", "Has finalizado la partida.")


# =====================================================
#  EJECUCIÓN PRINCIPAL
# =====================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazTypeFast(root)
    root.mainloop()
