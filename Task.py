class Task:
    def __init__(self, id_tarea, descripcion, prioridad, fecha_creacion, fecha_vencimiento):
        self.id = int(id_tarea)
        self.descripcion = descripcion
        self.prioridad_str = prioridad
        self.prioridad_val = self._asignar_valor_prioridad(prioridad)
        self.fecha_creacion = fecha_creacion
        self.fecha_vencimiento = fecha_vencimiento

        # Nuevo: estado de tarea (para historial)
        self.estado_final = "Activa"   # Activa | Atendida | Eliminada físicamente | Vencida

    def _asignar_valor_prioridad(self, p):
        if p == "Alta": return 3
        if p == "Media": return 2
        return 1

    def __lt__(self, other):
        return self.prioridad_val < other.prioridad_val

    def __str__(self):
        return (
            f"ID: {self.id} \n"
            f"Descripción: {self.descripcion} \n"
            f"Prioridad: {self.prioridad_str} \n"
            f"Fecha de creación: {self.fecha_creacion} \n"
            f"Fecha de vencimiento: {self.fecha_vencimiento} \n"
            f"Estado: {self.estado_final}"
        )

