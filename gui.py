import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json

# ============================
#   LÓGICA IMPORTADA DEL PROYECTO
# ============================

def puede_añadirse(tarea, bloques_dia, horas_por_dia):
    horas_ocupadas = sum(b["duracion"] for b in bloques_dia)
    return horas_ocupadas + tarea["duracion"] <= horas_por_dia

def crear_horario(dias):
    return {dia: [] for dia in dias}

def asignar_tareas(tareas, dias, horas_por_dia, horario, modo="ordenado"):
    if modo == "ordenado":
        tareas = sorted(tareas, key=lambda t: t["duracion"], reverse=True)
    else:
        import random
        tareas = tareas.copy()
        random.shuffle(tareas)

    no_asignadas = []

    for tarea in tareas:
        dias_ordenados = sorted(
            dias,
            key=lambda d: horas_por_dia - sum(b["duracion"] for b in horario[d]),
            reverse=True
        )

        asignada = False
        for dia in dias_ordenados:
            if puede_añadirse(tarea, horario[dia], horas_por_dia):
                horario[dia].append(tarea)
                asignada = True
                break

        if not asignada:
            no_asignadas.append(tarea)

    return no_asignadas

def insertar_descansos(horario, max_horas_seguidas=2, limite_dia=None):
    for dia, bloques in horario.items():
        nuevas = []
        acumuladas = 0
        horas_totales = 0

        for b in bloques:
            if limite_dia is not None and horas_totales + b["duracion"] > limite_dia:
                break

            if acumuladas + b["duracion"] > max_horas_seguidas:
                if limite_dia is None or horas_totales + 1 <= limite_dia:
                    nuevas.append({"nombre": "Descanso", "duracion": 1})
                    horas_totales += 1
                acumuladas = 0

            nuevas.append(b)
            horas_totales += b["duracion"]
            acumuladas += b["duracion"]

        horario[dia] = nuevas

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

        tk.Label(root, text="Nombre de la tarea:").pack()
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.pack()

        tk.Label(root, text="Duración (horas):").pack()
        self.entry_duracion = tk.Entry(root)
        self.entry_duracion.pack()

        tk.Label(root, text="Horas por día:").pack()
        self.entry_horas_dia = tk.Entry(root)
        self.entry_horas_dia.insert(0, "6.5")
        self.entry_horas_dia.pack()

        tk.Button(root, text="Añadir tarea", command=self.agregar_tarea).pack(pady=5)

        # 🔥 NUEVO: BOTÓN BORRAR TODAS LAS TAREAS (con confirmación)
        tk.Button(root, text="Borrar todas las tareas", command=self.borrar_todas_confirmacion).pack(pady=5)

        # 🔥 NUEVO: BOTÓN BORRAR UNA TAREA
        tk.Button(root, text="Borrar tarea seleccionada", command=self.borrar_tarea_seleccionada).pack(pady=5)

        # 🔥 NUEVO: BOTÓN EDITAR TAREA
        tk.Button(root, text="Editar tarea seleccionada", command=self.editar_tarea).pack(pady=5)

        # 🔥 NUEVO: BOTONES MOVER ARRIBA / ABAJO
        tk.Button(root, text="Mover ↑", command=self.mover_arriba).pack(pady=2)
        tk.Button(root, text="Mover ↓", command=self.mover_abajo).pack(pady=2)

        tk.Label(root, text="Tareas añadidas:").pack()
        self.lista = tk.Listbox(root, width=40)
        self.lista.pack()

        tk.Label(root, text="Modo de generación:").pack()
        self.modo_var = tk.StringVar(value="ordenado")
        self.combo_modo = ttk.Combobox(root, textvariable=self.modo_var, values=["ordenado", "aleatorio"])
        self.combo_modo.pack()

        self.descansos_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Insertar descansos", variable=self.descansos_var).pack()

        tk.Button(root, text="Generar horario", command=self.generar_horario).pack(pady=10)
        tk.Button(root, text="Exportar a JSON", command=self.exportar).pack()

        tk.Label(root, text="Horario generado:").pack()
        self.texto_horario = tk.Text(root, height=10, width=50)
        self.texto_horario.pack()

    # ============================
    #   FUNCIONES DE TAREAS
    # ============================

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

    # 🔥 BORRAR TODAS LAS TAREAS (con confirmación)
    def borrar_todas_confirmacion(self):
        if messagebox.askyesno("Confirmar", "¿Seguro que quieres borrar TODAS las tareas?"):
            self.tareas.clear()
            self.lista.delete(0, tk.END)
            self.texto_horario.delete("1.0", tk.END)

    # 🔥 BORRAR SOLO UNA TAREA
    def borrar_tarea_seleccionada(self):
        sel = self.lista.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona una tarea.")
            return

        index = sel[0]
        self.lista.delete(index)
        del self.tareas[index]

    # 🔥 EDITAR UNA TAREA
    def editar_tarea(self):
        sel = self.lista.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona una tarea para editar.")
            return

        index = sel[0]
        tarea = self.tareas[index]

        # Cargar datos en los campos
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, tarea["nombre"])

        self.entry_duracion.delete(0, tk.END)
        self.entry_duracion.insert(0, tarea["duracion"])

        # Guardar cambios al pulsar "Añadir tarea"
        def guardar_edicion():
            nuevo_nombre = self.entry_nombre.get()
            nueva_duracion = self.entry_duracion.get()

            if not nuevo_nombre or not nueva_duracion.isdigit():
                messagebox.showerror("Error", "Datos inválidos.")
                return

            self.tareas[index] = {"nombre": nuevo_nombre, "duracion": int(nueva_duracion)}
            self.lista.delete(index)
            self.lista.insert(index, f"{nuevo_nombre} - {nueva_duracion}h")

            ventana.destroy()

        ventana = tk.Toplevel(self.root)
        ventana.title("Editar tarea")
        tk.Label(ventana, text="Editar tarea").pack()
        tk.Button(ventana, text="Guardar cambios", command=guardar_edicion).pack()

    # 🔥 MOVER TAREA ARRIBA
    def mover_arriba(self):
        sel = self.lista.curselection()
        if not sel or sel[0] == 0:
            return

        index = sel[0]
        self.tareas[index], self.tareas[index - 1] = self.tareas[index - 1], self.tareas[index]

        texto = self.lista.get(index)
        self.lista.delete(index)
        self.lista.insert(index - 1, texto)
        self.lista.select_set(index - 1)

    # 🔥 MOVER TAREA ABAJO
    def mover_abajo(self):
        sel = self.lista.curselection()
        if not sel or sel[0] == len(self.tareas) - 1:
            return

        index = sel[0]
        self.tareas[index], self.tareas[index + 1] = self.tareas[index + 1], self.tareas[index]

        texto = self.lista.get(index)
        self.lista.delete(index)
        self.lista.insert(index + 1, texto)
        self.lista.select_set(index + 1)

    # ============================
    #   GENERAR HORARIO
    # ============================

    def generar_horario(self):
        try:
            horas_por_dia = float(self.entry_horas_dia.get())
        except ValueError:
            messagebox.showerror("Error", "Las horas por día deben ser un número.")
            return

        horario = crear_horario(self.dias)
        modo = self.modo_var.get()

        tareas_no_asignadas = asignar_tareas(self.tareas, self.dias, horas_por_dia, horario, modo)

        if self.descansos_var.get():
            insertar_descansos(horario, limite_dia=horas_por_dia)

        self.texto_horario.delete("1.0", tk.END)
        for dia, bloques in horario.items():
            self.texto_horario.insert(tk.END, f"{dia}:\n")
            for b in bloques:
                self.texto_horario.insert(tk.END, f" - {b['nombre']} ({b['duracion']}h)\n")
            self.texto_horario.insert(tk.END, "\n")

        if tareas_no_asignadas:
            self.texto_horario.insert(tk.END, "⚠ Tareas no asignadas:\n")
            for t in tareas_no_asignadas:
                self.texto_horario.insert(tk.END, f" - {t['nombre']} ({t['duracion']}h)\n")

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
