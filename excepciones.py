# MÓDULO 1: excepciones.py
# Este módulo define todas las excepciones personalizadas del sistema.
# Las excepciones personalizadas permiten identificar errores específicos
# del negocio de forma clara y profesional, en lugar de usar excepciones
# genéricas de Python.

# CLASE BASE: ErrorSistemaFJ
# Hereda de la clase built-in 'Exception' de Python.
# Todas las excepciones del sistema heredan de esta clase base, lo que permite capturarlas todas con un solo 'except ErrorSistemaFJ'.

class ErrorSistemaFJ(Exception):
    """Excepción base del sistema Software FJ.
    Todas las excepciones personalizadas heredan de esta clase."""

    def __init__(self, mensaje, codigo=None):
        # Llamamos al constructor de la clase padre (Exception)
        # para que el mensaje quede registrado correctamente
        super().__init__(mensaje)

        # 'mensaje' describe qué salió mal
        self.mensaje = mensaje

        # codigo es un identificador opcional del tipo de error (ej: "ERR-001")
        self.codigo = codigo

    def __str__(self):
        # Este método define cómo se muestra la excepción al imprimirse
        if self.codigo:
            # Si tiene código, lo mostramos junto al mensaje
            return f"[{self.codigo}] {self.mensaje}"
        # Si no tiene código, solo mostramos el mensaje
        return self.mensaje


# Excepciones relacionadas con clientes

class ErrorCliente(ErrorSistemaFJ):
    """Excepción base para errores relacionados con clientes.
    Hereda de ErrorSistemaFJ."""
    pass  # No agrega comportamiento nuevo; sirve para categorizar el error


class ErrorClienteInvalido(ErrorCliente):
    """Se lanza cuando los datos de un cliente no son válidos.
    Ejemplo: nombre vacío, email sin '@', teléfono con letras."""

    def __init__(self, campo, valor, razon):

        self.campo = campo   # qué campo falló (ej: "email")
        self.valor = valor   # qué valor se recibió (ej: "juansinArroba")
        self.razon = razon   # por qué es inválido (ej: "debe contener '@'")

        # Construimos un mensaje descriptivo automáticamente
        mensaje = (
            f"Dato inválido en cliente → Campo: '{campo}' | "
            f"Valor recibido: '{valor}' | Razón: {razon}"
        )
        # Llamamos al constructor de la clase padre con código de error
        super().__init__(mensaje, codigo="ERR-CLI-001")


class ErrorClienteDuplicado(ErrorCliente):
    """Se lanza cuando se intenta registrar un cliente que ya existe.
    Ejemplo: mismo número de documento o email ya registrado."""

    def __init__(self, identificador):
        # 'identificador' es el dato que ya existe en el sistema
        self.identificador = identificador
        mensaje = (
            f"El cliente con identificador '{identificador}' "
            f"ya está registrado en el sistema."
        )
        super().__init__(mensaje, codigo="ERR-CLI-002")


class ErrorClienteNoEncontrado(ErrorCliente):
    """Se lanza cuando se busca un cliente que no existe en el sistema."""

    def __init__(self, identificador):
        self.identificador = identificador
        mensaje = f"No se encontró ningún cliente con identificador '{identificador}'."
        super().__init__(mensaje, codigo="ERR-CLI-003")

# EXCEPCIONES RELACIONADAS CON SERVICIOS

class ErrorServicio(ErrorSistemaFJ):
    """Excepción base para errores relacionados con servicios."""
    pass

class ErrorServicioInvalido(ErrorServicio):
    """Se lanza cuando los parámetros de un servicio son incorrectos.
    Ejemplo: capacidad negativa, tarifa cero, nombre vacío."""

    def __init__(self, campo, valor, razon):
        self.campo = campo
        self.valor = valor
        self.razon = razon
        mensaje = (
            f"Parámetro inválido en servicio → Campo: '{campo}' | "
            f"Valor recibido: '{valor}' | Razón: {razon}"
        )
        super().__init__(mensaje, codigo="ERR-SRV-001")


class ErrorServicioNoDisponible(ErrorServicio):
    """Se lanza cuando un servicio existe pero no está disponible.
    Ejemplo: sala ya ocupada, equipo en mantenimiento."""

    def __init__(self, nombre_servicio, motivo):
        self.nombre_servicio = nombre_servicio
        self.motivo = motivo
        mensaje = (
            f"El servicio '{nombre_servicio}' no está disponible. "
            f"Motivo: {motivo}"
        )
        super().__init__(mensaje, codigo="ERR-SRV-002")


class ErrorServicioNoEncontrado(ErrorServicio):
    """Se lanza cuando se solicita un servicio que no existe en el catálogo."""

    def __init__(self, nombre_servicio):
        self.nombre_servicio = nombre_servicio
        mensaje = f"El servicio '{nombre_servicio}' no existe en el catálogo."
        super().__init__(mensaje, codigo="ERR-SRV-003")


# EXCEPCIONES RELACIONADAS CON RESERVAS

class ErrorReserva(ErrorSistemaFJ):
    """Excepción base para errores relacionados con reservas."""
    pass


class ErrorReservaInvalida(ErrorReserva):
    """Se lanza cuando los datos de una reserva son incorrectos.
    Ejemplo: duración negativa, fecha pasada, cliente o servicio nulos."""

    def __init__(self, razon):
        self.razon = razon
        mensaje = f"Reserva inválida: {razon}"
        super().__init__(mensaje, codigo="ERR-RES-001")


class ErrorReservaNoEncontrada(ErrorReserva):
    """Se lanza cuando se busca una reserva que no existe."""

    def __init__(self, id_reserva):
        self.id_reserva = id_reserva
        mensaje = f"No se encontró la reserva con ID '{id_reserva}'."
        super().__init__(mensaje, codigo="ERR-RES-002")


class ErrorCancelacionNoPermitida(ErrorReserva):
    """Se lanza cuando se intenta cancelar una reserva que no puede cancelarse.
    Ejemplo: reserva ya cancelada, reserva en curso, fuera de tiempo límite."""

    def __init__(self, id_reserva, motivo):
        self.id_reserva = id_reserva
        self.motivo = motivo
        mensaje = (
            f"No se puede cancelar la reserva '{id_reserva}'. "
            f"Motivo: {motivo}"
        )
        super().__init__(mensaje, codigo="ERR-RES-003")


# EXCEPCIONES RELACIONADAS CON CÁLCULOS Y COSTOS

class ErrorCalculo(ErrorSistemaFJ):
    """Se lanza cuando un cálculo de costo produce un resultado inválido.
    Ejemplo: costo negativo, descuento mayor al 100%, impuesto inválido."""

    def __init__(self, operacion, detalle):
        self.operacion = operacion
        self.detalle = detalle
        mensaje = (
            f"Error en cálculo de '{operacion}': {detalle}"
        )
        super().__init__(mensaje, codigo="ERR-CALC-001")


# BLOQUE DE PRUEBA DEL MÓDULO
# Este bloque solo se ejecuta si se corre el archivo directamente con 'python excepciones.py'
# No se ejecuta cuando otros módulos lo importan con 'import excepciones'

if __name__ == "__main__":

    print("=" * 40)
    print("  PRUEBA DEL MÓDULO 1: excepciones.py")
    print("=" * 40)

    # Prueba 1: Excepción base 
    print("\n[Prueba 1] ErrorSistemaFJ con código:")
    try:
        raise ErrorSistemaFJ("Error general del sistema", codigo="ERR-000")
    except ErrorSistemaFJ as e:
        print(f"  Capturado correctamente → {e}")

    # Prueba 2: Cliente inválido 
    print("\n[Prueba 2] ErrorClienteInvalido:")
    try:
        raise ErrorClienteInvalido("email", "juansinArroba", "debe contener '@'")
    except ErrorClienteInvalido as e:
        print(f"  Capturado correctamente → {e}")

    # Prueba 3: Cliente duplicado
    print("\n[Prueba 3] ErrorClienteDuplicado:")
    try:
        raise ErrorClienteDuplicado("1020304050")
    except ErrorClienteDuplicado as e:
        print(f"  Capturado correctamente → {e}")

    # Prueba 4: Servicio no disponible      
    print("\n[Prueba 4] ErrorServicioNoDisponible:")
    try:
        raise ErrorServicioNoDisponible("Sala A", "ya reservada para ese horario")
    except ErrorServicioNoDisponible as e:
        print(f"  Capturado correctamente → {e}")

    # Prueba 5: Reserva inválida 
    print("\n[Prueba 5] ErrorReservaInvalida:")
    try:
        raise ErrorReservaInvalida("la duración no puede ser negativa")
    except ErrorReservaInvalida as e:
        print(f"  Capturado correctamente → {e}")

    # Prueba 6: Encadenamiento de excepciones (raise ... from ...) 
    print("\n[Prueba 6] Encadenamiento de excepciones:")
    try:
        try:
            # Simulamos un error original de Python
            int("no_es_numero")
        except ValueError as error_original:
            # Encadenamos el error original con uno personalizado
            raise ErrorCalculo(
                "conversión de tarifa",
                "el valor recibido no es numérico"
            ) from error_original
    except ErrorCalculo as e:
        print(f"  Capturado correctamente → {e}")
        print(f"  Causa original → {e.__cause__}")

    # Prueba 7: Captura por clase base (polimorfismo de excepciones)
    print("\n[Prueba 7] Captura por clase base ErrorCliente:")
    try:
        raise ErrorClienteNoEncontrado("9999")
    except ErrorCliente as e:
        # ErrorClienteNoEncontrado ES UN ErrorCliente, por eso se captura aquí
        print(f"  Capturado como ErrorCliente → {e}")

    print("\n" + "=" * 45)
    print("  Todas las pruebas pasaron correctamente ✓")
    print("=" * 45)
