import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Partida:
    def __init__(self, jugador: Jugador, repositorio: RepositorioPalabras, gui):
        self.jugador = jugador
        self.repositorio = repositorio
        self.gui = gui
        self.numero_nivel = 1
        self.intentos_por_nivel = {1: 3, 2: 3, 3: 3}  # Máximo 3 intentos por nivel
        self.nivel_actual = Nivel(self.numero_nivel, repositorio)
        self.nivel_actual.generar_palabras()
        self.palabra_inicio = 0
        self.mostrar_palabra_actual()

    def mostrar_palabra_actual(self):
        palabra_obj = self.nivel_actual.obtener_palabra()
        if palabra_obj:
            self.gui.mostrar_palabra(palabra_obj.texto)
            self.palabra_inicio = time.time()
        else:
            self.completar_nivel()

    def procesar_entrada(self, entrada):
        palabra_obj = self.nivel_actual.obtener_palabra()
        if not palabra_obj:
            return

        fin = time.time()
        tiempo = fin - self.palabra_inicio
        velocidad = (1 / tiempo) * 60 if tiempo > 0 else 0
        precision = palabra_obj.comparar_con(entrada)
        self.nivel_actual.registrar_intento(precision, velocidad)

        prom_p, prom_v = self.nivel_actual.prom_totales()
        puntaje_total = self.jugador.puntaje_total + self.nivel_actual.puntaje_nivel
        self.gui.actualizar_promedios(prom_p, prom_v, puntaje_total)

        if self.nivel_actual.siguiente_palabra():
            self.mostrar_palabra_actual()
        else:
            self.completar_nivel()

    def completar_nivel(self):
        self.intentos_por_nivel[self.numero_nivel] -= 1

        prom_p, prom_v = self.nivel_actual.prom_totales()
        self.jugador.promedios_por_nivel[self.numero_nivel] = (prom_p, prom_v)
        self.jugador.puntaje_total += self.nivel_actual.puntaje_nivel
        self.jugador.puntaje_por_nivel[self.numero_nivel] = self.nivel_actual.puntaje_nivel

        if self.nivel_actual.puede_pasar():
            messagebox.showinfo("Nivel completado",
                                f"¡Superaste el nivel {self.numero_nivel}!\nPuntaje nivel: {self.nivel_actual.puntaje_nivel}")
            self.numero_nivel += 1
            if self.numero_nivel <= 3:
                self.gui.cambiar_fondo(self.numero_nivel)
                self.nivel_actual = Nivel(self.numero_nivel, self.repositorio)
                self.nivel_actual.generar_palabras()
                self.mostrar_palabra_actual()
            else:
                self.mostrar_resumen_final()
                self.gui.root.destroy()
        else:
            if self.intentos_por_nivel[self.numero_nivel] <= 0:
                messagebox.showwarning("Juego terminado",
                                       f" Has agotado los 3 intentos del nivel {self.numero_nivel}. Fin del juego.\nPuntaje nivel: {self.nivel_actual.puntaje_nivel}")
                self.mostrar_resumen_final()
                self.gui.root.destroy()
            else:
                messagebox.showwarning(
                    "Intenta otra vez",
                    f"No alcanzaste el promedio mínimo. Te quedan {self.intentos_por_nivel[self.numero_nivel]} intentos.\nPuntaje nivel: {self.nivel_actual.puntaje_nivel}"
                )
                self.nivel_actual.generar_palabras()
                self.mostrar_palabra_actual()

    def mostrar_resumen_final(self):
        resumen = "Resumen de promedios y puntaje por nivel:\n"
        for nivel, (p, v) in self.jugador.promedios_por_nivel.items():
            puntaje = self.jugador.puntaje_por_nivel.get(nivel, 0)
            resumen += f"Nivel {nivel}: Precisión {p:.1f}% | Velocidad {v:.1f} WPM | Puntaje {puntaje}\n"
        resumen += f"\n Puntaje Total: {self.jugador.puntaje_total}"
        messagebox.showinfo("Resumen Final", resumen)
        self.gui.info_resumen.config(text=resumen)















