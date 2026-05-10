# MÓDULO 8: main.py
# Este es el archivo principal del sistema. Al ejecutarlo se pone en marcha todo el programa y se simulan más de 10 operaciones completas que incluyen
# registros válidos e inválidos de clientes, creación correcta e incorrecta de servicios, y reservas exitosas y fallidas.
# El sistema demuestra que puede continuar funcionando aunque ocurran errores.

from gestor import GestorSistema
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


def separador(titulo):
    print(f"\n{'=' * 60}")
    print(f"  {titulo}")
    print(f"{'=' * 60}")


def ejecutar_operacion(descripcion, funcion, *args, **kwargs):
    """
    Ejecuta una operación del sistema de forma segura.
    Captura cualquier excepción del sistema, la muestra en pantalla
    y la registra en el log, pero no detiene la ejecución del programa.
    Esto demuestra que el sistema sigue funcionando ante errores graves.
    """
    print(f"\n  Operación: {descripcion}")
    try:
        resultado = funcion(*args, **kwargs)
        print(f"  Resultado: OK")
        return resultado

    except ErrorClienteDuplicado as e:
        print(f"  Error controlado (cliente duplicado): {e}")
        logger.registrar_excepcion(e, descripcion)

    except ErrorClienteInvalido as e:
        print(f"  Error controlado (dato de cliente inválido): {e}")
        logger.registrar_excepcion(e, descripcion)

    except ErrorClienteNoEncontrado as e:
        print(f"  Error controlado (cliente no encontrado): {e}")
        logger.registrar_excepcion(e, descripcion)

    except ErrorServicioInvalido as e:
        print(f"  Error controlado (dato de servicio inválido): {e}")
        logger.registrar_excepcion(e, descripcion)

    except ErrorServicioNoDisponible as e:
        print(f"  Error controlado (servicio no disponible): {e}")
        logger.registrar_excepcion(e, descripcion)

    except ErrorServicioNoEncontrado as e:
        print(f"  Error controlado (servicio no encontrado): {e}")
        logger.registrar_excepcion(e, descripcion)

    except ErrorReservaInvalida as e:
        print(f"  Error controlado (reserva inválida): {e}")
        logger.registrar_excepcion(e, descripcion)

    except ErrorReservaNoEncontrada as e:
        print(f"  Error controlado (reserva no encontrada): {e}")
        logger.registrar_excepcion(e, descripcion)

    except ErrorCancelacionNoPermitida as e:
        print(f"  Error controlado (cancelación no permitida): {e}")
        logger.registrar_excepcion(e, descripcion)

    except ErrorSistemaFJ as e:
        print(f"  Error controlado (error del sistema): {e}")
        logger.registrar_excepcion(e, descripcion)

    except Exception as e:
        print(f"  Error inesperado: {e}")
        logger.registrar_excepcion(e, descripcion)

    return None


def main():

    logger.separador("INICIO DEL SISTEMA SOFTWARE FJ")
    print("\n  Bienvenido al Sistema Integral de Gestión")
    print("  Software FJ - UNAD | Programación Orientada a Objetos")

    # Creamos la instancia central del sistema
    gestor = GestorSistema()

    # BLOQUE 1: REGISTRO DE CLIENTES

    separador("BLOQUE 1: REGISTRO DE CLIENTES")

    # Operación 1: registrar cliente válido
    c1 = ejecutar_operacion(
        "Registrar cliente válido: Juan Pérez",
        gestor.registrar_cliente,
        "1020304050", "Juan Pérez", "juan.perez@gmail.com", "3001234567", "Calle 10 Bogotá"
    )

    # Operación 2: registrar segundo cliente válido
    c2 = ejecutar_operacion(
        "Registrar cliente válido: María López",
        gestor.registrar_cliente,
        "2030405060", "María López", "maria.lopez@hotmail.com", "3109876543", "Carrera 5 Medellín"
    )

    # Operación 3: registrar tercer cliente válido
    c3 = ejecutar_operacion(
        "Registrar cliente válido: Carlos Ruiz",
        gestor.registrar_cliente,
        "3040506070", "Carlos Ruiz", "carlos.ruiz@outlook.com", "3201112233"
    )

    # Operación 4: intentar registrar cliente con email inválido (debe fallar)
    ejecutar_operacion(
        "Registrar cliente con email inválido (debe fallar)",
        gestor.registrar_cliente,
        "4050607080", "Pedro Mora", "correoSinArroba", "3151234567"
    )

    # Operación 5: intentar registrar cliente duplicado (debe fallar)
    ejecutar_operacion(
        "Registrar cliente duplicado con documento 1020304050 (debe fallar)",
        gestor.registrar_cliente,
        "1020304050", "Juan Repetido", "otro@gmail.com", "3001111111"
    )

    # Operación 6: intentar registrar cliente con nombre con números (debe fallar)
    ejecutar_operacion(
        "Registrar cliente con nombre inválido (debe fallar)",
        gestor.registrar_cliente,
        "5060708090", "Ana123 Gómez", "ana@gmail.com", "3161234567"
    )

    print(f"\n  Clientes registrados exitosamente: {len(gestor.listar_clientes())}")

    # BLOQUE 2: REGISTRO DE SERVICIOS

    separador("BLOQUE 2: REGISTRO DE SERVICIOS")

    # Operación 7: registrar sala válida
    s1 = ejecutar_operacion(
        "Registrar sala de juntas válida",
        gestor.registrar_sala,
        "SRV-001", "Sala de Juntas A", "Sala principal con videoconferencia", 80000, 10
    )

    # Operación 8: registrar equipo válido
    s2 = ejecutar_operacion(
        "Registrar equipo de alquiler válido",
        gestor.registrar_equipo,
        "SRV-002", "Laptop Dell Empresarial", "Laptop con Office y antivirus", 45000, 5, "Laptop"
    )

    # Operación 9: registrar asesoría válida
    s3 = ejecutar_operacion(
        "Registrar asesoría especializada válida",
        gestor.registrar_asesoria,
        "SRV-003", "Asesoría en Python", "Consultoría en Python para empresas", 120000, "Desarrollo de Software", "experto"
    )

    # Operación 10: intentar registrar sala con tarifa negativa (debe fallar)
    ejecutar_operacion(
        "Registrar sala con tarifa negativa (debe fallar)",
        gestor.registrar_sala,
        "SRV-004", "Sala Inválida", "Esta sala no debería crearse", -50000, 8
    )

    # Operación 11: intentar registrar asesoría con nivel inválido (debe fallar)
    ejecutar_operacion(
        "Registrar asesoría con nivel inválido (debe fallar)",
        gestor.registrar_asesoria,
        "SRV-005", "Asesoría Inválida", "Esta asesoría no debería crearse", 100000, "Marketing", "dios"
    )

    print(f"\n  Servicios registrados exitosamente: {len(gestor.listar_servicios())}")


    # BLOQUE 3: CREACIÓN Y GESTIÓN DE RESERVAS

    separador("BLOQUE 3: CREACIÓN Y GESTIÓN DE RESERVAS")

    # Operación 12: crear reserva válida con impuesto
    r1 = ejecutar_operacion(
        "Crear reserva de sala para Juan Pérez con IVA",
        gestor.crear_reserva,
        "1020304050", "SRV-001", 3, True, 0
    )

    # Operación 13: crear reserva válida con descuento
    r2 = ejecutar_operacion(
        "Crear reserva de equipo para María López con 10% de descuento",
        gestor.crear_reserva,
        "2030405060", "SRV-002", 5, False, 10
    )

    # Operación 14: crear reserva de asesoría válida
    r3 = ejecutar_operacion(
        "Crear reserva de asesoría para Carlos Ruiz",
        gestor.crear_reserva,
        "3040506070", "SRV-003", 2, True, 15
    )

    # Operación 15: intentar crear reserva con duración negativa (debe fallar)
    ejecutar_operacion(
        "Crear reserva con duración negativa (debe fallar)",
        gestor.crear_reserva,
        "1020304050", "SRV-001", -5
    )

    # Operación 16: intentar crear reserva con cliente inexistente (debe fallar)
    ejecutar_operacion(
        "Crear reserva con cliente inexistente (debe fallar)",
        gestor.crear_reserva,
        "9999999999", "SRV-001", 2
    )

    # Operación 17: intentar crear reserva con servicio deshabilitado (debe fallar)
    ejecutar_operacion(
        "Deshabilitar sala y crear reserva sobre ella (debe fallar)",
        lambda: [
            gestor.deshabilitar_servicio("SRV-001"),
            gestor.crear_reserva("1020304050", "SRV-001", 2)
        ]
    )
    # Volvemos a habilitar la sala para las siguientes operaciones
    gestor.habilitar_servicio("SRV-001")

    # BLOQUE 4: CICLO DE VIDA DE LAS RESERVAS
    
    separador("BLOQUE 4: CICLO DE VIDA DE LAS RESERVAS")

    if r1:
        # Operación 18: confirmar, procesar y finalizar reserva 1
        ejecutar_operacion(
            f"Confirmar reserva {r1.identificador}",
            gestor.confirmar_reserva, r1.identificador
        )
        ejecutar_operacion(
            f"Procesar reserva {r1.identificador}",
            gestor.procesar_reserva, r1.identificador
        )
        ejecutar_operacion(
            f"Finalizar reserva {r1.identificador}",
            gestor.finalizar_reserva, r1.identificador
        )
        print(f"\n  Estado final de {r1.identificador}: {r1.estado}")

    if r2:
        # Operación 19: cancelar reserva 2
        ejecutar_operacion(
            f"Cancelar reserva {r2.identificador}",
            gestor.cancelar_reserva,
            r2.identificador, "el cliente reprogramó para otra fecha"
        )
        print(f"\n  Estado final de {r2.identificador}: {r2.estado}")

    if r1:
        # Operación 20: intentar cancelar reserva ya finalizada (debe fallar)
        ejecutar_operacion(
            f"Cancelar reserva ya finalizada {r1.identificador} (debe fallar)",
            gestor.cancelar_reserva,
            r1.identificador, "intento inválido"
        )

    if r2:
        # Operación 21: intentar confirmar reserva ya cancelada (debe fallar)
        ejecutar_operacion(
            f"Confirmar reserva ya cancelada {r2.identificador} (debe fallar)",
            gestor.confirmar_reserva, r2.identificador
        )


    # BLOQUE 5: CONSULTAS Y RESUMEN FINAL
    
    separador("BLOQUE 5: CONSULTAS Y RESUMEN FINAL")

    print("\n  Listado de clientes activos:")
    for cliente in gestor.listar_clientes():
        print(f"    {cliente.identificador} | {cliente.nombre} | {cliente.email}")

    print("\n  Listado de servicios disponibles:")
    for servicio in gestor.listar_servicios():
        print(f"    {servicio.identificador} | {servicio.nombre} | {servicio.describir()}")

    print("\n  Listado de todas las reservas:")
    for reserva in gestor.listar_reservas():
        print(
            f"    {reserva.identificador} | "
            f"Cliente: {reserva.cliente.nombre} | "
            f"Servicio: {reserva.servicio.nombre} | "
            f"Estado: {reserva.estado} | "
            f"Costo: ${reserva.costo_total:,.2f}"
        )

    if c1:
        print(f"\n  Reservas del cliente {c1.nombre}:")
        for reserva in gestor.reservas_por_cliente(c1.identificador):
            print(f"    {reserva.identificador} | Estado: {reserva.estado}")

    # Resumen final del sistema
    gestor.imprimir_resumen()

    logger.separador("FIN DE LA SIMULACIÓN DEL SISTEMA SOFTWARE FJ")
    print("\n  Sistema ejecutado exitosamente.")
    print("  Revisa el archivo logs/sistema_fj.log para ver el registro completo.\n")


# Punto de entrada del programa
# Este bloque garantiza que main() solo se ejecute cuando corres este archivo
# directamente con: python main.py
if __name__ == "__main__":
    main()
