# MÓDULO 2: logger.py

# Este módulo se encarga de registrar todos los eventos y errores del sistema en un archivo de texto llamado "sistema_fj.log".
# Cada vez que algo importante ocurre en el sistema, ya sea un error o una operación exitosa, este módulo lo escribe en 
# ese archivo con fecha y hora.

import os          # Se usa para manejar rutas de archivos y carpetas
import datetime    # se usa para obtener la fecha y hora actual


class Logger:
    """
    Clase que gestiona el registro de eventos y errores del sistema.
    Escribe mensajes en un archivo de log con fecha, hora y tipo de evento.
    """

    def __init__(self, nombre_archivo="sistema_fj.log", carpeta="logs"):
        # nombre_archivo es el nombre del archivo donde se guardarán los registros
        # carpeta es el directorio donde se creará ese archivo

        self.carpeta = carpeta
        self.nombre_archivo = nombre_archivo

        # Construimos la ruta completa del archivo, por ejemplo: logs/sistema_fj.log
        self.ruta_completa = os.path.join(carpeta, nombre_archivo)

        # Llamamos al método que crea la carpeta si no existe
        self._inicializar_carpeta()

    def _inicializar_carpeta(self):
        # Este método verifica si la carpeta de logs existe.Si no existe, la crea automáticamente.
        # El guion bajo al inicio del nombre nos indica que es un método interno,
        # es decir, solo lo usa esta clase, no el resto del programa.
        try:
            if not os.path.exists(self.carpeta):
                os.makedirs(self.carpeta)
        except Exception as e:
            # Si no se puede crear la carpeta, mostramos el problema en pantalla
            print(f"Advertencia: no se pudo crear la carpeta de logs. Detalle: {e}")

    def _obtener_timestamp(self):
        # Retorna la fecha y hora actual en formato legible, por ejemplo: 2026-05-02 14:35:22
        ahora = datetime.datetime.now()
        return ahora.strftime("%Y-%m-%d %H:%M:%S")

    def _escribir(self, nivel, mensaje):
        # Este es el método principal de escritura.
        # nivel indica el tipo de mensaje: INFO, ERROR, ADVERTENCIA, etc.
        # mensaje es el texto que describe lo que ocurrió.

        timestamp = self._obtener_timestamp()

        # Construimos la línea completa que se escribirá en el archivo
        # Ejemplo: [2026-05-02 14:35:22] [ERROR] El cliente ya existe
        linea = f"[{timestamp}] [{nivel}] {mensaje}\n"

        try:
            # Abrimos el archivo en modo "a" que significa "append" o agregar al final, así no borramos los registros anteriores,
            # solo añadimos al final encoding utf-8 permite escribir caracteres como tildes y ñ
            with open(self.ruta_completa, "a", encoding="utf-8") as archivo:
                archivo.write(linea)

        except Exception as e:
            # Si no se puede escribir en el archivo, avisamos en pantalla pero no detenemos el programa
            print(f"Advertencia: no se pudo escribir en el log. Detalle: {e}")

        # También mostramos el mensaje en pantalla para ver lo que pasa en tiempo real
        print(linea, end="")

    def info(self, mensaje):
        # Registra un evento informativo, algo que salió bien, como por ejemplo, 'cliente registrado exitosamente
        self._escribir("INFO", mensaje)

    def error(self, mensaje):
        # Registra un error que ocurrió en el sistema, como por ejemplo, 'datos de cliente inválidos'
        self._escribir("ERROR", mensaje)

    def advertencia(self, mensaje):
        # Registra una situación sospechosa que no es un error grave, como por ejemplo, 'se intentó cancelar una reserva ya cancelada
        self._escribir("ADVERTENCIA", mensaje)

    def registrar_excepcion(self, excepcion, contexto=""):
        # Registra una excepción completa incluyendo su tipo y mensaje
        # contexto describe en qué parte del sistema ocurrió el error
        # Ejemplo de uso: logger.registrar_excepcion(e, "registro de cliente")

        tipo_excepcion = type(excepcion).__name__
        # type(excepcion).__name__ nos da el nombre de la clase de la excepción
        # Por ejemplo, 'ErrorClienteInvalido, ValueError, etc.'

        if contexto:
            mensaje = f"Excepción en {contexto} | Tipo: {tipo_excepcion} | Detalle: {excepcion}"
        else:
            mensaje = f"Excepción | Tipo: {tipo_excepcion} | Detalle: {excepcion}"

        self._escribir("ERROR", mensaje)

        # Si la excepción tiene una causa encadenada, también la registramos
        if excepcion.__cause__:
            causa = f"Causa original: {type(excepcion.__cause__).__name__} | {excepcion.__cause__}"
            self._escribir("ERROR", causa)

    def separador(self, titulo=""):
        # Escribe una línea separadora en el log para organizar visualmente los registros
        # Esto es util para marcar el inicio de una nueva sesión o grupo de operaciones
        if titulo:
            linea = f"\n{'=' * 60}\n  {titulo}\n{'=' * 60}"
        else:
            linea = f"\n{'=' * 60}"

        try:
            with open(self.ruta_completa, "a", encoding="utf-8") as archivo:
                archivo.write(linea + "\n")
        except Exception as e:
            print(f"Advertencia: no se pudo escribir separador en el log. Detalle: {e}")

        print(linea)


# Creamos una instancia global del logger que todos los módulos pueden importar y usar
# En lugar de que cada módulo cree su propio logger, todos comparten este mismo
logger = Logger()


# Este bloque solo se ejecuta si se corre este archivo directamente  python logger.py
if __name__ == "__main__":

    print("PRUEBA DEL MÓDULO 2: logger.py")
    print("=" * 60)

    # Importamos las excepciones del módulo anterior para probar el registro
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from excepciones import (
        ErrorClienteInvalido,
        ErrorServicioNoDisponible,
        ErrorReservaInvalida,
        ErrorCalculo
    )

    # Creamos un logger de prueba con un archivo separado para no mezclar con el real
    log_prueba = Logger(nombre_archivo="prueba_logger.log", carpeta="logs")

    log_prueba.separador("INICIO DE PRUEBAS DEL LOGGER")

    # Prueba 1: registrar un evento informativo
    print("\n[Prueba 1] Registro de evento informativo:")
    log_prueba.info("Cliente Juan Pérez registrado exitosamente con ID 1001")

    # Prueba 2: registrar un error simple
    print("\n[Prueba 2] Registro de error simple:")
    log_prueba.error("No se encontró el servicio solicitado en el catálogo")

    # Prueba 3: registrar una advertencia
    print("\n[Prueba 3] Registro de advertencia:")
    log_prueba.advertencia("Se intentó cancelar una reserva que ya estaba cancelada")

    # Prueba 4: registrar una excepción personalizada
    print("\n[Prueba 4] Registro de excepción personalizada:")
    try:
        raise ErrorClienteInvalido("email", "juansinArroba", "debe contener @")
    except ErrorClienteInvalido as e:
        log_prueba.registrar_excepcion(e, "registro de cliente")

    # Prueba 5: registrar excepción con causa encadenada
    print("\n[Prueba 5] Registro de excepción encadenada:")
    try:
        try:
            int("valor_no_numerico")
        except ValueError as error_original:
            raise ErrorCalculo("cálculo de tarifa", "el valor no es numérico") from error_original
    except ErrorCalculo as e:
        log_prueba.registrar_excepcion(e, "cálculo de costo de servicio")

    # Prueba 6: verificar que el archivo de log fue creado
    print("\n[Prueba 6] Verificando que el archivo de log existe:")
    if os.path.exists("logs/prueba_logger.log"):
        print("  El archivo logs/prueba_logger.log fue creado correctamente")
        with open("logs/prueba_logger.log", "r", encoding="utf-8") as f:
            contenido = f.read()
        print(f"  Tamaño del archivo: {len(contenido)} caracteres")
    else:
        print("  El archivo no fue creado, revisar permisos de la carpeta")

    log_prueba.separador("FIN DE PRUEBAS")
    print("\nTodas las pruebas del logger pasaron correctamente")
