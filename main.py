import json
import random

# ============================
#   FASE 1: DATOS INICIALES
# ============================

tareas = [
    {"nombre": "Matemáticas", "duracion": 2},
    {"nombre": "Programación", "duracion": 1},
    {"nombre": "Inglés", "duracion": 1},
    {"nombre": "Historia", "duracion": 2},
    {"nombre": "Física", "duracion": 1},
]

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
horas_por_dia = 4  # máximo de horas por día


# ============================
#   FASE 2: CREAR HORARIO
# ============================

def crear_horario(dias):
    return {dia: [] for dia in dias}


# ============================
#   FASE 3: VALIDACIONES
# ============================

def puede_añadirse(tarea, bloques_dia, horas_por_dia):
    horas_ocupadas = sum(b["duracion"] for b in bloques_dia)

    # Regla 1: que quepa en el día
    if horas_ocupadas + tarea["duracion"] > horas_por_dia:
        return False

    # Regla 2: evitar tareas iguales seguidas
    if bloques_dia and bloques_dia[-1]["nombre"] == tarea["nombre"]:
        return False

    return True


# ============================
#   FASE 4: ASIGNACIÓN
# ============================

def asignar_tareas(tareas, dias, horas_por_dia, horario, modo="ordenado"):
    # Modo ordenado: tareas largas primero
    if modo == "ordenado":
        tareas = sorted(tareas, key=lambda t: t["duracion"], reverse=True)

    # Modo aleatorio
    elif modo == "aleatorio":
        tareas = tareas.copy()
        random.shuffle(tareas)

    # Asignación
    for tarea in tareas:
        for dia in dias:
            if puede_añadirse(tarea, horario[dia], horas_por_dia):
                horario[dia].append(tarea)
                break


# ============================
#   FASE 5: DESCANSOS
# ============================

def insertar_descansos(horario, max_horas_seguidas=2):
    for dia, bloques in horario.items():
        nuevas = []
        acumuladas = 0

        for b in bloques:
            if acumuladas + b["duracion"] > max_horas_seguidas:
                nuevas.append({"nombre": "Descanso", "duracion": 1})
                acumuladas = 0

            nuevas.append(b)
            acumuladas += b["duracion"]

        horario[dia] = nuevas


# ============================
#   FASE 6: MOSTRAR HORARIO
# ============================

def mostrar_horario(horario):
    print("\n===== HORARIO GENERADO =====")
    for dia, bloques in horario.items():
        print(f"\n{dia}:")
        if not bloques:
            print("  (Sin tareas)")
        for b in bloques:
            print(f" - {b['nombre']} ({b['duracion']}h)")


# ============================
#   FASE 7: EXPORTAR JSON
# ============================

def exportar_json(horario, nombre_archivo="horario.json"):
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(horario, f, ensure_ascii=False, indent=4)


# ============================
#   FASE 8: MAIN
# ============================

def main():
    horario = crear_horario(dias)

    # Cambia "ordenado" por "aleatorio" si quieres probar otro modo
    asignar_tareas(tareas, dias, horas_por_dia, horario, modo="ordenado")

    insertar_descansos(horario)
    mostrar_horario(horario)

    exportar_json(horario)
    print("\nArchivo 'horario.json' exportado correctamente.")


if __name__ == "__main__":
    main()
