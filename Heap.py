class MaxHeap:
    def __init__(self):
        self.heap = []

    def insertar(self, tarea):
        self.heap.append(tarea)
        self._sift_up(len(self.heap) - 1)

    def extraer_maximo(self):
        if not self.heap:
            return None

        max_tarea = self.heap[0]
        ultimo = self.heap.pop()

        if self.heap:
            self.heap[0] = ultimo
            self._sift_down(0)

        return max_tarea


    def buscar_indice_por_id(self, id_tarea):
        for i, tarea in enumerate(self.heap):
            if tarea.id == id_tarea:
                return i
        return -1

    def eliminar_por_id(self, id_tarea):
        idx = self.buscar_indice_por_id(id_tarea)
        if idx == -1:
            return False  # No existe en el heap

        ultimo = len(self.heap) - 1

        # Si es el último, simplemente pop
        if idx == ultimo:
            self.heap.pop()
            return True

        # Intercambiar con el último
        self.heap[idx], self.heap[ultimo] = self.heap[ultimo], self.heap[idx]
        self.heap.pop()

        # Reacomodar heap
        self._sift_up(idx)
        self._sift_down(idx)

        return True

    # ---------------- sift up / down -----------------------------

    def _sift_up(self, idx):
        padre = (idx - 1) // 2
        if padre >= 0 and self.heap[idx].prioridad_val > self.heap[padre].prioridad_val:
            self.heap[idx], self.heap[padre] = self.heap[padre], self.heap[idx]
            self._sift_up(padre)

    def _sift_down(self, idx):
        mayor = idx
        izq = 2 * idx + 1
        der = 2 * idx + 2
        n = len(self.heap)

        if izq < n and self.heap[izq].prioridad_val > self.heap[mayor].prioridad_val:
            mayor = izq
        if der < n and self.heap[der].prioridad_val > self.heap[mayor].prioridad_val:
            mayor = der

        if mayor != idx:
            self.heap[idx], self.heap[mayor] = self.heap[mayor], self.heap[idx]
            self._sift_down(mayor)

    def imprimir_como_arbol(self):
        if not self.heap:
            print("Heap vacío.")
            return

        nivel = 0
        cantidad = 1
        idx = 0
        n = len(self.heap)

        print("\n===== HEAP COMO ÁRBOL =====")

        while idx < n:
            # elementos del nivel actual
            fila = self.heap[idx : idx + cantidad]

            # imprimir nivel
            print(f"Nivel {nivel}: ", end="")
            for t in fila:
                print(f"[ID {t.id} | Prio {t.prioridad_val}]", end="  ")
            print()

            idx += cantidad
            cantidad *= 2
            nivel += 1

        print("===========================\n")

    def imprimir_con_ramas(self):
        if not self.heap:
            print("Heap vacío.")
            return

        print("\n========== ÁRBOL DEL HEAP ==========\n")

        def _imprimir(idx, espacio):
            if idx >= len(self.heap):
                return

            # incrementa espacio para nivel siguiente
            espacio += 10  

            # primero imprime subárbol derecho
            _imprimir(2 * idx + 2, espacio)

            # imprime nodo actual
            print(" " * (espacio - 10) + f"[{self.heap[idx].id}|{self.heap[idx].prioridad_val}]")

            # imprime rama izquierda
            _imprimir(2 * idx + 1, espacio)

        _imprimir(0, 0)

        print("\n=====================================\n")

    def imprimir_arbol_centrado(self):
        if not self.heap:
            print("Heap vacío.")
            return

        import math

        n = len(self.heap)
        niveles = math.floor(math.log2(n)) + 1

        print("\n=========== HEAP (Árbol Centrado) ===========\n")

        index = 0
        max_width = 2 ** niveles * 4  # ancho total aproximado

        for nivel in range(niveles):
            nodos_en_nivel = 2 ** nivel
            espacio_entre = max_width // (nodos_en_nivel + 1)

            linea_valores = ""
            linea_ramas = ""

            for i in range(nodos_en_nivel):
                if index < n:
                    tarea = self.heap[index]
                    nodo_str = f"[{tarea.id}|{tarea.prioridad_val}]"
                    linea_valores += " " * espacio_entre + nodo_str
                    index += 1
                else:
                    break

            print(linea_valores)

            # Dibujar ramas entre niveles
            if nivel < niveles - 1:
                for i in range(nodos_en_nivel):
                    linea_ramas += " " * espacio_entre + "/ \\"

                print(linea_ramas)
                print()

        print("\n=============================================\n")
