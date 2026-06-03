# DataINC Processing Dashboard

## Objetivo

Permitir a los clientes subir archivos CSV para ser procesados de manera asíncrona, visualizar el estado de procesamiento de las órdenes y descargar el resultado final.

---

# Requerimientos Funcionales

## RF-001 - Crear Orden

Como cliente

Quiero subir un archivo CSV

Para que sea procesado por el sistema.

### Criterios de aceptación

- Debe aceptarse únicamente archivos .csv
- Debe generarse una nueva Order
- La Order debe crearse con estado CREATED
- Debe registrarse fecha y hora de creación

---

## RF-002 - Verificación de CSV

Como sistema

Quiero validar el archivo recibido

Para asegurar que cumple los requisitos mínimos.

### Criterios de aceptación

- Validar existencia de headers
- Validar columnas obligatorias
- Si falla la validación:
  - Estado FAILED
  - Registrar mensaje de error

---

## RF-003 - Normalización

Como sistema

Quiero normalizar los datos

Para estandarizar la información.

### Criterios de aceptación

- Fechas → ISO8601
- Texto → MAYÚSCULAS
- Valores vacíos → NULL

---

## RF-004 - Dashboard

Como usuario

Quiero visualizar las órdenes

Para conocer el estado del procesamiento.

### Criterios de aceptación

- Mostrar órdenes ordenadas por fecha de creación descendente
- Mostrar:
  - ID
  - Fecha creación
  - Estado
  - Acción descarga

---

## RF-005 - Descarga

Como usuario

Quiero descargar el archivo procesado

Para obtener el resultado final.

### Criterios de aceptación

- Solo disponible para órdenes DONE
- Descargar CSV normalizado

---

# Requerimientos No Funcionales

## RNF-001

El procesamiento debe ejecutarse de forma asíncrona mediante Celery.

## RNF-002

El sistema debe soportar múltiples órdenes concurrentes.

## RNF-003

La API debe estar documentada mediante OpenAPI/Swagger.

## RNF-004

La aplicación debe ejecutarse completamente mediante Docker Compose.

## RNF-005

La solución debe incluir tests automatizados.