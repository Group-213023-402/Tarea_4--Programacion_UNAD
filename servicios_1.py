
# MÓDULO 5: servicios.py
# Este módulo define la clase abstracta Servicio y los tres servicios especializados que ofrece la empresa Software FJ:
#   1. ReservaSala: para reservar salas de reuniones
#   2. AlquilerEquipo: para alquilar equipos tecnológicos
#   3. AsesoriEspecializada: para contratar asesorías con expertos
# Cada servicio hereda de Servicio y aplica polimorfismo implementando sus propios métodos de cálculo de costos y validaciones.

from entidad_base import EntidadBase
from excepciones import (
    ErrorServicioInvalido,
    ErrorServicioNoDisponible,
    ErrorCalculo
)
from logger import logger
from abc import abstractmethod


class Servicio(EntidadBase):
    """
    Clase abstracta que representa un servicio genérico de Software FJ.
    Define la estructura común que deben tener todos los servicios.
    Los tres servicios especializados heredan de esta clase.
    """

    def __init__(self, codigo, nombre, descripcion, tarifa_base):

        self._validar_nombre_servicio(nombre)
        self._validar_tarifa(tarifa_base)

        super().__init__(codigo)

        self._nombre = nombre.strip()
        self._descripcion = descripcion.strip()
        self._tarifa_base = float(tarifa_base)

        # disponible indica si el servicio puede reservarse en este momento
        self._disponible = True

        logger.info(f"Servicio creado: {self._nombre} con código {self._identificador}")

    def _validar_nombre_servicio(self, nombre):
        if not nombre or nombre.strip() == "":
            raise ErrorServicioInvalido("nombre", nombre, "no puede estar vacío")
        if len(nombre.strip()) < 3:
            raise ErrorServicioInvalido("nombre", nombre, "debe tener al menos 3 caracteres")

    def _validar_tarifa(self, tarifa):
        try:
            valor = float(tarifa)
        except (TypeError, ValueError):
            raise ErrorServicioInvalido("tarifa_base", tarifa, "debe ser un número válido")
        if valor <= 0:
            raise ErrorServicioInvalido("tarifa_base", tarifa, "debe ser mayor a cero")

    @property
    def nombre(self):
        return self._nombre

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    def habilitar(self):
        # Marca el servicio como disponible para ser reservado
        self._disponible = True
        logger.info(f"Servicio {self._nombre} habilitado")

    def deshabilitar(self):
        # Marca el servicio como no disponible temporalmente
        self._disponible = False
        logger.advertencia(f"Servicio {self._nombre} deshabilitado")

    def verificar_disponibilidad(self):
        # Verifica si el servicio está disponible y lanza excepción si no lo está
        if not self._disponible:
            raise ErrorServicioNoDisponible(
                self._nombre,
                "el servicio está marcado como no disponible"
            )
        if not self._activo:
            raise ErrorServicioNoDisponible(
                self._nombre,
                "el servicio fue desactivado del sistema"
            )

    def calcular_costo(self, duracion, con_impuesto=False, descuento=0):
        # Calcula el costo total del servicio según la duración y parámetros opcionales
        # duracion es la cantidad de horas o unidades del servicio
        # con_impuesto indica si se aplica el IVA del 19%
        # descuento es el porcentaje de descuento a aplicar, por ejemplo 10 para 10%

        try:
            if duracion <= 0:
                raise ErrorCalculo("duración", "la duración debe ser mayor a cero")
            if not (0 <= descuento <= 100):
                raise ErrorCalculo("descuento", "el descuento debe estar entre 0 y 100")

            # Llamamos al método abstracto que cada servicio implementa a su manera
            costo_base = self._calcular_costo_base(duracion)

            # Aplicamos el descuento si existe
            if descuento > 0:
                costo_base = costo_base * (1 - descuento / 100)

            # Aplicamos el impuesto del 19% si se solicita
            if con_impuesto:
                costo_final = costo_base * 1.19
            else:
                costo_final = costo_base

            if costo_final < 0:
                raise ErrorCalculo("costo final", "el resultado del cálculo es negativo")

            return round(costo_final, 2)

        except ErrorCalculo:
            raise
        except Exception as e:
            raise ErrorCalculo("calcular_costo", str(e)) from e

    @abstractmethod
    def _calcular_costo_base(self, duracion):
        # Método abstracto que cada servicio especializado implementa con su propia lógica de cálculo de costo base
        pass

    @abstractmethod
    def describir(self):
        # Método abstracto que cada servicio implementa para describirse
        pass

    @abstractmethod
    def validar_parametros(self, **kwargs):
        # Método abstracto para validar parámetros específicos de cada servicio
        pass

    def obtener_info(self):
        # Implementación del método abstracto de EntidadBase
        info = self.obtener_info_base()
        info.update({
            "nombre": self._nombre,
            "descripcion": self._descripcion,
            "tarifa_base": f"${self._tarifa_base:,.2f}",
            "disponible": self._disponible
        })
        return info

    def validar(self):
        # Implementación del método abstracto de EntidadBase
        try:
            self._validar_nombre_servicio(self._nombre)
            self._validar_tarifa(self._tarifa_base)
            return True
        except ErrorServicioInvalido as e:
            logger.error(f"Servicio {self._identificador} falló la validación: {e}")
            return False


class ReservaSala(Servicio):
    """
    Servicio especializado para la reserva de salas de reuniones.
    Hereda de Servicio e implementa sus propios métodos de cálculo y validación.
    El costo se calcula por hora según la capacidad de la sala.
    """

    def __init__(self, codigo, nombre, descripcion, tarifa_base, capacidad_maxima):
        # capacidad_maxima es el número máximo de personas que puede albergar la sala

        if not isinstance(capacidad_maxima, int) or capacidad_maxima <= 0:
            raise ErrorServicioInvalido(
                "capacidad_maxima", capacidad_maxima,
                "debe ser un número entero mayor a cero"
            )

        super().__init__(codigo, nombre, descripcion, tarifa_base)
        self._capacidad_maxima = capacidad_maxima

    @property
    def capacidad_maxima(self):
        return self._capacidad_maxima

    def _calcular_costo_base(self, duracion):
        # El costo base de una sala es simplemente tarifa por hora multiplicada por la cantidad de horas que se va a usar
        return self._tarifa_base * duracion

    def describir(self):
        # Implementación del método abstracto describir
        return (
            f"Sala: {self._nombre} | "
            f"Capacidad: {self._capacidad_maxima} personas | "
            f"Tarifa: ${self._tarifa_base:,.2f} por hora | "
            f"Disponible: {'Sí' if self._disponible else 'No'}"
        )

    def validar_parametros(self, **kwargs):
        # Valida parámetros específicos para reservar una sala
        duracion = kwargs.get("duracion", 0)
        asistentes = kwargs.get("asistentes", 0)

        if duracion <= 0:
            raise ErrorServicioInvalido("duracion", duracion, "debe ser mayor a cero")
        if duracion > 12:
            raise ErrorServicioInvalido("duracion", duracion, "no puede exceder 12 horas")
        if asistentes <= 0:
            raise ErrorServicioInvalido("asistentes", asistentes, "debe ser al menos 1 persona")
        if asistentes > self._capacidad_maxima:
            raise ErrorServicioInvalido(
                "asistentes", asistentes,
                f"excede la capacidad máxima de {self._capacidad_maxima} personas"
            )
        return True

    def obtener_info(self):
        info = super().obtener_info()
        info["capacidad_maxima"] = self._capacidad_maxima
        info["tipo_servicio"] = "Reserva de Sala"
        return info


class AlquilerEquipo(Servicio):
    """
    Servicio especializado para el alquiler de equipos tecnológicos.
    El costo se calcula por día de alquiler y varía según la cantidad de equipos.
    """

    def __init__(self, codigo, nombre, descripcion, tarifa_base, cantidad_disponible, tipo_equipo):
        # cantidad_disponible se refiere a cuántas unidades de ese equipo hay para alquilar
        # tipo_equipo describe el tipo de equipo, por ejemplo laptop, proyector, etc.

        if not isinstance(cantidad_disponible, int) or cantidad_disponible <= 0:
            raise ErrorServicioInvalido(
                "cantidad_disponible", cantidad_disponible,
                "debe ser un número entero mayor a cero"
            )
        if not tipo_equipo or tipo_equipo.strip() == "":
            raise ErrorServicioInvalido("tipo_equipo", tipo_equipo, "no puede estar vacío")

        super().__init__(codigo, nombre, descripcion, tarifa_base)
        self._cantidad_disponible = cantidad_disponible
        self._tipo_equipo = tipo_equipo.strip()

    @property
    def cantidad_disponible(self):
        return self._cantidad_disponible

    @property
    def tipo_equipo(self):
        return self._tipo_equipo

    def _calcular_costo_base(self, duracion):
        # Para el alquiler de equipos la duración representa días
        # El costo base es tarifa por día multiplicada por los días solicitados
        return self._tarifa_base * duracion

    def describir(self):
        return (
            f"Equipo: {self._nombre} | "
            f"Tipo: {self._tipo_equipo} | "
            f"Unidades disponibles: {self._cantidad_disponible} | "
            f"Tarifa: ${self._tarifa_base:,.2f} por día | "
            f"Disponible: {'Sí' if self._disponible else 'No'}"
        )

    def validar_parametros(self, **kwargs):
        # Valida parámetros específicos para alquilar un equipo
        # duracion es la cantidad de días, cantidad es cuántos equipos se necesitan
        duracion = kwargs.get("duracion", 0)
        cantidad = kwargs.get("cantidad", 1)

        if duracion <= 0:
            raise ErrorServicioInvalido("duracion", duracion, "debe ser mayor a cero")
        if duracion > 30:
            raise ErrorServicioInvalido("duracion", duracion, "no puede exceder 30 días")
        if cantidad <= 0:
            raise ErrorServicioInvalido("cantidad", cantidad, "debe ser al menos 1 unidad")
        if cantidad > self._cantidad_disponible:
            raise ErrorServicioInvalido(
                "cantidad", cantidad,
                f"supera las unidades disponibles: {self._cantidad_disponible}"
            )
        return True

    def obtener_info(self):
        info = super().obtener_info()
        info["tipo_equipo"] = self._tipo_equipo
        info["cantidad_disponible"] = self._cantidad_disponible
        info["tipo_servicio"] = "Alquiler de Equipo"
        return info


class AsesoriaEspecializada(Servicio):
    """
    Servicio especializado para asesorías con expertos de Software FJ.
    El costo varía según el nivel del asesor y la duración de la sesión.
    """

    NIVELES_VALIDOS = ["junior", "senior", "experto"]
    # Los multiplicadores definen cuánto más caro es cada nivel respecto a la tarifa base
    MULTIPLICADORES_NIVEL = {
        "junior": 1.0,
        "senior": 1.5,
        "experto": 2.0
    }

    def __init__(self, codigo, nombre, descripcion, tarifa_base, especialidad, nivel_asesor):
        # especialidad describe el área de conocimiento, por ejemplo ciberseguridad
        # nivel_asesor puede ser junior, senior o experto

        if not especialidad or especialidad.strip() == "":
            raise ErrorServicioInvalido("especialidad", especialidad, "no puede estar vacía")

        nivel_lower = nivel_asesor.strip().lower() if nivel_asesor else ""
        if nivel_lower not in self.NIVELES_VALIDOS:
            raise ErrorServicioInvalido(
                "nivel_asesor", nivel_asesor,
                f"debe ser uno de: {', '.join(self.NIVELES_VALIDOS)}"
            )

        super().__init__(codigo, nombre, descripcion, tarifa_base)
        self._especialidad = especialidad.strip()
        self._nivel_asesor = nivel_lower

    @property
    def especialidad(self):
        return self._especialidad

    @property
    def nivel_asesor(self):
        return self._nivel_asesor

    def _calcular_costo_base(self, duracion):
        # El costo base de una asesoría depende del nivel del asesor y la duración en horas
        multiplicador = self.MULTIPLICADORES_NIVEL[self._nivel_asesor]
        return self._tarifa_base * duracion * multiplicador

    def describir(self):
        return (
            f"Asesoría: {self._nombre} | "
            f"Especialidad: {self._especialidad} | "
            f"Nivel: {self._nivel_asesor.capitalize()} | "
            f"Tarifa base: ${self._tarifa_base:,.2f} por hora | "
            f"Multiplicador: x{self.MULTIPLICADORES_NIVEL[self._nivel_asesor]} | "
            f"Disponible: {'Sí' if self._disponible else 'No'}"
        )

    def validar_parametros(self, **kwargs):
        # Valida parámetros específicos para contratar una asesoría
        duracion = kwargs.get("duracion", 0)

        if duracion <= 0:
            raise ErrorServicioInvalido("duracion", duracion, "debe ser mayor a cero")
        if duracion > 8:
            raise ErrorServicioInvalido("duracion", duracion, "una asesoría no puede exceder 8 horas")
        return True

    def obtener_info(self):
        info = super().obtener_info()
        info["especialidad"] = self._especialidad
        info["nivel_asesor"] = self._nivel_asesor.capitalize()
        info["multiplicador"] = self.MULTIPLICADORES_NIVEL[self._nivel_asesor]
        info["tipo_servicio"] = "Asesoría Especializada"
        return info


# Este bloque solo se ejecutara si se corre este archivo directamente
if __name__ == "__main__":

    print("PRUEBA DEL MÓDULO 5: servicios.py")
    print("=" * 60)

    # Prueba 1: crear los tres servicios válidos
    print("\n[Prueba 1] Crear los tres servicios:")
    sala = ReservaSala("SRV-001", "Sala de Juntas A", "Sala equipada para reuniones", 80000, 10)
    equipo = AlquilerEquipo("SRV-002", "Laptop Dell", "Laptop para eventos", 45000, 5, "Laptop")
    asesoria = AsesoriaEspecializada("SRV-003", "Asesoría en Python", "Consultoría en Python avanzado", 120000, "Desarrollo de Software", "senior")
    print(f"  Sala creada: {sala.describir()}")
    print(f"  Equipo creado: {equipo.describir()}")
    print(f"  Asesoría creada: {asesoria.describir()}")

    # Prueba 2: calcular costos sin impuesto
    print("\n[Prueba 2] Calcular costos sin impuesto:")
    print(f"  Sala 3 horas: ${sala.calcular_costo(3):,.2f}")
    print(f"  Equipo 5 días: ${equipo.calcular_costo(5):,.2f}")
    print(f"  Asesoría 2 horas: ${asesoria.calcular_costo(2):,.2f}")

    # Prueba 3: calcular costos con impuesto y descuento (métodos sobrecargados)
    print("\n[Prueba 3] Calcular costos con impuesto y descuento:")
    print(f"  Sala 3h con IVA: ${sala.calcular_costo(3, con_impuesto=True):,.2f}")
    print(f"  Equipo 5d con 10% descuento: ${equipo.calcular_costo(5, descuento=10):,.2f}")
    print(f"  Asesoría 2h con IVA y 15% descuento: ${asesoria.calcular_costo(2, con_impuesto=True, descuento=15):,.2f}")

    # Prueba 4: validar parámetros correctos
    print("\n[Prueba 4] Validar parámetros correctos:")
    print(f"  Sala válida (5h, 8 asistentes): {sala.validar_parametros(duracion=5, asistentes=8)}")
    print(f"  Equipo válido (3 días, 2 unidades): {equipo.validar_parametros(duracion=3, cantidad=2)}")
    print(f"  Asesoría válida (2h): {asesoria.validar_parametros(duracion=2)}")

    # Prueba 5: validar parámetros incorrectos
    print("\n[Prueba 5] Validar parámetros incorrectos:")
    try:
        sala.validar_parametros(duracion=5, asistentes=15)
    except ErrorServicioInvalido as e:
        print(f"  Sala con exceso de asistentes: {e}")

    try:
        equipo.validar_parametros(duracion=3, cantidad=10)
    except ErrorServicioInvalido as e:
        print(f"  Equipo con cantidad excesiva: {e}")

    # Prueba 6: servicio no disponible
    print("\n[Prueba 6] Servicio no disponible:")
    sala.deshabilitar()
    try:
        sala.verificar_disponibilidad()
    except ErrorServicioNoDisponible as e:
        print(f"  Excepción capturada: {e}")
    sala.habilitar()

    # Prueba 7: polimorfismo, tratar todos los servicios como Servicio genérico
    print("\n[Prueba 7] Polimorfismo, misma llamada en los tres servicios:")
    servicios = [sala, equipo, asesoria]
    for servicio in servicios:
        costo = servicio.calcular_costo(2, con_impuesto=True)
        print(f"  {type(servicio).__name__}: costo 2 unidades con IVA = ${costo:,.2f}")

    print("\nTodas las pruebas del módulo 5 pasaron correctamente")
