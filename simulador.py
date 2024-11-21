import os

# Planificación de Procesos
class ProcessScheduler:
    def __init__(self):
        self.processes = []

    def add_process(self, name, burst_time, priority):
        """Agrega un nuevo proceso a la lista."""
        self.processes.append({"name": name, "burst_time": burst_time, "priority": priority})

    def fifo(self):
        """Planificación FIFO: procesa en orden de llegada."""
        total_wait_time = 0
        total_turnaround_time = 0
        current_time = 0

        print("\nFIFO Scheduling:")
        for process in self.processes:
            wait_time = current_time
            turnaround_time = wait_time + process["burst_time"]
            total_wait_time += wait_time
            total_turnaround_time += turnaround_time

            print(f"Process {process['name']} -> Wait Time: {wait_time}, Turnaround Time: {turnaround_time}")
            current_time += process["burst_time"]

        n = len(self.processes)
        print(f"Average Wait Time: {total_wait_time / n}, Average Turnaround Time: {total_turnaround_time / n}")

    def sjf(self):
        """Planificación SJF: procesa el de menor tiempo de ráfaga."""
        sorted_processes = sorted(self.processes, key=lambda x: x["burst_time"])
        total_wait_time = 0
        total_turnaround_time = 0
        current_time = 0

        print("\nSJF Scheduling:")
        for process in sorted_processes:
            wait_time = current_time
            turnaround_time = wait_time + process["burst_time"]
            total_wait_time += wait_time
            total_turnaround_time += turnaround_time

            print(f"Process {process['name']} -> Wait Time: {wait_time}, Turnaround Time: {turnaround_time}")
            current_time += process["burst_time"]

        n = len(sorted_processes)
        print(f"Average Wait Time: {total_wait_time / n}, Average Turnaround Time: {total_turnaround_time / n}")

    def round_robin(self, quantum):
        """Planificación Round Robin."""
        from collections import deque
        queue = deque(self.processes)
        current_time = 0
        total_wait_time = 0
        total_turnaround_time = 0

        print("\nRound Robin Scheduling:")
        while queue:
            process = queue.popleft()
            if process["burst_time"] > quantum:
                current_time += quantum
                process["burst_time"] -= quantum
                queue.append(process)
            else:
                current_time += process["burst_time"]
                process["burst_time"] = 0
                wait_time = current_time - process["burst_time"]
                turnaround_time = current_time
                total_wait_time += wait_time
                total_turnaround_time += turnaround_time

                print(f"Process {process['name']} -> Wait Time: {wait_time}, Turnaround Time: {turnaround_time}")

        n = len(self.processes)
        print(f"Average Wait Time: {total_wait_time / n}, Average Turnaround Time: {total_turnaround_time / n}")

# Administración de Memoria
class MemoryManager:
    def __init__(self, memory_size, page_size):
        self.memory_size = memory_size
        self.page_size = page_size
        self.pages = [-1] * (memory_size // page_size)
        self.page_queue = []  # Para FIFO
        self.page_access = {}  # Para LRU

    def allocate(self, process_id, process_size):
        """Asigna memoria para un proceso si hay suficiente espacio."""
        num_pages_needed = (process_size + self.page_size - 1) // self.page_size
        allocated_pages = 0

        for i in range(len(self.pages)):
            if self.pages[i] == -1:  # Si el marco está vacío
                self.pages[i] = process_id
                self.page_queue.append(process_id)
                allocated_pages += 1
                if allocated_pages == num_pages_needed:
                    return True  # Asignación exitosa

        # Si no hay suficiente espacio, revertimos los cambios
        for i in range(len(self.pages)):
            if self.pages[i] == process_id:
                self.pages[i] = -1
        return False  # No hay espacio suficiente

    def load_page(self, process_id, page_number):
        """Carga una página en memoria con manejo de reemplazo."""
        if process_id in self.pages:
            print(f"Page {page_number} of Process {process_id} already in memory.")
            return

        if -1 in self.pages:
            # Espacio disponible
            free_index = self.pages.index(-1)
            self.pages[free_index] = process_id
            self.page_queue.append(process_id)
            self.page_access[process_id] = free_index
            print(f"Loaded Page {page_number} of Process {process_id} into Frame {free_index}.")
        else:
            # Reemplazo FIFO
            evicted = self.page_queue.pop(0)
            evict_index = self.pages.index(evicted)
            self.pages[evict_index] = process_id
            self.page_queue.append(process_id)
            self.page_access[process_id] = evict_index
            print(f"Page {page_number} of Process {evicted} evicted. Loaded Process {process_id}.")

    def display_memory(self):
        """Muestra el estado actual de la memoria."""
        print("\nMemory State:")
        for i, process in enumerate(self.pages):
            print(f"Frame {i}: {'Empty' if process == -1 else f'Process {process}'}")


class FileSystem:
    def __init__(self, base_path="."):  # Cambia el directorio base al actual (raíz del proyecto)
        self.base_path = base_path

    def mkdir(self, name):
        """Crea un directorio físicamente."""
        dir_path = os.path.join(self.base_path, name)
        if os.path.exists(dir_path):
            print(f"Directory {name} already exists.")
        else:
            os.makedirs(dir_path)
            print(f"Directory {name} created.")

    def touch(self, name):
        """Crea un archivo físicamente."""
        file_path = os.path.join(self.base_path, name)
        if os.path.exists(file_path):
            print(f"File {name} already exists.")
        else:
            with open(file_path, "w") as f:
                pass
            print(f"File {name} created.")

    def write(self, name, content):
        """Escribe contenido en un archivo físicamente."""
        file_path = os.path.join(self.base_path, name)
        if os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(content)
            print(f"Content written to file {name}.")
        else:
            print(f"File {name} does not exist.")

    def read(self, name):
        """Lee el contenido de un archivo físicamente."""
        file_path = os.path.join(self.base_path, name)
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()
            print(f"Content of {name}: {content}")
        else:
            print(f"File {name} does not exist.")

    def rm(self, name):
        """Elimina un archivo o directorio físicamente."""
        path = os.path.join(self.base_path, name)
        if os.path.exists(path):
            if os.path.isdir(path):
                os.rmdir(path)
            else:
                os.remove(path)
            print(f"{name} deleted.")
        else:
            print(f"{name} does not exist.")

    def ls(self):
        """Lista los contenidos del directorio base."""
        contents = os.listdir(self.base_path)
        print("\nContents:")
        for item in contents:
            print(item)
