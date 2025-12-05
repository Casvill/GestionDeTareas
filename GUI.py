import tkinter as tk
from tkinter import messagebox, ttk
import GestorTareas
import datetime
from tkcalendar import DateEntry


class App:

    #------------------------------------------------------------------------------------
    def __init__(self, root):

        self.gestor = GestorTareas.GestorTareas()
        self.root = root
        self.root.title("Sistema de Gestión de Tareas (Heap + AVL)")
        self.root.geometry("1150x630")
        self.root.configure(bg="#eef1f5")   # Fondo moderno


        # =========================== ESTILO GENERAL ===================================
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel", background="#eef1f5", font=("Segoe UI", 10))
        style.configure("Title.TLabelframe", background="#ffffff",
                        font=("Segoe UI", 11, "bold"))
        style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=6)

        style.configure("Treeview.Heading",
                        font=("Segoe UI", 10, "bold"),
                        background="#dfe3ee")
        style.configure("Treeview", rowheight=25)
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
        # =========================================================================================



        # ============================ TABLA ===================================================
        self.tree = ttk.Treeview(root,
                                columns=("ID", "Descripción", "Prioridad", "Fecha creación", "Vencimiento"),
                                show="headings")

        for col in ("ID", "Descripción", "Prioridad", "Fecha creación", "Vencimiento"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=15, pady=15)
        # =========================================================================================


    #------------------------------------------------------------------------------------
    def actualizar_lista(self):
        # Refresca la vista de tareas activas
        for i in self.tree.get_children():
            self.tree.delete(i)
        tareas = self.gestor.listar_todas()
        for t in tareas:
            self.tree.insert("", "end", values=(t.id, t.descripcion, t.prioridad_str, t.fecha_creacion, t.fecha_vencimiento))

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
        else:
            messagebox.showinfo("Info", "No hay tareas pendientes.")
        
        # for nodo in self.gestor.listar_todas():
        #     print(f"Nodo: {nodo.id} \n")
        
        # self.gestor.heap.imprimir_con_ramas()
        print("HEAP:")
        self.gestor.heap.imprimir_arbol_centrado()

        # self.gestor.avl.imprimir_arbol(self.gestor.raiz_avl)
        # self.gestor.avl.imprimir_vertical(self.gestor.raiz_avl)
        print("AVL")
        self.gestor.avl.imprimir_arb_leetcode(self.gestor.raiz_avl)


    #------------------------------------------------------------------------------------
    def buscar(self):
        # Busca por ID y muestra resultado
        try:
            id_b = self.entry_buscar.get()
            tarea = self.gestor.buscar(id_b)
            if tarea:
                messagebox.showinfo("Encontrado", str(tarea))
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
            tree_h.insert(
                "",
                "end",
                values=(t["id"], t["descripcion"], t["prioridad"], t["fecha_creacion"],t["fecha_vencimiento"], t["estado_final"])
            )

        tk.Button(ventana_h, text="Cerrar", command=ventana_h.destroy).pack(pady=5)

    #------------------------------------------------------------------------------------