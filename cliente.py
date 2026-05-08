# MÓDULO 4: cliente.py
# Este modulo define la clase Cliente que representa a cada persona que solicita servicios en la empresa Software FJ.
# La clase hereda de EntidadBase y agrega validaciones estrictas sobre los datos personales del cliente como nombre, email y teléfono.
# Aplica encapsulación para proteger los datos sensibles del cliente.

import re
# Este módulo re permite trabajar con expresiones regulares en Python
# Las expresiones regulares son patrones que sirven para validar formato de texto como emails o números de teléfono.

from entidad_base import EntidadBase
from excepciones import ErrorClienteInvalido, ErrorClienteDuplicado
from logger import logger


class Cliente(EntidadBase):
    """
    Clase que representa a un cliente de Software FJ.
    Hereda de EntidadBase y agrega datos personales con validaciones estrictas.
    Aplica encapsulación protegiendo los atributos con getters y setters.
    """

    def __init__(self, documento, nombre, email, telefono, direccion=""):

        # Primero se validan todos los datos antes de crear el objeto y si algún dato es inválido se lanza una excepción y el objeto no se crea
        self._validar_documento(documento)
        self._validar_nombre(nombre)
        self._validar_email(email)
        self._validar_telefono(telefono)

        # Llamamos al constructor de EntidadBase pasando el documento como identificador
        # Esto registra la entidad en el log y asigna el identificador único
        super().__init__(documento)

        # Asignamos los atributos protegidos con el guion bajo al inicio, esto indica que no deben modificarse directamente desde fuera de la clase
        self._nombre = nombre.strip()
        self._email = email.strip().lower()
        # lower() convierte el email a minúsculas para evitar duplicados por mayúsculas
        self._telefono = telefono.strip()
        self._direccion = direccion.strip()

        # Lista interna para guardar el historial de reservas del cliente, cada vez que el cliente haga una reserva se agregará aquí su ID
        self._historial_reservas = []

        logger.info(f"Cliente registrado: {self._nombre} con documento {self._identificador}")

    # Métodos de validación internos

    def _validar_documento(self, documento):
        # El documento debe ser un texto o número no vacío con al menos 5 caracteres
        if not documento or str(documento).strip() == "":
            raise ErrorClienteInvalido("documento", documento, "no puede estar vacío")
        if len(str(documento).strip()) < 5:
            raise ErrorClienteInvalido("documento", documento, "debe tener al menos 5 caracteres")
        if not str(documento).strip().isdigit():
            raise ErrorClienteInvalido("documento", documento, "debe contener solo números")

    def _validar_nombre(self, nombre):
        # El nombre debe tener al menos 3 caracteres y no puede contener números
        if not nombre or nombre.strip() == "":
            raise ErrorClienteInvalido("nombre", nombre, "no puede estar vacío")
        if len(nombre.strip()) < 3:
            raise ErrorClienteInvalido("nombre", nombre, "debe tener al menos 3 caracteres")
        if any(caracter.isdigit() for caracter in nombre):
            raise ErrorClienteInvalido("nombre", nombre, "no puede contener números")

    def _validar_email(self, email):
        # Usamos una expresión regular para verificar que el email tiene formato válido
        # El patrón verifica que tenga texto, arroba, texto y un punto con extensión
        if not email or email.strip() == "":
            raise ErrorClienteInvalido("email", email, "no puede estar vacío")
        patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron_email, email.strip()):
            raise ErrorClienteInvalido("email", email, "formato inválido, debe ser ejemplo@dominio.com")

    def _validar_telefono(self, telefono):
        # El teléfono debe tener entre 7 y 15 dígitos, puede tener + al inicio
        if not telefono or telefono.strip() == "":
            raise ErrorClienteInvalido("telefono", telefono, "no puede estar vacío")
        telefono_limpio = telefono.strip().replace(" ", "").replace("-", "")
        if telefono_limpio.startswith("+"):
            telefono_limpio = telefono_limpio[1:]
        if not telefono_limpio.isdigit():
            raise ErrorClienteInvalido("telefono", telefono, "debe contener solo números")
        if not (7 <= len(telefono_limpio) <= 15):
            raise ErrorClienteInvalido("telefono", telefono, "debe tener entre 7 y 15 dígitos")

    # Getters: metodos para leer los atributos protegidos desde fuera de la clase

    @property
    def nombre(self):
        return self._nombre

    @property
    def email(self):
        return self._email

    @property
    def telefono(self):
        return self._telefono

    @property
    def direccion(self):
        return self._direccion

    @property
    def historial_reservas(self):
        # se retorna una copia de la lista para que nadie pueda modificarla directamente
        return list(self._historial_reservas)

    # Setters: métodos para modificar atributos con validación previa

    @nombre.setter
    def nombre(self, nuevo_nombre):
        # Antes de cambiar el nombre lo validamos
        self._validar_nombre(nuevo_nombre)
        nombre_anterior = self._nombre
        self._nombre = nuevo_nombre.strip()
        logger.info(f"Cliente {self._identificador}: nombre actualizado de {nombre_anterior} a {self._nombre}")

    @email.setter
    def email(self, nuevo_email):
        self._validar_email(nuevo_email)
        email_anterior = self._email
        self._email = nuevo_email.strip().lower()
        logger.info(f"Cliente {self._identificador}: email actualizado de {email_anterior} a {self._email}")

    @telefono.setter
    def telefono(self, nuevo_telefono):
        self._validar_telefono(nuevo_telefono)
        self._telefono = nuevo_telefono.strip()
        logger.info(f"Cliente {self._identificador}: teléfono actualizado")

    @direccion.setter
    def direccion(self, nueva_direccion):
        self._direccion = nueva_direccion.strip()
        logger.info(f"Cliente {self._identificador}: dirección actualizada")

    def agregar_reserva(self, id_reserva):
        # Agrega el ID de una reserva al historial del cliente
        if id_reserva not in self._historial_reservas:
            self._historial_reservas.append(id_reserva)
            logger.info(f"Reserva {id_reserva} agregada al historial del cliente {self._identificador}")

    def total_reservas(self):
        # Retorna cuántas reservas ha hecho el cliente en total
        return len(self._historial_reservas)

    def obtener_info(self):
        # Implementación obligatoria del método abstracto de EntidadBase
        # Retorna un diccionario con toda la información del cliente
        info = self.obtener_info_base()
        info.update({
            "nombre": self._nombre,
            "email": self._email,
            "telefono": self._telefono,
            "direccion": self._direccion if self._direccion else "No registrada",
            "total_reservas": self.total_reservas()
        })
        return info

    def validar(self):
        # Implementación obligatoria del método abstracto de EntidadBase
        # Verifica que los datos actuales del cliente siguen siendo válidos
        try:
            self._validar_documento(self._identificador)
            self._validar_nombre(self._nombre)
            self._validar_email(self._email)
            self._validar_telefono(self._telefono)
            return True
        except ErrorClienteInvalido as e:
            logger.error(f"Cliente {self._identificador} falló la validación: {e}")
            return False


# Este bloque solo se ejecuta si se corre este archivo directamente
if __name__ == "__main__":

    print("PRUEBA DEL MÓDULO 4: cliente.py")
    print("=" * 60)

    # Prueba 1: crear un cliente válido
    print("\n[Prueba 1] Crear cliente válido:")
    try:
        cliente1 = Cliente(
            documento="1020304050",
            nombre="Juan Pérez",
            email="juan.perez@gmail.com",
            telefono="3001234567",
            direccion="Calle 123 Bogotá"
        )
        print(cliente1)
    except Exception as e:
        print(f"  Error inesperado: {e}")

    # Prueba 2: crear cliente con email inválido
    print("\n[Prueba 2] Cliente con email inválido:")
    try:
        cliente2 = Cliente("2030405060", "María López", "correoSinArroba", "3109876543")
    except ErrorClienteInvalido as e:
        print(f"  Excepción capturada correctamente: {e}")

    # Prueba 3: crear cliente con documento muy corto
    print("\n[Prueba 3] Cliente con documento muy corto:")
    try:
        cliente3 = Cliente("123", "Carlos Ruiz", "carlos@gmail.com", "3201112233")
    except ErrorClienteInvalido as e:
        print(f"  Excepción capturada correctamente: {e}")

    # Prueba 4: crear cliente con nombre con números
    print("\n[Prueba 4] Cliente con nombre con números:")
    try:
        cliente4 = Cliente("3040506070", "Pedro123", "pedro@gmail.com", "3151234567")
    except ErrorClienteInvalido as e:
        print(f"  Excepción capturada correctamente: {e}")

    # Prueba 5: modificar datos del cliente con setter
    print("\n[Prueba 5] Modificar email del cliente:")
    try:
        cliente1.email = "juan.nuevo@hotmail.com"
        print(f"  Email actualizado a: {cliente1.email}")
    except ErrorClienteInvalido as e:
        print(f"  Error: {e}")

    # Prueba 6: agregar reservas al historial
    print("\n[Prueba 6] Agregar reservas al historial:")
    cliente1.agregar_reserva("RES-001")
    cliente1.agregar_reserva("RES-002")
    cliente1.agregar_reserva("RES-001")
    print(f"  Historial: {cliente1.historial_reservas}")
    print(f"  Total reservas: {cliente1.total_reservas()}")

    # Prueba 7: validar cliente
    print("\n[Prueba 7] Validar cliente:")
    print(f"  Cliente válido: {cliente1.validar()}")

    # Prueba 8: cliente con teléfono inválido
    print("\n[Prueba 8] Cliente con teléfono inválido:")
    try:
        cliente5 = Cliente("4050607080", "Ana Gómez", "ana@gmail.com", "123abc")
    except ErrorClienteInvalido as e:
        print(f"  Excepción capturada correctamente: {e}")

    print("\nTodas las pruebas del módulo 4 pasaron correctamente")
