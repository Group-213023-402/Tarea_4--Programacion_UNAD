# Software FJ — Sistema Integral de Gestión de Clientes, Servicios y Reservas

Sistema orientado a objetos desarrollado en Python para la gestión de clientes, servicios y reservas de la empresa Software FJ. Proyecto académico del curso Programación Orientada a Objetos (Código 213023) — Universidad Nacional Abierta y a Distancia (UNAD).

---

## Descripción general

El sistema permite registrar clientes, gestionar un catálogo de servicios (salas, equipos y asesorías) y administrar reservas con un ciclo de vida completo. Toda la información se mantiene en memoria mediante objetos y listas, sin uso de base de datos. Los errores y eventos se registran automáticamente en un archivo de logs.

---

## Principios de programación orientada a objetos aplicados

- **Abstracción:** clases abstractas `EntidadBase` y `Servicio` que definen la estructura general del sistema
- **Herencia:** `Cliente`, `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` heredan de las clases base
- **Polimorfismo:** cada servicio calcula su costo y se describe de forma diferente usando el mismo método
- **Encapsulación:** atributos protegidos con getters y setters que validan los datos antes de modificarlos
- **Manejo de excepciones:** excepciones personalizadas, bloques try/except, try/except/else, try/except/finally y encadenamiento de excepciones

---

## Estructura del proyecto

```
sistema-gestion-softwarefj/
│
├── excepciones.py       Módulo 1 — Excepciones personalizadas del sistema
├── logger.py            Módulo 2 — Sistema de registro de eventos y errores
├── entidad_base.py      Módulo 3 — Clase abstracta base del sistema
├── cliente.py           Módulo 4 — Clase Cliente con validaciones y encapsulación
├── servicios.py         Módulo 5 — Servicios especializados con herencia y polimorfismo
├── reserva.py           Módulo 6 — Clase Reserva con ciclo de vida completo
├── gestor.py            Módulo 7 — Gestor central del sistema
├── main.py              Módulo 8 — Simulación de operaciones completas
├── interfaz.py          Módulo 9 — Interfaz gráfica con Tkinter
├── README.md            Documentación del proyecto
└── logs/
    └── sistema_fj.log   Archivo de registro de eventos y errores
```

---

## Jerarquía de clases

```
EntidadBase (abstracta)
├── Cliente
├── Servicio (abstracta)
│   ├── ReservaSala
│   ├── AlquilerEquipo
│   └── AsesoriaEspecializada
└── Reserva

Exception
└── ErrorSistemaFJ
    ├── ErrorCliente
    │   ├── ErrorClienteInvalido
    │   ├── ErrorClienteDuplicado
    │   └── ErrorClienteNoEncontrado
    ├── ErrorServicio
    │   ├── ErrorServicioInvalido
    │   ├── ErrorServicioNoDisponible
    │   └── ErrorServicioNoEncontrado
    ├── ErrorReserva
    │   ├── ErrorReservaInvalida
    │   ├── ErrorReservaNoEncontrada
    │   └── ErrorCancelacionNoPermitida
    └── ErrorCalculo
```

---

## Requisitos

- Python 3.8 o superior
- Tkinter (incluido con Python, necesario solo para la interfaz gráfica)
- No requiere instalación de librerías externas

---

## Cómo ejecutar el proyecto

### Opción A — Simulación automática en terminal

Ejecuta el archivo principal que simula más de 20 operaciones completas:

```bash
python main.py
```

Verás el resultado de cada operación en pantalla y todos los eventos quedarán registrados en `logs/sistema_fj.log`.

### Opción B — Interfaz gráfica interactiva

Ejecuta la interfaz visual para interactuar con el sistema manualmente:

```bash
python interfaz.py
```

---

## Datos de prueba para la interfaz gráfica

### Clientes

| Documento | Nombre | Email | Teléfono |
|---|---|---|---|
| 1020304050 | Juan Perez | juan.perez@gmail.com | 3001234567 |
| 2030405060 | Maria Lopez | maria.lopez@hotmail.com | 3109876543 |
| 3040506070 | Carlos Ruiz | carlos.ruiz@outlook.com | 3201112233 |

### Servicios

| Código | Tipo | Nombre | Tarifa | Extra |
|---|---|---|---|---|
| SRV-001 | Sala | Sala de Juntas A | 80000 | Capacidad: 10 |
| SRV-002 | Equipo | Laptop Dell | 45000 | Cantidad: 5 |
| SRV-003 | Asesoría | Asesoria en Python | 120000 | Nivel: experto |

### Reservas y costos esperados

| Cliente | Servicio | Duración | Descuento | IVA | Costo |
|---|---|---|---|---|---|
| 1020304050 | SRV-001 | 3 horas | 0% | Sí | $285,600 |
| 2030405060 | SRV-002 | 5 días | 10% | No | $202,500 |
| 3040506070 | SRV-003 | 2 horas | 15% | Sí | $485,520 |

---

## Ciclo de vida de una reserva

```
pendiente → confirmada → en_proceso → finalizada
                ↓
            cancelada
```

Una reserva solo puede cancelarse si está en estado pendiente o confirmada. Una vez finalizada no puede modificarse.

---

## Registro de logs

Cada operación del sistema queda registrada automáticamente en `logs/sistema_fj.log` con fecha, hora y tipo de evento:

```
[2026-05-10 14:35:22] [INFO] Cliente Juan Perez registrado exitosamente
[2026-05-10 14:35:23] [ERROR] Dato inválido en cliente → Campo: 'email' | Razón: debe contener '@'
[2026-05-10 14:35:24] [ADVERTENCIA] Servicio Sala de Juntas A deshabilitado
```

---

## Integrantes del equipo

| Nombre | Usuario GitHub |
|---|---|
| John Rincon | @usuario |
| *(pendiente)* | — |
| *(pendiente)* | — |
| *(pendiente)* | — |
| *(pendiente)* | — |

---

## Información académica

- **Universidad:** Universidad Nacional Abierta y a Distancia — UNAD
- **Programa:** Ingeniería de Sistemas
- **Curso:** Programación Orientada a Objetos
- **Código:** 213023
- **Actividad:** Fase 4 — Trabajo colaborativo
