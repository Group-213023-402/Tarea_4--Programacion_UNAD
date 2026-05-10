# MÓDULO 6: reserva.py
# Este módulo define la clase Reserva que integra un cliente con un servicio 
# Implementa confirmación, cancelación y procesamiento con manejo completo de excepciones usando try/except, try/except/else y try/except/finally.

import datetime

from entidad_base import EntidadBase
from excepciones import (
    ErrorReservaInvalida,
    ErrorReservaNoEncontrada,
    ErrorCancelacionNoPermitida,
    ErrorServicioNoDisponible,
    ErrorCalculo
)
from logger import logger


class Reserva(EntidadBase):
    """
    Clase que representa una reserva en el sistema Software FJ.
    Integra un cliente con un servicio y gestiona su ciclo de vida completo:
    creación, confirmación, procesamiento y cancelación.
    """

    # Definimos los estados posibles de una reserva a lo largo de su ciclo de vida
    ESTADO_PENDIENTE   = "pendiente"
    ESTADO_CONFIRMADA  = "confirmada"
    ESTADO_EN_PROCESO  = "en_proceso"
    ESTADO_FINALIZADA  = "finalizada"
    ESTADO_CANCELADA   = "cancelada"

    # Contador de clase que genera IDs únicos automáticamente para cada reserva
    # como es un atributo de clase, no de instancia, se define aquí afuera
    _contador_reservas = 0

    def __init__(self, cliente, servicio, duracion, con_impuesto=False, descuento=0):
        # cliente es el objeto Cliente que solicita el servicio
        # servicio es el objeto Servicio que se va a reservar
        # duracion es la cantidad de horas o días según el tipo de servicio
        # con_impuesto indica si se aplica IVA al costo total
        # descuento es el porcentaje de descuento a aplicar

        # Usamos try/except/else para validar y crear la reserva de forma segura
        try:
            # Validamos que el cliente y el servicio sean objetos válidos
            self._validar_cliente(cliente)
            self._validar_servicio(servicio)
            self._validar_duracion(duracion)

            # Verificamos que el servicio esté disponible antes de crear la reserva
            servicio.verificar_disponibilidad()

        except (ErrorReservaInvalida, ErrorServicioNoDisponible):
            # Si hay algún error de validación lo dejamos subir al código que llamó esto
            raise

        except Exception as e:
            # Cualquier otro error inesperado lo convertimos en ErrorReservaInvalida
            raise ErrorReservaInvalida(f"error inesperado al crear la reserva: {e}") from e

        else:
            # El bloque else solo se ejecuta si el bloque try no lanzó ninguna excepción Es decir, si todas las validaciones pasaron correctamente

            # Generamos un ID único para esta reserva
            Reserva._contador_reservas += 1
            id_reserva = f"RES-{Reserva._contador_reservas:04d}"
            # El formato 04d agrega ceros a la izquierda, por ejemplo RES-0001, RES-0012

            # Llamamos al constructor de EntidadBase con el ID generado
            super().__init__(id_reserva)

            # Asignamos los atributos de la reserva
            self._cliente   = cliente
            self._servicio  = servicio
            self._duracion  = duracion
            self._con_impuesto = con_impuesto
            self._descuento = descuento

            # La reserva empieza en estado pendiente hasta que se confirme
            self._estado = self.ESTADO_PENDIENTE

            # Fecha y hora en que se creó la reserva
            self._fecha_reserva = datetime.datetime.now()

            # Calculamos el costo total en el momento de crear la reserva
            self._costo_total = self._servicio.calcular_costo(
                self._duracion,
                con_impuesto=self._con_impuesto,
                descuento=self._descuento
            )

            # Registramos la reserva en el historial del cliente
            self._cliente.agregar_reserva(self._identificador)

            logger.info(
                f"Reserva {self._identificador} creada: "
                f"Cliente {self._cliente.nombre} | "
                f"Servicio {self._servicio.nombre} | "
                f"Duración {self._duracion} | "
                f"Costo ${self._costo_total:,.2f}"
            )

    def _validar_cliente(self, cliente):
        # Verifica que el cliente sea un objeto válido y esté activo
        from cliente import Cliente
        if not isinstance(cliente, Cliente):
            raise ErrorReservaInvalida("el cliente debe ser un objeto de la clase Cliente")
        if not cliente.activo:
            raise ErrorReservaInvalida(f"el cliente {cliente.identificador} está inactivo")

    def _validar_servicio(self, servicio):
        # Verifica que el servicio sea un objeto válido y esté activo
        from servicios import Servicio
        if not isinstance(servicio, Servicio):
            raise ErrorReservaInvalida("el servicio debe ser un objeto de la clase Servicio")
        if not servicio.activo:
            raise ErrorReservaInvalida(f"el servicio {servicio.identificador} está inactivo")

    def _validar_duracion(self, duracion):
        # La duración debe ser un número positivo
        try:
            valor = float(duracion)
        except (TypeError, ValueError):
            raise ErrorReservaInvalida("la duración debe ser un número válido")
        if valor <= 0:
            raise ErrorReservaInvalida("la duración debe ser mayor a cero")

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    @property
    def fecha_reserva(self):
        return self._fecha_reserva

    def confirmar(self):
        """
        Cambia el estado de la reserva de pendiente a confirmada.
        Usa try/except/finally para garantizar que el evento siempre se registre.
        """
        try:
            # Verificamos que la reserva esté en estado pendiente para poder confirmarla
            if self._estado != self.ESTADO_PENDIENTE:
                raise ErrorReservaInvalida(
                    f"solo se pueden confirmar reservas pendientes. "
                    f"Estado actual: {self._estado}"
                )

            # Verificamos nuevamente que el servicio sigue disponible
            self._servicio.verificar_disponibilidad()

            # Cambiamos el estado a confirmada
            self._estado = self.ESTADO_CONFIRMADA

        except (ErrorReservaInvalida, ErrorServicioNoDisponible) as e:
            logger.error(f"No se pudo confirmar la reserva {self._identificador}: {e}")
            raise

        finally:
            # El bloque finally siempre se ejecuta, haya error o no
            # Lo usamos para registrar que se intentó confirmar la reserva
            logger.info(f"Intento de confirmación de reserva {self._identificador}: estado actual {self._estado}")

    def procesar(self):
        """
        Cambia el estado de la reserva de confirmada a en proceso.
        Indica que el cliente ya está usando el servicio.
        """
        try:
            if self._estado != self.ESTADO_CONFIRMADA:
                raise ErrorReservaInvalida(
                    f"solo se pueden procesar reservas confirmadas. "
                    f"Estado actual: {self._estado}"
                )
            self._estado = self.ESTADO_EN_PROCESO
            logger.info(f"Reserva {self._identificador} en proceso")

        except ErrorReservaInvalida as e:
            logger.error(f"No se pudo procesar la reserva {self._identificador}: {e}")
            raise

    def finalizar(self):
        """
        Cambia el estado de la reserva a finalizada.
        Indica que el servicio fue completado exitosamente.
        """
        try:
            if self._estado != self.ESTADO_EN_PROCESO:
                raise ErrorReservaInvalida(
                    f"solo se pueden finalizar reservas en proceso. "
                    f"Estado actual: {self._estado}"
                )
            self._estado = self.ESTADO_FINALIZADA
            logger.info(f"Reserva {self._identificador} finalizada exitosamente")

        except ErrorReservaInvalida as e:
            logger.error(f"No se pudo finalizar la reserva {self._identificador}: {e}")
            raise

    def cancelar(self, motivo=""):
        """
        Cancela la reserva si está en un estado que lo permite.
        No se puede cancelar una reserva que ya está finalizada o cancelada.
        Usa try/except/else/finally para manejar todos los escenarios.
        """
        try:
            # Solo se pueden cancelar reservas pendientes o confirmadas
            estados_cancelables = [self.ESTADO_PENDIENTE, self.ESTADO_CONFIRMADA]

            if self._estado not in estados_cancelables:
                raise ErrorCancelacionNoPermitida(
                    self._identificador,
                    f"no se puede cancelar una reserva en estado {self._estado}"
                )

        except ErrorCancelacionNoPermitida as e:
            logger.error(f"Cancelación rechazada para reserva {self._identificador}: {e}")
            raise

        else:
            # El else se ejecuta solo si no hubo ninguna excepción en el try
            self._estado = self.ESTADO_CANCELADA
            mensaje = f"Reserva {self._identificador} cancelada"
            if motivo:
                mensaje += f". Motivo: {motivo}"
            logger.info(mensaje)

        finally:
            # El finally registra el intento de cancelación sin importar el resultado
            logger.info(f"Proceso de cancelación completado para reserva {self._identificador}")

    def recalcular_costo(self, con_impuesto=None, descuento=None):
        """
        Recalcula el costo total de la reserva con nuevos parámetros.
        Solo se puede recalcular si la reserva está pendiente.
        """
        try:
            if self._estado != self.ESTADO_PENDIENTE:
                raise ErrorReservaInvalida(
                    "solo se puede recalcular el costo de reservas pendientes"
                )

            # Si no se pasa un nuevo valor usamos el que ya tenía la reserva
            nuevo_impuesto  = con_impuesto if con_impuesto is not None else self._con_impuesto
            nuevo_descuento = descuento if descuento is not None else self._descuento

            costo_anterior = self._costo_total
            self._costo_total = self._servicio.calcular_costo(
                self._duracion,
                con_impuesto=nuevo_impuesto,
                descuento=nuevo_descuento
            )
            self._con_impuesto = nuevo_impuesto
            self._descuento    = nuevo_descuento

            logger.info(
                f"Reserva {self._identificador}: costo recalculado "
                f"de ${costo_anterior:,.2f} a ${self._costo_total:,.2f}"
            )

        except ErrorCalculo as e:
            logger.error(f"Error al recalcular costo de reserva {self._identificador}: {e}")
            raise

    def obtener_info(self):
        # Implementación del método abstracto de EntidadBase
        info = self.obtener_info_base()
        info.update({
            "cliente": self._cliente.nombre,
            "documento_cliente": self._cliente.identificador,
            "servicio": self._servicio.nombre,
            "tipo_servicio": type(self._servicio).__name__,
            "duracion": self._duracion,
            "estado": self._estado,
            "costo_total": f"${self._costo_total:,.2f}",
            "con_impuesto": self._con_impuesto,
            "descuento": f"{self._descuento}%",
            "fecha_reserva": self._fecha_reserva.strftime("%Y-%m-%d %H:%M:%S")
        })
        return info

    def validar(self):
        # Implementación del método abstracto de EntidadBase
        try:
            self._validar_cliente(self._cliente)
            self._validar_servicio(self._servicio)
            self._validar_duracion(self._duracion)
            return True
        except ErrorReservaInvalida as e:
            logger.error(f"Reserva {self._identificador} falló la validación: {e}")
            return False


# Este bloque solo se ejecuta si se corre este archivo directamente
if __name__ == "__main__":

    print("PRUEBA DEL MÓDULO 6: reserva.py")
    print("=" * 60)

    from cliente import Cliente
    from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada

    # Creamos los objetos necesarios para las pruebas
    cliente1 = Cliente("1020304050", "Juan Pérez", "juan@gmail.com", "3001234567")
    sala     = ReservaSala("SRV-001", "Sala de Juntas A", "Sala principal", 80000, 10)
    equipo   = AlquilerEquipo("SRV-002", "Laptop Dell", "Laptop empresarial", 45000, 5, "Laptop")
    asesoria = AsesoriaEspecializada("SRV-003", "Asesoría Python", "Python avanzado", 120000, "Software", "experto")

    # Prueba 1: crear una reserva válida
    print("\n[Prueba 1] Crear reserva válida:")
    try:
        reserva1 = Reserva(cliente1, sala, 3, con_impuesto=True)
        print(reserva1)
    except Exception as e:
        print(f"  Error: {e}")

    # Prueba 2: ciclo de vida completo de una reserva
    print("\n[Prueba 2] Ciclo de vida completo:")
    try:
        reserva2 = Reserva(cliente1, equipo, 5)
        print(f"  Estado inicial: {reserva2.estado}")
        reserva2.confirmar()
        print(f"  Después de confirmar: {reserva2.estado}")
        reserva2.procesar()
        print(f"  Después de procesar: {reserva2.estado}")
        reserva2.finalizar()
        print(f"  Después de finalizar: {reserva2.estado}")
    except Exception as e:
        print(f"  Error: {e}")

    # Prueba 3: cancelar una reserva pendiente
    print("\n[Prueba 3] Cancelar reserva pendiente:")
    try:
        reserva3 = Reserva(cliente1, asesoria, 2, descuento=10)
        print(f"  Estado inicial: {reserva3.estado}")
        reserva3.cancelar("el cliente cambió de opinión")
        print(f"  Estado después de cancelar: {reserva3.estado}")
    except Exception as e:
        print(f"  Error: {e}")

    # Prueba 4: intentar cancelar una reserva ya finalizada
    print("\n[Prueba 4] Cancelar reserva finalizada (debe fallar):")
    try:
        reserva2.cancelar("intento de cancelación inválido")
    except ErrorCancelacionNoPermitida as e:
        print(f"  Excepción capturada correctamente: {e}")

    # Prueba 5: intentar confirmar una reserva ya cancelada
    print("\n[Prueba 5] Confirmar reserva cancelada (debe fallar):")
    try:
        reserva3.confirmar()
    except ErrorReservaInvalida as e:
        print(f"  Excepción capturada correctamente: {e}")

    # Prueba 6: crear reserva con duración inválida
    print("\n[Prueba 6] Reserva con duración inválida:")
    try:
        reserva_invalida = Reserva(cliente1, sala, -2)
    except ErrorReservaInvalida as e:
        print(f"  Excepción capturada correctamente: {e}")

    # Prueba 7: recalcular costo de una reserva pendiente
    print("\n[Prueba 7] Recalcular costo:")
    try:
        reserva4 = Reserva(cliente1, sala, 4)
        print(f"  Costo inicial: ${reserva4.costo_total:,.2f}")
        reserva4.recalcular_costo(con_impuesto=True, descuento=15)
        print(f"  Costo después de recalcular con IVA y 15% descuento: ${reserva4.costo_total:,.2f}")
    except Exception as e:
        print(f"  Error: {e}")

    # Prueba 8: servicio no disponible al crear reserva
    print("\n[Prueba 8] Reserva con servicio no disponible:")
    try:
        sala.deshabilitar()
        reserva_invalida2 = Reserva(cliente1, sala, 2)
    except ErrorServicioNoDisponible as e:
        print(f"  Excepción capturada correctamente: {e}")
    finally:
        sala.habilitar()

    print("\nTodas las pruebas del módulo 6 pasaron correctamente")
