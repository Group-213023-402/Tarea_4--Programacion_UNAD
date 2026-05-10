# MÓDULO 7: gestor.py
# Este módulo define la clase GestorSistema que actúa como el cerebro central del sistema. Se encarga de coordinar todas las operaciones entre clientes,
# servicios y reservas, manteniendo las listas internas de cada uno y exponiendo métodos para registrar, buscar, listar y eliminar entidades.
# Es el único módulo que el archivo main.py necesita importar para operar
# todo el sistema.

from cliente import Cliente
from servicios import Servicio, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import (
    ErrorClienteInvalido,
    ErrorClienteDuplicado,
    ErrorClienteNoEncontrado,
    ErrorServicioInvalido,
    ErrorServicioNoDisponible,
    ErrorServicioNoEncontrado,
    ErrorReservaInvalida,
    ErrorReservaNoEncontrada,
    ErrorCancelacionNoPermitida,
    ErrorSistemaFJ
)
from logger import logger


class GestorSistema:
    """
    Clase central del sistema Software FJ.
    Administra las listas de clientes, servicios y reservas,
    y coordina todas las operaciones del sistema sin usar base de datos.
    Toda la información se mantiene en memoria usando listas y diccionarios.
    """

    def __init__(self):
        # Usamos diccionarios para almacenar las entidades porque permiten buscar por identificador de forma rápida y directa.
        # La clave es el identificador y el valor es el objeto correspondiente.

        self._clientes  = {}
        self._servicios = {}
        self._reservas  = {}

        logger.info("Sistema Software FJ iniciado correctamente")

    # definimos los metodos para gestion de clientes

    def registrar_cliente(self, documento, nombre, email, telefono, direccion=""):
        """
        Registra un nuevo cliente en el sistema.
        Lanza excepción si el documento ya está registrado o los datos son inválidos.
        """
        try:
            # Verificamos que no exista un cliente con ese documento
            if documento in self._clientes:
                raise ErrorClienteDuplicado(documento)

            # Creamos el objeto Cliente, las validaciones ocurren dentro del constructor
            nuevo_cliente = Cliente(documento, nombre, email, telefono, direccion)

            # Guardamos el cliente en el diccionario usando su documento como clave
            self._clientes[documento] = nuevo_cliente
            logger.info(f"Cliente {nombre} registrado exitosamente en el sistema")
            return nuevo_cliente

        except (ErrorClienteDuplicado, ErrorClienteInvalido):
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error inesperado al registrar cliente: {e}") from e

    def buscar_cliente(self, documento):
        """
        Busca y retorna un cliente por su número de documento.
        Lanza excepción si no existe.
        """
        try:
            if documento not in self._clientes:
                raise ErrorClienteNoEncontrado(documento)
            return self._clientes[documento]

        except ErrorClienteNoEncontrado:
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error inesperado al buscar cliente: {e}") from e

    def listar_clientes(self, solo_activos=True):
        """
        Retorna la lista de todos los clientes registrados.
        Si solo_activos es True retorna únicamente los clientes activos.
        """
        try:
            if solo_activos:
                return [c for c in self._clientes.values() if c.activo]
            return list(self._clientes.values())

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al listar clientes: {e}") from e

    def desactivar_cliente(self, documento):
        """
        Desactiva un cliente del sistema sin eliminarlo para conservar el historial.
        """
        try:
            cliente = self.buscar_cliente(documento)
            cliente.desactivar()
            logger.info(f"Cliente {documento} desactivado del sistema")

        except ErrorClienteNoEncontrado:
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al desactivar cliente: {e}") from e

    # definimos los metodos para la gestion de los servicios

    def registrar_sala(self, codigo, nombre, descripcion, tarifa, capacidad):
        """
        Registra una nueva sala de reuniones en el catálogo de servicios.
        """
        try:
            if codigo in self._servicios:
                raise ErrorServicioInvalido("codigo", codigo, "ya existe un servicio con ese código")

            sala = ReservaSala(codigo, nombre, descripcion, tarifa, capacidad)
            self._servicios[codigo] = sala
            logger.info(f"Sala {nombre} registrada en el catálogo")
            return sala

        except (ErrorServicioInvalido, ErrorServicioNoDisponible):
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al registrar sala: {e}") from e

    def registrar_equipo(self, codigo, nombre, descripcion, tarifa, cantidad, tipo):
        """
        Registra un nuevo equipo de alquiler en el catálogo de servicios.
        """
        try:
            if codigo in self._servicios:
                raise ErrorServicioInvalido("codigo", codigo, "ya existe un servicio con ese código")

            equipo = AlquilerEquipo(codigo, nombre, descripcion, tarifa, cantidad, tipo)
            self._servicios[codigo] = equipo
            logger.info(f"Equipo {nombre} registrado en el catálogo")
            return equipo

        except ErrorServicioInvalido:
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al registrar equipo: {e}") from e

    def registrar_asesoria(self, codigo, nombre, descripcion, tarifa, especialidad, nivel):
        """
        Registra una nueva asesoría especializada en el catálogo de servicios.
        """
        try:
            if codigo in self._servicios:
                raise ErrorServicioInvalido("codigo", codigo, "ya existe un servicio con ese código")

            asesoria = AsesoriaEspecializada(codigo, nombre, descripcion, tarifa, especialidad, nivel)
            self._servicios[codigo] = asesoria
            logger.info(f"Asesoría {nombre} registrada en el catálogo")
            return asesoria

        except ErrorServicioInvalido:
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al registrar asesoría: {e}") from e

    def buscar_servicio(self, codigo):
        """
        Busca y retorna un servicio por su código.
        Lanza excepción si no existe.
        """
        try:
            if codigo not in self._servicios:
                raise ErrorServicioNoEncontrado(codigo)
            return self._servicios[codigo]

        except ErrorServicioNoEncontrado:
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al buscar servicio: {e}") from e

    def listar_servicios(self, solo_disponibles=True):
        """
        Retorna la lista de servicios del catálogo.
        Si solo_disponibles es True retorna únicamente los servicios disponibles.
        """
        try:
            if solo_disponibles:
                return [s for s in self._servicios.values() if s.disponible and s.activo]
            return list(self._servicios.values())

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al listar servicios: {e}") from e

    def deshabilitar_servicio(self, codigo):
        """
        Marca un servicio como no disponible temporalmente.
        """
        try:
            servicio = self.buscar_servicio(codigo)
            servicio.deshabilitar()

        except ErrorServicioNoEncontrado:
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al deshabilitar servicio: {e}") from e

    def habilitar_servicio(self, codigo):
        """
        Marca un servicio como disponible nuevamente.
        """
        try:
            servicio = self.buscar_servicio(codigo)
            servicio.habilitar()

        except ErrorServicioNoEncontrado:
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al habilitar servicio: {e}") from e

    # Definimos los metodos para la gestion de reservas

    def crear_reserva(self, documento_cliente, codigo_servicio, duracion,
                      con_impuesto=False, descuento=0):
        """
        Crea una nueva reserva vinculando un cliente con un servicio.
        Busca ambos objetos por sus identificadores y delega la creación a la clase Reserva.
        """
        try:
            # Buscamos el cliente y el servicio en las listas del sistema
            cliente  = self.buscar_cliente(documento_cliente)
            servicio = self.buscar_servicio(codigo_servicio)

            # Creamos la reserva, todas las validaciones ocurren en el constructor de Reserva
            nueva_reserva = Reserva(cliente, servicio, duracion, con_impuesto, descuento)

            # Guardamos la reserva en el diccionario usando su ID como clave
            self._reservas[nueva_reserva.identificador] = nueva_reserva
            logger.info(f"Reserva {nueva_reserva.identificador} creada y registrada en el sistema")
            return nueva_reserva

        except (ErrorClienteNoEncontrado, ErrorServicioNoEncontrado,
                ErrorReservaInvalida, ErrorServicioNoDisponible):
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error inesperado al crear reserva: {e}") from e

    def buscar_reserva(self, id_reserva):
        """
        Busca y retorna una reserva por su ID.
        Lanza excepción si no existe.
        """
        try:
            if id_reserva not in self._reservas:
                raise ErrorReservaNoEncontrada(id_reserva)
            return self._reservas[id_reserva]

        except ErrorReservaNoEncontrada:
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al buscar reserva: {e}") from e

    def confirmar_reserva(self, id_reserva):
        """
        Confirma una reserva que está en estado pendiente.
        """
        try:
            reserva = self.buscar_reserva(id_reserva)
            reserva.confirmar()
            return reserva

        except (ErrorReservaNoEncontrada, ErrorReservaInvalida, ErrorServicioNoDisponible):
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al confirmar reserva: {e}") from e

    def procesar_reserva(self, id_reserva):
        """
        Cambia el estado de una reserva confirmada a en proceso.
        """
        try:
            reserva = self.buscar_reserva(id_reserva)
            reserva.procesar()
            return reserva

        except (ErrorReservaNoEncontrada, ErrorReservaInvalida):
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al procesar reserva: {e}") from e

    def finalizar_reserva(self, id_reserva):
        """
        Finaliza una reserva que está en proceso.
        """
        try:
            reserva = self.buscar_reserva(id_reserva)
            reserva.finalizar()
            return reserva

        except (ErrorReservaNoEncontrada, ErrorReservaInvalida):
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al finalizar reserva: {e}") from e

    def cancelar_reserva(self, id_reserva, motivo=""):
        """
        Cancela una reserva si su estado lo permite.
        """
        try:
            reserva = self.buscar_reserva(id_reserva)
            reserva.cancelar(motivo)
            return reserva

        except (ErrorReservaNoEncontrada, ErrorCancelacionNoPermitida):
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al cancelar reserva: {e}") from e

    def listar_reservas(self, estado=None):
        """
        Retorna la lista de todas las reservas del sistema.
        Si se pasa un estado filtra las reservas por ese estado.
        Por ejemplo listar_reservas(estado="confirmada") retorna solo las confirmadas.
        """
        try:
            if estado:
                return [r for r in self._reservas.values() if r.estado == estado]
            return list(self._reservas.values())

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al listar reservas: {e}") from e

    def reservas_por_cliente(self, documento):
        """
        Retorna todas las reservas asociadas a un cliente específico.
        """
        try:
            cliente = self.buscar_cliente(documento)
            return [r for r in self._reservas.values()
                    if r.cliente.identificador == cliente.identificador]

        except ErrorClienteNoEncontrado:
            raise

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al listar reservas del cliente: {e}") from e

    # Definimos los metodos de reporte y resumen

    def resumen_sistema(self):
        """
        Retorna un resumen general del estado actual del sistema.
        """
        try:
            total_clientes  = len(self._clientes)
            clientes_activos = len(self.listar_clientes(solo_activos=True))
            total_servicios  = len(self._servicios)
            servicios_disponibles = len(self.listar_servicios(solo_disponibles=True))
            total_reservas   = len(self._reservas)

            # Contamos reservas por estado
            estados = [Reserva.ESTADO_PENDIENTE, Reserva.ESTADO_CONFIRMADA,
                       Reserva.ESTADO_EN_PROCESO, Reserva.ESTADO_FINALIZADA,
                       Reserva.ESTADO_CANCELADA]

            conteo_estados = {}
            for estado in estados:
                conteo_estados[estado] = len(self.listar_reservas(estado=estado))

            # Calculamos los ingresos totales de reservas finalizadas
            ingresos_totales = sum(
                r.costo_total for r in self._reservas.values()
                if r.estado == Reserva.ESTADO_FINALIZADA
            )

            resumen = {
                "clientes_registrados": total_clientes,
                "clientes_activos": clientes_activos,
                "servicios_registrados": total_servicios,
                "servicios_disponibles": servicios_disponibles,
                "total_reservas": total_reservas,
                "reservas_por_estado": conteo_estados,
                "ingresos_finalizados": f"${ingresos_totales:,.2f}"
            }

            return resumen

        except Exception as e:
            raise ErrorSistemaFJ(f"Error al generar resumen del sistema: {e}") from e

    def imprimir_resumen(self):
        """
        Imprime el resumen del sistema de forma legible en pantalla.
        """
        resumen = self.resumen_sistema()
        print("\n" + "=" * 60)
        print("  RESUMEN DEL SISTEMA SOFTWARE FJ")
        print("=" * 60)
        print(f"  Clientes registrados : {resumen['clientes_registrados']}")
        print(f"  Clientes activos     : {resumen['clientes_activos']}")
        print(f"  Servicios registrados: {resumen['servicios_registrados']}")
        print(f"  Servicios disponibles: {resumen['servicios_disponibles']}")
        print(f"  Total reservas       : {resumen['total_reservas']}")
        print("\n  Reservas por estado:")
        for estado, cantidad in resumen["reservas_por_estado"].items():
            print(f"    {estado:<15}: {cantidad}")
        print(f"\n  Ingresos finalizados : {resumen['ingresos_finalizados']}")
        print("=" * 60)


# Este bloque solo se ejecuta si se corre este archivo directamente
if __name__ == "__main__":

    print("PRUEBA DEL MÓDULO 7: gestor.py")
    print("=" * 60)

    gestor = GestorSistema()

    # Prueba 1: registrar clientes válidos
    print("\n[Prueba 1] Registrar clientes válidos:")
    try:
        c1 = gestor.registrar_cliente("1020304050", "Juan Pérez", "juan@gmail.com", "3001234567", "Calle 1")
        c2 = gestor.registrar_cliente("2030405060", "María López", "maria@gmail.com", "3109876543")
        print(f"  Cliente 1: {c1.nombre}")
        print(f"  Cliente 2: {c2.nombre}")
    except Exception as e:
        print(f"  Error: {e}")

    # Prueba 2: registrar cliente duplicado
    print("\n[Prueba 2] Registrar cliente duplicado:")
    try:
        gestor.registrar_cliente("1020304050", "Juan Otro", "otro@gmail.com", "3001111111")
    except ErrorClienteDuplicado as e:
        print(f"  Excepción capturada: {e}")

    # Prueba 3: registrar servicios
    print("\n[Prueba 3] Registrar servicios:")
    try:
        s1 = gestor.registrar_sala("SRV-001", "Sala Principal", "Sala de juntas grande", 80000, 10)
        s2 = gestor.registrar_equipo("SRV-002", "Laptop Dell", "Laptop empresarial", 45000, 5, "Laptop")
        s3 = gestor.registrar_asesoria("SRV-003", "Asesoría Python", "Python avanzado", 120000, "Software", "senior")
        print(f"  Servicio 1: {s1.nombre}")
        print(f"  Servicio 2: {s2.nombre}")
        print(f"  Servicio 3: {s3.nombre}")
    except Exception as e:
        print(f"  Error: {e}")

    # Prueba 4: crear reservas válidas
    print("\n[Prueba 4] Crear reservas válidas:")
    try:
        r1 = gestor.crear_reserva("1020304050", "SRV-001", 3, con_impuesto=True)
        r2 = gestor.crear_reserva("2030405060", "SRV-002", 5)
        print(f"  Reserva 1: {r1.identificador} | Costo: ${r1.costo_total:,.2f}")
        print(f"  Reserva 2: {r2.identificador} | Costo: ${r2.costo_total:,.2f}")
    except Exception as e:
        print(f"  Error: {e}")

    # Prueba 5: ciclo de vida de una reserva a través del gestor
    print("\n[Prueba 5] Ciclo de vida completo a través del gestor:")
    try:
        gestor.confirmar_reserva(r1.identificador)
        gestor.procesar_reserva(r1.identificador)
        gestor.finalizar_reserva(r1.identificador)
        print(f"  Reserva {r1.identificador} finalizada. Estado: {r1.estado}")
    except Exception as e:
        print(f"  Error: {e}")

    # Prueba 6: cancelar una reserva
    print("\n[Prueba 6] Cancelar reserva:")
    try:
        gestor.cancelar_reserva(r2.identificador, "el cliente no se presentó")
        print(f"  Reserva {r2.identificador} cancelada. Estado: {r2.estado}")
    except Exception as e:
        print(f"  Error: {e}")

    # Prueba 7: buscar cliente inexistente
    print("\n[Prueba 7] Buscar cliente inexistente:")
    try:
        gestor.buscar_cliente("9999999999")
    except ErrorClienteNoEncontrado as e:
        print(f"  Excepción capturada: {e}")

    # Prueba 8: servicio no disponible
    print("\n[Prueba 8] Reservar servicio no disponible:")
    try:
        gestor.deshabilitar_servicio("SRV-003")
        gestor.crear_reserva("1020304050", "SRV-003", 2)
    except ErrorServicioNoDisponible as e:
        print(f"  Excepción capturada: {e}")
    finally:
        gestor.habilitar_servicio("SRV-003")

    # Prueba 9: imprimir resumen del sistema
    print("\n[Prueba 9] Resumen del sistema:")
    gestor.imprimir_resumen()

    print("\nTodas las pruebas del módulo 7 pasaron correctamente")
