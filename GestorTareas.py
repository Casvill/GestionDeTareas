import Tarea
from AVL import AVLTree
from Heap import MaxHeap

class GestorTareas:
    #------------------------------------------------------------------------------------
    def __init__(self):
        self.heap = MaxHeap()
        self.avl = AVLTree()
        self.raiz_avl = None
        self.historial = []
    #------------------------------------------------------------------------------------
    def agregar(self, id, descripcion, prioridad, fecha_creacion, fecha_vencimiento):
        if self.avl.buscar(self.raiz_avl, int(id)):
            return False, "ID ya existe"
        
        nueva = Tarea.Tarea(id, descripcion, prioridad, fecha_creacion,fecha_vencimiento)
        self.heap.insertar(nueva)
        self.raiz_avl = self.avl.insertar(self.raiz_avl, nueva)
        return True, "Tarea agregada"
    #------------------------------------------------------------------------------------
    def registrar_historial(self, tarea, estado):
        tarea.estado_final = estado
        self.historial.append({
            "id": tarea.id,
            "descripcion": tarea.descripcion,
            "prioridad": tarea.prioridad_str,
            "fecha_creacion": tarea.fecha_creacion,
            "fecha_vencimiento": tarea.fecha_vencimiento,
            "estado_final": tarea.estado_final
        })
    #------------------------------------------------------------------------------------
    def atender_prioritaria(self):
        while True:
            tarea = self.heap.extraer_maximo()
            if not tarea:
                return None

            if tarea.estado_final == "Activa":
                self.eliminar_fisico(tarea.id)
                self.registrar_historial(tarea, "Atendida")
                return tarea
    #------------------------------------------------------------------------------------
    def buscar(self, id_tarea):
        nodo = self.avl.buscar(self.raiz_avl, int(id_tarea))
        if nodo and nodo.tarea.estado_final == "Activa":
            #print("GestorTareas -> buscar")
            return nodo.tarea
        return None
    #------------------------------------------------------------------------------------
    def listar_todas(self):
        res = []
        self.avl.recorrido_inorder(self.raiz_avl, res)
        return res
    #------------------------------------------------------------------------------------
    def eliminar_fisico(self, id_tarea):
        id_tarea = int(id_tarea)
        nodo = self.avl.buscar(self.raiz_avl, id_tarea)

        if not nodo:
            return False, "No existe una tarea con ese ID"

        tarea = nodo.tarea

        self.heap.eliminar_por_id(id_tarea)
        self.raiz_avl = self.avl.eliminar(self.raiz_avl, id_tarea)

        tarea.estado_final = "Eliminada"
        return True, "Tarea eliminada físicamente"
    #------------------------------------------------------------------------------------
    def eliminar_vencidas(self, fecha_actual):
        vencidas = []
        tareas = self.listar_todas()

        for tarea in tareas:
            if tarea.fecha < fecha_actual:
                vencidas.append(tarea)

        for t in vencidas:
            self.eliminar_fisico(t.id)
            self.registrar_historial(t, "Vencida")

        return len(vencidas)
    #------------------------------------------------------------------------------------