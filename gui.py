import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json

# ============================
#   LÓGICA IMPORTADA DEL PROYECTO
# ============================

def puede_añadirse(tarea, bloques_dia, horas_por_dia):
    horas_ocupadas = sum(b["duracion"] for b in bloques_dia)
    if horas_ocupadas + tarea["duracion"] > horas_por_dia:
        return False
    if bloques_dia and bloques_dia[-1]["nombre"] == tarea["nombre"]:
        return False
    return True

def crear_horario(dias):
    return {dia: [] for dia in dias}

def asignar_tareas(tareas, dias, horas_por_dia, horario):
    tareas_ordenadas = sorted(tareas, key=lambda t: t["duracion"], reverse=True)
    for tarea in tareas_ordenadas:
        for dia in dias:
            if puede_añadirse(tarea, horario[dia], horas_por_dia):
                horario[dia].append(tarea)
                break

def exportar_json(horario):
    with open("horario.json", "w", encoding="utf-8") as f:
        json.dump(horario, f, ensure_ascii=False, indent=4)
    messagebox.showinfo("Exportado", "Archivo horario.json creado correctamente.")

# ============================
#   INTERFAZ GRÁFICA
# ============================

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Horarios Automáticos")

        self.tareas = []
        self.dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        self.horas_por_dia = 4

        # Entrada de tarea
        tk.Label(root, text="Nombre de la tarea:").pack()
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.pack()

        tk.Label(root, text="Duración (horas):").pack()
        self.entry_duracion = tk.Entry(root)
        self.entry_duracion.pack()

        tk.Button(root, text="Añadir tarea", command=self.agregar_tarea).pack(pady=5)

        # Lista de tareas
        tk.Label(root, text="Tareas añadidas:").pack()
        self.lista = tk.Listbox(root, width=40)
        self.lista.pack()

        # Botones principales
        tk.Button(root, text="Generar horario", command=self.generar_horario).pack(pady=10)
        tk.Button(root, text="Exportar a JSON", command=self.exportar).pack()

        # Resultado
        tk.Label(root, text="Horario generado:").pack()
        self.texto_horario = tk.Text(root, height=10, width=50)
        self.texto_horario.pack()

    def agregar_tarea(self):
        nombre = self.entry_nombre.get()
        duracion = self.entry_duracion.get()

        if not nombre or not duracion.isdigit():
            messagebox.showerror("Error", "Datos inválidos.")
            return

        tarea = {"nombre": nombre, "duracion": int(duracion)}
        self.tareas.append(tarea)
        self.lista.insert(tk.END, f"{nombre} - {duracion}h")

        self.entry_nombre.delete(0, tk.END)
        self.entry_duracion.delete(0, tk.END)

    def generar_horario(self):
        horario = crear_horario(self.dias)
        asignar_tareas(self.tareas, self.dias, self.horas_por_dia, horario)

        self.texto_horario.delete("1.0", tk.END)
        for dia, bloques in horario.items():
            self.texto_horario.insert(tk.END, f"{dia}:\n")
            for b in bloques:
                self.texto_horario.insert(tk.END, f" - {b['nombre']} ({b['duracion']}h)\n")
            self.texto_horario.insert(tk.END, "\n")

        self.horario = horario

    def exportar(self):
        if hasattr(self, "horario"):
            exportar_json(self.horario)
        else:
            messagebox.showerror("Error", "Primero genera un horario.")

# ============================
#   EJECUCIÓN
# ============================

root = tk.Tk()
app = App(root)
root.mainloop()
