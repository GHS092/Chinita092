# Guía de Solución de Errores: Carrusel de Múltiples API Keys y Proxy Local en Hermes

Este documento registra la serie de problemas y soluciones técnicas implementadas para hacer funcionar correctamente el **Carrusel de API Keys** (Pooling) y el **Proxy Local** en el sistema Hermes, integrándolo con Gemini y OpenRouter. Sirve como referencia y guía para futuros desarrolladores.

## Contexto
El objetivo era permitir que el usuario pudiera introducir una lista de múltiples API Keys (separadas por coma) en el panel de UI. El sistema debía detectar automáticamente esto, encender un servidor proxy local y enviar las peticiones del Agente a través del proxy rotando las llaves automáticamente para evadir los límites de cuota (Rate Limits) en la capa gratuita.

A continuación, la bitácora cronológica de los errores encontrados y cómo se solucionaron.

---

### Problema 1: El Proxy le mentía al Agente sobre el "Proveedor" (`Unknown provider 'openai'`)
**El Problema:** 
Cuando el Gateway encendía el servidor proxy local para rotar las llaves, inyectaba el servidor de la siguiente manera: `OPENAI_BASE_URL="http://127.0.0.1:8080/proxy/gemini/v1"` y le indicaba al agente que usara el proveedor `provider: "openai"`. Sin embargo, el núcleo de Hermes no reconocía la cadena `"openai"` como un proveedor válido y se cerraba con el error `Unknown provider 'openai'`.

**La Solución:**
En el núcleo de Hermes, las conexiones hacia endpoints compatibles con la API de OpenAI (como nuestro proxy local) no utilizan el slug `"openai"`, sino `"custom"`.
Se modificó `server.py` para asignar `provider_slug = "custom"` cada vez que se detectan llaves separadas por comas.

---

### Problema 2: El Agente ignoraba el Proxy Local y se iba a OpenRouter
**El Problema:**
Tras solucionar el primer error, los logs mostraron que el agente intentaba conectarse a `https://openrouter.ai/api/v1` en lugar de nuestro servidor proxy local (`127.0.0.1:8080`).

**El Análisis:**
Aunque enviábamos correctamente la URL del proxy a través de la variable de entorno `OPENAI_BASE_URL`, el agente cargaba el archivo de configuración base por defecto (`cli-config.yaml.example`). Este archivo tiene "quemada" la URL de OpenRouter como ruta por defecto si no se le provee una explícitamente en el YAML. Las rutas en el archivo YAML tienen mayor jerarquía que las variables de entorno.

**La Solución:**
En `server.py`, durante la función `write_config_yaml()` que reescribe el cerebro del agente, forzamos la escritura física de la ruta.
```yaml
model:
  default: "gemini-2.5-flash"
  provider: "custom"
  base_url: "http://127.0.0.1:8080/proxy/gemini/v1"
```
Al dejar la URL grabada a fuego en el archivo `.yaml`, el agente dejó de buscar rutas por defecto.

---

### Problema 3: Error 500 en el Proxy (`No Gemini keys configured`)
**El Problema:**
El Agente finalmente llegó a nuestro Proxy Local, pero este respondió con un Error 500: `No Gemini keys configured`. El proxy pensaba que no habían llaves.

**El Análisis:**
El panel de UI guardaba la lista de claves introducida por el usuario bajo la variable estándar `GEMINI_API_KEY` en el archivo `/data/.hermes/.env`. 
Sin embargo, el código asíncrono del proxy intentaba leer la variable temporal `GEMINI_CAROUSEL_KEYS`, que sólo existía en la memoria del proceso Gateway secundario y jamás era escrita en el archivo `.env`. Por lo tanto, leía un valor vacío.

**La Solución:**
Se corrigieron las rutas asíncronas `gemini_proxy` y `openrouter_proxy` en `server.py` para que lean directamente las variables maestras `GEMINI_API_KEY` y `OPENROUTER_API_KEY` del archivo `.env`.

---

### Problema 4: El temido `Error -3 while decompressing data` (Doble Descompresión)
**El Problema:**
El proxy finalmente rotaba las llaves y se conectaba con éxito a la API de Google Gemini. Sin embargo, al devolver la respuesta al Agente, este generaba un error crítico: `Error -3 while decompressing data: incorrect header check`.

**El Análisis:**
1. Google Gemini responde al proxy con los datos comprimidos en `.gzip`.
2. La librería `httpx` de Python en nuestro proxy recibe el `.gzip` y lo **descomprime automáticamente** en texto plano a medida que transmite el flujo de datos (Streaming).
3. **El error crítico:** Al retornar el texto plano al Agente, a nuestro proxy se le olvidó borrar las cabeceras HTTP originales (`Content-Encoding: gzip` y `Content-Length`).
4. El Agente recibía texto puro, pero la cabecera decía "esto está comprimido". Al intentar "descomprimir" un texto que ya estaba puro, fallaba miserablemente arrojando el Error -3.

**La Solución:**
Se ordenó explícitamente a las funciones `gemini_proxy` y `openrouter_proxy` que eliminaran las cabeceras de compresión justo antes de devolver la respuesta al cliente:
```python
response_headers = {
    k: v for k, v in resp.headers.items()
    if k.lower() not in HOP_BY_HOP
    and k.lower() not in ("content-encoding", "content-length")
}
```

---

### Notas Adicionales sobre la Infraestructura en Railway
- **Persistencia de Datos:** Railway utiliza contenedores efímeros. Esto significa que la carpeta `/data/.hermes` se destruye en cada re-deploy, perdiéndose el archivo `.env`.
- **Mitigación:** Para evitar esto, los usuarios deben añadir sus variables de entorno (como el chorro de llaves API) directamente en la pestaña **Variables de Railway**, ya que estas sobreviven a los re-deploys y son inyectadas en la memoria del servidor al arrancar. La alternativa es configurar un **Persistent Volume** mapeado a la carpeta `/data`.

*Generado automáticamente por Antigravity (IA) durante la depuración de la arquitectura multi-llaves de Hermes Gateway.*
