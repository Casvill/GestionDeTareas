class NodoAVL:
    def __init__(self, tarea):
        self.tarea = tarea
        self.izquierda = None
        self.derecha = None
        self.altura = 1


class AVLTree:

    #------------------ UTILIDADES BÁSICAS ------------------#
    def obtener_altura(self, nodo):
        return nodo.altura if nodo else 0

    def obtener_balance(self, nodo):
        return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha) if nodo else 0


    #------------------ ROTACIONES ------------------#
    def rotar_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha

        y.derecha = z
        z.izquierda = T3

        z.altura = 1 + max(self.obtener_altura(z.izquierda), self.obtener_altura(z.derecha))
        y.altura = 1 + max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha))

        return y

    def rotar_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda

        y.izquierda = z
        z.derecha = T2

        z.altura = 1 + max(self.obtener_altura(z.izquierda), self.obtener_altura(z.derecha))
        y.altura = 1 + max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha))

        return y


    #------------------ MÉTODO UNIFICADO: BALANCEAR ------------------#
    def balancear(self, nodo):
        """Revisa balance y aplica la rotación necesaria."""
        balance = self.obtener_balance(nodo)

        # Caso Izquierda-Izquierda
        if balance > 1 and self.obtener_balance(nodo.izquierda) >= 0:
            return self.rotar_derecha(nodo)

        # Caso Izquierda-Derecha
        if balance > 1 and self.obtener_balance(nodo.izquierda) < 0:
            nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
            return self.rotar_derecha(nodo)

        # Caso Derecha-Derecha
        if balance < -1 and self.obtener_balance(nodo.derecha) <= 0:
            return self.rotar_izquierda(nodo)

        # Caso Derecha-Izquierda
        if balance < -1 and self.obtener_balance(nodo.derecha) > 0:
            nodo.derecha = self.rotar_derecha(nodo.derecha)
            return self.rotar_izquierda(nodo)

        return nodo


    #------------------ INSERCIÓN ------------------#
    def insertar(self, nodo, tarea):
        if not nodo:
            return NodoAVL(tarea)

        if tarea.id < nodo.tarea.id:
            nodo.izquierda = self.insertar(nodo.izquierda, tarea)
        elif tarea.id > nodo.tarea.id:
            nodo.derecha = self.insertar(nodo.derecha, tarea)
        else:
            return nodo  # ID duplicado

        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierda),
                              self.obtener_altura(nodo.derecha))

        return self.balancear(nodo)


    #------------------ BUSCAR ------------------#
    def buscar(self, nodo, id_buscado):
        if not nodo or nodo.tarea.id == id_buscado:
            return nodo
        if id_buscado < nodo.tarea.id:
            return self.buscar(nodo.izquierda, id_buscado)
        return self.buscar(nodo.derecha, id_buscado)


    #------------------ RECORRIDO ------------------#
    def recorrido_inorder(self, nodo, lista_resultado):
        if nodo:
            self.recorrido_inorder(nodo.izquierda, lista_resultado)
            lista_resultado.append(nodo.tarea)
            self.recorrido_inorder(nodo.derecha, lista_resultado)


    #------------------ ELIMINAR (FÍSICO) ------------------#

    def minimo(self, nodo):
        """Devuelve el nodo con el valor más pequeño (más a la izquierda)."""
        actual = nodo
        while actual.izquierda:
            actual = actual.izquierda
        return actual

    def eliminar(self, nodo, id_tarea):
        if not nodo:
            return nodo

        # Buscar nodo a eliminar
        if id_tarea < nodo.tarea.id:
            nodo.izquierda = self.eliminar(nodo.izquierda, id_tarea)
        elif id_tarea > nodo.tarea.id:
            nodo.derecha = self.eliminar(nodo.derecha, id_tarea)
        else:
            # Caso 1: sin hijos
            if not nodo.izquierda and not nodo.derecha:
                return None

            # Caso 2: un hijo
            if not nodo.izquierda:
                return nodo.derecha
            elif not nodo.derecha:
                return nodo.izquierda

            # Caso 3: dos hijos
            sucesor = self.minimo(nodo.derecha)
            nodo.tarea = sucesor.tarea
            nodo.derecha = self.eliminar(nodo.derecha, sucesor.tarea.id)

        # Actualizar altura
        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierda),
                              self.obtener_altura(nodo.derecha))

        return self.balancear(nodo)
    



    #----------------MÉTODOS PARA IMPRIMIR EL AVL EN FORMATO ASCII---------------------------------------

    #------------------ IMPRIMIR AVL ------------------#
    def imprimir_arbol(self, nodo, nivel=0, prefijo="· "):
        """Imprime el árbol AVL horizontalmente (rotado 90°)."""
        if nodo is not None:
            # Primero imprime la derecha (se verá arriba)
            self.imprimir_arbol(nodo.derecha, nivel + 1, "↳ ")

            # Imprime el nodo actual
            print("    " * nivel + prefijo + f"[{nodo.tarea.id}] {nodo.tarea.descripcion}")

            # Luego imprime la izquierda (se verá abajo)
            self.imprimir_arbol(nodo.izquierda, nivel + 1, "↲ ")

    #------------------ IMPRIMIR AVL EN VERTICAL ------------------#
    def imprimir_vertical(self, nodo, prefijo="", es_ultimo=True):
        """Imprime el árbol AVL de forma vertical (padre arriba, hijos abajo)."""

        if nodo is None:
            return

        # Dibujar prefijo del nodo
        print(prefijo + ("└── " if es_ultimo else "├── ") + f"[{nodo.tarea.id}] {nodo.tarea.descripcion}")

        # Prefijo para hijos
        nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")

        hijos = []
        if nodo.izquierda:
            hijos.append(("izq", nodo.izquierda))
        if nodo.derecha:
            hijos.append(("der", nodo.derecha))

        for i, (_, hijo) in enumerate(hijos):
            self.imprimir_vertical(hijo, nuevo_prefijo, i == len(hijos) - 1)

    #------------------ IMPRIMIR AVL (ESTILO LEETCODE) ------------------#
    def imprimir_arb_leetcode(self, root):
        """Imprime el árbol AVL centrado con formato estilo LeetCode."""

        if not root:
            print("Árbol vacío")
            return

        # Obtener altura del árbol
        def altura(nodo):
            if not nodo:
                return 0
            return 1 + max(altura(nodo.izquierda), altura(nodo.derecha))

        h = altura(root)

        # Obtener nodos por nivel
        def obtener_nivel(nodos):
            nuevo_nivel = []
            valores = []
            for nodo in nodos:
                if nodo:
                    valores.append(str(nodo.tarea.id))
                    nuevo_nivel.append(nodo.izquierda)
                    nuevo_nivel.append(nodo.derecha)
                else:
                    valores.append(None)
                    nuevo_nivel.append(None)
                    nuevo_nivel.append(None)
            return valores, nuevo_nivel

        # Cantidad máxima de nodos en el último nivel
        max_nodos = 2 ** h
        max_ancho = max_nodos * 4  # espacio horizontal base

        nivel = [root]

        for i in range(h):

            valores, nivel = obtener_nivel(nivel)

            # Remover niveles completamente vacíos
            if all(v is None for v in valores):
                break

            nivel_ancho = max_ancho // (2 ** i)

            linea = ""
            for v in valores:
                if v is None:
                    linea += " " * (nivel_ancho // 2) + " " + " " * (nivel_ancho // 2)
                else:
                    v = "[" + v + "]"
                    linea += " " * (nivel_ancho // 2 - len(v)//2) + v + " " * (nivel_ancho // 2 - len(v)//2)

            print(linea)

            # Dibujar ramas / \
            if i < h - 1:
                rama_line = ""
                for v in valores:
                    espacio = nivel_ancho // 2
                    if v is None:
                        rama_line += " " * (nivel_ancho)
                    else:
                        rama_line += " " * (espacio - 1) + "/" + " " * 2 + "\\" + " " * (espacio - 3)
                print(rama_line)

        print("---------------------------------------------------------")

    #----------------------------------------------------------------------------------------------
