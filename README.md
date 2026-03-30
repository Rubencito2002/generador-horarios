# 🗓️ Generador de Horarios Automáticos

Un proyecto en Python diseñado para generar horarios de forma automática a partir de una lista de tareas, su duración y las restricciones definidas por el usuario.  
Este proyecto evoluciona por fases, cada una añadida en ramas separadas para mantener un control de versiones profesional.

---

## 🚀 Características principales

- Añadir tareas manualmente desde consola  
- Generar horarios automáticamente  
- Dos modos de asignación:
    - **Ordenado** (tareas largas primero)
    - **Aleatorio**
- Evita tareas repetidas consecutivas  
- Inserta descansos automáticos opcionales  
- Exportación del horario a **JSON**  
- Interfaz por consola (versión actual)

---

## 🧩 Tecnologías utilizadas

- **Python 3.10+**
- Estructuras de datos (listas, diccionarios)
- Control de flujo y validaciones
- Entrada interactiva por consola
- Exportación a archivos JSON

---

## 📂 Estructura del proyecto
generador_horarios/
│
├── main.py          # Código principal del generador
├── horario.json     # Archivo exportado (se genera al usar la app)
└── README.md        # Este archivo

---

## 🖥️ Cómo ejecutar el proyecto

1. Clona el repositorio:

```bash
    git clone https://github.com/Rubencito2002/generador-horarios.git
```
2. Entra en la carpeta:
```bash
    cd generador-horarios
```
3. Ejecuta el programa:
```bash
    python main.py
```
---

## 🧪 Uso del programa
Al ejecutar main.py, verás un menú interactivo:
```bash
    1. Añadir tarea
    2. Ver tareas actuales
    3. Generar horario
    4. Exportar horario a JSON
    5. Salir
```
Puedes añadir tantas tareas como quieras, elegir el modo de generación y decidir si quieres descansos automáticos.

---

## 🌿 Control de versiones (Ramas)
El proyecto sigue un flujo de trabajo basado en ramas:

main → versión estable

v1-basico → versión inicial con asignación simple
v2-mejoras → validaciones, descansos, ordenación
v3-interactivo → menú por consola (versión actual)
v4-grafica → interfaz gráfica (próxima fase)

---

## 🛣️ Roadmap
[x] Versión básica funcional

[x] Validaciones y descansos

[x] Interfaz por consola

[ ] Interfaz gráfica con Tkinter

[ ] Exportación a CSV

[ ] Sistema de prioridades

[ ] API REST con Flask o FastAPI

[ ] Versión web completa

### 🤝 Contribuciones
Este proyecto está en evolución constante.
Si quieres proponer mejoras, abre un issue o envía un pull request.

#### 📄 Licencia
Este proyecto se distribuye bajo la licencia MIT.
Puedes usarlo, modificarlo y compartirlo libremente.

```bash
    ---
    Cuando lo pegues en tu repo, quedará perfecto.

    ¿Listo para empezar la **siguiente fase**?  
    Si quieres, arrancamos ya con la **interfaz gráfica (Tkinter)** o con una mejora adicional en la versión de consola.
```