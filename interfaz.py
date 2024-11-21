import tkinter as tk
from tkinter import simpledialog, messagebox
import os
from simulador import ProcessScheduler, MemoryManager, FileSystem

# Instancias globales
scheduler = ProcessScheduler()
memory_manager = MemoryManager(memory_size=16, page_size=4)
file_system = FileSystem()

# Colores y estilos
BG_COLOR = "#282c34"  # Fondo principal
BTN_BG_COLOR = "#61afef"  # Fondo de botones
BTN_FG_COLOR = "#ffffff"  # Texto de botones
TEXT_BG_COLOR = "#21252b"  # Fondo de áreas de texto
TEXT_FG_COLOR = "#abb2bf"  # Texto de áreas de texto
FONT_STYLE = ("Helvetica", 12)

# Funciones de Planificación de Procesos
def open_process_scheduler():
    scheduler_window = tk.Toplevel(bg=BG_COLOR)
    scheduler_window.title("Planificación de Procesos")
    scheduler_window.geometry("400x400")
    tk.Label(scheduler_window, text="Planificación de Procesos", font=("Helvetica", 16), bg=BG_COLOR, fg=BTN_FG_COLOR).pack(pady=10)

    text_widget = tk.Text(scheduler_window, height=10, width=50, bg=TEXT_BG_COLOR, fg=TEXT_FG_COLOR, font=FONT_STYLE)
    text_widget.pack(pady=10)

    def actualizar_estado_memoria():
        memoria_estado = "Estado de Memoria:\n"
        for i, proceso in enumerate(memory_manager.pages):
            memoria_estado += f"Frame {i}: {'Vacío' if proceso == -1 else f'Proceso {proceso}'}\n"
        text_widget.insert(tk.END, memoria_estado)

    def add_process():
        name = simpledialog.askstring("Agregar Proceso", "Nombre del proceso:")
        burst_time = simpledialog.askinteger("Agregar Proceso", "Tiempo de ráfaga:")
        priority = simpledialog.askinteger("Agregar Proceso", "Prioridad:")
        if name and burst_time and priority is not None:
            if memory_manager.allocate(name, burst_time):  # Intentar asignar memoria
                scheduler.add_process(name, burst_time, priority)
                text_widget.insert(tk.END, f"Proceso '{name}' agregado con tiempo de ráfaga {burst_time} y prioridad {priority}.\n")
            else:
                text_widget.insert(tk.END, f"Error: No hay suficiente memoria para el proceso '{name}'.\n")
        else:
            text_widget.insert(tk.END, "Error: Datos inválidos para el proceso.\n")

    def execute_fifo():
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, "Planificación FIFO:\n")
        total_wait_time = 0
        total_turnaround_time = 0
        current_time = 0

        for process in scheduler.processes:
            wait_time = current_time
            turnaround_time = wait_time + process["burst_time"]
            total_wait_time += wait_time
            total_turnaround_time += turnaround_time
            resultado = f"Proceso {process['name']} -> Tiempo de espera: {wait_time}, Tiempo de retorno: {turnaround_time}\n"
            text_widget.insert(tk.END, resultado)
            current_time += process["burst_time"]

        n = len(scheduler.processes)
        promedios = f"Promedio de espera: {total_wait_time / n}, Promedio de retorno: {total_turnaround_time / n}\n"
        text_widget.insert(tk.END, promedios)

    def execute_sjf():
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, "Planificación SJF:\n")
        sorted_processes = sorted(scheduler.processes, key=lambda x: x["burst_time"])
        total_wait_time = 0
        total_turnaround_time = 0
        current_time = 0

        for process in sorted_processes:
            wait_time = current_time
            turnaround_time = wait_time + process["burst_time"]
            total_wait_time += wait_time
            total_turnaround_time += turnaround_time

            resultado = f"Proceso {process['name']} -> Tiempo de espera: {wait_time}, Tiempo de retorno: {turnaround_time}\n"
            text_widget.insert(tk.END, resultado)
            current_time += process["burst_time"]

        n = len(sorted_processes)
        promedios = f"Promedio de espera: {total_wait_time / n}, Promedio de retorno: {total_turnaround_time / n}\n"
        text_widget.insert(tk.END, promedios)

    def execute_rr():
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, "Planificación Round Robin:\n")
        quantum = simpledialog.askinteger("Round Robin", "Quantum:")
        if quantum:
            from collections import deque
            queue = deque(scheduler.processes)
            current_time = 0

            while queue:
                process = queue.popleft()
                if process["burst_time"] > quantum:
                    current_time += quantum
                    process["burst_time"] -= quantum
                    queue.append(process)
                else:
                    current_time += process["burst_time"]
                    process["burst_time"] = 0
                    resultado = f"Proceso {process['name']} -> Completado en el tiempo: {current_time}\n"
                    text_widget.insert(tk.END, resultado)
        else:
            text_widget.insert(tk.END, "Error: Quantum inválido.\n")

    tk.Button(scheduler_window, text="Agregar Proceso", command=add_process, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=5)
    tk.Button(scheduler_window, text="Ejecutar FIFO", command=execute_fifo, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=5)
    tk.Button(scheduler_window, text="Ejecutar SJF", command=execute_sjf, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=5)
    tk.Button(scheduler_window, text="Ejecutar Round Robin", command=execute_rr, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=5)
    tk.Button(scheduler_window, text="Cerrar", command=scheduler_window.destroy, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=5)

# Funciones del Sistema de Archivos
def create_directory(text_widget):
    name = simpledialog.askstring("Crear Directorio", "Nombre del directorio:")
    if name:
        if not os.path.exists(name):
            os.makedirs(name)
            text_widget.insert(tk.END, f"Directorio '{name}' creado.\n")
        else:
            text_widget.insert(tk.END, f"El directorio '{name}' ya existe.\n")
    else:
        text_widget.insert(tk.END, "Error: Nombre inválido.\n")

def create_file(text_widget):
    name = simpledialog.askstring("Crear Archivo", "Nombre del archivo:")
    if name:
        if not os.path.exists(name):
            with open(name, "w") as f:
                pass
            text_widget.insert(tk.END, f"Archivo '{name}' creado.\n")
        else:
            text_widget.insert(tk.END, f"El archivo '{name}' ya existe.\n")
    else:
        text_widget.insert(tk.END, "Error: Nombre inválido.\n")

def write_file(text_widget):
    name = simpledialog.askstring("Escribir en Archivo", "Nombre del archivo:")
    if name:
        content = simpledialog.askstring("Escribir en Archivo", "Contenido:")
        if os.path.exists(name):
            with open(name, "w") as f:
                f.write(content)
            text_widget.insert(tk.END, f"Contenido escrito en '{name}'.\n")
        else:
            text_widget.insert(tk.END, f"El archivo '{name}' no existe.\n")
    else:
        text_widget.insert(tk.END, "Error: Nombre inválido.\n")

def read_file(text_widget):
    name = simpledialog.askstring("Leer Archivo", "Nombre del archivo:")
    if name:
        if os.path.exists(name):
            with open(name, "r") as f:
                content = f.read()
            text_widget.insert(tk.END, f"Contenido de '{name}': {content}\n")
        else:
            text_widget.insert(tk.END, f"El archivo '{name}' no existe.\n")
    else:
        text_widget.insert(tk.END, "Error: Nombre inválido.\n")

def delete_file_or_dir(text_widget):
    name = simpledialog.askstring("Eliminar", "Nombre del archivo/directorio:")
    if name:
        if os.path.exists(name):
            if os.path.isdir(name):
                os.rmdir(name)
            else:
                os.remove(name)
            text_widget.insert(tk.END, f"'{name}' eliminado correctamente.\n")
        else:
            text_widget.insert(tk.END, f"'{name}' no existe.\n")
    else:
        text_widget.insert(tk.END, "Error: Nombre inválido.\n")

def list_contents(text_widget):
    contents = os.listdir(".")
    text_widget.insert(tk.END, "Contenido del directorio raíz:\n")
    for item in contents:
        text_widget.insert(tk.END, f"{item}\n")
    text_widget.insert(tk.END, "\n")

def open_file_system():
    fs_window = tk.Toplevel(bg=BG_COLOR)
    fs_window.title("Sistema de Archivos")
    fs_window.geometry("500x400")
    tk.Label(fs_window, text="Sistema de Archivos (Físico)", font=("Helvetica", 16), bg=BG_COLOR, fg=BTN_FG_COLOR).pack(pady=10)

    tk.Button(fs_window, text="Crear Directorio", command=lambda: create_directory(text_widget), bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=5)
    tk.Button(fs_window, text="Crear Archivo", command=lambda: create_file(text_widget), bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=5)
    tk.Button(fs_window, text="Escribir en Archivo", command=lambda: write_file(text_widget), bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=5)
    tk.Button(fs_window, text="Leer Archivo", command=lambda: read_file(text_widget), bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=5)
    tk.Button(fs_window, text="Eliminar", command=lambda: delete_file_or_dir(text_widget), bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=5)
    tk.Button(fs_window, text="Listar Contenidos", command=lambda: list_contents(text_widget), bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=5)
    tk.Button(fs_window, text="Cerrar", command=fs_window.destroy, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=10)
    
    text_widget = tk.Text(fs_window, height=15, width=60, bg=TEXT_BG_COLOR, fg=TEXT_FG_COLOR, font=FONT_STYLE)
    text_widget.pack(pady=10)

def open_memory_manager():
    memory_window = tk.Toplevel(bg=BG_COLOR)
    memory_window.title("Administración de Memoria")
    memory_window.geometry("400x300")
    tk.Label(memory_window, text="Administración de Memoria", font=("Helvetica", 16), bg=BG_COLOR, fg=BTN_FG_COLOR).pack(pady=10)

    text_widget = tk.Text(memory_window, height=10, width=50, bg=TEXT_BG_COLOR, fg=TEXT_FG_COLOR, font=FONT_STYLE)
    text_widget.pack(pady=10)

    def show_memory_state():
        text_widget.delete(1.0, tk.END)  # Limpia el área de texto
        text_widget.insert(tk.END, "Estado de Memoria:\n")
        for i, process in enumerate(memory_manager.pages):
            state = f"Frame {i}: {'Vacío' if process == -1 else f'Proceso {process}'}\n"
            text_widget.insert(tk.END, state)

    tk.Button(memory_window, text="Mostrar Estado de Memoria", command=show_memory_state, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=5)
    tk.Button(memory_window, text="Cerrar", command=memory_window.destroy, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=5)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Simulador de Sistema Operativo")
root.geometry("400x300")
root.configure(bg=BG_COLOR)

tk.Label(root, text="Simulador de Sistema Operativo", font=("Helvetica", 16), bg=BG_COLOR, fg=BTN_FG_COLOR).pack(pady=20)
tk.Button(root, text="Planificación de Procesos", width=25, command=open_process_scheduler, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=10)
tk.Button(root, text="Administración de Memoria", width=25, command=open_memory_manager, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=10)
tk.Button(root, text="Sistema de Archivos (Físico)", width=25, command=open_file_system, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=10)
tk.Button(root, text="Salir", width=25, command=root.quit, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR).pack(pady=10)

# Iniciar la interfaz
root.mainloop()

