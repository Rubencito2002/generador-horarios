import json
import random

# ============================================
#   CREAR HORARIO VACÍO
# ============================================

def crear_horario(dias):
    return {dia: [] for dia in dias}


# ============================================
#   VALIDACIONES
# ============================================

def puede_añadirse(tarea, bloques_dia, horas_por_dia):
    horas_ocupadas = sum(b["duracion"] for b in bloques_dia)

    # Regla 1: que quepa en el día
    if horas_ocupadas + tarea["duracion"] > horas_por_dia:
        return False

    # Regla 2: evitar tareas iguales seguidas
    if bloques_dia and bloques_dia[-1]["nombre"] == tarea["nombre"]:
        return False

    return True


# ============================================
#   ASIGNACIÓN DE TAREAS
# ============================================

def asignar_tareas(tareas, dias, horas_por_dia, horario, modo="ordenado"):
    if modo == "ordenado":
        tareas = sorted(tareas, key=lambda t: t["duracion"], reverse=True)
    elif modo == "aleatorio":
        tareas = tareas.copy()
        random.shuffle(tareas)

    for tarea in tareas:
        asignada = False
        for dia in dias:
            if puede_añadirse(tarea, horario[dia], horas_por_dia):
                horario[dia].append(tarea)
                asignada = True
                break
        if not asignada:
            print(f"⚠️ No se pudo asignar la tarea: {tarea['nombre']}")


# ============================================
#   INSERTAR DESCANSOS
# ============================================

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


# ============================================
#   MOSTRAR HORARIO
# ============================================

def mostrar_horario(horario):
    print("\n===== HORARIO GENERADO =====")
    for dia, bloques in horario.items():
        print(f"\n{dia}:")
        if not bloques:
            print("  (Sin tareas)")
        for b in bloques:
            print(f" - {b['nombre']} ({b['duracion']}h)")


# ============================================
#   EXPORTAR JSON
# ============================================

def exportar_json(horario, nombre_archivo="horario.json"):
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(horario, f, ensure_ascii=False, indent=4)
    print(f"\n📁 Archivo '{nombre_archivo}' exportado correctamente.")


# ============================================
#   MENÚ INTERACTIVO
# ============================================

def menu():
    print("\n===== GENERADOR DE HORARIOS AUTOMÁTICO =====")
    print("1. Añadir tarea")
    print("2. Ver tareas actuales")
    print("3. Generar horario")
    print("4. Exportar horario a JSON")
    print("5. Salir")
    return input("\nSelecciona una opción: ")


# ============================================
#   PROGRAMA PRINCIPAL
# ============================================

def main():
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    horas_por_dia = 4
    tareas = []
    horario = None

    while True:
        opcion = menu()

        # -------------------------
        # 1. Añadir tarea
        # -------------------------
        if opcion == "1":
            nombre = input("Nombre de la tarea: ")
            duracion = int(input("Duración en horas: "))
            tareas.append({"nombre": nombre, "duracion": duracion})
            print("✔️ Tarea añadida.")

        # -------------------------
        # 2. Ver tareas
        # -------------------------
        elif opcion == "2":
            print("\n===== TAREAS ACTUALES =====")
            if not tareas:
                print("(No hay tareas aún)")
            else:
                for t in tareas:
                    print(f"- {t['nombre']} ({t['duracion']}h)")

        # -------------------------
        # 3. Generar horario
        # -------------------------
        elif opcion == "3":
            if not tareas:
                print("⚠️ No hay tareas para generar el horario.")
                continue

            modo = input("Modo (ordenado/aleatorio): ").lower()
            if modo not in ["ordenado", "aleatorio"]:
                modo = "ordenado"

            usar_descansos = input("¿Insertar descansos? (s/n): ").lower() == "s"

            horario = crear_horario(dias)
            asignar_tareas(tareas, dias, horas_por_dia, horario, modo)

            if usar_descansos:
                insertar_descansos(horario)

            mostrar_horario(horario)

        # -------------------------
        # 4. Exportar JSON
        # -------------------------
        elif opcion == "4":
            if horario is None:
                print("⚠️ Primero genera un horario.")
            else:
                exportar_json(horario)

        # -------------------------
        # 5. Salir
        # -------------------------
        elif opcion == "5":
            print("👋 Saliendo del programa...")
            break

        else:
            print("❌ Opción no válida.")


if __name__ == "__main__":
    main()
