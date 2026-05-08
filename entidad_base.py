# MÓDULO 3: entidad_base.py
# En este módulo definimos la clase abstracta base del sistema

from abc import ABC, abstractmethod
# ABC significa Abstract Base Class, es la clase de Python que nos permite crear clases abstractas
# abstractmethod es el decorador que marca el método como abstracto, lo que obliga a las clases hijas a implementarlo obligatoriamente.

import datetime
# Se usa para registrar la fecha y hora en que se crea cada entidad

from logger import logger
# Importamos el logger que creamos en el módulo 2 para registrar eventos
# Usamos la instancia global que definimos al final de logger.py

from excepciones import ErrorSistemaFJ
# Importamos la excepción base para usarla en las validaciones generales


class EntidadBase(ABC):
    """
    Clase abstracta base del sistema Software FJ.
    Define la estructura y comportamiento común que deben tener
    todas las entidades del sistema como Cliente, Servicio y Reserva.
    Al heredar de ABC esta clase no puede instanciarse directamente.
    """

    def __init__(self, identificador):

        # Validamos que el identificador no esté vacío antes de asignarlo
        if not identificador or str(identificador).strip() == "":
            raise ErrorSistemaFJ("El identificador de la entidad no puede estar vacío")

        # El guion bajo al inicio nos indica que es un atributo protegido
        self._identificador = str(identificador).strip()

        # Guardamos la fecha y hora exacta en que se creó esta entidad
        self._fecha_creacion = datetime.datetime.now()

        self._activo = True

        # Registramos en el log que se creó una nueva entidad
        logger.info(f"Nueva entidad creada: {type(self).__name__} con ID {self._identificador}")

    # Los métodos decorados con @property permiten acceder a los atributos protegidos como si fueran atributos públicos pero de forma controlada(encapsulacion).

    @property
    def identificador(self):
        # Permite leer el identificador desde fuera de la clase
        return self._identificador

    @property
    def fecha_creacion(self):
        # Permite leer la fecha de creación desde fuera de la clase
        return self._fecha_creacion

    @property
    def activo(self):
        # Permite saber si la entidad está activa o no
        return self._activo

    def activar(self):
        # Cambia el estado de la entidad a activo
        if self._activo:
            logger.advertencia(f"{type(self).__name__} {self._identificador} ya estaba activo")
        else:
            self._activo = True
            logger.info(f"{type(self).__name__} {self._identificador} fue activado")

    def desactivar(self):
        # Cambia el estado de la entidad a inactivo
        # Esto es mejor que eliminar la entidad, ya que asi se conserva el historial
        if not self._activo:
            logger.advertencia(f"{type(self).__name__} {self._identificador} ya estaba inactivo")
        else:
            self._activo = False
            logger.info(f"{type(self).__name__} {self._identificador} fue desactivado")

    def obtener_info_base(self):
        # Retorna un diccionario con la información básica de cualquier entidad
        # Este metodo pueden usarlo todas las clases hijas para incluir la información base dentro de su propia información
        return {
            "identificador": self._identificador,
            "tipo": type(self).__name__,
            "fecha_creacion": self._fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
            "activo": self._activo
        }

    @abstractmethod
    def obtener_info(self):
        # Este método es abstracto, lo que significa que cada clase hija esta obligada a implementarlo con su propia version
        # Si una clase hereda de EntidadBase y no implementa este método,
        # Python lanzará un error al intentar crear un objeto de esa clase.
        # Aquí solo declaramos que debe existir, no lo implementamos.
        pass

    @abstractmethod
    def validar(self):
        # metodo abstracto
        pass

    def __str__(self):
        # A traves de este metodo especial definimos cómo se muestra el objeto cuando se imprime
    
        info = self.obtener_info()
        # Convertimos el diccionario en texto legible línea por línea
        lineas = [f"  {clave}: {valor}" for clave, valor in info.items()]
        return f"{type(self).__name__}:\n" + "\n".join(lineas)

    def __eq__(self, otro):
        # Este método especial permite comparar dos entidades con el operador ==
        # Dos entidades son iguales si son del mismo tipo y tienen el mismo identificador
        if not isinstance(otro, EntidadBase):
            return False
        return (type(self) == type(otro) and
                self._identificador == otro._identificador)

    def __hash__(self):
        # Este método es necesario cuando se define __eq__ para que los objetos puedan usarse en conjuntos o como claves de diccionario
        return hash((type(self).__name__, self._identificador))


# Este bloque solo se ejecuta si corres este archivo directamente
if __name__ == "__main__":

    print("PRUEBA DEL MÓDULO 3: entidad_base.py")
    print("=" * 60)

    # Prueba 1: verificar que no se puede instanciar la clase abstracta directamente
    print("\n[Prueba 1] Intentando instanciar la clase abstracta directamente:")
    try:
        entidad = EntidadBase("001")
    except TypeError as e:
        print(f"  Correcto, no se puede instanciar. Error: {e}")

    # Prueba 2: crear una clase hija de prueba que implemente los métodos abstractos
    print("\n[Prueba 2] Creando una clase hija que hereda de EntidadBase:")

    class EntidadDePrueba(EntidadBase):
        # Esta clase de prueba implementa los dos métodos abstractos obligatorios

        def __init__(self, identificador, nombre):
            super().__init__(identificador)
            # super().__init__ llama al constructor de EntidadBase
            # pasándole el identificador para que lo procese
            self._nombre = nombre

        def obtener_info(self):
            # Implementación obligatoria del método abstracto
            info = self.obtener_info_base()
            info["nombre"] = self._nombre
            return info

        def validar(self):
            # Implementación obligatoria del método abstracto
            if not self._nombre or self._nombre.strip() == "":
                raise ErrorSistemaFJ("El nombre no puede estar vacío")
            return True

    entidad1 = EntidadDePrueba("E001", "Entidad de prueba uno")
    print(f"  Entidad creada exitosamente")
    print(entidad1)

    # Prueba 3: verificar activar y desactivar
    print("\n[Prueba 3] Activar y desactivar entidad:")
    entidad1.desactivar()
    print(f"  Estado activo después de desactivar: {entidad1.activo}")
    entidad1.activar()
    print(f"  Estado activo después de activar: {entidad1.activo}")

    # Prueba 4: verificar comparación entre entidades
    print("\n[Prueba 4] Comparación entre entidades:")
    entidad2 = EntidadDePrueba("E001", "Entidad con mismo ID")
    entidad3 = EntidadDePrueba("E002", "Entidad diferente")
    print(f"  entidad1 == entidad2 (mismo ID): {entidad1 == entidad2}")
    print(f"  entidad1 == entidad3 (distinto ID): {entidad1 == entidad3}")

    # Prueba 5: verificar que el identificador vacío lanza excepción
    print("\n[Prueba 5] Identificador vacío:")
    try:
        entidad_invalida = EntidadDePrueba("", "Sin ID")
    except ErrorSistemaFJ as e:
        print(f"  Excepción capturada correctamente: {e}")

    print("\nTodas las pruebas del módulo 3 pasaron correctamente")
