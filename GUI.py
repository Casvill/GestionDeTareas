import tkinter as tk
from tkinter import messagebox, ttk
import GestorTareas
import datetime
from tkcalendar import DateEntry

# Matplotlib para las visualizaciones embebidas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import patches


class App:

    #------------------------------------------------------------------------------------
    def __init__(self, root):

        self.gestor = GestorTareas.GestorTareas()
        self.root = root
        self.root.title("Sistema de Gestión de Tareas (Heap + AVL)")
        self.root.geometry("1150x720")
        self.root.configure(bg="#eef1f5")   # Fondo moderno


        # =========================== ESTILO GENERAL ===================================
        style = ttk.Style()
        style.theme_use("clam")

        # --- Labels, frames, encabezados ---
        style.configure("TLabel", background="#eef1f5", font=("Segoe UI", 10))
        style.configure("Title.TLabelframe", background="#eef1f5")
        style.configure("TLabelframe.Label", background="#eef1f5",
                        font=("Segoe UI", 11, "bold"))
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 10, "bold"),
                        background="#dfe3ee")
        style.configure("Treeview", rowheight=25)

        # --- Combobox ---
        style.configure("TCombobox",
                        fieldbackground="#ffffff",
                        background="#ffffff",
                        foreground="#000000")
        
        # --- Combobox en modo readonly ---
        style.map("TCombobox",
            fieldbackground=[("readonly", "#ffffff")],   # Fondo dentro del combobox
            foreground=[("readonly", "#000000")],
            background=[("readonly", "#ffffff")])

        # =========================================================================================



        # ============================== BOTÓN REDONDO PERSONALIZADO =========================
        def rounded_button(parent, text, cmd, color):
            return tk.Button(
                parent, text=text, command=cmd,
                bg=color, fg="#000",
                relief="flat", padx=13, pady=6,
                bd=0, highlightthickness=0,
                font=("Segoe UI", 10)
            )
        # =========================================================================================



        # ========================= PANEL: NUEVA TAREA ===========================================
        frame_in = ttk.Labelframe(root, text="Nueva Tarea",
                                style="Title.TLabelframe", padding=10)
        frame_in.pack(fill="x", padx=15, pady=10)

        ttk.Label(frame_in, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = ttk.Entry(frame_in, width=12)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_in, text="Descripción:").grid(row=0, column=2, padx=5)
        self.entry_desc = ttk.Entry(frame_in, width=40)
        self.entry_desc.grid(row=0, column=3, padx=5)

        ttk.Label(frame_in, text="Prioridad:").grid(row=0, column=4, padx=5)
        self.combo_prio = ttk.Combobox(
            frame_in, values=["Alta", "Media", "Baja"],
            state="readonly", width=10
        )
        self.combo_prio.current(1)
        self.combo_prio.grid(row=0, column=5, padx=5)

        ttk.Label(frame_in, text="Vence:").grid(row=0, column=6)
        self.selector_fecha = DateEntry(frame_in, width=12,
                                        date_pattern='yyyy-mm-dd')
        self.selector_fecha.grid(row=0, column=7, padx=5)

        # Botón "Agregar" estilo pastel
        rounded_button(frame_in, "Agregar Tarea",
                    self.agregar_tarea, "#c6f7d0").grid(row=0, column=8, padx=15)
        # =========================================================================================



        # ========================== PANEL: ACCIONES =============================================
        frame_act = tk.Frame(root, bg="#eef1f5")
        frame_act.pack(fill="x", pady=5)

        rounded_button(frame_act, "Atender más urgente (Heap)",
                    self.atender, "#ffd6d6").pack(side="left", padx=10)

        ttk.Label(frame_act, text="Buscar ID:",
                background="#eef1f5").pack(side="left", padx=5)
        self.entry_buscar = ttk.Entry(frame_act, width=12)
        self.entry_buscar.pack(side="left")

        rounded_button(frame_act, "Buscar (AVL)",
                    self.buscar, "#d4e4ff").pack(side="left", padx=10)

        rounded_button(frame_act, "Historial",
                    self.ver_historial, "#fff2c6").pack(side="left", padx=10)

        # botones para refrescar visualizaciones
        rounded_button(frame_act, "Refrescar AVL (Visual)", self.dibujar_avl, "#e0ffe4").pack(side="right", padx=8)
        rounded_button(frame_act, "Refrescar Heap (Visual)", self.dibujar_heap, "#e0f7ff").pack(side="right", padx=8)
        
        # =========================================================================================



        # ============================ NOTEBOOK: Tabla + Visual ===================================
        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=15, pady=10)

        # -- Pestaña: Tabla (tu Treeview original)
        frame_tabla = ttk.Frame(notebook)
        frame_tabla.pack(fill="both", expand=True)
        notebook.add(frame_tabla, text="Tabla")

        self.tree = ttk.Treeview(frame_tabla,
                                columns=("ID", "Descripción", "Prioridad", "Fecha creación", "Vencimiento"),
                                show="headings")
        self.tree.tag_configure("prio_alta", background="#ffc9c9")    # rojo suave
        self.tree.tag_configure("prio_media", background="#fff4c2")   # amarillo pastel
        self.tree.tag_configure("prio_baja", background="#d6ffd6")    # verde suave


        for col in ("ID", "Descripción", "Prioridad", "Fecha creación", "Vencimiento"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # -- Pestaña: Visual (Heap arriba, AVL abajo)
        frame_visual = ttk.Frame(notebook)
        frame_visual.pack(fill="both", expand=True)
        notebook.add(frame_visual, text="Visual")

        # dividir verticalmente: top = heap, bottom = avl
        frame_heap_viz = ttk.Frame(frame_visual)
        frame_heap_viz.pack(fill="both", expand=True, padx=5, pady=5)

        frame_avl_viz = ttk.Frame(frame_visual)
        frame_avl_viz.pack(fill="both", expand=True, padx=5, pady=5)

        # Figura heap
        self.fig_heap = Figure(figsize=(8, 3.2), tight_layout=True)
        self.ax_heap = self.fig_heap.add_subplot(111)
        self.canvas_heap = FigureCanvasTkAgg(self.fig_heap, master=frame_heap_viz)
        self.canvas_heap.get_tk_widget().pack(fill="both", expand=True)

        # Figura avl
        self.fig_avl = Figure(figsize=(8, 3.2), tight_layout=True)
        self.ax_avl = self.fig_avl.add_subplot(111)
        self.canvas_avl = FigureCanvasTkAgg(self.fig_avl, master=frame_avl_viz)
        self.canvas_avl.get_tk_widget().pack(fill="both", expand=True)
        # =========================================================================================


        # Inicializar vistas (vacias)
        self.actualizar_lista()
        self.dibujar_heap()
        self.dibujar_avl()


    #------------------------------------------------------------------------------------
    def actualizar_lista(self):
        # Limpiar tabla
        for i in self.tree.get_children():
            self.tree.delete(i)

        tareas = self.gestor.listar_todas()

        for t in tareas:
            if t.prioridad_str == "Alta":
                tag = "prio_alta"
            elif t.prioridad_str == "Media":
                tag = "prio_media"
            else:
                tag = "prio_baja"

            self.tree.insert(
                "",
                "end",
                values=(t.id, t.descripcion, t.prioridad_str, t.fecha_creacion, t.fecha_vencimiento),
                tags=(tag,)
            )


    #------------------------------------------------------------------------------------
    def agregar_tarea(self):
        # Recolecta campos y solicita al gestor agregar tarea
        try:
            id_t = int(self.entry_id.get())
            desc = self.entry_desc.get()
            prio = self.combo_prio.get()
            fecha_creacion = datetime.date.today()
            fecha_vencimiento = self.selector_fecha.get_date()
            
            ok, msg = self.gestor.agregar(id_t, desc, prio, fecha_creacion, fecha_vencimiento)
            if ok:
                self.actualizar_lista()
                # refrescar visualizaciones
                self.dibujar_heap()
                self.dibujar_avl()
                self.entry_id.delete(0, 'end')
                self.entry_desc.delete(0, 'end')
            else:
                messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")

    #------------------------------------------------------------------------------------
    def atender(self):
        # Atiende la tarea más prioritaria y actualiza GUI
        tarea = self.gestor.atender_prioritaria()
        if tarea:
            messagebox.showinfo("Tarea Atendida", 
                                f"Se atendió la tarea {tarea.id}: {tarea.descripcion} \n"
                                f"Prioridad: {tarea.prioridad_str} \n"
                                f"Fecha de creación: {tarea.fecha_creacion} \n"
                                f"Fecha de vencimiento: {tarea.fecha_vencimiento} \n")
            self.actualizar_lista()
            # refrescar visualizaciones
            self.dibujar_heap()
            self.dibujar_avl()
        else:
            messagebox.showinfo("Info", "No hay tareas pendientes.")
        
        # depuración consola - mantuve tus prints
        print("HEAP:")
        self.gestor.heap.imprimir_arbol_centrado()
        print("AVL")
        self.gestor.avl.imprimir_arb_leetcode(self.gestor.raiz_avl)


    #------------------------------------------------------------------------------------
    def buscar(self):
        try:
            id_b = self.entry_buscar.get()
            tarea = self.gestor.buscar(id_b)
            if tarea:
                messagebox.showinfo("Encontrado", str(tarea))

                # Resaltar en la tabla
                for i in self.tree.get_children():
                    if self.tree.item(i, "values")[0] == str(tarea.id):
                        self.tree.selection_set(i)
                        self.tree.see(i)
            else:
                messagebox.showwarning("No encontrado", "No existe tarea con ese ID.")
        except:
            print("App -> buscar -> except")


    #------------------------------------------------------------------------------------
    def ver_historial(self):
        # Ventana que muestra las tareas atendidas (historial)
        ventana_h = tk.Toplevel(self.root)
        ventana_h.title("Historial de Tareas")
        ventana_h.geometry("1200x600")

        # Título
        tk.Label(ventana_h, text="Tareas Atendidas / Eliminadas / Vencidas",
                font=("Arial", 12, "bold")).pack(pady=10)

        # Tabla del historial (se agrega columna Estado)
        tree_h = ttk.Treeview(
            ventana_h,
            columns=("ID", "Desc", "Prio", "Fecha_C", "Fecha_V", "Estado"),
            show="headings"
        )

        tree_h.heading("ID", text="ID")
        tree_h.heading("Desc", text="Descripción")
        tree_h.heading("Prio", text="Prioridad")
        tree_h.heading("Fecha_C", text="Fecha Creación")
        tree_h.heading("Fecha_V", text="Fecha Vencimiento")
        tree_h.heading("Estado", text="Estado")  # ← NUEVA COLUMNA

        tree_h.pack(fill="both", expand=True, padx=10, pady=10)

        # Llenar tabla
        for t in self.gestor.historial:
            # historial guarda dicts según tu implementación
            tree_h.insert(
                "",
                "end",
                values=(t.get("id"), t.get("descripcion"), t.get("prioridad"),
                        t.get("fecha_creacion"), t.get("fecha_vencimiento"), t.get("estado_final"))
            )

        tk.Button(ventana_h, text="Cerrar", command=ventana_h.destroy).pack(pady=5)

    # -----------------------------------------------------------------------------------
    # ----------------------- Visualización: HEAP y AVL (Matplotlib) --------------------
    # -----------------------------------------------------------------------------------

    def dibujar_heap(self):
        """Dibuja el heap (self.gestor.heap.heap) como árbol completo por niveles."""
        self.ax_heap.clear()

        heap_list = getattr(self.gestor.heap, "heap", [])
        n = len(heap_list)

        if n == 0:
            self.ax_heap.text(0.5, 0.5, "Heap vacío", ha="center", va="center")
            self.ax_heap.set_axis_off()
            self.canvas_heap.draw()
            return

        # calcular niveles
        niveles = []
        i = 0
        count = 1
        while i < n:
            niveles.append(heap_list[i:i+count])
            i += count
            count *= 2

        # layout: x por posición en nivel, y por nivel
        niveles_count = len(niveles)
        for lvl, nodos in enumerate(niveles):
            y = 1 - (lvl + 1) / (niveles_count + 1)
            m = len(nodos)
            for j, tarea in enumerate(nodos):
                x = (j + 1) / (m + 1)
                # dibujar líneas hacia hijos si existen
                idx_global = sum(len(l) for l in niveles[:lvl]) + j
                left = 2 * idx_global + 1
                right = 2 * idx_global + 2

                # calcular coordenadas de hijos en su respectivo nivel
                if left < n:
                    # encontrar posición del hijo en su nivel
                    # left pertenece a nivel lvl+1, posición p_left en ese nivel:
                    next_nodes = niveles[lvl+1]
                    # la posición relativa del hijo en el siguiente nivel se puede derivar:
                    # p_left = index in next_nodes where global idx == left
                    # simple: compute cumulative to find index
                    cum = 0
                    for p_i in range(len(niveles[lvl+1])):
                        if sum(len(l) for l in niveles[:lvl+1]) + p_i == left:
                            p_left = p_i
                            break
                    else:
                        p_left = 0
                    x_left = (p_left + 1) / (len(niveles[lvl+1]) + 1)
                    y_left = 1 - (lvl + 2) / (niveles_count + 1)
                    self.ax_heap.plot([x, x_left], [y, y_left], linewidth=1, color="k")

                if right < n:
                    cum = 0
                    for p_i in range(len(niveles[lvl+1])):
                        if sum(len(l) for l in niveles[:lvl+1]) + p_i == right:
                            p_right = p_i
                            break
                    else:
                        p_right = 0
                    x_right = (p_right + 1) / (len(niveles[lvl+1]) + 1)
                    y_right = 1 - (lvl + 2) / (niveles_count + 1)
                    self.ax_heap.plot([x, x_right], [y, y_right], linewidth=1, color="k")

                # dibujar nodo (círculo)
                circ = patches.Circle((x, y), 0.03, facecolor="#a9d6ff", edgecolor="#0366d6")
                self.ax_heap.add_patch(circ)
                label = str(tarea.id) if hasattr(tarea, "id") else str(tarea)
                self.ax_heap.text(x, y, label, ha="center", va="center", fontsize=8)

        self.ax_heap.set_xlim(0, 1)
        self.ax_heap.set_ylim(0, 1)
        self.ax_heap.set_axis_off()
        self.canvas_heap.draw()

    def dibujar_avl(self):
        """Dibuja el árbol AVL a partir de self.gestor.raiz_avl (NodoAVL)."""
        self.ax_avl.clear()

        raiz = getattr(self.gestor, "raiz_avl", None)
        if not raiz:
            self.ax_avl.text(0.5, 0.5, "AVL vacío", ha="center", va="center")
            self.ax_avl.set_axis_off()
            self.canvas_avl.draw()
            return

        # calcular posiciones (in-order) para espacios x, y = depth
        posiciones = {}
        x_counter = [0]

        def asignar_x(nodo, depth=0):
            if not nodo:
                return
            asignar_x(nodo.izquierda, depth + 1)
            posiciones[nodo] = (x_counter[0], depth)
            x_counter[0] += 1
            asignar_x(nodo.derecha, depth + 1)

        asignar_x(raiz, 0)

        if not posiciones:
            self.ax_avl.text(0.5, 0.5, "AVL vacío", ha="center", va="center")
            self.ax_avl.set_axis_off()
            self.canvas_avl.draw()
            return

        # normalizar coordenadas: x -> [0.05,0.95], y -> [0.9,0.1] según depth
        max_x = max(x for x, y in posiciones.values())
        max_depth = max(y for x, y in posiciones.values())

        norm = {}
        for nodo, (x, d) in posiciones.items():
            nx = 0.05 + 0.9 * (x / (max_x if max_x > 0 else 1))
            ny = 0.9 - 0.8 * (d / (max_depth if max_depth > 0 else 1))
            norm[nodo] = (nx, ny)

        # dibujar aristas
        for nodo, (nx, ny) in norm.items():
            if getattr(nodo, "izquierda", None):
                child = nodo.izquierda
                cx, cy = norm[child]
                self.ax_avl.plot([nx, cx], [ny, cy], color="k", linewidth=1)
            if getattr(nodo, "derecha", None):
                child = nodo.derecha
                cx, cy = norm[child]
                self.ax_avl.plot([nx, cx], [ny, cy], color="k", linewidth=1)

        # dibujar nodos
        for nodo, (nx, ny) in norm.items():
            tid = nodo.tarea.id if hasattr(nodo.tarea, "id") else str(nodo.tarea)
            circ = patches.Circle((nx, ny), 0.03, facecolor="#c7f9d4", edgecolor="#2b8f4a")
            self.ax_avl.add_patch(circ)
            self.ax_avl.text(nx, ny, str(tid), ha="center", va="center", fontsize=8)

        self.ax_avl.set_xlim(0, 1)
        self.ax_avl.set_ylim(0, 1)
        self.ax_avl.set_axis_off()
        self.canvas_avl.draw()
