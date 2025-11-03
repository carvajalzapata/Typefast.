import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, \
    ImageTk  # Aunque PIL/Image no se usan en la lógica base, se mantiene por si quieres añadir imágenes


# =====================================================
#  CLASE JUGADOR
# =====================================================
class Jugador:
    """Representa al jugador y sus estadísticas."""

    def __init__(self, nombre: str):
        self.nombre: str = nombre
        self.puntaje_total = 0
        self.promedios_por_nivel = {}  # Guardar promedio precisión y velocidad por nivel
        self.puntaje_por_nivel = {}  # Guardar puntaje por nivel


# =====================================================
#  CLASE PALABRA
# =====================================================
class PalabraJuego:
    """Representa una palabra del juego y calcula la precisión."""

    def __init__(self, texto: str):
        self.texto = texto
        self.precision = 0.0

    def comparar_con(self, entrada: str) -> float:
        """Compara la palabra y calcula la precisión."""
        # R8 - Calcular errores por número e igualación de caracteres
        errores = sum(1 for a, b in zip(self.texto, entrada) if a != b) + abs(len(self.texto) - len(entrada))
        total = max(len(self.texto), 1)
        # R9 - Cálculo de precisión
        self.precision = ((len(self.texto) - errores) / total) * 100
        return self.precision


# =====================================================
#  REPOSITORIO
# =====================================================
class RepositorioPalabras:
    """Gestiona el conjunto de palabras disponibles."""

    def __init__(self):
        self.palabras = []
        self.cargar_palabras()  # Cargar automáticamente al inicializar

    def cargar_palabras(self):
        """R3 - Carga la lista de palabras estáticas."""
        self.palabras = [
            PalabraJuego("sol"), PalabraJuego("luz"), PalabraJuego("mar"),
            PalabraJuego("casa"), PalabraJuego("gato"),
            PalabraJuego("teclado"), PalabraJuego("pantalla"),
            PalabraJuego("programa"), PalabraJuego("robotico"),
            PalabraJuego("computadora"), PalabraJuego("inteligencia"),
            PalabraJuego("programacion")
        ]

    def obtener_por_nivel(self, nivel: int, cantidad: int):
        """R4 - Selecciona palabras según el nivel (longitud)."""
        palabras_nivel = []
        for palabra in self.palabras:
            l = len(palabra.texto)
            if nivel == 1 and l <= 5:
                palabras_nivel.append(palabra)
            elif nivel == 2 and 6 <= l <= 8:
                palabras_nivel.append(palabra)
            elif nivel == 3 and l > 8:
                palabras_nivel.append(palabra)

        # Usar un poco de aleatoriedad para seleccionar las primeras 'cantidad'
        import random
        random.shuffle(palabras_nivel)
        return palabras_nivel[:cantidad]


# =====================================================
#  NIVEL
# =====================================================
class Nivel:
    """Gestiona la lógica y requerimientos de un nivel."""

    def __init__(self, numero: int, repositorio: 'RepositorioPalabras'):
        self.numero = numero
        self.repositorio = repositorio
        self.palabras = []
        self.indice_actual = 0
        self.intentos_precision = []
        self.intentos_velocidad = []
        self.puntaje_nivel = 0

        # R14 - Requisitos mínimos para pasar (dificultad incremental)
        if numero == 1:
            self.precision_requerida = 80
            self.velocidad_requerida = 5
            self.tiempo_limite_seg = 30  # R12 - 30 segundos para nivel 1
        elif numero == 2:
            self.precision_requerida = 90
            self.velocidad_requerida = 10
            self.tiempo_limite_seg = 45  # R12 - 45 segundos para nivel 2 (aumenta por más palabras/complejidad)
        else:
            self.precision_requerida = 100
            self.velocidad_requerida = 15
            self.tiempo_limite_seg = 60  # R12 - 60 segundos para nivel 3

    def generar_palabras(self):
        """Inicializa las palabras para un nuevo intento de nivel."""
        self.palabras = self.repositorio.obtener_por_nivel(self.numero, 5)  # 5 palabras por nivel
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

        # R11 - Asignación de puntaje
        puntaje_palabra = int((precision * velocidad) / 10)
        self.puntaje_nivel += puntaje_palabra

    def prom_totales(self):
        if not self.intentos_precision:
            return 0, 0
        prom_p = sum(self.intentos_precision) / len(self.intentos_precision)
        prom_v = sum(self.intentos_velocidad) / len(self.intentos_velocidad)
        return prom_p, prom_v

    def puede_pasar(self):
        """R13 - Evalúa si el jugador alcanzó los requerimientos mínimos."""
        prom_p, prom_v = self.prom_totales()
        return prom_p >= self.precision_requerida and prom_v >= self.velocidad_requerida


# =====================================================
#  PARTIDA
# =====================================================
class Partida:
    """Coordina el flujo del juego, niveles y jugador."""

    def __init__(self, jugador: Jugador, repositorio: RepositorioPalabras, gui):
        self.jugador = jugador
        self.repositorio = repositorio
        self.gui = gui
        self.numero_nivel = 1
        self.intentos_por_nivel = {1: 3, 2: 3, 3: 3}
        self.nivel_actual = None
        self.palabra_inicio = 0
        self.juego_activo = False
        self.tiempo_fin_nivel = 0  # Para el control de tiempo (R12)
        self.id_cronometro = None

        # Iniciar el juego
        self.iniciar_nivel(self.numero_nivel)

    def iniciar_nivel(self, numero: int):
        """Inicializa un nivel específico."""
        self.numero_nivel = numero
        self.nivel_actual = Nivel(self.numero_nivel, self.repositorio)
        self.nivel_actual.generar_palabras()
        self.juego_activo = True

        # R12 - Control de tiempo: Establecer el límite de tiempo y el cronómetro.
        self.tiempo_fin_nivel = time.time() + self.nivel_actual.tiempo_limite_seg
        self.gui.actualizar_cronometro(self.nivel_actual.tiempo_limite_seg)
        self.gui.mostrar_nivel(self.numero_nivel)
        self.iniciar_cronometro()
        self.mostrar_palabra_actual()

    def iniciar_cronometro(self):
        """Inicia el contador regresivo (R12)."""
        if self.id_cronometro:
            self.gui.root.after_cancel(self.id_cronometro)

        tiempo_restante = max(0, int(self.tiempo_fin_nivel - time.time()))

        if tiempo_restante <= 0:
            if self.juego_activo:
                self.juego_activo = False
                self.gui.actualizar_cronometro(0)
                messagebox.showwarning("¡Tiempo agotado!",
                                       "❌ El tiempo límite del nivel ha terminado. Se evaluará tu desempeño.")  # R16
                self.completar_nivel(por_tiempo=True)
            return

        self.gui.actualizar_cronometro(tiempo_restante)
        self.id_cronometro = self.gui.root.after(1000, self.iniciar_cronometro)

    def mostrar_palabra_actual(self):
        """R5 - Muestra la palabra actual y registra el tiempo de inicio."""
        palabra_obj = self.nivel_actual.obtener_palabra()
        if palabra_obj:
            self.gui.mostrar_palabra(palabra_obj.texto)
            self.gui.entrada_texto.delete(0, tk.END)  # Limpiar entrada
            self.palabra_inicio = time.time()
        elif self.juego_activo:
            self.completar_nivel()  # Todas las palabras escritas antes de tiempo

    def procesar_entrada(self, entrada: str):
        """R6 - Captura y procesa la entrada del jugador al presionar Enter."""
        if not self.juego_activo:
            return

        palabra_obj = self.nivel_actual.obtener_palabra()
        if not palabra_obj:
            return

        fin = time.time()
        tiempo = fin - self.palabra_inicio
        # R10 - Cálculo de velocidad (WPM)
        velocidad = (len(palabra_obj.texto) / 5) / (tiempo / 60) if tiempo > 0 else 0
        precision = palabra_obj.comparar_con(entrada)
        self.nivel_actual.registrar_intento(precision, velocidad)

        # Actualizar GUI con estadísticas
        prom_p, prom_v = self.nivel_actual.prom_totales()
        puntaje_total = self.jugador.puntaje_total + self.nivel_actual.puntaje_nivel
        self.gui.actualizar_promedios(prom_p, prom_v, puntaje_total)

        if self.nivel_actual.siguiente_palabra():
            self.mostrar_palabra_actual()
        else:
            self.completar_nivel()

    def completar_nivel(self, por_tiempo=False):
        """Maneja la lógica de fin de nivel."""
        if self.id_cronometro:
            self.gui.root.after_cancel(self.id_cronometro)
        self.juego_activo = False

        # Actualizar datos del jugador
        self.intentos_por_nivel[self.numero_nivel] -= 1
        prom_p, prom_v = self.nivel_actual.prom_totales()
        self.jugador.promedios_por_nivel[self.numero_nivel] = (prom_p, prom_v)
        self.jugador.puntaje_total += self.nivel_actual.puntaje_nivel
        self.jugador.puntaje_por_nivel[self.numero_nivel] = self.nivel_actual.puntaje_nivel

        if self.nivel_actual.puede_pasar() and not por_tiempo:
            # Nivel Aprobado
            messagebox.showinfo("Nivel completado",
                                f"✅ ¡Superaste el nivel {self.numero_nivel}!\nPuntaje nivel: {self.nivel_actual.puntaje_nivel}")  # R16

            # R14 - Aumentar dificultad (pasar al siguiente nivel)
            self.numero_nivel += 1
            if self.numero_nivel <= 3:
                self.gui.cambiar_fondo(self.numero_nivel)
                self.iniciar_nivel(self.numero_nivel)
            else:
                self.mostrar_resumen_final()
                self.gui.mostrar_menu_final()  # R19, R20
        else:
            # Nivel Reprobado
            if self.intentos_por_nivel[self.numero_nivel] <= 0:
                # Fin del juego por agotar intentos
                messagebox.showwarning("Juego terminado",
                                       f"❌ Has agotado los 3 intentos del nivel {self.numero_nivel}. Fin del juego.\nPuntaje nivel: {self.nivel_actual.puntaje_nivel}")  # R16
                self.mostrar_resumen_final()
                self.gui.mostrar_menu_final()  # R19, R20
            else:
                # R15 - Repetir nivel
                messagebox.showwarning(
                    "Intenta otra vez",
                    f"❌ No alcanzaste el promedio mínimo ({self.nivel_actual.precision_requerida}% P | {self.nivel_actual.velocidad_requerida} V).\nTe quedan {self.intentos_por_nivel[self.numero_nivel]} intentos."
                )
                # Reiniciar el nivel (R15)
                self.jugador.puntaje_total -= self.nivel_actual.puntaje_nivel  # Quitar puntaje de este intento fallido
                self.iniciar_nivel(self.numero_nivel)

    def mostrar_resumen_final(self):
        """R19 - Muestra los resultados finales de la partida."""
        resumen = f"📊 Resumen de {self.jugador.nombre} - Resultados Finales:\n"

        # R19 - Mostrar promedios y puntaje por nivel
        for nivel, (p, v) in self.jugador.promedios_por_nivel.items():
            puntaje = self.jugador.puntaje_por_nivel.get(nivel, 0)
            resumen += f"Nivel {nivel}: Precisión {p:.1f}% | Velocidad {v:.1f} WPM | Puntaje {puntaje}\n"

        # R19 - Mostrar puntaje total
        resumen += f"\n🏆 Puntaje Total: {self.jugador.puntaje_total}"

        # R18 - (Pendiente) Aquí se implementaría la lógica de GUARDAR RESULTADOS

        self.gui.info_resumen.config(text=resumen)
        return resumen

    def reiniciar_partida(self):
        """R20 - Reinicia el juego desde el nivel 1."""
        self.gui.root.after_cancel(self.id_cronometro)
        nuevo_jugador = Jugador(self.jugador.nombre)
        self.jugador = nuevo_jugador
        self.__init__(self.jugador, self.repositorio, self.gui)  # Re-inicializar la partida


# =====================================================
#  CLASE GUI
# =====================================================
class TypingGameGUI:
    """Implementa la interfaz gráfica y maneja eventos."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Typing Master - Juego de Mecanografía")
        self.partida = None
        self.setup_ui_base()
        self.mostrar_pantalla_registro()

    def setup_ui_base(self):
        """Configuración inicial de la ventana."""
        self.frame_main = tk.Frame(self.root, padx=10, pady=10)
        self.frame_main.pack(expand=True, fill='both')

        # Variables de la GUI
        self.current_word_var = tk.StringVar(value="...")
        self.prom_prec_var = tk.StringVar(value="0.0%")
        self.prom_vel_var = tk.StringVar(value="0.0 WPM")
        self.total_score_var = tk.StringVar(value="0")
        self.cronometro_var = tk.StringVar(value="Tiempo: --")
        self.nivel_var = tk.StringVar(value="Nivel: 1")

        # R21 - Salir de juego de manera segura
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # --- VISTAS ---

    def mostrar_pantalla_registro(self):
        """Muestra la pantalla para registrar el nombre del jugador."""
        for widget in self.frame_main.winfo_children():
            widget.destroy()

        tk.Label(self.frame_main, text="🎮 Ingresa tu nombre para empezar:", font=('Arial', 14, 'bold')).pack(pady=20)

        self.nombre_entry = tk.Entry(self.frame_main, font=('Arial', 16), width=20)
        self.nombre_entry.pack(pady=10)

        tk.Button(self.frame_main, text="Iniciar Partida (R1)", command=self.iniciar_juego, font=('Arial', 12),
                  bg='#4CAF50', fg='white').pack(pady=20)

    def iniciar_juego(self):
        """Inicia la partida después del registro (R1, R2)."""
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "Debes ingresar un nombre.")
            return

        jugador = Jugador(nombre)  # R1 - Registrar jugador
        repositorio = RepositorioPalabras()
        self.partida = Partida(jugador, repositorio, self)  # R2 - Iniciar partida
        self.mostrar_pantalla_juego()

    def mostrar_pantalla_juego(self):
        """Muestra la interfaz de juego principal."""
        for widget in self.frame_main.winfo_children():
            widget.destroy()

        # 1. Cabecera (Nivel y Tiempo)
        frame_header = tk.Frame(self.frame_main, pady=5)
        frame_header.pack(fill='x')
        tk.Label(frame_header, textvariable=self.nivel_var, font=('Arial', 12, 'bold')).pack(side='left', padx=10)
        tk.Label(frame_header, textvariable=self.cronometro_var, font=('Arial', 12, 'bold'), fg='red').pack(
            side='right', padx=10)  # R12

        # 2. Palabra a Escribir (R5)
        tk.Label(self.frame_main, text="Escribe esta palabra:", font=('Arial', 10)).pack(pady=(20, 5))
        self.lbl_palabra = tk.Label(self.frame_main, textvariable=self.current_word_var,
                                    font=('Courier New', 30, 'bold'), fg='#006400')
        self.lbl_palabra.pack(pady=5)

        # 3. Entrada del Jugador (R6)
        self.entrada_texto = tk.Entry(self.frame_main, font=('Arial', 18), justify='center', width=30)
        self.entrada_texto.pack(pady=20)

        # R6 - Capturar entrada al presionar Enter
        self.entrada_texto.bind("<Return>", self.handle_input)

        # R17 - (PENDIENTE) Control de errores del teclado (Ejemplo de implementación: usar validatecommand, no incluido aquí)
        # Para el R17, tendrías que añadir lógica de validación para ignorar caracteres inválidos.

        # 4. Estadísticas
        frame_stats = tk.Frame(self.frame_main, pady=10)
        frame_stats.pack(fill='x')

        tk.Label(frame_stats, text="Precisión: ", font=('Arial', 10)).grid(row=0, column=0, padx=10)
        tk.Label(frame_stats, textvariable=self.prom_prec_var, font=('Arial', 10, 'bold'), fg='blue').grid(row=0,
                                                                                                           column=1)

        tk.Label(frame_stats, text="Velocidad: ", font=('Arial', 10)).grid(row=0, column=2, padx=10)
        tk.Label(frame_stats, textvariable=self.prom_vel_var, font=('Arial', 10, 'bold'), fg='blue').grid(row=0,
                                                                                                          column=3)

        tk.Label(frame_stats, text="Puntaje Total: ", font=('Arial', 10)).grid(row=0, column=4, padx=10)
        tk.Label(frame_stats, textvariable=self.total_score_var, font=('Arial', 10, 'bold'), fg='purple').grid(row=0,
                                                                                                               column=5)

        frame_stats.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

    def mostrar_menu_final(self):
        """Muestra las opciones de menú al finalizar el juego (R19, R20, R21)."""
        for widget in self.frame_main.winfo_children():
            widget.destroy()

        tk.Label(self.frame_main, text="GAME OVER", font=('Arial', 24, 'bold'), fg='red').pack(pady=10)

        # R19 - Resumen (Se usará este Label para mostrar el texto del resumen)
        self.info_resumen = tk.Label(self.frame_main, text="", justify=tk.LEFT, font=('Courier New', 12))
        self.info_resumen.pack(pady=20)

        # Mostrar el resumen final
        self.partida.mostrar_resumen_final()

        # R20 - Opción de reiniciar
        tk.Button(self.frame_main, text="🔁 Reiniciar Partida (R20)", command=self.partida.reiniciar_partida,
                  font=('Arial', 14), bg='#FFC107').pack(pady=10)

        # R21 - Opción de salir
        tk.Button(self.frame_main, text="🚪 Salir del Juego (R21)", command=self.on_closing, font=('Arial', 14),
                  bg='#F44336', fg='white').pack(pady=10)

    # --- MÉTODOS DE ACTUALIZACIÓN ---

    def handle_input(self, event):
        """Maneja el evento de presionar Enter."""
        entrada = self.entrada_texto.get().strip()
        if entrada and self.partida and self.partida.juego_activo:
            self.partida.procesar_entrada(entrada)

    def mostrar_palabra(self, palabra: str):
        """Actualiza la palabra a escribir (R5)."""
        self.current_word_var.set(palabra)
        self.entrada_texto.focus_set()

    def actualizar_promedios(self, prom_p: float, prom_v: float, puntaje_total: int):
        """Actualiza las estadísticas en la GUI (R9, R10, R11)."""
        self.prom_prec_var.set(f"{prom_p:.1f}%")
        self.prom_vel_var.set(f"{prom_v:.1f} WPM")
        self.total_score_var.set(str(puntaje_total))

    def actualizar_cronometro(self, segundos: int):
        """Actualiza el cronómetro visible (R12)."""
        minutos = segundos // 60
        segundos_restantes = segundos % 60
        self.cronometro_var.set(f"Tiempo: {minutos:02}:{segundos_restantes:02}")

    def mostrar_nivel(self, nivel: int):
        """Actualiza el número de nivel actual."""
        self.nivel_var.set(f"Nivel: {nivel}")

    def cambiar_fondo(self, nivel: int):
        """Simula el cambio de fondo/dificultad visual."""
        colores = {1: 'lightgreen', 2: 'lightblue', 3: 'lightcoral'}
        self.root.config(bg=colores.get(nivel, 'white'))
        self.frame_main.config(bg=colores.get(nivel, 'white'))

    def on_closing(self):
        """Maneja la salida segura del juego (R21)."""
        if messagebox.askokcancel("Salir", "¿Estás seguro que quieres salir del juego?"):
            self.root.destroy()


# =====================================================
#  INICIO DEL JUEGO
# =====================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingGameGUI(root)
    root.mainloop()