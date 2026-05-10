# MÓDULO 9: interfaz.py
# Este módulo define la interfaz gráfica del sistema usando Tkinter.
# La interfaz permite al usuario interactuar con el sistema de forma visual
# a través de pestañas para gestionar clientes, servicios y reservas.

import tkinter as tk
from tkinter import ttk, messagebox

from gestor import GestorSistema
from excepciones import ErrorSistemaFJ


# Paleta de colores del sistema
COLOR_FONDO         = "#1a1a2e"
COLOR_PANEL         = "#16213e"
COLOR_ACENTO        = "#0f3460"
COLOR_BOTON         = "#e94560"
COLOR_BOTON_HOVER   = "#c73652"
COLOR_TEXTO         = "#eaeaea"
COLOR_TEXTO_SUAVE   = "#a0a0b0"
COLOR_EXITO         = "#4caf50"
COLOR_ERROR         = "#e94560"
COLOR_ADVERTENCIA   = "#ff9800"
COLOR_TABLA_FILA1   = "#1a1a2e"
COLOR_TABLA_FILA2   = "#16213e"


class AplicacionSoftwareFJ:
    """
    Clase principal de la interfaz gráfica del sistema Software FJ.
    Crea la ventana principal con pestañas para cada sección del sistema.
    """

    def __init__(self, root):
        # Ventana principal de Tkinter que recibimos desde el bloque main
        self.root = root
        self.root.title("Software FJ - Sistema de Gestión Integral")
        self.root.geometry("1000x680")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(True, True)

        # Creamos la instancia central del sistema que usarán todas las pestañas
        self.gestor = GestorSistema()

        # Configuramos los estilos visuales de los widgets
        self._configurar_estilos()

        # Construimos la interfaz completa
        self._construir_encabezado()
        self._construir_pestanas()
        self._construir_barra_estado()

        # Centramos la ventana en la pantalla al abrir
        self._centrar_ventana()

    def _centrar_ventana(self):
        # Calcula la posición para centrar la ventana en la pantalla
        self.root.update_idletasks()
        ancho  = self.root.winfo_width()
        alto   = self.root.winfo_height()
        x = (self.root.winfo_screenwidth()  // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _configurar_estilos(self):
        # Configuramos los estilos visuales usando ttk.Style
        # Esto permite personalizar la apariencia de los widgets de ttk
        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Estilo del notebook, que es el contenedor de pestañas
        estilo.configure("TNotebook",
            background=COLOR_FONDO,
            borderwidth=0
        )
        estilo.configure("TNotebook.Tab",
            background=COLOR_ACENTO,
            foreground=COLOR_TEXTO,
            padding=[16, 8],
            font=("Consolas", 10, "bold")
        )
        estilo.map("TNotebook.Tab",
            background=[("selected", COLOR_BOTON)],
            foreground=[("selected", "#ffffff")]
        )

        # Estilo de las tablas (Treeview)
        estilo.configure("Treeview",
            background=COLOR_PANEL,
            foreground=COLOR_TEXTO,
            fieldbackground=COLOR_PANEL,
            borderwidth=0,
            rowheight=28,
            font=("Consolas", 9)
        )
        estilo.configure("Treeview.Heading",
            background=COLOR_ACENTO,
            foreground=COLOR_TEXTO,
            font=("Consolas", 9, "bold"),
            borderwidth=0
        )
        estilo.map("Treeview",
            background=[("selected", COLOR_BOTON)],
            foreground=[("selected", "#ffffff")]
        )

        # Estilo del scrollbar
        estilo.configure("TScrollbar",
            background=COLOR_ACENTO,
            troughcolor=COLOR_PANEL
        )

    def _construir_encabezado(self):
        # Panel superior con el título del sistema
        encabezado = tk.Frame(self.root, bg=COLOR_BOTON, height=60)
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        # MEJORA: Se añadió la versión del sistema (v1.1)
        tk.Label(
            encabezado,
            text="  SOFTWARE FJ  —  Sistema Integral de Gestión v1.1",
            font=("Consolas", 14, "bold"),
            bg=COLOR_BOTON,
            fg="#ffffff"
        ).pack(side="left", padx=20, pady=15)

        # MEJORA: Se añadió el crédito del colaborador y se resaltó la fuente
        tk.Label(
            encabezado,
            text="UNAD · POO · 213023 | Colaborador: (Cesar Enciso)",
            font=("Consolas", 9, "bold"),
            bg=COLOR_BOTON,
            fg="#ffffff"
        ).pack(side="right", padx=20)


    def _construir_pestanas(self):
        # Contenedor principal de pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Creamos cada pestaña como un frame independiente
        self.tab_clientes  = tk.Frame(self.notebook, bg=COLOR_FONDO)
        self.tab_servicios = tk.Frame(self.notebook, bg=COLOR_FONDO)
        self.tab_reservas  = tk.Frame(self.notebook, bg=COLOR_FONDO)
        self.tab_resumen   = tk.Frame(self.notebook, bg=COLOR_FONDO)

        self.notebook.add(self.tab_clientes,  text="  👤 Clientes  ")
        self.notebook.add(self.tab_servicios, text="  🛠 Servicios  ")
        self.notebook.add(self.tab_reservas,  text="  📋 Reservas  ")
        self.notebook.add(self.tab_resumen,   text="  📊 Resumen  ")

        # Construimos el contenido de cada pestaña
        self._construir_tab_clientes()
        self._construir_tab_servicios()
        self._construir_tab_reservas()
        self._construir_tab_resumen()

    def _construir_barra_estado(self):
        # Barra inferior que muestra mensajes de estado del sistema
        self.barra_estado = tk.Frame(self.root, bg=COLOR_ACENTO, height=30)
        self.barra_estado.pack(fill="x", side="bottom")
        self.barra_estado.pack_propagate(False)

        self.label_estado = tk.Label(
            self.barra_estado,
            text="Sistema listo",
            font=("Consolas", 9),
            bg=COLOR_ACENTO,
            fg=COLOR_TEXTO_SUAVE
        )
        self.label_estado.pack(side="left", padx=10, pady=5)

    def _actualizar_estado(self, mensaje, tipo="info"):
        # Actualiza el mensaje de la barra de estado con color según el tipo
        colores = {
            "info":       COLOR_TEXTO_SUAVE,
            "exito":      COLOR_EXITO,
            "error":      COLOR_ERROR,
            "advertencia":COLOR_ADVERTENCIA
        }
        self.label_estado.config(
            text=f"  {mensaje}",
            fg=colores.get(tipo, COLOR_TEXTO_SUAVE)
        )

    # =========================================================================
    # WIDGETS DE APOYO REUTILIZABLES
    # =========================================================================

    def _crear_frame_formulario(self, padre, titulo):
        # Crea un panel con título para agrupar campos de formulario
        frame = tk.LabelFrame(
            padre,
            text=f"  {titulo}  ",
            font=("Consolas", 10, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_BOTON,
            bd=1,
            relief="solid"
        )
        return frame

    def _crear_campo(self, padre, etiqueta, fila, ancho=30):
        # Crea una etiqueta y un campo de entrada en la fila indicada
        tk.Label(
            padre,
            text=etiqueta,
            font=("Consolas", 9),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SUAVE,
            anchor="w"
        ).grid(row=fila, column=0, sticky="w", padx=12, pady=5)

        campo = tk.Entry(
            padre,
            font=("Consolas", 10),
            bg=COLOR_ACENTO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="flat",
            width=ancho
        )
        campo.grid(row=fila, column=1, sticky="ew", padx=12, pady=5)
        return campo

    def _crear_boton(self, padre, texto, comando, color=None):
        # Crea un botón con el estilo visual del sistema
        color_fondo = color or COLOR_BOTON

        boton = tk.Button(
            padre,
            text=texto,
            command=comando,
            font=("Consolas", 10, "bold"),
            bg=color_fondo,
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=6
        )

        # Efectos hover al pasar el mouse sobre el botón
        boton.bind("<Enter>", lambda e: boton.config(bg=COLOR_BOTON_HOVER))
        boton.bind("<Leave>", lambda e: boton.config(bg=color_fondo))
        return boton

    def _crear_tabla(self, padre, columnas):
        # Crea una tabla con scrollbar vertical y horizontal
        frame = tk.Frame(padre, bg=COLOR_FONDO)

        scroll_y = ttk.Scrollbar(frame, orient="vertical")
        scroll_x = ttk.Scrollbar(frame, orient="horizontal")

        tabla = ttk.Treeview(
            frame,
            columns=columnas,
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        scroll_y.config(command=tabla.yview)
        scroll_x.config(command=tabla.xview)

        # Configuramos los encabezados de cada columna
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center", width=120)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        tabla.pack(fill="both", expand=True)

        return frame, tabla

    # =========================================================================
    # PESTAÑA CLIENTES
    # =========================================================================

    def _construir_tab_clientes(self):
        # Panel izquierdo con el formulario de registro
        panel_izq = tk.Frame(self.tab_clientes, bg=COLOR_FONDO, width=340)
        panel_izq.pack(side="left", fill="y", padx=(10, 5), pady=10)
        panel_izq.pack_propagate(False)

        form = self._crear_frame_formulario(panel_izq, "Registrar Nuevo Cliente")
        form.pack(fill="x", pady=(0, 10))
        form.columnconfigure(1, weight=1)

        self.cli_documento = self._crear_campo(form, "Documento *",    0)
        self.cli_nombre    = self._crear_campo(form, "Nombre *",       1)
        self.cli_email     = self._crear_campo(form, "Email *",        2)
        self.cli_telefono  = self._crear_campo(form, "Teléfono *",     3)
        self.cli_direccion = self._crear_campo(form, "Dirección",      4)

        frame_botones = tk.Frame(form, bg=COLOR_PANEL)
        frame_botones.grid(row=5, column=0, columnspan=2, pady=10)

        self._crear_boton(frame_botones, "✚  Registrar Cliente",
            self._registrar_cliente).pack(side="left", padx=5)
        self._crear_boton(frame_botones, "✕  Limpiar",
            self._limpiar_form_cliente, color=COLOR_ACENTO).pack(side="left", padx=5)

        # Panel derecho con la tabla de clientes
        panel_der = tk.Frame(self.tab_clientes, bg=COLOR_FONDO)
        panel_der.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        tk.Label(
            panel_der,
            text="Clientes Registrados",
            font=("Consolas", 10, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(anchor="w", pady=(0, 5))

        frame_tabla, self.tabla_clientes = self._crear_tabla(
            panel_der,
            ["Documento", "Nombre", "Email", "Teléfono", "Reservas", "Estado"]
        )
        frame_tabla.pack(fill="both", expand=True)

        self._crear_boton(panel_der, "↻  Actualizar lista",
            self._cargar_clientes, color=COLOR_ACENTO).pack(pady=8)

    def _registrar_cliente(self):
        # Recoge los datos del formulario y llama al gestor para registrar el cliente
        try:
            self.gestor.registrar_cliente(
                self.cli_documento.get().strip(),
                self.cli_nombre.get().strip(),
                self.cli_email.get().strip(),
                self.cli_telefono.get().strip(),
                self.cli_direccion.get().strip()
            )
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            self._limpiar_form_cliente()
            self._cargar_clientes()
            self._actualizar_estado(f"Cliente registrado: {self.cli_nombre.get()}", "exito")

        except ErrorSistemaFJ as e:
            messagebox.showerror("Error", str(e))
            self._actualizar_estado(str(e), "error")

    def _limpiar_form_cliente(self):
        # Borra el contenido de todos los campos del formulario de clientes
        for campo in [self.cli_documento, self.cli_nombre,
                      self.cli_email, self.cli_telefono, self.cli_direccion]:
            campo.delete(0, tk.END)

    def _cargar_clientes(self):
        # Limpia la tabla y la vuelve a llenar con los datos actuales del gestor
        for fila in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(fila)

        for cliente in self.gestor.listar_clientes(solo_activos=False):
            self.tabla_clientes.insert("", "end", values=(
                cliente.identificador,
                cliente.nombre,
                cliente.email,
                cliente.telefono,
                cliente.total_reservas(),
                "Activo" if cliente.activo else "Inactivo"
            ))

    # =========================================================================
    # PESTAÑA SERVICIOS
    # =========================================================================

    def _construir_tab_servicios(self):
        panel_izq = tk.Frame(self.tab_servicios, bg=COLOR_FONDO, width=360)
        panel_izq.pack(side="left", fill="y", padx=(10, 5), pady=10)
        panel_izq.pack_propagate(False)

        # Selector del tipo de servicio
        tipo_frame = tk.Frame(panel_izq, bg=COLOR_FONDO)
        tipo_frame.pack(fill="x", pady=(0, 8))

        tk.Label(
            tipo_frame,
            text="Tipo de servicio:",
            font=("Consolas", 9),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SUAVE
        ).pack(side="left", padx=5)

        self.tipo_servicio = tk.StringVar(value="sala")
        for valor, texto in [("sala", "Sala"), ("equipo", "Equipo"), ("asesoria", "Asesoría")]:
            tk.Radiobutton(
                tipo_frame,
                text=texto,
                variable=self.tipo_servicio,
                value=valor,
                font=("Consolas", 9),
                bg=COLOR_FONDO,
                fg=COLOR_TEXTO,
                selectcolor=COLOR_ACENTO,
                command=self._actualizar_form_servicio
            ).pack(side="left", padx=5)

        # Formulario de servicios
        self.form_srv = self._crear_frame_formulario(panel_izq, "Registrar Servicio")
        self.form_srv.pack(fill="x")
        self.form_srv.columnconfigure(1, weight=1)

        self.srv_codigo      = self._crear_campo(self.form_srv, "Código *",      0)
        self.srv_nombre      = self._crear_campo(self.form_srv, "Nombre *",      1)
        self.srv_descripcion = self._crear_campo(self.form_srv, "Descripción",   2)
        self.srv_tarifa      = self._crear_campo(self.form_srv, "Tarifa base *", 3)

        # Campo extra que cambia según el tipo de servicio seleccionado
        self.label_extra = tk.Label(
            self.form_srv,
            text="Capacidad *",
            font=("Consolas", 9),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SUAVE,
            anchor="w"
        )
        self.label_extra.grid(row=4, column=0, sticky="w", padx=12, pady=5)

        self.srv_extra = tk.Entry(
            self.form_srv,
            font=("Consolas", 10),
            bg=COLOR_ACENTO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="flat",
            width=30
        )
        self.srv_extra.grid(row=4, column=1, sticky="ew", padx=12, pady=5)

        # Campo nivel solo visible para asesorías
        self.label_nivel = tk.Label(
            self.form_srv,
            text="Nivel asesor *",
            font=("Consolas", 9),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SUAVE,
            anchor="w"
        )
        self.srv_nivel = ttk.Combobox(
            self.form_srv,
            values=["junior", "senior", "experto"],
            font=("Consolas", 10),
            state="readonly",
            width=28
        )

        frame_botones_srv = tk.Frame(self.form_srv, bg=COLOR_PANEL)
        frame_botones_srv.grid(row=6, column=0, columnspan=2, pady=10)

        self._crear_boton(frame_botones_srv, "✚  Registrar Servicio",
            self._registrar_servicio).pack(side="left", padx=5)
        self._crear_boton(frame_botones_srv, "✕  Limpiar",
            self._limpiar_form_servicio, color=COLOR_ACENTO).pack(side="left", padx=5)

        # Panel derecho con tabla de servicios
        panel_der = tk.Frame(self.tab_servicios, bg=COLOR_FONDO)
        panel_der.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        tk.Label(
            panel_der,
            text="Catálogo de Servicios",
            font=("Consolas", 10, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(anchor="w", pady=(0, 5))

        frame_tabla, self.tabla_servicios = self._crear_tabla(
            panel_der,
            ["Código", "Nombre", "Tipo", "Tarifa base", "Disponible"]
        )
        frame_tabla.pack(fill="both", expand=True)

        self._crear_boton(panel_der, "↻  Actualizar lista",
            self._cargar_servicios, color=COLOR_ACENTO).pack(pady=8)

    def _actualizar_form_servicio(self):
        # Cambia la etiqueta del campo extra según el tipo de servicio seleccionado
        tipo = self.tipo_servicio.get()

        self.label_nivel.grid_forget()
        self.srv_nivel.grid_forget()

        if tipo == "sala":
            self.label_extra.config(text="Capacidad máx *")
        elif tipo == "equipo":
            self.label_extra.config(text="Cant. disponible *")
        elif tipo == "asesoria":
            self.label_extra.config(text="Especialidad *")
            self.label_nivel.grid(row=5, column=0, sticky="w", padx=12, pady=5)
            self.srv_nivel.grid(row=5, column=1, sticky="ew", padx=12, pady=5)

    def _registrar_servicio(self):
        try:
            tipo   = self.tipo_servicio.get()
            codigo = self.srv_codigo.get().strip()
            nombre = self.srv_nombre.get().strip()
            desc   = self.srv_descripcion.get().strip()
            tarifa = float(self.srv_tarifa.get().strip())
            extra  = self.srv_extra.get().strip()

            if tipo == "sala":
                self.gestor.registrar_sala(codigo, nombre, desc, tarifa, int(extra))
            elif tipo == "equipo":
                self.gestor.registrar_equipo(codigo, nombre, desc, tarifa, int(extra), nombre)
            elif tipo == "asesoria":
                nivel = self.srv_nivel.get()
                self.gestor.registrar_asesoria(codigo, nombre, desc, tarifa, extra, nivel)

            messagebox.showinfo("Éxito", "Servicio registrado correctamente.")
            self._limpiar_form_servicio()
            self._cargar_servicios()
            self._actualizar_estado(f"Servicio registrado: {nombre}", "exito")

        except ErrorSistemaFJ as e:
            messagebox.showerror("Error", str(e))
            self._actualizar_estado(str(e), "error")
        except ValueError:
            messagebox.showerror("Error", "La tarifa y la cantidad deben ser números válidos.")
            self._actualizar_estado("Datos numéricos inválidos", "error")

    def _limpiar_form_servicio(self):
        for campo in [self.srv_codigo, self.srv_nombre,
                      self.srv_descripcion, self.srv_tarifa, self.srv_extra]:
            campo.delete(0, tk.END)

    def _cargar_servicios(self):
        for fila in self.tabla_servicios.get_children():
            self.tabla_servicios.delete(fila)

        for srv in self.gestor.listar_servicios(solo_disponibles=False):
            self.tabla_servicios.insert("", "end", values=(
                srv.identificador,
                srv.nombre,
                type(srv).__name__,
                f"${srv.tarifa_base:,.0f}",
                "Sí" if srv.disponible else "No"
            ))

    # =========================================================================
    # PESTAÑA RESERVAS
    # =========================================================================

    def _construir_tab_reservas(self):
        panel_izq = tk.Frame(self.tab_reservas, bg=COLOR_FONDO, width=360)
        panel_izq.pack(side="left", fill="y", padx=(10, 5), pady=10)
        panel_izq.pack_propagate(False)

        form = self._crear_frame_formulario(panel_izq, "Crear Nueva Reserva")
        form.pack(fill="x", pady=(0, 10))
        form.columnconfigure(1, weight=1)

        self.res_documento = self._crear_campo(form, "Doc. Cliente *", 0)
        self.res_servicio  = self._crear_campo(form, "Cód. Servicio *", 1)
        self.res_duracion  = self._crear_campo(form, "Duración *", 2)

        tk.Label(form, text="Descuento %",
            font=("Consolas", 9), bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SUAVE, anchor="w"
        ).grid(row=3, column=0, sticky="w", padx=12, pady=5)

        self.res_descuento = tk.Spinbox(
            form, from_=0, to=100, width=28,
            font=("Consolas", 10), bg=COLOR_ACENTO,
            fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
            relief="flat", buttonbackground=COLOR_ACENTO
        )
        self.res_descuento.grid(row=3, column=1, sticky="ew", padx=12, pady=5)

        self.res_impuesto = tk.BooleanVar()
        tk.Checkbutton(
            form,
            text="Aplicar IVA (19%)",
            variable=self.res_impuesto,
            font=("Consolas", 9),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            selectcolor=COLOR_ACENTO
        ).grid(row=4, column=0, columnspan=2, sticky="w", padx=12, pady=5)

        frame_botones_res = tk.Frame(form, bg=COLOR_PANEL)
        frame_botones_res.grid(row=5, column=0, columnspan=2, pady=10)

        self._crear_boton(frame_botones_res, "✚  Crear Reserva",
            self._crear_reserva).pack(side="left", padx=5)
        self._crear_boton(frame_botones_res, "✕  Limpiar",
            self._limpiar_form_reserva, color=COLOR_ACENTO).pack(side="left", padx=5)

        # Acciones sobre reservas existentes
        acciones = self._crear_frame_formulario(panel_izq, "Gestionar Reserva")
        acciones.pack(fill="x")

        self.res_id_accion = self._crear_campo(acciones, "ID Reserva *", 0)

        frame_acciones = tk.Frame(acciones, bg=COLOR_PANEL)
        frame_acciones.grid(row=1, column=0, columnspan=2, pady=8)

        self._crear_boton(frame_acciones, "✔ Confirmar",
            self._confirmar_reserva, color="#2e7d32").pack(side="left", padx=3)
        self._crear_boton(frame_acciones, "▶ Procesar",
            self._procesar_reserva, color="#1565c0").pack(side="left", padx=3)
        self._crear_boton(frame_acciones, "■ Finalizar",
            self._finalizar_reserva, color="#6a1e6a").pack(side="left", padx=3)

        self._crear_boton(acciones, "✕  Cancelar Reserva",
            self._cancelar_reserva, color=COLOR_BOTON
        ).grid(row=2, column=0, columnspan=2, pady=(0, 10))

        # Panel derecho con tabla de reservas
        panel_der = tk.Frame(self.tab_reservas, bg=COLOR_FONDO)
        panel_der.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        tk.Label(
            panel_der,
            text="Reservas del Sistema",
            font=("Consolas", 10, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(anchor="w", pady=(0, 5))

        frame_tabla, self.tabla_reservas = self._crear_tabla(
            panel_der,
            ["ID", "Cliente", "Servicio", "Duración", "Costo", "Estado"]
        )
        frame_tabla.pack(fill="both", expand=True)

        self._crear_boton(panel_der, "↻  Actualizar lista",
            self._cargar_reservas, color=COLOR_ACENTO).pack(pady=8)

    def _crear_reserva(self):
        try:
            reserva = self.gestor.crear_reserva(
                self.res_documento.get().strip(),
                self.res_servicio.get().strip(),
                float(self.res_duracion.get().strip()),
                self.res_impuesto.get(),
                int(self.res_descuento.get())
            )
            messagebox.showinfo("Éxito",
                f"Reserva {reserva.identificador} creada.\nCosto: ${reserva.costo_total:,.2f}")
            self._limpiar_form_reserva()
            self._cargar_reservas()
            self._actualizar_estado(f"Reserva {reserva.identificador} creada", "exito")

        except ErrorSistemaFJ as e:
            messagebox.showerror("Error", str(e))
            self._actualizar_estado(str(e), "error")
        except ValueError:
            messagebox.showerror("Error", "La duración debe ser un número válido.")

    def _limpiar_form_reserva(self):
        for campo in [self.res_documento, self.res_servicio, self.res_duracion]:
            campo.delete(0, tk.END)
        self.res_impuesto.set(False)

    def _confirmar_reserva(self):
        self._accion_reserva("confirmar")

    def _procesar_reserva(self):
        self._accion_reserva("procesar")

    def _finalizar_reserva(self):
        self._accion_reserva("finalizar")

    def _cancelar_reserva(self):
        self._accion_reserva("cancelar")

    def _accion_reserva(self, accion):
        # Ejecuta la acción indicada sobre la reserva cuyo ID está en el campo
        id_reserva = self.res_id_accion.get().strip()
        if not id_reserva:
            messagebox.showwarning("Atención", "Ingresa el ID de la reserva.")
            return
        try:
            acciones = {
                "confirmar": self.gestor.confirmar_reserva,
                "procesar":  self.gestor.procesar_reserva,
                "finalizar": self.gestor.finalizar_reserva,
                "cancelar":  self.gestor.cancelar_reserva
            }
            acciones[accion](id_reserva)
            messagebox.showinfo("Éxito", f"Reserva {id_reserva} → {accion}da correctamente.")
            self._cargar_reservas()
            self._actualizar_estado(f"Reserva {id_reserva}: {accion}", "exito")

        except ErrorSistemaFJ as e:
            messagebox.showerror("Error", str(e))
            self._actualizar_estado(str(e), "error")

    def _cargar_reservas(self):
        for fila in self.tabla_reservas.get_children():
            self.tabla_reservas.delete(fila)

        for res in self.gestor.listar_reservas():
            self.tabla_reservas.insert("", "end", values=(
                res.identificador,
                res.cliente.nombre,
                res.servicio.nombre,
                res.duracion,
                f"${res.costo_total:,.2f}",
                res.estado
            ))

    # =========================================================================
    # PESTAÑA RESUMEN
    # =========================================================================

    def _construir_tab_resumen(self):
        tk.Label(
            self.tab_resumen,
            text="Resumen General del Sistema",
            font=("Consolas", 13, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(pady=(20, 10))

        self.frame_resumen = tk.Frame(self.tab_resumen, bg=COLOR_FONDO)
        self.frame_resumen.pack(fill="both", expand=True, padx=20, pady=10)

        self._crear_boton(
            self.tab_resumen,
            "↻  Actualizar Resumen",
            self._cargar_resumen,
            color=COLOR_BOTON
        ).pack(pady=10)

        self._cargar_resumen()

    def _cargar_resumen(self):
        # Limpiamos el frame y lo volvemos a construir con datos actuales
        for widget in self.frame_resumen.winfo_children():
            widget.destroy()

        try:
            resumen = self.gestor.resumen_sistema()

            # Tarjetas de resumen
            datos = [
                ("👤 Clientes registrados",  resumen["clientes_registrados"],  COLOR_BOTON),
                ("✅ Clientes activos",       resumen["clientes_activos"],       COLOR_EXITO),
                ("🛠 Servicios registrados",  resumen["servicios_registrados"],  "#1565c0"),
                ("📋 Total reservas",         resumen["total_reservas"],         "#6a1e6a"),
                ("💰 Ingresos finalizados",   resumen["ingresos_finalizados"],   COLOR_EXITO),
            ]

            for i, (etiqueta, valor, color) in enumerate(datos):
                tarjeta = tk.Frame(
                    self.frame_resumen,
                    bg=color,
                    padx=20,
                    pady=15
                )
                tarjeta.grid(row=0, column=i, padx=8, pady=10, sticky="nsew")
                self.frame_resumen.columnconfigure(i, weight=1)

                tk.Label(
                    tarjeta,
                    text=str(valor),
                    font=("Consolas", 20, "bold"),
                    bg=color,
                    fg="#ffffff"
                ).pack()

                tk.Label(
                    tarjeta,
                    text=etiqueta,
                    font=("Consolas", 8),
                    bg=color,
                    fg="#ffeeee"
                ).pack()

            # Tabla de reservas por estado
            tk.Label(
                self.frame_resumen,
                text="Reservas por estado",
                font=("Consolas", 10, "bold"),
                bg=COLOR_FONDO,
                fg=COLOR_TEXTO
            ).grid(row=1, column=0, columnspan=5, pady=(20, 5), sticky="w")

            colores_estado = {
                "pendiente":  COLOR_ADVERTENCIA,
                "confirmada": "#1565c0",
                "en_proceso": "#6a1e6a",
                "finalizada": COLOR_EXITO,
                "cancelada":  COLOR_ERROR
            }

            for i, (estado, cantidad) in enumerate(resumen["reservas_por_estado"].items()):
                color = colores_estado.get(estado, COLOR_ACENTO)
                tarjeta = tk.Frame(self.frame_resumen, bg=color, padx=15, pady=10)
                tarjeta.grid(row=2, column=i, padx=8, pady=5, sticky="nsew")

                tk.Label(tarjeta, text=str(cantidad),
                    font=("Consolas", 18, "bold"),
                    bg=color, fg="#ffffff").pack()
                tk.Label(tarjeta, text=estado.replace("_", " ").capitalize(),
                    font=("Consolas", 8),
                    bg=color, fg="#ffeeee").pack()

        except ErrorSistemaFJ as e:
            tk.Label(
                self.frame_resumen,
                text=f"Error al cargar resumen: {e}",
                font=("Consolas", 10),
                bg=COLOR_FONDO,
                fg=COLOR_ERROR
            ).pack()


# Punto de entrada de la interfaz gráfica
if __name__ == "__main__":
    root = tk.Tk()
    app  = AplicacionSoftwareFJ(root)
    root.mainloop()
